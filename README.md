# ~4B Agent Model Benchmark

How reliably can small models running locally use tools to investigate, change state, and know when to stop? This benchmark tests six approximately 3B–4B models on seven deterministic simulated operations tasks. An agent may need to choose the right tool, revise a diagnosis, preserve state, avoid an irreversible action, and verify the outcome.

**The highest capability total was 25/80, and verified completion was rare.** Ministral 3 3B earned that total but had zero verified completions across 21 repeated task observations. Its lead over Qwen3 came from the double-weighted recovery task; Qwen3 scored more on the other six tasks. This is evidence of uneven agent behavior, not a general model ranking. Resource viability was measured separately: four models passed the frozen memory and swap rule, and two failed in their final evaluated sets.

| Model | Capability points | Observations | Resource eligibility |
|---|---:|---|---|
| Ministral 3 3B | 25/80 | 25, 25, 25 | PASS |
| NVIDIA Nemotron 3 Nano 4B | Mean 18.67/80 | 20, 18, 18 | FAIL, resolution set |
| Qwen3 4B | 17/80 | 17, 17, 17 | FAIL, finalist set |
| Qwen2.5 3B | 14/80 | First round only | PASS |
| Granite 4.1 3B | 12/80 | First round only | PASS |
| Meta Llama 3.2 3B Instruct | 12/80 | First round only | PASS |

Scores are bounded points on these tasks. PASS/FAIL applies to a separate local memory and swap rule; Nemotron and Qwen3 retain their observed scores but did not meet it. See the report for the per-task breakdown.

## What the tasks test

The [seven fixtures](tasks/fixtures.json) cover tool selection, a precise configuration update, a migration with dependencies, diagnosis of a misleading error, replanning after the world changes, restraint when evidence is insufficient, and a longer recovery that must avoid lost or duplicate work. Q01–Q06 are worth 10 points each; Q07 is worth 20. A simulator tracks tool calls and state transitions. A deterministic scorer awards explicit points and applies caps for serious mistakes; there is no LLM judge.

## What happened

Models sometimes made useful partial progress, but verified completion was scarce. In repeated observations, Ministral had 0/21 verified completions and Qwen3 had 3/21. Each of those models, and Nemotron in its resolution set, made a catastrophic Q06 action in all three repetitions. Ministral scored 12/20 on Q07 while Qwen3 scored 0/20; on Q01–Q06, Qwen3 scored 17/60 and Ministral 13/60. Identical totals under the frozen common configuration establish neither stochastic reliability nor transfer to new tasks.

Nemotron's final result comes from a separately preregistered configuration resolution using NVIDIA-documented tool-calling settings. Its earlier common-configuration observations (17, 17, 17; resource PASS) are preserved as **superseded and attribution-limited**, not combined with the final observations. The pre-parser raw token stream was unavailable for precise failure attribution. The resolution scored 20, 18, and 18; Q01 transport failure persisted and the resolution set failed the resource rule. The [report](docs/REPORT.md) explains the model/server failure boundary.

Capability, resource eligibility, structured-tool compatibility, and failure modes answer different questions. Pre-exposure interface exclusions and an invalid shared-runner batch have no final scores. See the [scientific freeze](V1.0_SCIENTIFIC_FREEZE.md) for the field definition.

## How it was run

Inference used Q4_K_M GGUF weights on a ThinkPad T14 Gen 2a (Ryzen 7 PRO 5850U; 14.5 GiB usable RAM), frozen llama.cpp commit `972d2313bc0bf0a45f634f77d95c9fb03aeab12c`, and Vulkan/RADV. The protocol set a 16,384-token context ceiling, a 768-token generation ceiling, a structured-tool admission gate, and a frozen resource rule. Common-field requests used temperature 0 and seed 0; Nemotron's separately preregistered resolution used temperature 0.6, top_p 0.95, and thinking off. Model weights are external and are not redistributed.

## Inspect the evidence

- Read the [full report](docs/REPORT.md) and [scientific freeze](V1.0_SCIENTIFIC_FREEZE.md).
- Inspect the [protocol](protocol/), [task fixtures](tasks/fixtures.json), [model identities](models/), [simulator](simulator/), and [scorer](scoring/).
- Check [processed results](runs/processed/) against [raw run evidence](runs/raw/). The [Nemotron resolution result](runs/processed/nemotron-configuration-resolution-v1.0.0-results.json) and [forensic audit](analysis/NEMOTRON_TOOL_CALL_FORENSIC_AUDIT.md) document that case.
- Run `python -m unittest discover -s tests -v` to check the repository's deterministic tests. See [analysis](analysis/) for result derivations; no model run is required to inspect the frozen record.

See [NOTICE.md](NOTICE.md) for model terms and attribution. Cite this work as “~4B Agent Model Benchmark, v1.0 scientific freeze,” with the release commit and model manifest revisions.
