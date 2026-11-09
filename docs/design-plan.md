# Plan: A GO-CAM-style Schema for the AOP Framework

**Date:** 2026-11-09
**Context:** Issue #76 proposes framing KE → KER → AOP as a GO-CAM-style causal
activity model. This plan compares the three schemas in play and lays out how to
draft the new AOP framework schema.

---

## 1. The three schemas in play, and what each one is

### gocam-py (`../gocam-py/src/gocam/schema/gocam.yaml`) — the paradigm donor

The GO-CAM schema is small (~950 lines) and its whole design fits in five ideas:

1. **Model** = one named causal graph (id, title, taxon, lifecycle `status`
   with a rule that production models must have activities, `activities`,
   shared `objects`, provenance, and an optional precomputed `query_index`).
2. **Activity** = one node, defined entirely by its *associations*: what
   enables it (`enabled_by`), what it does (`molecular_function`), where
   (`occurs_in`), what it is part of (`part_of`), and what it causes
   (`causal_associations`).
3. **Association** = an abstract class holding `evidence[]` and
   `provenances[]`, with a `designates_type` discriminator. Every edge and
   every term assignment is an Association subtype. **Evidence hangs off
   every individual assertion, not off the node.**
4. **CausalAssociation** = `predicate` (an RO term) + `downstream_activity`.
   Initial and terminal nodes are implicit: no incoming edge = initial, no
   outgoing edge = terminal.
5. **EvidenceItem** = ECO term (with a binding enum) + publication reference +
   supporting objects. Typed `TermObject` subclasses with `id_prefixes`
   constrain what each slot can point at (same idea as SOMA's `*Reference`
   classes).

### linkml-aop (`EHS-Data-Standards/linkml-aop`) — the data reality

Your hunch is confirmed. The original hand-written schema
(`linkml_aop.yaml`) is **archived** (September 2026). The current schema,
`aop_emod_linkml.yaml`, is generated from the AOP-Wiki EMOD 3.0 database and
is a faithful relational mirror of it: integer ids, join tables
(`AopToEvent`, `KeRelationshipToTaxon`, ...), admin entities (License,
Handbook, OecdStatus), and KER evidence as free-text narrative fields
(`how_it_works`, `biological_plausibility`, `empirical_support`, ...). It is
**not** GO-CAM-shaped: no typed causal predicates, no per-assertion evidence
objects, causality expressed only as upstream/downstream id pairs plus an
adjacency flag.

It does carry two things the other schemas lack:

- **EventComponent**: action + object + process per Key Event — AOP-Wiki's
  proto-EQ decomposition, with ids so components can be shared.
- **The EMOD extension**: Assay, Observation, Evidence, BioTargetFamily,
  TestGuideline — a regulatory-flavored assay layer that overlaps SOMA's
  territory (see section 5).

### SOMA's `aop_framework.yaml` — the current in-between

Compositional KE slots (GO process, direction enum, CL/UBERON context),
AdverseOutcome as a terminal KeyEvent (recent change), evidence attachable to
KEs and KERs, assays linked via `informs_on_key_event`. Closer in spirit to
GO-CAM than linkml-aop is, but ad hoc: `relationship_type` is a free string,
evidence lives on records rather than on assertions, and there is no model
lifecycle.

## 2. The core mapping

| GO-CAM | New AOP schema | Notes |
|---|---|---|
| Model | AopModel | One AOP (or AOP network slice) as a named causal graph; adopt lifecycle status enum; taxon applicability |
| Activity | KeyEventNode | A KE instance in a model |
| enabled_by / molecular_function / occurs_in / part_of | ProcessAssociation (GO/MESH), ObjectAssociation, DirectionAssociation (PATO), CellTypeAssociation (CL), AnatomyAssociation (UBERON), LevelAssociation | The KE's contextual dimensions, each an Association subtype carrying its own evidence — this is the single biggest paradigm upgrade over current SOMA, where these are bare slot values |
| CausalAssociation | CausalAssociation (KER) | `predicate` from an RO causal-predicate enum + `downstream_event`; keep AOP-Wiki's adjacency, weight of evidence, quantitative understanding as additional slots |
| EvidenceItem | EvidenceItem | ECO-typed, with publication reference; **a SOMA assay becomes the supporting object of an EvidenceItem** — formalizing `informs_on_key_event` as evidence on an assertion |
| initial / terminal activity (implicit) | MIE / AO | Keep explicit subtyping too (AOP practice names them), but the graph position becomes checkable: an AO with outgoing causal edges is a modeling error a validator can catch |
| TermObject subclasses with id_prefixes | SOMA's `*Reference` pattern | Already aligned; converge naming conventions |

Mapping AOP-Wiki's edge semantics onto RO:
- `adjacent` → RO:0002412 (immediately causally upstream of), or the
  regulates variants where direction of effect is curated
- `non-adjacent` → RO:0002411 (causally upstream of)
- The 11 AOP-Wiki biological actions → PATO directional qualities (a tiny
  hand-curated mapping table, done once)

## 3. What GO-CAM does not cover (the AOP extensions)

These are additions, not deviations:

1. **Direction of change as node state.** GO-CAM expresses direction through
   its relation types; AOPs need "decreased X" as part of the node itself.
   DirectionAssociation (PATO quality) carries it.
2. **Levels of biological organization.** GO-CAM lives at molecular/cellular
   scale; AOP nodes span molecular → population. A level slot (existing
   enum), plus UBERON gross anatomy on nodes (GO-CAM has
   GrossAnatomyAssociation already, so even this is nearly covered).
3. **Outcome grounding.** The AO is the terminal node, defined by its
   composition; optional computed `outcome_mappings` (HP / MONDO / UPHENO)
   decorate it (see the outcome-grounding discussion in issue #76).
4. **Regulatory metadata.** OECD status, test guidelines — keep as
   model-level and evidence-level metadata, imported from the linkml-aop
   vocabulary rather than reinvented.

## 4. Implementation steps

1. **Placement decision (made 2026-11-09).** The schema lives in its own
   repo — this one (EHS-Data-Standards/aop-cam) — so that the schema and
   the graph instances can be imported separately by soma, somamech, and
   other consumers, each versioned on its own cadence. SOMA imports the
   schema; instance releases are tagged to the AOP-Wiki snapshot they were
   built from. EMOD is not a dependency.
2. **Skeleton.** AopModel, KeyEventNode, the Association hierarchy
   (abstract Association with evidence/provenance + the TermAssociation
   subtypes + CausalAssociation), EvidenceItem, ProvenanceInfo, and the
   typed term-object/reference classes. Mirror the GO-CAM *pattern*; do not
   import gocam.yaml directly (its id prefixes, GO-specific bindings, and
   gene-product machinery don't transfer).
3. **Causal predicate enum.** Minimal RO subset needed by AOPs:
   causally upstream of, immediately causally upstream of, the
   positive/negative regulates pair, and causally upstream of with
   positive/negative effect. Document the AOP-Wiki adjacency mapping.
4. **ETL from the corpus.** A loader from `data/*.tsv` (built
   2026-11-09: aops, key_events, key_event_relationships, ke_components,
   bio_* vocabularies) into instances of the new schema. The 11-row
   action→PATO mapping table is part of this. Validate by round-tripping the
   respiratory slice (Aop:148, 411, 424, 425) and comparing against the
   hand-curated network in the paper's Figure 2.
5. **SOMA integration.** An assay's `informs_on_key_event` link becomes (or
   is supplemented by) an EvidenceItem on the relevant node association —
   assays are the experimental support layer of the model. AdverseOutcome
   stays a KeyEvent subtype; `outcome_term` evolves into computed
   `outcome_mappings` per the uPheno discussion.
6. **Assay layer (decision 2026-11-09): SOMA assays are the evidence
   layer.** EMOD is ignored unless something it covers is modeled better
   natively here; the only candidates worth absorbing later are
   test-guideline references and target-family groupings, as small native
   classes if a use case demands them.
7. **Validation and docs.** Examples + counter-examples (an AO with outgoing
   causal edges; a causal edge with a non-RO predicate; a production model
   with no events), gen-doc integration, and eventually a query_index
   analog for precomputed network statistics.

## 5. Open questions

- **How literal to be with GO-CAM?** Recommendation: mirror the pattern
  (Association-with-evidence, typed predicates, model lifecycle), not the
  vocabulary. A KE is not a molecular Activity; pretending otherwise would
  confuse both communities.
- **Evidence granularity vs curation burden.** Per-assertion evidence is the
  paradigm's power, but AOP-Wiki data arrives with narrative-level evidence
  only. Make evidence optional everywhere; let the loader attach what it can
  (weight-of-evidence labels as model-level annotations) and let new
  curation do better.
- **One model per AOP, or per network?** GO-CAM models merge by shared
  ontology ids; start with one model per AOP-Wiki AOP (keeps citation
  clean), and treat networks (like Figure 2) as merged views.
- **Population-level outcomes** sit outside every phenotype ontology;
  composition carries them, mappings stay empty, and that is fine.

## 6. Suggested first milestone

A draft `aop_cam.yaml` plus a loader that round-trips the four respiratory
AOPs from the TSV corpus into valid instances, with the Figure 2 network
reproduced by a traversal query. That exercises every design decision above
on data the working group already knows by heart.
