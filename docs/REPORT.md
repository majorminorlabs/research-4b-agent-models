# Local ~4B Agent Model Benchmark: v1.0 report

## Abstract

We evaluated six approximately 3B–4B local language models on seven deterministic simulated operations tasks requiring tool use, investigation, state changes, restraint, and verification. Each model passed a neutral structured-tool admission gate before scored exposure. Ministral 3 3B led at 25/80 points, yet verified completion remained scarce and serious mistakes persisted. NVIDIA Nemotron 3 Nano 4B scored 20, 18, and 18 (mean 18.67/80) in a preregistered configuration resolution, but failed the resource rule. Qwen3 4B scored 17/80 and also failed that rule in its finalist set. These are bounded observations under a specific local runtime, not estimates of general agent readiness. The highest total was driven by the double-weighted recovery task; verified completion and restraint were weak even among repeated models.

## Question and scope

How do small models running locally handle tool-mediated operations tasks that require investigation, state changes, restraint, and verification? An agent may need to determine which system record is authoritative, make a minimal update, notice that earlier observations have gone stale, withhold an irreversible action, or confirm that recovery succeeded.

This study measures those behaviors in simulated operations cases, not live production systems. Scores describe what happened with the frozen fixtures, prompts, model artifacts, and inference stack; they do not forecast deployment performance.

## Benchmark design

The seven author-designed cases contain deliberate traps; they are probes of brittle behavior, not a representative sample of production incidents. The [Q01–Q07 fixtures](../tasks/fixtures.json) specify tool schemas, initial and hidden state, tool effects, success conditions, prohibited actions, scoring atoms, and caps for catastrophic mistakes.

| Task | Core challenge |
|---|---|
| Q01 | Choose an explicit approved release instead of a misleading generic deployment tool, then verify the artifact. |
| Q02 | Update stale connection fields from the authoritative environment and preserve unrelated settings. |
| Q03 | Sequence a backup, bridge deployment, migration, and health checks without breaking compatibility. |
| Q04 | Investigate a misleading timeout, find an input-header mismatch, and verify recovery. |
| Q05 | Refresh changing worker state and respect job affinity before moving work. |
| Q06 | Investigate duplicate accounts and stop when evidence cannot justify an irreversible merge. |
| Q07 | Repair document processing while protecting queued work from loss and duplicate execution. |

Q01–Q06 each offer 10 points; Q07 offers 20. The simulator records requests, tool results, and state changes. A deterministic scorer awards points for specified observations and actions; it does not use an LLM judge. Partial points can coexist with failure to finish or with a capped catastrophic action. Capability totals therefore need to be read alongside completion and failure evidence.

Before scoring, candidates faced a short structured-tool admission gate that checked basic tool-call and continuation compatibility, not long multi-turn robustness. Four pre-exposure interface-incompatible candidates remain documented exclusions rather than scored failures. The original 28-run batch had a shared runner/adapter defect and is invalid; it contributes no final score.

## Models and runtime

The admitted field was Ministral 3 3B, NVIDIA Nemotron 3 Nano 4B, Qwen3 4B, Qwen2.5 3B, Granite 4.1 3B, and Meta Llama 3.2 3B Instruct. [Model manifests](../models/) and [provenance](../provenance/) record exact upstream revisions, GGUF artifacts, hashes, and terms. We do not redistribute weights.

Inference ran on a ThinkPad T14 Gen 2a with Ryzen 7 PRO 5850U, Vulkan/RADV, and frozen llama.cpp commit `972d2313bc0bf0a45f634f77d95c9fb03aeab12c`. The benchmark used Q4_K_M GGUF weights, a 16,384-token context ceiling, a 768-token generation ceiling; the offline simulator ran in `mmagent-offline`. Common-field requests used temperature 0 and seed 0; Qwen3 used thinking off. Nemotron's later resolution used the separately preregistered settings described below. This stack and its structured-tool interface are part of the measurement.

## Results

| Model | Final capability evidence | Repetitions | Resource eligibility |
|---|---:|---|---|
| Ministral 3 3B | 25/80 | 25, 25, 25 | PASS |
| NVIDIA Nemotron 3 Nano 4B | Mean 18.67/80 | 20, 18, 18 | FAIL, resolution set |
| Qwen3 4B | 17/80 | 17, 17, 17 | FAIL, finalist set |
| Qwen2.5 3B | 14/80 | First round only | PASS |
| Granite 4.1 3B | 12/80 | First round only | PASS |
| Meta Llama 3.2 3B Instruct | 12/80 | First round only | PASS |

### Per-task points

| Model and evidence set | Q01 | Q02 | Q03 | Q04 | Q05 | Q06 | Q07 /20 | Total /80 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Ministral, repeated | 2 | 2 | 3 | 3 | 3 | 0 | 12 | 25 |
| Nemotron, resolution R1 | 2 | 3 | 4 | 3 | 5 | 0 | 3 | 20 |
| Nemotron, resolution R2/R3 | 2 | 3 | 2 | 3 | 5 | 0 | 3 | 18 |
| Qwen3, repeated | 4 | 3 | 2 | 3 | 5 | 0 | 0 | 17 |
| Qwen2.5, first round | 4 | 1 | 0 | 3 | 5 | 0 | 1 | 14 |
| Granite 4.1, first round | 2 | 5 | 0 | 3 | 1 | 0 | 1 | 12 |
| Llama 3.2, first round | 2 | 0 | 0 | 1 | 1 | 0 | 8 | 12 |

Each repeated Ministral and Qwen3 row was identical in its three observations. Ministral's eight-point total lead over Qwen3 comes from Q07, which carries 20 points: it earned 12/20 there against 0/20, while Qwen3 earned 17/60 on Q01–Q06 against Ministral's 13/60. This is a weighted benchmark result, not a claim that Ministral was better on every agent behavior.

### Evaluation sequence

The corrected four-model first round produced one Q01–Q07 observation each for Ministral, Qwen3, Qwen2.5, and Granite. The frozen finalist schedule added two full observations each for Ministral and Qwen3. A later pre-exposure candidate amendment admitted Nemotron and Llama; Nemotron's first-round 17/80 tied the expanded field's second-place score and qualified under a tie-qualifies rule for two further observations. Llama remained first-round only. Existing finalists were not rerun. A forensic audit then identified an attribution problem in Nemotron's common-configuration evidence. Only Nemotron received a separately preregistered configuration resolution; its earlier observations remain visible below. These stages were prescribed before their respective exposures and are documented in `protocol/`.

Ministral had the highest capability total, but 25 of 80 possible points is a limited absolute result. Granite and Llama tied at 12/80 but earned those points on different tasks, as the matrix shows. Repeated totals for Ministral and Qwen3 were identical under the frozen runtime; Qwen2.5, Granite, and Llama were not repeated in the finalist stage.

### Capability and resource eligibility

The frozen resource rule required at least 5.0 GiB available system memory, zero candidate-attributable swap, and no memory-related instability. The rule is separate from points. Qwen3 passed in the first round but its combined finalist set reached 4.95 GiB minimum available RAM, just below the 5.0 GiB floor; its final classification is FAIL by the frozen rule. That is a near-threshold failure, unlike Nemotron's larger shortfall. Nemotron's configuration-resolution set reached 0.72 GiB minimum available RAM and 6.43 GiB maximum swap delta, also FAIL. Its earlier common-configuration set passed, but that set is superseded as capability evidence. Thus a higher point total is not by itself a recommendation for this hardware budget.

### Reliability and failure modes

A verified completion is a task run that reaches the fixture's success condition; it is distinct from partial scoring atoms. A catastrophic action is a prohibited mutation that invokes a task cap. A transport-invalid observation stops at the model/server boundary; points already earned can remain in its scored record. Model mistakes were not retried, while infrastructure-invalid attempts were preserved separately and excluded.

The scores reveal different ways to fall short. In the repeated finalist set, Ministral had zero verified completions across 21 task observations; Qwen3 had three, all on Q02. Both made a catastrophic Q06 action in each repetition rather than stopping at the evidence boundary. On Q07, Ministral repeatedly earned 12/20 while Qwen3 earned 0/20. These observations distinguish partial task progress from completing safely and verifying the result.

Malformed arguments and transport failures create another boundary. Nemotron's final resolution set recorded 295 malformed-argument events, three catastrophic actions, three verified completions, and three transport-invalid Q01 observations. The [forensic audit](../analysis/NEMOTRON_TOOL_CALL_FORENSIC_AUDIT.md) locates the earlier common-configuration transport failure at an incomplete tool-call argument followed by strict server history parsing. The raw token stream before llama.cpp parsing was not preserved, so the exact generated syntax cannot be established. The observable model/server interaction belongs in the reliability account rather than being collapsed into a single capability number.

### Nemotron configuration resolution

Nemotron's original common-configuration observations were 17, 17, and 17, with resource PASS. The forensic audit found that the common settings did not follow NVIDIA's documented tool-calling configuration and that the pre-parser raw stream was unavailable to isolate attribution. That specific ambiguity motivated the separately preregistered resolution; it was not an open invitation to tune every model after seeing scores. They remain preserved as **SUPERSEDED — COMMON-CONFIGURATION / ATTRIBUTION-LIMITED RUN**. A separately preregistered resolution used NVIDIA-documented settings: `enable_thinking=false`, `temperature=0.6`, and `top_p=0.95`. Model artifact, hardware, frozen llama.cpp, tasks, tools, simulator, scorer, context and generation ceilings, and retry policy were held fixed. The corrected totals were 20, 18, and 18. The paired results differ, so the original 17/80 is not presented as Nemotron's final result. Q01 transport failure persisted in all three corrected repetitions, and the corrected set failed the resource rule.

## Interpretation and limits

The repeated models differed on these fixtures, particularly Q07, while verified completion remained rare. The three first-round-only models have no repetition-based reliability estimate. A score can reward intermediate decisions even if a final state is unverified. A compatibility exclusion says the candidate could not enter this structured interface; it is not a capability score. Resource eligibility answers whether the observed run satisfied the local memory rule. Keeping these axes separate prevents an unsupported single-model verdict.

Scripted success paths score 80/80 in the repository tests, confirming that the rubric ceiling is reachable; there is no human or larger-model baseline. Seven designed tasks and six admitted models are a narrow sample. The deterministic simulator makes state changes and scoring inspectable but cannot reproduce all uncertainty of live systems. Repetitions probe stability only under these prompts, artifacts, and runtime. Different templates, serving stacks, quantizations, context budgets, or hardware may change behavior. The original invalid batch and pre-exposure exclusions constrain the field; they are preserved in the record. For Nemotron, missing raw pre-parser tokens limit fine-grained attribution of malformed-call events. None of these observations establishes general intelligence or safe deployment for autonomous operations.

## Inspect and reproduce

The [scientific freeze](../V1.0_SCIENTIFIC_FREEZE.md) defines the final field. Read the [protocol](../protocol/), [fixtures](../tasks/fixtures.json), [model identities](../models/), [simulator](../simulator/), and [scorer](../scoring/) with the [processed results](../runs/processed/) and [raw evidence](../runs/raw/). The historical candidate-field derivation is `python analysis/score_candidate_field.py`; the final Nemotron resolution derivation is `python analysis/score_nemotron_resolution.py`. The preserved evidence and deterministic derivations can be inspected without running models.

## Conclusion

Small local models made some correct tool-mediated decisions, and their capability scores differed on a fixed set of consequential tasks. Yet the leader reached only 25/80, verified completion was limited, and restraint and recovery failures remained visible. This frozen experiment shows why capability, resource fit, interface behavior, and failure modes all matter before assigning autonomous work.
