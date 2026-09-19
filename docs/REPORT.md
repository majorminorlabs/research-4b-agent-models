# Local ~4B agent model benchmark: v1.0 report

## Abstract

This study evaluates whether approximately 3B–4B local language models can reason, use tools, preserve state, exercise restraint, recover from misleading evidence, and verify outcomes in seven deterministic simulated operations tasks. Six candidates were admitted under a frozen llama.cpp/Vulkan protocol. Scores are bounded task points, not general intelligence estimates. The reference model scored 25/80; the final Nemotron configuration-resolution observations scored 20, 18, and 18 but failed the resource rule and retained repeated transport failures on Q01.

## Research question and motivation

The benchmark asks how much reliable agent behavior is available in small local models on consumer hardware. The tasks emphasize observable action sequences rather than conversational quality: safe investigation, precise updates, dependency-aware sequencing, hypothesis revision, dynamic state tracking, epistemic restraint, and long-horizon recovery.

## Models and runtime

The final field contains Ministral 3 3B, Qwen3 4B, Qwen2.5 3B, Granite 4.1 3B, NVIDIA Nemotron 3 Nano 4B, and Meta Llama 3.2 3B Instruct. Exact upstream revisions, GGUF filenames, quantization, hashes, and licenses are recorded in models/ and provenance/; model weights are not in this repository.

All inference ran on a Lenovo ThinkPad T14 Gen 2a with AMD Ryzen 7 PRO 5850U, using Vulkan/RADV and frozen llama.cpp commit 972d2313bc0bf0a45f634f77d95c9fb03aeab12c. The benchmark context ceiling was 16,384 tokens, the generated-token ceiling was 768, and the simulator ran offline in mmagent-offline.

## Benchmark design and scoring

Q01–Q07 are deterministic fixtures with explicit tool schemas, state transitions, traps, success conditions, prohibited actions, scoring atoms, and catastrophic caps. The simulator records every tool call and result. The scorer is deterministic and does not use an LLM judge. Each task contributes up to 10 points except Q07, which contributes up to 20.

Every candidate first passed or failed a neutral structured-tool admission gate. The original invalid batch remains excluded. No model weights or live services are redistributed here.

## Results

| Model | Capability evidence | Repetitions | Resource eligibility |
|---|---:|---:|---|
| Ministral 3B | 25/80 | 25, 25, 25 | PASS |
| Qwen3 4B | 17/80 | 17, 17, 17 | FAIL in finalist set |
| Qwen2.5 3B | 14/80 | — | PASS |
| Granite 4.1 3B | 12/80 | — | PASS |
| NVIDIA Nemotron 3 Nano 4B | 20, 18, 18; mean 18.67 | 3 observations | FAIL in resolution set |
| Meta Llama 3.2 3B Instruct | 12/80 | — | PASS |

Nemotron resolution per-task scores were R1 2,3,4,3,5,0,3, R2 2,3,2,3,5,0,3, and R3 2,3,2,3,5,0,3. The original common-configuration 17,17,17 observations remain superseded and attribution-limited.

## Resource results

The corrected Nemotron run reached 0.72 GiB minimum available RAM and 6.43 GiB maximum swap delta, failing the frozen 5.0 GiB resource rule. This is reported separately from capability points. The original Nemotron observations passed resource eligibility, but are not the final configuration-resolved evidence.

## Behavioral failure analysis

The strongest recurring negative findings are low verified completion, malformed argument events, catastrophic actions on restraint-sensitive tasks, and transport-invalid calls. The corrected Nemotron run had 295 malformed-argument events, 3 catastrophic actions, 3 verified completions, and 3 transport-invalid Q01 observations. The raw token stream before llama.cpp parsing was not preserved; structured responses and generation traces are preserved. This prevents stronger causal claims than the evidence supports.

## Nemotron configuration-resolution note

NVIDIA documents enable_thinking=False for reasoning-off and recommends temperature=0.6, top_p=0.95 for tool calling. The preregistered resolution used those settings while holding the benchmark contract fixed. The change materially altered Nemotron scores and reduced the repeated transport pattern to Q01, so the original 17/80 is not a clean capability estimate. The corrected run is the final Nemotron evidence, with resource ineligibility disclosed.

## Discussion and limitations

The highest result, 25/80, is weak relative to the 80-point ceiling and should not be described as strong autonomous-agent capability. Repetition stability is stability under these prompts and runtime, not broad stochastic uncertainty. Resource pressure materially affects eligibility. The tool interface and llama.cpp version are part of the measurement. The six-model field is narrow, and compatibility exclusions are scientifically meaningful rather than missing scores.

## Reproducibility

Start with V1.0_SCIENTIFIC_FREEZE.md, protocol/, tasks/fixtures.json, models/, simulator/, scoring/, and the processed result files. Run python analysis/score_candidate_field.py for the historical candidate-field result and python analysis/score_nemotron_resolution.py for the resolution result. The raw evidence paths are preserved under runs/raw/.

## Conclusion

Small local models can produce isolated correct tool-use sequences, but the benchmark exposes substantial failures in verification, restraint, malformed-call control, and long-horizon reliability. Nemotron’s configuration resolution materially changed its observed behavior; its corrected evidence is stronger than the original 17/80 but resource-ineligible and still failure-prone. The release tree is ready to publish after the completed privacy/redaction review; external publication still requires explicit human authorization.
