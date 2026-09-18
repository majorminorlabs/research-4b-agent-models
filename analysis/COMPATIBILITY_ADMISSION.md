# Compatibility and admission history

Candidates below failed the frozen neutral structured-interface gate before valid scored exposure. They are not zero capability scores and do not appear in the scored leaderboard.

| Candidate | Status | Historical reason |
|---|---|---|
| Phi-4 Mini | `removed_pre_exposure_interface_incompatible` | Structured interface failure |
| Gemma 3 4B | `removed_pre_exposure_interface_incompatible` | Structured interface failure |
| Granite 3.3 2B | `removed_pre_exposure_interface_incompatible` | JSON call emitted as ordinary assistant content; structured tool transport unavailable |
| SmolLM3 3B | `removed_pre_exposure_interface_incompatible` | Exact GGUF/runtime gate reported no structured tool calls |

The replacement field admitted Ministral 3 3B, Qwen3 4B, Qwen2.5 3B, and Granite 4.1 3B. The original 28-run batch is preserved separately as `INVALID — SHARED RUNNER/ADAPTER FAILURE` and contributes no capability result.

## Candidate-field v1.1.0 admission

Both authorized candidates passed the frozen neutral structured-tool gate on the ThinkPad using native templates and the pinned llama.cpp runtime. Exact hashes, sizes, paths, and gate evidence are recorded in `provenance/candidate-field-v1.1.0-admission.json`.

| Candidate | Admission | Reason |
|---|---|---|
| NVIDIA Nemotron 3 Nano 4B | `PASS` | Structured tool call, canonical arguments, tool-role result, and second turn succeeded |
| Meta Llama 3.2 3B Instruct | `PASS` | Structured tool call, canonical arguments, tool-role result, and second turn succeeded |

During scored Nemotron runs, malformed generated tool-call JSON caused frozen llama.cpp to return transport errors. These are preserved behavioral outcomes, not pre-exposure exclusions and not retried infrastructure attempts.
