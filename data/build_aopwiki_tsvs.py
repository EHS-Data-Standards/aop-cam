#!/usr/bin/env python3
"""Build a TSV corpus from the AOP-Wiki nightly XML dump.

Usage:
    python3 -I build_aopwiki_tsvs.py <aop-wiki-xml path> <output dir>

Emits entity tables keyed by AOP-Wiki public identifiers (Aop:N, Event:N,
Relationship:N — the same key style as the official aop_ke_*.tsv downloads,
so everything joins). The three official TSVs (aop_ke_mie_ao, aop_ke_ker,
aop_ke_ec) remain the source for per-AOP event typing; these tables add the
entity-level detail the official TSVs do not carry.
"""
import csv
import sys
import xml.etree.ElementTree as ET

NS = "{http://www.aopkb.org/aop-xml}"


def text(el, tag):
    c = el.find(NS + tag)
    return (c.text or "").strip() if c is not None and c.text else ""


def term(el, tag):
    """Return (source_id, name) for a cell-term / organ-term style child."""
    c = el.find(NS + tag)
    if c is None:
        return "", ""
    return text(c, "source-id"), text(c, "name")


def main(xml_path, out_dir):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # ------------------------------------------------------------------
    # UUID -> public AOP-Wiki id maps, from the vendor-specific block
    # ------------------------------------------------------------------
    vs = root.find(NS + "vendor-specific")
    maps = {}  # element kind -> {uuid: public id}
    prefix = {
        "aop-reference": "Aop:",
        "key-event-reference": "Event:",
        "key-event-relationship-reference": "Relationship:",
        "stressor-reference": "Stressor:",
        "chemical-reference": "Chemical:",
        "biological-process-reference": "",
        "biological-object-reference": "",
        "biological-action-reference": "",
        "taxonomy-reference": "",
    }
    for ref in vs:
        kind = ref.tag.split("}")[-1]
        maps.setdefault(kind, {})[ref.get("id")] = prefix.get(kind, "") + ref.get(
            "aop-wiki-id", ""
        )

    def pid(kind, uuid):
        return maps.get(kind + "-reference", {}).get(uuid, uuid or "")

    def write(name, header, rows):
        path = f"{out_dir}/{name}.tsv"
        with open(path, "w", newline="") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            w.writerow(header)
            w.writerows(rows)
        print(f"{name}.tsv\t{len(rows)} rows")

    # ------------------------------------------------------------------
    # aops.tsv
    # ------------------------------------------------------------------
    rows = []
    aop_stressor_rows = []
    aop_ker_rows = []
    for aop in root.findall(NS + "aop"):
        aid = pid("aop", aop.get("id"))
        status = aop.find(NS + "status")
        mies = [
            pid("key-event", m.get("key-event-id"))
            for m in aop.findall(NS + "molecular-initiating-event")
        ]
        aos = [
            pid("key-event", a.get("key-event-id"))
            for a in aop.findall(NS + "adverse-outcome")
        ]
        rows.append(
            [
                aid,
                aop.get("id"),
                text(aop, "title"),
                text(aop, "short-name"),
                text(status, "wiki-status") if status is not None else "",
                text(status, "oecd-status") if status is not None else "",
                text(status, "saaop-status") if status is not None else "",
                "|".join(mies),
                "|".join(aos),
                text(aop, "creation-timestamp"),
                text(aop, "last-modification-timestamp"),
            ]
        )
        st = aop.find(NS + "aop-stressors")
        if st is not None:
            for s in st.findall(NS + "aop-stressor"):
                aop_stressor_rows.append(
                    [aid, pid("stressor", s.get("stressor-id")), text(s, "evidence")]
                )
        kers = aop.find(NS + "key-event-relationships")
        if kers is not None:
            for r in kers.findall(NS + "relationship"):
                aop_ker_rows.append(
                    [
                        aid,
                        pid("key-event-relationship", r.get("id")),
                        text(r, "adjacency"),
                        text(r, "evidence"),
                        text(r, "quantitative-understanding-value"),
                    ]
                )
    write(
        "aops",
        [
            "aop_id",
            "uuid",
            "title",
            "short_name",
            "wiki_status",
            "oecd_status",
            "saaop_status",
            "mie_event_ids",
            "ao_event_ids",
            "created",
            "updated",
        ],
        rows,
    )
    write("aop_stressors", ["aop_id", "stressor_id", "evidence"], aop_stressor_rows)
    write(
        "aop_kers",
        ["aop_id", "ker_id", "adjacency", "evidence", "quantitative_understanding"],
        aop_ker_rows,
    )

    # ------------------------------------------------------------------
    # key_events.tsv + ke_components.tsv
    # ------------------------------------------------------------------
    rows = []
    comp_rows = []
    for ke in root.findall(NS + "key-event"):
        kid = pid("key-event", ke.get("id"))
        cell_id, cell_name = term(ke, "cell-term")
        organ_id, organ_name = term(ke, "organ-term")
        rows.append(
            [
                kid,
                ke.get("id"),
                text(ke, "title"),
                text(ke, "short-name"),
                text(ke, "biological-organization-level"),
                cell_id,
                cell_name,
                organ_id,
                organ_name,
                text(ke, "creation-timestamp"),
                text(ke, "last-modification-timestamp"),
            ]
        )
        be = ke.find(NS + "biological-events")
        if be is not None:
            for ev in be.findall(NS + "biological-event"):
                comp_rows.append(
                    [
                        kid,
                        pid("biological-action", ev.get("action-id")),
                        pid("biological-process", ev.get("process-id")),
                        pid("biological-object", ev.get("object-id")),
                    ]
                )
    write(
        "key_events",
        [
            "event_id",
            "uuid",
            "title",
            "short_name",
            "biological_organization_level",
            "cell_term_id",
            "cell_term_name",
            "organ_term_id",
            "organ_term_name",
            "created",
            "updated",
        ],
        rows,
    )
    write(
        "ke_components",
        ["event_id", "action_wiki_id", "process_wiki_id", "object_wiki_id"],
        comp_rows,
    )

    # ------------------------------------------------------------------
    # key_event_relationships.tsv
    # ------------------------------------------------------------------
    rows = []
    for ker in root.findall(NS + "key-event-relationship"):
        rid = pid("key-event-relationship", ker.get("id"))
        title = ker.find(NS + "title")
        up = text(title, "upstream-id") if title is not None else ""
        down = text(title, "downstream-id") if title is not None else ""
        rows.append(
            [
                rid,
                ker.get("id"),
                pid("key-event", up),
                pid("key-event", down),
                text(ker, "creation-timestamp"),
                text(ker, "last-modification-timestamp"),
            ]
        )
    write(
        "key_event_relationships",
        ["ker_id", "uuid", "upstream_event_id", "downstream_event_id", "created", "updated"],
        rows,
    )

    # ------------------------------------------------------------------
    # stressors.tsv (with any chemical linkage present)
    # ------------------------------------------------------------------
    rows = []
    for s in root.findall(NS + "stressor"):
        chem_ids = [
            pid("chemical", c.get("chemical-id"))
            for c in s.iter()
            if c.get("chemical-id")
        ]
        rows.append(
            [
                pid("stressor", s.get("id")),
                s.get("id"),
                text(s, "name"),
                "|".join(chem_ids),
            ]
        )
    write("stressors", ["stressor_id", "uuid", "name", "chemical_ids"], rows)

    # ------------------------------------------------------------------
    # chemicals.tsv
    # ------------------------------------------------------------------
    rows = []
    for c in root.findall(NS + "chemical"):
        syns = c.find(NS + "synonyms")
        syn = (
            "|".join(
                (x.text or "").strip() for x in syns if (x.text or "").strip()
            )
            if syns is not None
            else ""
        )
        rows.append(
            [
                pid("chemical", c.get("id")),
                c.get("id"),
                text(c, "preferred-name"),
                text(c, "casrn"),
                text(c, "dsstox-id"),
                text(c, "jchem-inchi-key"),
                syn,
            ]
        )
    write(
        "chemicals",
        ["chemical_id", "uuid", "preferred_name", "casrn", "dsstox_id", "inchi_key", "synonyms"],
        rows,
    )

    # ------------------------------------------------------------------
    # Controlled vocabularies: processes, objects, actions, taxonomy
    # ------------------------------------------------------------------
    for tag, name, kind in [
        ("biological-process", "bio_processes", "biological-process"),
        ("biological-object", "bio_objects", "biological-object"),
        ("biological-action", "bio_actions", "biological-action"),
        ("taxonomy", "taxonomy", "taxonomy"),
    ]:
        rows = []
        for el in root.findall(NS + tag):
            rows.append(
                [
                    pid(kind, el.get("id")),
                    el.get("id"),
                    text(el, "source"),
                    text(el, "source-id"),
                    text(el, "name"),
                ]
            )
        write(name, ["wiki_id", "uuid", "source", "source_id", "name"], rows)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
