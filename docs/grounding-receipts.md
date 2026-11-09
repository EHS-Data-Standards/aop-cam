# Grounding Receipts: assigning AOP-Wiki text to ontology terms

Every ontology term in an aop_cam instance should be traceable: where the
source text came from, what method assigned the term, and how the assignment
can be re-verified. The schema supports this natively — every term assignment
is an Association carrying its own `evidence[]` — so receipts live *in the
data*, per assertion, with the canonical mapping records kept as versioned
SSSOM files under `mappings/`.

Receipt classes, strongest claim first:

## 1. Upstream-asserted (AOP-Wiki supplied the ID)

Key event components (process/object ids like GO:0008283), cell terms (CL)
and organ terms (UBERON) arrive from AOP-Wiki with ontology ids already
assigned. The receipt is the AOP-Wiki record id plus the pinned snapshot
(quarterly dump date + SHA-256 of the dump file; nightly dumps are
overwritten daily and are not citable). Evidence type: **ECO:0000311
(imported information)**. CI obligation: the **label-drift check** — the id
still exists, is not obsolete, and the stored label still matches a current
label or synonym (OAK validation).

## 2. Mapping-table (deterministic, versioned, SSSOM)

Closed vocabularies map through committed SSSOM files — see
`mappings/aopwiki-action-to-pato.sssom.tsv` for the 11 biological actions.
Each row carries predicate (exact/closeMatch), `mapping_justification`,
author, date, confidence, and a comment explaining any closeMatch. Evidence
type: **ECO:0000305 (curator inference used in manual assertion)**, with the
SSSOM record referenced from `supporting_objects`. CI obligation: the loader
may only emit assignments present in the table; an unmapped source value
fails the build instead of guessing.

## 3. Lexical-match (reproducible automation)

Free text matching an ontology label or synonym records: the source string
verbatim, the matched label or synonym and its scope, the ontology version,
and the matcher. Evidence type: **ECO:0000203 (automatic assertion)**. CI
obligation: re-run the matcher against the pinned ontology version and
require the same answer.

## 4. Curator/agent judgment (the fuzzy residue)

Where no automation is honest, the receipt records the candidate set
considered (with scores), the choice, proposer, confirmer, and date —
`semapv:ManualMappingCuration` in SSSOM, alternatives retained. Evidence
type: **ECO:0000305**.

## 5. Compositional and negative receipts

Most adverse outcomes have no precomposed term; the assignment is a
composition (process + PATO direction + anatomy), each piece carrying its
own class 1–4 receipt. Record the **negative receipt** too: "searched the
uPheno pattern space on date X, version Y; no equivalent above threshold."
CI re-runs the search; a future hit surfaces as a proposed
`outcome_mappings` candidate instead of silence.

## Summary of CI checks

1. **Source**: quoted AOP-Wiki text occurs in the pinned, hashed dump.
2. **Term**: id exists, not obsolete, stored label matches (OAK).
3. **Method**: deterministic methods (tables, matchers) reproduce.
4. **Composition**: EQ pieces are type-consistent (PATO quality, GO
   process, UBERON anatomy in the expected branches).

ECO ids verified 2026-11-09 via OAK: ECO:0000311 "imported information",
ECO:0000203 "automatic assertion", ECO:0000305 "curator inference used in
manual assertion".
