# Small-Model Operational Benchmark

How reliably can small models running locally use tools to investigate, change state, and know when to stop? This benchmark tests six approximately 3B–4B models on seven deterministic simulated operations tasks. An agent may need to choose the right tool, revise a diagnosis, preserve state, avoid an irreversible action, and verify the outcome.

**Canonical V2 result: no complete run achieved a full objective.** The corrected benchmark found limited verified partial behavior, concentrated in Q01 and Q03. V2 is now canonical; the original V1 scores remain preserved as historical evidence. Behavioral points and resource eligibility are separate.

| Model | Canonical V2 points | Observations | Resource eligibility |
|---|---:|---|---|
| Granite 4.1 3B | 6/80 | 6 | PASS |
| Qwen2.5 3B | 4/80 | 4 | PASS |
| Ministral 3 3B | 2/80 | 2, 2, 2 | PASS |
| Llama 3.2 3B Instruct | 2/80 | 2 | PASS |
| Qwen3 4B | 0/80 | 0, 0, 0 | FAIL |
| NVIDIA Nemotron 3 Nano 4B | unresolved | Q01 unresolved in 3 runs | FAIL |

Scores are bounded points on these tasks. Nemotron is not ranked: its Q01 observations remain unresolved after three authorized replacement attempts. PASS/FAIL applies to a separate local memory and swap rule. See the [canonical V2 results](runs/processed/canonical-v2-results-2026-09-20.json) and [full report](docs/REPORT.md).

Read the [MAJOR//minor write-up](https://majorminor.xyz/notebook/small-local-models-agent-tasks), which covers this benchmark and the 7B/8B sibling-scaling follow-up.

## Methodology correction

I audited the original scorer, froze an outcome-based V2 scorer, reconstructed defensible historical measurements, reran only preregistered invalid Nemotron Q01 observations, and preserved unresolved evidence rather than imputing scores. V2 removed credit for proxy/intermediate behavior, unchanged state, and unverified outcomes. The correction materially changed the results; [V1 remains available as historical evidence](V1.0_SCIENTIFIC_FREEZE.md), while [V2 is canonical](runs/processed/canonical-v2-results-2026-09-20.json).

## What the tasks test

The [seven fixtures](tasks/fixtures.json) cover tool selection, a precise configuration update, a migration with dependencies, diagnosis of a misleading error, replanning after the world changes, restraint when evidence is insufficient, and a longer recovery that must avoid lost or duplicate work. Q01–Q06 are worth 10 points each; Q07 is worth 20. A simulator tracks tool calls and state transitions. A deterministic scorer awards explicit points and applies caps for serious mistakes; there is no LLM judge.

## What V2 establishes

Across 112 audited decisions, 100 were retrospectively rescored and 12 remain unresolved Nemotron decisions. No complete canonical run achieved a full objective. Granite has the highest complete V2 total at 6/80, but this does not establish broad superiority. Q05 remains methodologically qualified because historical executions used the earlier simulator contract.

Nemotron's Q01 result is unresolved rather than zero. The three authorized replacements reproduced malformed-argument/transport failures without preserving pre-parser generations. Its validly reconstructed Q02–Q07 outcomes are zero, and its resolution set fails the resource rule. The [public Nemotron forensic audit](analysis/NEMOTRON_TOOL_CALL_FORENSIC_AUDIT.md) preserves the systems evidence.

Capability, resource eligibility, structured-tool compatibility, and failure modes answer different questions. Pre-exposure interface exclusions and an invalid shared-runner batch have no final scores. See the [scientific freeze](V1.0_SCIENTIFIC_FREEZE.md) for the field definition.

## How it was run

Inference used Q4_K_M GGUF weights on a ThinkPad T14 Gen 2a (Ryzen 7 PRO 5850U; 14.5 GiB usable RAM), frozen llama.cpp commit `972d2313bc0bf0a45f634f77d95c9fb03aeab12c`, and Vulkan/RADV. The protocol set a 16,384-token context ceiling, a 768-token generation ceiling, a structured-tool admission gate, and a frozen resource rule. Common-field requests used temperature 0 and seed 0; Nemotron's separately preregistered resolution used temperature 0.6, top_p 0.95, and thinking off. Model weights are external and are not redistributed.

## Inspect the evidence

- Read the [full report](docs/REPORT.md) and [scientific freeze](V1.0_SCIENTIFIC_FREEZE.md).
- Inspect the [protocol](protocol/), [task fixtures](tasks/fixtures.json), [model identities](models/), [simulator](simulator/), and [scorer](scoring/).
- Check [canonical processed results](runs/processed/canonical-v2-results-2026-09-20.json), [V1 processed results](runs/processed/), and [raw run evidence](runs/raw/). The [Nemotron forensic audit](analysis/NEMOTRON_TOOL_CALL_FORENSIC_AUDIT.md) documents the systems boundary.
- Read the [public methodology correction](docs/V2_METHODOLOGY_CORRECTION.md).
- Run `python -m unittest discover -s tests -v` to check the repository's deterministic tests. See [analysis](analysis/) for result derivations; no model run is required to inspect the frozen record.

See [NOTICE.md](NOTICE.md) for model terms and attribution. Cite this work as “Small-Model Operational Benchmark, canonical V2,” with public artifact commit `d4fc747` and the model manifest revisions.
