# Final publication analysis (superseded V1 record)

> This file preserves the original V1 publication analysis. It is historical evidence, not the current benchmark result. The canonical result is V2; consult the repository README, `docs/REPORT.md`, the methodology correction, and the canonical JSON.

The v1.0 field is scientifically frozen at six intended/admitted candidates. No further model or configuration experiments are authorized.

| Candidate | Final capability evidence | Repetitions | Resource eligibility | Interpretation |
|---|---:|---:|---|---|
| Ministral 3 3B | 25/80 | 25, 25, 25 | PASS | selected reference under frozen field |
| NVIDIA Nemotron 3 Nano 4B | 20, 18, 18; mean 18.67 | 3 resolution observations | FAIL | final configuration-resolved evidence; resource-ineligible |
| Qwen3 4B | 17/80 | 17, 17, 17 | FAIL | final evidence; resource-ineligible |
| Qwen2.5 3B | 14/80 | — | PASS | first-round evidence |
| Granite 4.1 3B | 12/80 | — | PASS | first-round evidence |
| Meta Llama 3.2 3B Instruct | 12/80 | — | PASS | first-round evidence |

## Nemotron resolution

The original 17,17,17 observations are preserved as **SUPERSEDED — COMMON-CONFIGURATION / ATTRIBUTION-LIMITED RUN**. The preregistered corrected configuration used enable_thinking=false, temperature=0.6, and top_p=0.95 while keeping the benchmark model, GGUF, host, frozen llama.cpp, prompts, tools, simulator, scorer, context, 768-token ceiling, and retry policy fixed. The corrected observations scored R1 2,3,4,3,5,0,3 = 20, R2 2,3,2,3,5,0,3 = 18, and R3 2,3,2,3,5,0,3 = 18.

The change materially affected the result. Q01 remained transport-invalid in all three corrected repetitions; Q06 was catastrophic in all three. The corrected set had 295 malformed-argument events, 3 catastrophic actions, and 3 verified completions. Its resource eligibility failed with 0.72 GiB minimum available RAM and 6.43 GiB maximum swap delta.

## Interpretation

Capability score, resource eligibility, compatibility/admission, and reliability are separate axes. The 25/80 maximum is low in absolute terms and should not be described as strong autonomous-agent capability. The benchmark exposes frequent malformed calls, unsafe irreversible actions, weak verification, and long-horizon failures. Repetitions show stability under the exact frozen tasks/runtime, not broad real-world uncertainty.

## Provenance

- Forensic audit: d5d7cf6
- Resolution preregistration: 1dd561b
- Resolution evidence: 77a67c9
- Scientific freeze: final release-preparation commit
- Processed resolution result: runs/processed/nemotron-configuration-resolution-v1.0.0-results.json
- Public report: docs/REPORT.md
