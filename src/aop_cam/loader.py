"""Load the AOP-Wiki TSV corpus into aop_cam ModelCollection instances.

Every ontology-term assignment the loader emits carries a grounding receipt
as per-assertion evidence (see docs/grounding-receipts.md):

* Class 1, upstream-asserted (ECO:0000311 "imported information"): AOP-Wiki
  supplied the ontology id (key event components, cell terms, organ terms,
  and the causal edges themselves). The receipt cites the AOP-Wiki record
  page and the pinned, hashed dump from data/aopwiki-snapshot.yaml.
* Class 2, mapping-table (ECO:0000305 "curator inference used in manual
  assertion"): the 11 biological actions map to PATO through the committed
  SSSOM file mappings/aopwiki-action-to-pato.sssom.tsv. The loader may only
  emit assignments present in the table; an unmapped action raises
  LoaderError instead of guessing.

Source values that cannot be grounded (e.g. a vocabulary source with no
CURIE form) are skipped with a warning, never guessed. Stressors keep their
AOP-Wiki identity (AOPWIKI:stressors/N) until a chemical grounding pass
exists.

Usage:
    python -m aop_cam.loader --data-dir data \
        --aops Aop:148 Aop:411 Aop:424 Aop:425 \
        -o examples/output/respiratory-slice.yaml
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.yamlutils import YAMLRoot

from aop_cam.datamodel.aop_cam import (
    AnatomyTermObject,
    AopModel,
    CausalAssociation,
    CellTypeAssociation,
    CellTypeTermObject,
    DirectionAssociation,
    DirectionTermObject,
    EvidenceItem,
    GrossAnatomyAssociation,
    KeyEventComponent,
    KeyEventNode,
    ModelCollection,
    ObjectAssociation,
    ObjectTermObject,
    ProcessAssociation,
    ProcessTermObject,
    ProvenanceInfo,
    StressorTermObject,
)

# Receipt vocabulary (ids verified via OAK; see docs/grounding-receipts.md)
ECO_IMPORTED = "ECO:0000311"  # imported information
ECO_CURATOR = "ECO:0000305"  # curator inference used in manual assertion

ACTION_MAPPING_SET = (
    "https://w3id.org/EHS-Data-Standards/aop-cam/mappings/aopwiki-action-to-pato"
)
ACTION_MAPPING_FILE = "aopwiki-action-to-pato.sssom.tsv"

# AOP-Wiki edge semantics onto RO (see CausalAssociation in the schema)
ADJACENCY_PREDICATE = {
    "adjacent": "immediately causally upstream of",  # RO:0002412
    "non-adjacent": "causally upstream of",  # RO:0002411
}

CONFIDENCE = {
    "High": "high",
    "Moderate": "moderate",
    "Low": "low",
    "Not Specified": "not_specified",
}


class LoaderError(Exception):
    """A violation of the loading rules (e.g. a source value absent from a
    closed mapping table). Loudly fails the build instead of guessing."""


@dataclass
class ActionMapping:
    """One row of the action->PATO SSSOM table."""

    subject_id: str
    subject_label: str
    predicate_id: str
    object_id: str
    object_label: str
    confidence: str
    mapping_date: str
    comment: str


@dataclass
class Corpus:
    """The TSV corpus plus its snapshot pin, indexed for loading."""

    aops: dict[str, dict] = field(default_factory=dict)
    key_events: dict[str, dict] = field(default_factory=dict)
    kers: dict[str, dict] = field(default_factory=dict)
    aop_kers: dict[str, list[dict]] = field(default_factory=dict)
    components: dict[str, list[dict]] = field(default_factory=dict)
    actions: dict[str, dict] = field(default_factory=dict)
    processes: dict[str, dict] = field(default_factory=dict)
    objects: dict[str, dict] = field(default_factory=dict)
    stressors: dict[str, dict] = field(default_factory=dict)
    aop_stressors: dict[str, list[dict]] = field(default_factory=dict)
    snapshot: dict = field(default_factory=dict)

    @property
    def snapshot_citation(self) -> str:
        sha = self.snapshot.get("sha256", {}).get("aop-wiki-xml.gz", "unknown")
        return (
            f"AOP-Wiki {self.snapshot.get('dump_kind', 'nightly')} dump "
            f"{self.snapshot.get('snapshot_date', 'unknown')}, "
            f"sha256(aop-wiki-xml.gz)={sha}"
        )


def _read_tsv(path: Path) -> list[dict]:
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def load_corpus(data_dir: Path) -> Corpus:
    data_dir = Path(data_dir)
    corpus = Corpus()
    corpus.aops = {r["aop_id"]: r for r in _read_tsv(data_dir / "aops.tsv")}
    corpus.key_events = {
        r["event_id"]: r for r in _read_tsv(data_dir / "key_events.tsv")
    }
    corpus.kers = {
        r["ker_id"]: r for r in _read_tsv(data_dir / "key_event_relationships.tsv")
    }
    for r in _read_tsv(data_dir / "aop_kers.tsv"):
        corpus.aop_kers.setdefault(r["aop_id"], []).append(r)
    for r in _read_tsv(data_dir / "ke_components.tsv"):
        corpus.components.setdefault(r["event_id"], []).append(r)
    corpus.actions = {r["wiki_id"]: r for r in _read_tsv(data_dir / "bio_actions.tsv")}
    corpus.processes = {
        r["wiki_id"]: r for r in _read_tsv(data_dir / "bio_processes.tsv")
    }
    corpus.objects = {r["wiki_id"]: r for r in _read_tsv(data_dir / "bio_objects.tsv")}
    corpus.stressors = {
        r["stressor_id"]: r for r in _read_tsv(data_dir / "stressors.tsv")
    }
    for r in _read_tsv(data_dir / "aop_stressors.tsv"):
        corpus.aop_stressors.setdefault(r["aop_id"], []).append(r)
    snapshot_path = data_dir / "aopwiki-snapshot.yaml"
    if snapshot_path.exists():
        with open(snapshot_path) as fh:
            corpus.snapshot = yaml.safe_load(fh)
    return corpus


def load_action_mappings(sssom_path: Path) -> dict[str, ActionMapping]:
    """Read the action->PATO SSSOM table, keyed by the AOP-Wiki action
    source_id (the local part of the AOPWIKIBA subject curie)."""
    mappings: dict[str, ActionMapping] = {}
    with open(sssom_path, newline="") as fh:
        rows = csv.DictReader(
            (line for line in fh if not line.startswith("#")), delimiter="\t"
        )
        for r in rows:
            local = r["subject_id"].split(":", 1)[1]
            mappings[local] = ActionMapping(
                subject_id=r["subject_id"],
                subject_label=r["subject_label"],
                predicate_id=r["predicate_id"],
                object_id=r["object_id"],
                object_label=r["object_label"],
                confidence=r["confidence"],
                mapping_date=r["mapping_date"],
                comment=r.get("comment", "") or "",
            )
    return mappings


# ---------------------------------------------------------------------------
# Identifier helpers
# ---------------------------------------------------------------------------


def _num(aopwiki_id: str) -> str:
    """'Aop:425' -> '425' (same for Event:, Relationship:, Stressor:)."""
    return aopwiki_id.split(":", 1)[1]


def model_id(aop_id: str) -> str:
    return f"aop_cam:aop-{_num(aop_id)}"


def node_id(aop_id: str, event_id: str) -> str:
    return f"aop_cam:aop-{_num(aop_id)}/event-{_num(event_id)}"


def wiki_page(aopwiki_id: str) -> str:
    """CURIE for the AOP-Wiki page of a record, e.g. AOPWIKI:events/1250."""
    kind, num = aopwiki_id.split(":", 1)
    path = {"Aop": "aops", "Event": "events", "Relationship": "relationships",
            "Stressor": "stressors"}[kind]
    return f"AOPWIKI:{path}/{num}"


def vocab_curie(source: str, source_id: str) -> str | None:
    """CURIE for an AOP-Wiki vocabulary entry, or None if ungroundable.

    AOP-Wiki stores full CURIEs for OBO-style sources (GO:0005006,
    PR:000006933, VT:0002327, ...) and bare ids for MESH (D006965).
    """
    source_id = (source_id or "").strip()
    if not source_id or source in ("", "N/A", "WIKI"):
        return None
    if ":" in source_id:
        return source_id
    if source == "MESH":
        return f"MESH:{source_id}"
    return None


# ---------------------------------------------------------------------------
# Receipts
# ---------------------------------------------------------------------------


def upstream_receipt(corpus: Corpus, record_id: str) -> EvidenceItem:
    """Class-1 receipt: AOP-Wiki supplied this assignment."""
    return EvidenceItem(
        term=ECO_IMPORTED,
        reference=wiki_page(record_id),
        description=(
            f"Ontology id supplied by AOP-Wiki on {record_id}; "
            f"source: {corpus.snapshot_citation}."
        ),
    )


def sssom_receipt(mapping: ActionMapping) -> EvidenceItem:
    """Class-2 receipt: assignment made through the committed SSSOM table."""
    desc = (
        f"AOP-Wiki biological action '{mapping.subject_label}' mapped to "
        f"{mapping.object_id} '{mapping.object_label}' "
        f"({mapping.predicate_id}, confidence {mapping.confidence}) per "
        f"mappings/{ACTION_MAPPING_FILE} dated {mapping.mapping_date}."
    )
    if mapping.comment:
        desc += f" Note: {mapping.comment}"
    return EvidenceItem(
        term=ECO_CURATOR,
        reference=ACTION_MAPPING_SET,
        supporting_objects=[mapping.subject_id, mapping.object_id],
        description=desc,
    )


def _provenance(row: dict, corpus: Corpus) -> list[ProvenanceInfo]:
    return [
        ProvenanceInfo(
            created=row.get("created") or None,
            modified=row.get("updated") or None,
            source=corpus.snapshot_citation,
        )
    ]


# ---------------------------------------------------------------------------
# Building models
# ---------------------------------------------------------------------------


def _build_component(
    comp_row: dict,
    event_id: str,
    corpus: Corpus,
    action_mappings: dict[str, ActionMapping],
    warnings: list[str],
) -> KeyEventComponent | None:
    component = KeyEventComponent()

    action_row = corpus.actions.get(comp_row["action_wiki_id"])
    if action_row is not None:
        mapping = action_mappings.get(action_row["source_id"])
        if mapping is None:
            raise LoaderError(
                f"{event_id}: biological action '{action_row['name']}' "
                f"(source_id {action_row['source_id']}) is not in "
                f"mappings/{ACTION_MAPPING_FILE}; refusing to guess. "
                "Add a reviewed SSSOM row and re-run."
            )
        component.direction = DirectionAssociation(
            term=DirectionTermObject(id=mapping.object_id, label=mapping.object_label),
            evidence=[sssom_receipt(mapping)],
        )

    process_row = corpus.processes.get(comp_row["process_wiki_id"])
    if process_row is not None:
        curie = vocab_curie(process_row["source"], process_row["source_id"])
        if curie is None:
            warnings.append(
                f"{event_id}: process '{process_row['name']}' "
                f"(source {process_row['source'] or 'none'}) has no CURIE form; "
                "association skipped."
            )
        else:
            component.process = ProcessAssociation(
                term=ProcessTermObject(id=curie, label=process_row["name"]),
                evidence=[upstream_receipt(corpus, event_id)],
            )

    object_row = corpus.objects.get(comp_row["object_wiki_id"])
    if object_row is not None:
        curie = vocab_curie(object_row["source"], object_row["source_id"])
        if curie is None:
            warnings.append(
                f"{event_id}: object '{object_row['name']}' "
                f"(source {object_row['source'] or 'none'}) has no CURIE form; "
                "association skipped."
            )
        else:
            component.object = ObjectAssociation(
                term=ObjectTermObject(id=curie, label=object_row["name"]),
                evidence=[upstream_receipt(corpus, event_id)],
            )

    if component.process is None and component.object is None and component.direction is None:
        return None
    return component


def _build_node(
    aop_id: str,
    event_id: str,
    event_type: str,
    corpus: Corpus,
    action_mappings: dict[str, ActionMapping],
    warnings: list[str],
) -> KeyEventNode:
    ke = corpus.key_events[event_id]
    node = KeyEventNode(
        id=node_id(aop_id, event_id),
        title=ke["title"],
        aopwiki_id=event_id,
        event_type=event_type,
        provenances=_provenance(ke, corpus),
    )
    level = ke["biological_organization_level"].strip().lower()
    if level:
        node.level_of_biological_organization = level

    if ke["cell_term_id"]:
        node.occurs_in_cell_type = CellTypeAssociation(
            term=CellTypeTermObject(id=ke["cell_term_id"], label=ke["cell_term_name"]),
            evidence=[upstream_receipt(corpus, event_id)],
        )
    if ke["organ_term_id"]:
        node.occurs_in_anatomy = GrossAnatomyAssociation(
            term=AnatomyTermObject(id=ke["organ_term_id"], label=ke["organ_term_name"]),
            evidence=[upstream_receipt(corpus, event_id)],
        )

    for comp_row in corpus.components.get(event_id, []):
        component = _build_component(
            comp_row, event_id, corpus, action_mappings, warnings
        )
        if component is not None:
            node.components.append(component)
    return node


def build_model(
    aop_id: str,
    corpus: Corpus,
    action_mappings: dict[str, ActionMapping],
    warnings: list[str],
) -> AopModel:
    aop = corpus.aops[aop_id]
    mies = set(filter(None, aop["mie_event_ids"].split("|")))
    aos = set(filter(None, aop["ao_event_ids"].split("|")))

    # Membership: every event on one of this AOP's KERs, plus the asserted
    # MIEs and AOs (which can exist without any relationship yet).
    ker_rows = corpus.aop_kers.get(aop_id, [])
    events: set[str] = set(mies) | set(aos)
    for row in ker_rows:
        ker = corpus.kers[row["ker_id"]]
        events.add(ker["upstream_event_id"])
        events.add(ker["downstream_event_id"])
    events.discard("")

    def event_type(event_id: str) -> str:
        if event_id in mies:
            return "molecular_initiating_event"
        if event_id in aos:
            return "adverse_outcome"
        return "key_event"

    nodes: dict[str, KeyEventNode] = {}
    for event_id in sorted(events, key=lambda e: int(_num(e))):
        nodes[event_id] = _build_node(
            aop_id, event_id, event_type(event_id), corpus, action_mappings, warnings
        )

    # Causal edges hang off their upstream node.
    for row in sorted(ker_rows, key=lambda r: int(_num(r["ker_id"]))):
        ker = corpus.kers[row["ker_id"]]
        upstream = nodes[ker["upstream_event_id"]]
        upstream.causal_associations.append(
            CausalAssociation(
                predicate=ADJACENCY_PREDICATE[row["adjacency"]],
                downstream_event=node_id(aop_id, ker["downstream_event_id"]),
                aopwiki_ker_id=row["ker_id"],
                evidence_level=CONFIDENCE.get(row["evidence"]),
                quantitative_understanding=CONFIDENCE.get(
                    row["quantitative_understanding"]
                ),
                evidence=[upstream_receipt(corpus, row["ker_id"])],
            )
        )

    model = AopModel(
        id=model_id(aop_id),
        title=aop["title"],
        aopwiki_id=aop_id,
        oecd_status=aop["oecd_status"] or None,
        key_events=[nodes[e] for e in sorted(nodes, key=lambda e: int(_num(e)))],
        provenances=_provenance(aop, corpus),
    )

    for srow in corpus.aop_stressors.get(aop_id, []):
        stressor = corpus.stressors.get(srow["stressor_id"])
        if stressor is None:
            continue
        model.stressors.append(
            StressorTermObject(
                id=wiki_page(srow["stressor_id"]), label=stressor["name"]
            )
        )
    return model


def strip_unknown_type(obj) -> None:
    """linkml's pythongen leaves a spurious 'unknown_type' attribute on every
    instance of a class with a designates_type slot, which then leaks into
    dumps. Remove it recursively (generator bug workaround; the real 'type'
    discriminator is set correctly and untouched)."""
    if isinstance(obj, list):
        for item in obj:
            strip_unknown_type(item)
    elif isinstance(obj, YAMLRoot):
        if "unknown_type" in vars(obj):
            delattr(obj, "unknown_type")
        for name, value in list(vars(obj).items()):
            if not name.startswith("_"):
                strip_unknown_type(value)


def build_collection(
    data_dir: Path,
    sssom_path: Path,
    aop_ids: list[str] | None = None,
) -> tuple[ModelCollection, list[str]]:
    """Build a ModelCollection from the TSV corpus.

    Returns the collection and the list of grounding warnings (source
    values that could not be grounded and were skipped).
    """
    corpus = load_corpus(data_dir)
    action_mappings = load_action_mappings(sssom_path)
    if aop_ids is None:
        aop_ids = list(corpus.aops)
    missing = [a for a in aop_ids if a not in corpus.aops]
    if missing:
        raise LoaderError(f"AOP ids not in corpus: {', '.join(missing)}")

    warnings: list[str] = []
    collection = ModelCollection(
        snapshot_date=corpus.snapshot.get("snapshot_date"),
        models=[
            build_model(a, corpus, action_mappings, warnings)
            for a in sorted(aop_ids, key=lambda a: int(_num(a)))
        ],
    )
    strip_unknown_type(collection)
    return collection, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Load the AOP-Wiki TSV corpus into aop_cam instances."
    )
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument(
        "--mappings",
        type=Path,
        default=Path("mappings") / ACTION_MAPPING_FILE,
        help="Path to the action->PATO SSSOM table.",
    )
    parser.add_argument(
        "--aops",
        nargs="+",
        metavar="AOP_ID",
        help="AOP ids to load (e.g. Aop:425); default: all.",
    )
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args(argv)

    collection, warnings = build_collection(args.data_dir, args.mappings, args.aops)
    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    yaml_dumper.dump(collection, str(args.output))
    n_edges = sum(
        len(ke.causal_associations) for m in collection.models for ke in m.key_events
    )
    print(
        f"Wrote {len(collection.models)} models, "
        f"{sum(len(m.key_events) for m in collection.models)} key event nodes, "
        f"{n_edges} causal associations -> {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
