# Canonical V2 results for the original 3B/4B study

Date: 2026-09-20  
Frozen V2 reference: `<WORKDIR>/tests/mm-8b-benchmark`, commit `ba5ae8fedbf7fe9907dd8ebe985451c04cbf5e1a`  
Machine-readable result: `runs/processed/canonical-v2-results-2026-09-20.json`

This is the canonical corrected result set. It preserves unresolved observations instead of assigning them a convenient score. Historical V1 evidence remains unchanged.

## Canonical behavioral results

| Model | V2 per-run totals | Q01 | Q02 | Q03 | Q04 | Q05 | Q06 | Q07 /20 | Resource status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Ministral 3 3B | 2, 2, 2 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | PASS |
| Qwen3 4B | 0, 0, 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | FAIL |
| Qwen2.5 3B | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | PASS |
| Granite 4.1 3B | 6 | 4 | 0 | 2 | 0 | 0 | 0 | 0 | PASS |
| Llama 3.2 3B | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | PASS |
| Nemotron 3 Nano 4B | unresolved; each run is 0–10 conditional on Q01 | unresolved | 0 | 0 | 0 | 0 | 0 | 0 | FAIL |

For Nemotron, Q01 is unresolved in all three canonical repetitions. The corrected replacements reproduced one-turn malformed-argument/HTTP 500 transport behavior without preserving the pre-parser generation. The canonical result is therefore incomplete for that model; neither zero nor success is imputed.

## Per-question and full-objective accounting

Across the nine complete canonical runs, observed V2 points are Q01 10, Q02 0, Q03 8, Q04 0, Q05 0, Q06 0, and Q07 0. No complete run achieved a full objective on any question. Nemotron's unresolved Q01 observations are excluded from observed-point and full-objective counts.

All complete scores carry `V2_RETROSPECTIVE_RESCORE` provenance. Nemotron Q01 carries `V2_REPLACEMENT_MEASUREMENT` provenance with outcome `UNRESOLVED_INSUFFICIENT_EVIDENCE`; Nemotron Q02–Q07 carry retrospective provenance.

## V1 → V2 comparison

The frozen audit contains 112 audited decisions: 100 fully rescored and 12 unresolved. Representative canonical totals are:

| Model | Historical V1 totals | Canonical V2 totals | Interpretation |
|---|---:|---:|---|
| Ministral 3 3B | 25, 25, 25 | 2, 2, 2 | proxy/intermediate credit removed; no full objective |
| Qwen3 4B | 17, 17, 17 | 0, 0, 0 | proxy and non-outcome credit removed |
| Qwen2.5 3B | 14 | 4 | outcome-only correction |
| Granite 4.1 3B | 12 | 6 | outcome-only correction plus verified partial credit |
| Llama 3.2 3B | 12 | 2 | unsafe/unfinished actions no longer count as completion |
| Nemotron 3 Nano 4B | 20, 18, 18 | incomplete | Q01 transport/evidence gap remains unresolved; Q02–Q07 are zero |

These are separate instruments, not a common numeric scale. The detailed decision-level deltas and explanations remain in the frozen V2 comparison artifact.

## Replaced and unresolved historical results

The only canonical historical results replaced for measurement purposes were Nemotron resolution R1/Q01, R2/Q01, and R3/Q01. Each was transport-invalid and lacked pre-parser evidence. Each received one declared replacement execution; all three replacements remained unresolved. The nine earlier noncanonical Nemotron transport-invalid observations remain preserved and were not converted to zero or silently substituted.

No Q05 rerun was authorized. Historical Q05 traces are scored conservatively from observed state and movement only; corrected simulator-only predicates are not imputed. Old-simulator and corrected-simulator evidence are not combined.

## Headline assessment

The original broad claim that small local models showed useful partial progress can survive only in a narrower form: the corrected V2 evidence shows small amounts of verified partial credit, not reliable autonomous completion. Any headline based on the former 25-point Ministral lead, proxy success, unchanged state, tool/read counts, or old Q05 semantics does not hold under V2. The separate resource conclusion does hold: Qwen3's finalist set and Nemotron's resolution set fail the frozen local resource rule. Nemotron must not be ranked as a complete V2 point estimate.

The failure/methodology archive records the parser, transport, admission-test, simulator-contract, and resource incidents without treating them as model scores.
