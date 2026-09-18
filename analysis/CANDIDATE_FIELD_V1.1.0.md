# Candidate field amendment v1.1.0

This amendment freezes the final pre-publication expansion of the standalone benchmark.

The original extracted benchmark had four valid scored candidates. Extraction and publication preparation occurred before this expansion. Exactly two additional candidates were authorized before either candidate saw Q01–Q07: NVIDIA Nemotron 3 Nano 4B and Meta Llama 3.2 3B Instruct. The intended maximum field is therefore six. No further v1.0 field expansion is planned.

## Frozen decision

Tasks Q01–Q07, prompts, simulator semantics, scoring atoms, catastrophic caps, structured-call requirements, normalization, resource eligibility, host, network policy, quantization policy, inference semantics, temperature, context policy, retry classification, and infrastructure-invalid classification remain unchanged.

The amendment is committed before candidate weights are downloaded or any scored task is exposed. Admission failures are compatibility results, not zero scores. Existing observations remain unchanged.

## Candidate identity and provenance

The exact pinned identities are recorded in `provenance/candidate-field-v1.1.0.json`.

- Nemotron: official NVIDIA `nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16`, revision `dfaf35de3e30f1867dd8dbc38a7fc9fb52d3914f`; official GGUF `nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF`, revision `ba223d14e45525f7fae81db77ea8cabeb2fc6c25`, file `NVIDIA-Nemotron3-Nano-4B-Q4_K_M.gguf`, 2,837,072,864 bytes. It is the canonical 3.97B Nemotron-Hybrid/Mamba2-Transformer model, not Nemotron Mini or the larger Nano MoE model.
- Llama: canonical Meta `meta-llama/Llama-3.2-3B-Instruct`, revision `0cb88a4f764b7a12671c53f0838cd831a0843b95`; trusted GGUF `bartowski/Llama-3.2-3B-Instruct-GGUF`, revision `5ab33fa94d1d04e903623ae72c95d1696f09f9e8`, file `Llama-3.2-3B-Instruct-Q4_K_M.gguf`, 2,019,377,696 bytes.

File SHA-256 values are intentionally null until the exact downloaded artifacts are hashed on the execution host. No weight has been downloaded in this pre-exposure commit.

## Frozen schedule and repetition rule

If both candidates pass admission, first-round execution is balanced and interleaved by task: N-Q01, L-Q01, through N-Q07, L-Q07. If only one passes, its seven tasks run in the fixed order Q01–Q07. No intermediate score changes the schedule.

A newly admitted candidate qualifies for two additional full repetitions when its first-round total is at least the expanded-field second-place score; ties qualify. Existing finalists are never rerun. If neither new candidate reaches or ties second place, no repetitions occur.

## Runtime gate

The pinned llama.cpp source contains `nemotron_h` support and Llama support. This source-level check is not an admission result. Each exact GGUF must still pass the neutral two-turn structured-tool gate on the ThinkPad with Vulkan/RADV, native template, simulator tool-role result, and offline operation, without a shim, patch, template rewrite, or cloud fallback.

At this workstation the ThinkPad weight paths and frozen llama.cpp binary are unavailable, so exposure is not authorized from this checkout. The next operator action is the required ThinkPad resource preflight followed by artifact hash and neutral admission probes.

