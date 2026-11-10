# Project Context

**Last updated:** 2026-11-09. This file captures where aop-cam came from, the
design discussions behind it, the decisions made, and where the work stands —
so a new contributor (or a future working session) can pick up without
re-deriving any of it. Companion documents: `docs/design-plan.md` (the schema
plan), `docs/grounding-receipts.md` (the receipt rules), and issue #2 (the
GO-CAM framing proposal, transferred from the soma repo).

## What this repo is

Adverse Outcome Pathways represented as **causal activity models** (CAM = the
GO-CAM paradigm): an AOP is a named causal graph; each Key Event is a node
whose meaning lives in associations to ontology terms in context; each Key
Event Relationship is a typed causal edge drawn from the Relation Ontology;
evidence attaches to individual assertions, not whole records. "Models, not
terms": no new ontology term is ever minted for a pathway or an outcome —
everything is composed from existing terms and wired together.

## How it started

The SOMA paper's Outcomes Working Group review asked a deceptively simple
question: *"I am looking for data on this outcome — what assays might be
relevant?"* The SOMA schema at the time could not answer it: AdverseOutcome
was not a KeyEvent (despite its own description), outcomes had no ontology
grounding, and the only outcome-to-KE bridge was a curated AOP record. SOMA
fixed the immediate gap (AdverseOutcome is_a KeyEvent, outcome term slot,
container-level outcomes), but the discussion kept going and produced the
design positions below, which this repo exists to implement properly.

## Design positions (with reasoning)

1. **Single-term outcome grounding is a dead end.** "Decreased lung
   function" is not an HPO phenotype, a MONDO disease, or a PATO quality on
   its own. HPO itself obsoleted "Decreased pulmonary function"
   (HP:0005952) — the ontology community already tried holding vague
   functional-decline concepts as single terms and retreated to measurable
   precomposed phenotypes. MONDO fits only when the outcome is literally
   disease onset. PATO qualities need a bearer.

2. **Composition is the anchor; terms are decoration.** An outcome (or any
   Key Event) is defined by entity + quality in context: biological process
   (GO) or object + direction of change (PATO) + anatomy (UBERON) + level of
   biological organization. uPheno classes are themselves precomputed EQ
   compositions, so storing the EQ pieces stores the source of truth; any
   precomposed term is derivable packaging. `outcome_mappings`
   (HP/MONDO/UPHENO) decorate for discovery; candidates are *computable* by
   matching the stored composition against uPheno's pattern space, so
   mapping is a CI aid, not a curation burden.

3. **Nobody has mapped AOPs to uPheno or EQ before** (checked 2026-11-09).
   Closest neighbors: CTD manually mapped the ~179 AO terms to their
   disease/GO vocabularies (now stale — manual tables rot as AOP-Wiki
   edits titles); a 2026 preprint annotates KEs with GO BP terms for
   transcriptomics; AOP-Wiki's own Key Event Components
   (process/object/action) are a proto-EQ decomposition nobody connected to
   the phenotype world. Computing mappings from composition fixes the
   staleness problem CTD hit, and this team (SOMA working group + the
   Monarch/uPheno lineage) is positioned to do it first.

4. **The GO-CAM paradigm fits AOPs almost exactly.** KE node with
   GO/CL/UBERON context ≈ Activity with its term associations; KER ≈
   CausalAssociation (RO predicate + evidence); AOP ≈ Model; MIE/AO ≈
   initial/terminal nodes (graph position is checkable against the asserted
   event_type); AOP networks ≈ models merging on shared ontology ids. The
   schema mirrors the *pattern* but does not import gocam.yaml — a KE is
   not a molecular Activity, and the gene-product machinery doesn't
   transfer. AOP extensions beyond GO-CAM: direction of change as node
   state (PATO), levels up to population, outcome mappings.

5. **The end-state vision (three layers).** Layer 1: every node
   self-describing via EQ composition. Layer 2: AOP-Wiki slices curated
   into CAMs = a knowledge graph of mechanistic pathways. Layer 3: that KG
   serves extraction pipelines (somamech) as a *semantic receipt* — when an
   agent asserts "this assay informs KE X", the claim is checked against
   the KE's composition (cell type descends-from, anatomy descends-from,
   process matches or is causally adjacent). Complementary to somamech's
   textual receipts: the quote proves the paper said it; the KG check
   proves the claim coheres with the mechanism it was filed under. Also
   enables placement (rank candidate KEs for an extraction) and gap
   analysis (which KEs lack assay evidence → corpus prioritization).

6. **Every text-to-term assignment carries a receipt.** Five classes,
   strongest first: upstream-asserted (AOP-Wiki supplied the id),
   mapping-table (versioned SSSOM), lexical match (reproducible),
   curator/agent judgment (candidates + confirmation recorded), and
   compositional + negative receipts ("searched uPheno on date X, no
   match" — so future hits surface as candidates instead of silence).
   Details and the ECO code for each class: `docs/grounding-receipts.md`.

## Decisions log

- **Standalone repo** (not inside soma): schema and graph instances are
  imported separately by soma, somamech, and others; each versioned on its
  own cadence; instance releases pinned to AOP-Wiki quarterly snapshots
  (nightly dumps are overwritten daily — not citable). Also establishes
  provenance for this work publicly and datably.
- **EMOD is ignored.** Not a dependency, not an ingest format. The only
  things worth absorbing later, as small native classes if a use case
  demands them: test-guideline references and target-family groupings.
- **SOMA remains the experimental evidence layer.** Its assays attach here
  as EvidenceItem.supporting_objects on node associations. SOMA's
  aop_framework.yaml stays until this schema is stable, then soma swaps to
  importing it.
- **Name: aop_cam** (CAM = causal activity model; the copier scaffold's
  aop_cap was a typo, fixed project-wide).

## State of the work (2026-11-09)

Done:
- Baseline schema `src/aop_cam/schema/aop_cam.yaml`: ModelCollection →
  AopModel → KeyEventNode, the Association hierarchy with per-assertion
  evidence, CausalAssociation with the RO predicate enum (values copied
  from gocam.yaml's CausalPredicateEnum), EvidenceItem, term objects,
  aopwiki_id crosswalk slots. Tests pass; the counter-example proves a
  free-text predicate ("leads to") is rejected by the enum.
- AOP-Wiki TSV corpus in `data/` (12 tables + builder script, from the
  2026-11-09 nightly dump; includes the four respiratory AOPs 148, 411,
  424, 425 used by the SOMA paper's Figure 2).
- `mappings/aopwiki-action-to-pato.sssom.tsv`: all 11 biological actions
  mapped to PATO, OAK-verified; closeMatch rows carry explanatory comments.
- Receipts doc, design plan, issue #2.
- **The loader** (`src/aop_cam/loader.py`, run as `python -m
  aop_cam.loader`): `data/*.tsv` → ModelCollection instances with
  per-assertion receipts (class 1 ECO:0000311 citing the hashed dump in
  `data/SNAPSHOT.yaml`; class 2 ECO:0000305 citing the SSSOM row; an
  action missing from the table fails the build). `src/aop_cam/network.py`
  merges models on shared key events and checks event types against graph
  position. First contact with real data forced two schema evolutions:
  KeyEventNode now holds `components` (a list of KeyEventComponent
  grouping process+object+direction, because Events 941/962 carry two
  paired biological-event triples each and flat slots would lose the
  pairing), and the process/object vocabularies widened (AOP-Wiki
  processes also come from HP/MP/VT/NBO…, objects from CL/UBERON/FMA).
  Milestone met: the four respiratory AOPs round-trip and the merged
  traversal reproduces the paper's Figure 2 network exactly (11 nodes,
  13 adjacent edges, MIEs {941, 1392}, AO 1250) — see
  `tests/test_loader.py`. The full corpus also loads: 603 models, 3474
  nodes, 3350 edges, with exactly 2 ungroundable assertions (the
  "Acute phase proteins" object, source N/A). Known gaps, deliberate:
  stressors keep AOPWIKI ids (no chemical grounding pass yet, and the
  per-AOP stressor evidence level has nowhere to live on a TermObject);
  no AOP-level taxon table in the corpus, so `taxa` stays empty;
  AOP-Wiki's `wiki-status` is empty in the dump, so model `status` is
  unset. The generated dataclasses carry a linkml pythongen bug (a
  spurious `unknown_type` attribute from designates_type handling);
  `loader.strip_unknown_type` works around it before dumping.

Next (in order):
1. **uPheno candidate mapper**: composition → candidate outcome_mappings,
   as a CI/curation aid (and the negative-receipt generator).
2. **Consistency checker** for extraction pipelines: assay context vs KE
   composition (the Layer-3 semantic receipt), consumable by somamech CI.
3. **soma integration**: swap soma's AOP layer to import this schema;
   evolve soma's outcome_term into outcome_mappings.

## Related repos

- **EHS-Data-Standards/soma** — the assay/evidence schema (the paper's
  subject); remote `ehs` in local checkouts.
- **somamech** — the paper-extraction pipeline (corpus, claim/fetch skills,
  quote receipts); future consumer of the KG for semantic checking.
- **gocam-py** — the paradigm source; pattern mirrored, not imported.
- **EHS-Data-Standards/linkml-aop** — original hand-written AOP schema is
  archived (2026-09); current schema mirrors the AOP-Wiki EMOD database.
  Per the decisions log, not a dependency.
