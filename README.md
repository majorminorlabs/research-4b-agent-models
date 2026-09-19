# ~4B Agent Model Benchmark

## Research question

How reliably can approximately 3B–4B local language models reason, use tools, preserve state, exercise restraint, recover from misleading evidence, and verify outcomes in deterministic simulated operations tasks on consumer hardware?

This is a bounded behavioral benchmark, not a general intelligence test. The final v1.0 scientific record is frozen in V1.0_SCIENTIFIC_FREEZE.md; the release tree is ready to publish after the documented privacy pass, subject to explicit human authorization.

## Final results

| Model | Capability evidence | Repetitions | Resource eligibility |
|---|---:|---:|---|
| Ministral 3 3B | 25/80 | 25, 25, 25 | PASS |
| NVIDIA Nemotron 3 Nano 4B | 20, 18, 18; mean 18.67 | 3 | FAIL in resolution set |
| Qwen3 4B | 17/80 | 17, 17, 17 | FAIL in finalist set |
| Qwen2.5 3B | 14/80 | — | PASS |
| Granite 4.1 3B | 12/80 | — | PASS |
| Meta Llama 3.2 3B Instruct | 12/80 | — | PASS |

Nemotron’s earlier 17, 17, 17 common-configuration observations remain preserved but are labeled superseded and attribution-limited. The corrected resolution used NVIDIA-documented tool-calling settings and materially changed the result.

## Design

Seven deterministic tasks, Q01–Q07, exercise tool discrimination, precise updates, dependency planning, hypothesis revision, dynamic state tracking, restraint, and long-horizon recovery. Each task has explicit simulator semantics, scoring atoms, and catastrophic caps. A neutral structured-tool admission gate precedes scored exposure.

Inference used Q4_K_M GGUF weights, frozen llama.cpp 972d2313bc0bf0a45f634f77d95c9fb03aeab12c, Vulkan/RADV, a 16,384-token context ceiling, and a 768-token generation ceiling on a ThinkPad T14 Gen 2a with Ryzen 7 PRO 5850U. Model weights remain external.

## Major findings and limitations

- The highest result, 25/80, is weak relative to the 80-point ceiling and is not strong autonomous-agent capability.
- Malformed calls, catastrophic actions, low verified completion, and transport failures are prominent failure modes.
- Nemotron’s corrected run had 295 malformed-argument events, 3 catastrophic actions, 3 verified completions, and repeated Q01 transport failures.
- Resource eligibility is separate from capability score; Nemotron and Qwen3 failed the frozen memory/swap rule in their relevant finalist/resolution sets.
- The field is narrow, repetitions measure stability only under this exact runtime, and the raw pre-parser token stream was not available from frozen llama.cpp.
- The original invalid shared-runner batch and pre-exposure compatibility exclusions remain preserved and do not contribute scores.

## Reproduce and inspect

Start with V1.0_SCIENTIFIC_FREEZE.md, docs/REPORT.md, protocol/, tasks/, models/, simulator/, scoring/, and runs/processed/. The Nemotron forensic audit is analysis/NEMOTRON_TOOL_CALL_FORENSIC_AUDIT.md. The resolution derivation is python analysis/score_nemotron_resolution.py.

## License and citation

Model terms and source links are summarized in NOTICE.md. No weights are redistributed. Cite this repository as “~4B Agent Model Benchmark, v1.0 scientific freeze,” with the release commit and model manifest revisions.
