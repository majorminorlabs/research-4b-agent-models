# Small-Model Operational Benchmark: canonical V2 report

> **Methodology correction:** MAJOR//minor identified material defects in the original scoring methodology. It audited the historical evidence, froze a corrected outcome-based V2 scorer, reconstructed all defensible measurements, reran only preregistered invalid Nemotron Q01 observations, and preserved unresolved observations rather than imputing results. V2 is now canonical; V1 remains preserved as historical evidence.

## Research question and scope

How do approximately 3B–4B local language models handle tool-mediated operational tasks requiring investigation, precise state changes, restraint, recovery, and verification? This is a bounded study of seven deterministic simulated tasks, not a general intelligence or deployment-readiness test.

The six evaluated models were Ministral 3 3B, Qwen3 4B, Qwen2.5 3B, Granite 4.1 3B, Llama 3.2 3B Instruct, and NVIDIA Nemotron 3 Nano 4B. Q01–Q06 are worth 10 points each and Q07 is worth 20.

## Runtime and original methodology

Inference used Q4_K_M GGUF weights on a ThinkPad T14 Gen 2a with Ryzen 7 PRO 5850U, Vulkan/RADV, frozen llama.cpp commit `972d2313bc0bf0a45f634f77d95c9fb03aeab12c`, a 16,384-token context ceiling, and a 768-token generation ceiling. The simulator records requests, tool results, and state transitions. The original V1 scorer awarded explicit atoms, but its audit found material over-crediting of proxy metrics, tool/read counts, unchanged state, contradictory intermediate labels, and incorrect predicates.

V1 artifacts, raw evidence, invalid batches, exclusions, and scores remain preserved. They are historical evidence, not the current canonical result.

## V2 audit and repair

The frozen V2 scorer uses verified outcome predicates and explicit safety conditions. Across 112 audited decisions, 100 were retrospectively rescored from sufficient preserved evidence and 12 historical Nemotron decisions remain unresolved. Exactly three authorized replacement executions were performed for canonical Nemotron Q01. All three reproduced malformed-argument/transport failures without preserving pre-parser generations. No unresolved observation was converted to zero, and no historical raw evidence or V1 score was overwritten.

Q05 requires special qualification: historical executions used the earlier simulator contract. V2 therefore scores only observable historical movement and does not impute corrected pause/load/affinity predicates. A corrected-simulator Q05 replication is future work, not part of this study.

## Canonical V2 results

| Model | Canonical V2 score | Runs | Per-question Q01–Q07 | Resource eligibility |
|---|---:|---|---|---|
| Granite 4.1 3B | 6/80 | 6 | 4, 0, 2, 0, 0, 0, 0 | PASS |
| Qwen2.5 3B | 4/80 | 4 | 4, 0, 0, 0, 0, 0, 0 | PASS |
| Ministral 3 3B | 2/80 | 2, 2, 2 | 0, 0, 2, 0, 0, 0, 0 | PASS |
| Llama 3.2 3B Instruct | 2/80 | 2 | 2, 0, 0, 0, 0, 0, 0 | PASS |
| Qwen3 4B | 0/80 | 0, 0, 0 | 0, 0, 0, 0, 0, 0, 0 | FAIL |
| Nemotron 3 Nano 4B | unresolved | Q01 unresolved ×3 | unresolved, 0, 0, 0, 0, 0, 0 | FAIL |

Percentages for the complete models are Granite 7.5%, Qwen2.5 5%, Ministral 2.5%, Llama 2.5%, and Qwen3 0%. No complete canonical run achieved a full objective. Across the nine complete runs, observed points were Q01 10, Q02 0, Q03 8, Q04 0, Q05 0, Q06 0, and Q07 0.

Nemotron is not assigned a percentage or ordinal position. Each run has 70 known scorable points, all zero, while Q01's 10 points remain unresolved. Its conditional total range is 0–10, not a canonical score.

Complete scores carry `V2_RETROSPECTIVE_RESCORE` provenance. Nemotron Q01 carries `V2_REPLACEMENT_MEASUREMENT` provenance with outcome `UNRESOLVED_INSUFFICIENT_EVIDENCE`; Nemotron Q02–Q07 carry retrospective provenance.

## Per-question interpretation

- **Q01:** limited verified partial success. Granite and Qwen2.5 scored 4; Llama scored 2; Ministral and Qwen3 scored 0. Nemotron remains unresolved because the transport boundary prevented reconstruction.
- **Q02:** all canonical models scored 0. V2 requires an actual nonempty update and changed authoritative state; reads and preservation claims do not count.
- **Q03:** Granite and Ministral each earned 2 points from verified partial evidence. Other complete models scored 0.
- **Q04:** all complete canonical runs scored 0 because investigation and rerun attempts did not establish verified processing.
- **Q05:** all scored 0. This is a conservative historical result, not a fresh measurement under the corrected simulator. No corrected pause/load/affinity behavior is imputed.
- **Q06:** all scored 0. The V2 evidence does not show a complete safe-stop objective.
- **Q07:** all scored 0. The former V1 credit for diagnosis, narration, or intermediate recovery was not evidence of executed repair, safe retries, and verified final health.

Partial V2 behavior is therefore concentrated in Q01 and Q03. Q02, Q04, Q05, Q06, and Q07 provide no observed points in the complete canonical runs.

## V1 → V2 comparison

| Model | V1 score(s) | V2 score(s) | Change |
|---|---:|---:|---:|
| Ministral 3B | 25, 25, 25 | 2, 2, 2 | −23 each |
| Qwen3 4B | 17, 17, 17 | 0, 0, 0 | −17 each |
| Qwen2.5 3B | 14 | 4 | −10 |
| Granite 4.1 3B | 12 | 6 | −6 |
| Llama 3.2 3B | 12 | 2 | −10 |
| Nemotron 3 Nano 4B | 20, 18, 18 | unresolved | not computable |

The largest changes came from scorer correction: unverified processing, unchanged state, read counts, and diagnostic narration no longer earn outcome credit. Q07 proxy/intermediate scoring was a major source of V1 distortion. Q05 additionally has a simulator-contract qualification. Nemotron Q01 differs because of replacement measurement and unresolved evidence, not because a zero was assigned.

## Ordering and resource eligibility

The V1 ordering was Ministral, Nemotron, Qwen3, Qwen2.5, then Granite/Llama tied. Among complete V2 measurements, the ordering is Granite, Qwen2.5, Ministral/Llama tied, then Qwen3. Nemotron is unranked.

Granite has the highest complete V2 score, but 6/80 with zero full objectives does not support a broad “best” or “winning” claim. The changed ordering primarily reflects removal of V1 scoring artifacts, not evidence that V2 establishes a stable general model hierarchy. Qwen3 and Nemotron fail the separate resource eligibility requirement; behavioral points do not override that status.

## Nemotron systems boundary

Nemotron's validly reconstructed Q02–Q07 outcomes are zero under V2, subject to the Q05 qualification. Those are not automatically infrastructure failures. The canonical Q01 observations are different: malformed arguments and HTTP 500 transport failures occurred without preserved pre-parser generations, so model behavior cannot be separated from parser/interface/transport termination. Three corrected replacement attempts reproduced this gap. Nemotron's resolution set also failed the resource rule with approximately 0.72 GiB minimum available RAM and 6.43 GiB swap delta.

What can be concluded is that Nemotron showed serious tool/interface reliability problems in this local setup, failed resource eligibility, and had no verified Q01 result. What cannot be concluded is its complete V2 total, Q01 behavioral score, or fair ordinal rank.

The detailed systems evidence is preserved in the [public Nemotron forensic audit](../analysis/NEMOTRON_TOOL_CALL_FORENSIC_AUDIT.md), including transport failures, malformed arguments, parser boundary, missing pre-parser generations, resource limitations, simulator mismatch, admission-test limitations, and unresolved attribution.

## Original conclusions: final assessment

The original claim that Ministral led at 25/80 is **NO LONGER SUPPORTED**. The original Nemotron 20/18/18 and Qwen3 17/80 capability claims are **NO LONGER SUPPORTED** as canonical V2 results. The Qwen3 and Nemotron resource-failure conclusions are **STILL SUPPORTED**. The claim that small models showed some useful partial progress is **MODIFIED** to mean limited verified partial behavior, not broad operational competence. The claim that verified completion was scarce is **STILL SUPPORTED**, and is strengthened by zero full objectives in complete V2 runs. Claims about model-size effects, generalization, or a complete Nemotron ranking **CANNOT BE DETERMINED**. The caution about practical local deployment **STILL HOLDS** because behavior, resources, and interface reliability remain weak and separate concerns.

## Supported findings, limitations, and future work

Supported findings are low absolute V2 performance, no complete objectives, partial credit concentrated in Q01/Q03, separate resource failures for Qwen3/Nemotron, and unresolved Nemotron Q01 transport evidence. Suggestive findings include task-specific model differences and repeated stability under this exact runtime. The experiment cannot establish model-size effects, transfer to unseen work, or a complete Nemotron rank.

Future work is limited to two separate experiments: a corrected-simulator Q05 replication, and Nemotron interface forensics with raw pre-parser generation capture. Neither is required to complete this study and neither is a blocker.

## Reproducibility and canonical artifacts

The canonical machine-readable result is [`runs/processed/canonical-v2-results-2026-09-20.json`](../runs/processed/canonical-v2-results-2026-09-20.json). The public methodology correction is [`docs/V2_METHODOLOGY_CORRECTION.md`](V2_METHODOLOGY_CORRECTION.md). V1 remains frozen in [`V1.0_SCIENTIFIC_FREEZE.md`](../V1.0_SCIENTIFIC_FREEZE.md). No model run is required to inspect the canonical record.
