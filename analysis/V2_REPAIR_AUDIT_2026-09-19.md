# Corrected V2 repair audit

Date: 2026-09-19  
Repository: `<WORKDIR>/tests/mm-4b-benchmark`  
Historical repository state: `master` at `fed50452ffbdb4ca4d84bffd880b760925dc73c4`  
Frozen V2 measurement/scorer reference: `<WORKDIR>/tests/mm-8b-benchmark`, commit `ba5ae8fedbf7fe9907dd8ebe985451c04cbf5e1a`

This is a read-only audit and repair manifest. No model was launched, no historical raw evidence was edited, and no existing score was overwritten.

## Current evidence state

The V2 rescore artifact reports 112 score-bearing decisions: 100 fully retrospectively rescored and 12 unresolved transport-invalid Nemotron decisions. The existing canonical V2 matrix has complete non-Nemotron results and three incomplete Nemotron repetitions. Each incomplete canonical repetition has one unresolved Q01 and complete historical V2 scores for Q02–Q07.

Existing canonical V2 behavioral results are:

| Model | Repetitions | Per-task V2 scores | Per-run V2 total | Resource status |
|---|---:|---|---:|---|
| Ministral-3-3B-Instruct-2512 | 3 | Q01–Q07: 0,0,2,0,0,0,0 | 2, 2, 2 | historical PASS |
| Qwen3-4B | 3 | 0,0,0,0,0,0,0 | 0, 0, 0 | historical finalist FAIL |
| Qwen2.5-3B-Instruct | 1 | 0,0,0,0,0,0,0 | 4 | historical PASS |
| Granite-4.1-3B | 1 | 4,0,2,0,0,0,0 | 6 | historical PASS |
| Llama-3.2-3B-Instruct | 1 | 2,0,0,0,0,0,0 | 2 | historical PASS |
| Nemotron-3-Nano-4B | 3 | Q01 unresolved; Q02–Q07 all 0 | 20, 18, 18 in V1; V2 incomplete | historical resolution FAIL |

The V1 values above are provenance context only. V1 and V2 raw totals are not commensurate measurements.

## Decision classification

### Retrospective V2 rescore — no rerun

All complete preserved traces with valid simulator execution remain `V2_RETROSPECTIVE_RESCORE`. This includes the canonical Q02–Q07 Nemotron resolution traces, all non-Nemotron canonical traces, and historical Q05 traces. The frozen V2 scorer reads preserved events and final state; it does not infer credit from tool counts, unchanged state, or prose.

### Unresolved, noncanonical Nemotron traces — preserve, do not rerun

Nine unresolved decisions belong to the earlier `candidate-field-v1.1.0` field set:

| Historical paths | Cases | Classification | Disposition |
|---|---|---|---|
| `runs/raw/candidate-field-v1.1.0/thinkpad/first-round/nemotron-3-nano-4b/` | Q01, Q02, Q03 | `UNRESOLVED_INSUFFICIENT_EVIDENCE` / transport-invalid | Preserve unchanged; not part of canonical resolution repetitions |
| `runs/raw/candidate-field-v1.1.0/thinkpad/repetitions/nemotron/R2/` | Q01, Q02, Q03 | `UNRESOLVED_INSUFFICIENT_EVIDENCE` / transport-invalid | Preserve unchanged; superseded noncanonical repetition |
| `runs/raw/candidate-field-v1.1.0/thinkpad/repetitions/nemotron/R3/` | Q01, Q02, Q03 | `UNRESOLVED_INSUFFICIENT_EVIDENCE` / transport-invalid | Preserve unchanged; superseded noncanonical repetition |

Their missing pre-parser generations and transport failures prevent a V2 determination. They must not be converted to zero and do not justify opportunistic reruns because the canonical Nemotron resolution schedule already superseded these attempts.

### Canonical replacement measurements — minimum required set

Three canonical decisions require replacement:

| Historical case | Cause | Replacement identity | Reason |
|---|---|---|---|
| `nemotron-configuration-resolution-v1.0.0/thinkpad/R1/Q01` | repeated malformed tool arguments followed by server transport failure; pre-parser generation not preserved | `V2_REPLACEMENT_MEASUREMENT / N-REPAIR-R1-Q01` | canonical R1 Q01 remains indeterminate |
| `.../R2/Q01` | same | `V2_REPLACEMENT_MEASUREMENT / N-REPAIR-R2-Q01` | canonical R2 Q01 remains indeterminate |
| `.../R3/Q01` | same | `V2_REPLACEMENT_MEASUREMENT / N-REPAIR-R3-Q01` | canonical R3 Q01 remains indeterminate |

The replacement schedule is exactly three Q01 observations, not a new full Nemotron sweep. It uses the already resolved Nemotron configuration: `enable_thinking=false`, temperature `0.6`, `top_p=0.95`, seed `0`, max tokens `768`, reasoning fields `none`, native frozen interface/template, unchanged Q01 prompt/tools/fixture, Q4_K_M GGUF, frozen llama.cpp commit `972d2313bc0bf0a45f634f77d95c9fb03aeab12`, ThinkPad Vulkan/RADV, and the frozen resource rule. The V2 simulator/scorer reference is the pinned `ba5ae8fedbf7fe9907dd8ebe985451c04cbf5e1a` snapshot; no V1 simulator trace may be silently substituted.

The original Nemotron resolution restriction is superseded only for these three predeclared Q01 replacement measurements. No exploratory retries, configuration search, or favorable-result selection is authorized.

## Q05 audit

Historical Q05 traces use the earlier simulator, which did not enforce the future pause/load/affinity state predicates. V2 therefore cannot award the forward-only `queue_paused_for_move` atom from historical evidence. The canonical traces also show no actual compatible movement and no final destination placement. Under V2, the observable outcome is deterministically zero; no unresolved score remains and no replacement is needed to determine the canonical point result.

This is a scoring-only backward-compatible use of the old trace, not a claim that the old trace tested the corrected environment. A new Q05 execution would be required for a separate claim about corrected pause/load/affinity behavior, but it is outside the minimum repair because it cannot change the existing canonical zero.

## Resource and execution audit

Resource eligibility remains a separate axis. Historical status is retained exactly: Qwen3 finalist repetitions and Nemotron resolution failed the frozen resource requirements; the other historical rows were recorded as eligible under the original records. A behaviorally reconstructed score does not make a run resource-eligible.

No benchmark process is currently running on the audit host. The visible Ollama service is an unrelated desktop service and was not disturbed. The ThinkPad execution endpoint is the original protocol hardware; no alternate hardware is proposed for these three replacements. Before execution, the manifest requires a clean host/resource preflight and exact runtime/model hash verification. If that preflight or the frozen V2 runner is unavailable, execution must stop rather than silently changing hardware or methodology.

## Repair scope

- Historical artifacts modified: none.
- Historical scores overwritten: none.
- Retrospective V2 decisions reused: 100 complete decisions, plus the complete canonical Nemotron Q02–Q07 traces.
- New executions authorized by the frozen manifest: 3 Q01 replacement measurements.
- New executions not authorized: all other Nemotron tasks, all non-Nemotron tasks, all exploratory tests, and any additional Q05 runs.
- Final canonical table remains incomplete until the three Q01 replacements are completed and deterministically scored.

