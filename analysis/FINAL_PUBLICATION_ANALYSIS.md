# Final publication analysis

## Field status

The intended v1.0 field is complete at six authorized candidates. The admitted/scored field is also six candidates. No further model additions are planned for v1.0.

| Candidate | First round | Repetitions | Admission | Resource eligibility |
|---|---:|---|---|---|
| Ministral 3 3B | 25/80 | 25, 25, 25 | PASS, retained prior gate | PASS |
| Qwen3 4B | 17/80 | 17, 17, 17 | PASS, retained prior gate | Finalist repetition rule: FAIL resource floor |
| Qwen2.5 3B | 14/80 | — | PASS, retained prior gate | PASS |
| Granite 4.1 3B | 12/80 | — | PASS | PASS |
| NVIDIA Nemotron 3 Nano 4B | 17/80 | 17, 17 | PASS | PASS |
| Meta Llama 3.2 3B Instruct | 12/80 | — | PASS | PASS |

New-candidate per-task scores were Nemotron `2, 3, 2, 3, 5, 2, 0` and Llama `2, 0, 0, 1, 1, 0, 8`. Nemotron tied second place and qualified for two repetitions. Its three totals were 17, 17, and 17; mean 17, median 17, range 17–17. Per-task stability was identical.

## Compatibility and admission

Both new candidates passed the neutral structured-tool gate using native GGUF templates, structured tool calls, canonical arguments, a simulator tool-role result, and a successful second turn. No shim, source patch, template rewrite, or cloud fallback was used. Historical pre-exposure exclusions remain separate and are not zero scores.

## Methodology summary

The unchanged qualification-v1.0.0 protocol uses Q01–Q07, deterministic simulator state transitions, explicit scoring atoms, catastrophic caps, temperature 0, fixed seed 0, Q4_K_M weights, a 16,384-token context ceiling, Vulkan/RADV, and no external network during inference. The Mac Studio orchestrated SSH execution; all inference ran on the ThinkPad T14 Gen 2a in `mmagent-offline`.

## Resources

| Candidate | Minimum available RAM GiB | Peak RSS GiB | Swap delta GiB | Prompt tok/s | Generation tok/s | First-round wall time s | Eligibility |
|---|---:|---:|---:|---:|---:|---:|---|
| Nemotron 3 Nano 4B | 5.85 | 2.02 | 0.000 | 62.25 | 6.98 | 860.4 | PASS |
| Llama 3.2 3B Instruct | 7.00 | 0.17 | 0.000 | 71.21 | 9.77 | 382.5 | PASS |

The frozen 5 GiB minimum-available-RAM rule was not relaxed. Existing candidates retain their previously recorded resource measurements.

## Failure-mode analysis

Nemotron repeatedly generated malformed or incomplete tool-call JSON in scored exposure. The frozen llama.cpp server rejected those outputs with transport errors; they are preserved as model behavioral evidence and were not retried. Nemotron also produced catastrophic actions in Q06/Q07, while Llama’s strongest result was Q07 at 8/20 but it had catastrophic behavior in Q01/Q06. The small absolute totals reinforce that these are bounded task scores, not general intelligence estimates.

One controller-side simulator exception occurred when an initial Nemotron Q01 malformed call reached an uncaught `KeyError`. That attempt is preserved as infrastructure-invalid, excluded from the 14 valid first-round observations, and the scheduled observation was rerun with exception recording fixed. No model-generated behavioral outcome was repaired.

## Limitations and publication position

The fixture set is narrow, the structured-tool gate measures interface compatibility as well as model behavior, and repeated observations establish stability only under this exact runtime and prompt set. Resource eligibility and capability remain separate. Model weights remain external; hashes and upstream revisions are recorded in provenance. Publication drafts are updated but nothing has been published and no live website or GitHub repository was modified.
