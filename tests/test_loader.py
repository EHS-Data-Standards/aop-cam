"""Tests for the AOP-Wiki corpus loader: the first-milestone round-trip of
the four respiratory AOPs (148, 411, 424, 425) and the reproduction of the
SOMA paper's Figure 2 network by traversal of the merged models."""

from pathlib import Path

import pytest
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.loaders import yaml_loader

import aop_cam.datamodel.aop_cam as dm
from aop_cam.loader import (
    ACTION_MAPPING_SET,
    ECO_CURATOR,
    ECO_IMPORTED,
    LoaderError,
    build_collection,
    strip_unknown_type,
)
from aop_cam.network import event_type_position_errors, merge

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / "data"
SSSOM_PATH = REPO_ROOT / "mappings" / "aopwiki-action-to-pato.sssom.tsv"

RESPIRATORY_AOPS = ["Aop:148", "Aop:411", "Aop:424", "Aop:425"]

# The respiratory AOP network of the SOMA paper's Figure 2, as
# (upstream event, downstream event) pairs merged across the four models.
FIGURE_2_EDGES = {
    # Aop:148 - EGFR activation branch
    ("Event:941", "Event:2117"),
    ("Event:941", "Event:962"),
    ("Event:2117", "Event:962"),
    ("Event:962", "Event:1250"),
    # Aop:424 - CFTR branch
    ("Event:1392", "Event:1906"),
    ("Event:1906", "Event:1907"),
    ("Event:1907", "Event:1908"),
    # Aop:425 - FOXJ1 branch
    ("Event:1392", "Event:1911"),
    ("Event:1911", "Event:1912"),
    ("Event:1912", "Event:1908"),
    # Aop:411 - direct oxidative stress branch, shared spine
    ("Event:1392", "Event:1908"),
    ("Event:1908", "Event:1909"),
    ("Event:1909", "Event:1250"),
}


@pytest.fixture(scope="module")
def respiratory():
    collection, warnings = build_collection(DATA_DIR, SSSOM_PATH, RESPIRATORY_AOPS)
    return collection, warnings


def test_slice_loads_fully_grounded(respiratory):
    """The flagship slice must load with every term assignment grounded."""
    collection, warnings = respiratory
    assert warnings == []
    assert [str(m.aopwiki_id) for m in collection.models] == RESPIRATORY_AOPS
    assert str(collection.snapshot_date) == "2026-11-09"


def test_model_shapes(respiratory):
    collection, _ = respiratory
    by_id = {str(m.aopwiki_id): m for m in collection.models}
    assert len(by_id["Aop:148"].key_events) == 4
    assert len(by_id["Aop:411"].key_events) == 4
    assert len(by_id["Aop:424"].key_events) == 6
    assert len(by_id["Aop:425"].key_events) == 6
    # Edges per model, hanging off their upstream nodes.
    edges_424 = sum(
        len(ke.causal_associations) for ke in by_id["Aop:424"].key_events
    )
    assert edges_424 == 5
    # Stressors carried over with AOP-Wiki identity.
    assert [str(s.id) for s in by_id["Aop:148"].stressors] == ["AOPWIKI:stressors/303"]


def test_round_trip(respiratory, tmp_path):
    """Dump -> reload -> dump is stable and valid against the tree root."""
    collection, _ = respiratory
    out = tmp_path / "respiratory.yaml"
    yaml_dumper.dump(collection, str(out))
    reloaded = yaml_loader.load(str(out), target_class=dm.ModelCollection)
    # Loading re-triggers the pythongen designates_type artifact; strip it
    # the same way the loader does before comparing.
    strip_unknown_type(reloaded)
    assert yaml_dumper.dumps(reloaded) == yaml_dumper.dumps(collection)


def test_component_pairing_preserved(respiratory):
    """Event:941 has two AOP-Wiki biological events; each direction must
    stay attached to the process it was asserted with."""
    collection, _ = respiratory
    model = next(m for m in collection.models if str(m.aopwiki_id) == "Aop:148")
    node = next(ke for ke in model.key_events if str(ke.aopwiki_id) == "Event:941")
    assert len(node.components) == 2
    pairs = {
        (str(c.process.term.id), str(c.direction.term.id)) for c in node.components
    }
    assert pairs == {
        ("GO:0005006", "PATO:0000467"),  # occurrence of receptor activity
        ("GO:0016310", "PATO:0002300"),  # increased phosphorylation
    }


def test_every_term_assignment_carries_a_receipt(respiratory):
    collection, _ = respiratory
    for model in collection.models:
        for ke in model.key_events:
            assocs = [ke.occurs_in_cell_type, ke.occurs_in_anatomy]
            for comp in ke.components:
                assocs += [comp.process, comp.object, comp.direction]
            for assoc in filter(None, assocs):
                assert assoc.evidence, f"{ke.id}: bare assertion {assoc.type}"
                eco = {str(e.term) for e in assoc.evidence}
                if str(assoc.type) == "DirectionAssociation":
                    # Class-2 receipt: via the committed SSSOM table.
                    assert eco == {ECO_CURATOR}
                    assert {str(e.reference) for e in assoc.evidence} == {
                        ACTION_MAPPING_SET
                    }
                else:
                    # Class-1 receipt: AOP-Wiki supplied the id.
                    assert eco == {ECO_IMPORTED}
            for ca in ke.causal_associations:
                assert {str(e.term) for e in ca.evidence} == {ECO_IMPORTED}


def test_unmapped_action_fails_the_build(tmp_path):
    """Receipts rule for class 2: a source value absent from the mapping
    table fails the load instead of being guessed."""
    truncated = tmp_path / "truncated.sssom.tsv"
    lines = SSSOM_PATH.read_text().splitlines()
    header = [ln for ln in lines if ln.startswith(("#", "subject_id"))]
    body = [ln for ln in lines if not (ln.startswith(("#", "subject_id")))]
    truncated.write_text("\n".join(header + body[:2]) + "\n")
    with pytest.raises(LoaderError, match="refusing to guess"):
        build_collection(DATA_DIR, truncated, RESPIRATORY_AOPS)


def test_event_types_match_graph_position(respiratory):
    collection, _ = respiratory
    assert event_type_position_errors(collection) == []


def test_figure_2_network_reproduced_by_traversal(respiratory):
    """Merging the four models on shared key events yields the paper's
    Figure 2 respiratory network."""
    collection, _ = respiratory
    network = merge(collection)

    assert len(network.nodes) == 11
    assert {(e.upstream, e.downstream) for e in network.edges.values()} == (
        FIGURE_2_EDGES
    )
    # Graph position agrees with the asserted roles across the network.
    assert network.initial_nodes() == {"Event:941", "Event:1392"}
    assert network.terminal_nodes() == {"Event:1250"}
    # The models truly merge: the shared spine is reached from both MIEs.
    assert network.reachable_from({"Event:941"}) >= {"Event:962", "Event:1250"}
    assert network.reachable_from({"Event:1392"}) >= {"Event:1908", "Event:1250"}
    # Every key event lies on a path from a molecular initiating event.
    assert network.reachable_from(network.initial_nodes()) == set(network.nodes)
    # Shared events are attributed to every model that carries them.
    assert network.nodes["Event:1250"].models == set(RESPIRATORY_AOPS)
    # All KERs in this slice are curated as adjacent -> RO:0002412.
    assert {e.predicate for e in network.edges.values()} == {
        "immediately causally upstream of"
    }


def test_full_corpus_loads():
    """The loader holds up beyond the flagship slice: every AOP in the
    corpus builds, with only honest grounding warnings (never errors)."""
    collection, warnings = build_collection(DATA_DIR, SSSOM_PATH)
    assert len(collection.models) == len(
        [m for m in collection.models]
    )  # materialized
    assert len(collection.models) > 400
    for w in warnings:
        assert "no CURIE form" in w
