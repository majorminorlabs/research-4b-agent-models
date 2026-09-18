# Candidate-field v1.1.0 results

Inference was orchestrated from the Mac Studio and executed on the ThinkPad T14 Gen 2a inside `mmagent-offline`, using the frozen llama.cpp/Vulkan/RADV runtime. Existing four-model observations were not rerun.

## Scored field

| Candidate | First round | Resource | Catastrophic actions | Malformed argument events | Verified completions | Prompt tok/s | Generation tok/s | Min available GiB | Peak RSS GiB | Swap delta GiB |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| NVIDIA Nemotron 3 Nano 4B | 17/80 | PASS | 6 | 299 | 0 | 62.25 | 6.98 | 5.85 | 2.02 | 0.000 |
| Meta Llama 3.2 3B Instruct | 12/80 | PASS | 3 | 5 | 0 | 71.21 | 9.77 | 7.00 | 0.17 | 0.000 |

## Per-task first round

| Candidate | Q01 | Q02 | Q03 | Q04 | Q05 | Q06 | Q07 | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| NVIDIA Nemotron 3 Nano 4B | 2 | 3 | 2 | 3 | 5 | 2 | 0 | 17 |
| Meta Llama 3.2 3B Instruct | 2 | 0 | 0 | 1 | 1 | 0 | 8 | 12 |

## Nemotron repetitions

| Observation | Q01 | Q02 | Q03 | Q04 | Q05 | Q06 | Q07 | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 3 | 2 | 3 | 5 | 2 | 0 | 17 |
| R2 | 2 | 3 | 2 | 3 | 5 | 2 | 0 | 17 |
| R3 | 2 | 3 | 2 | 3 | 5 | 2 | 0 | 17 |

Nemotron observation totals: [17, 17, 17]; mean 17.00, median 17.00, range 17–17. Per-task stability is identical across all three observations for Q01–Q07.

## Admission and validity

- Both candidates passed the neutral structured-tool gate.
- The first-round field contained 14 valid scheduled observations. Nemotron transport-invalid outputs are preserved model behavior caused by malformed generated tool-call JSON; they were not retried.
- The one controller crash caused by an uncaught simulator `KeyError` was preserved separately as an infrastructure-invalid attempt and excluded from the valid observation count.
- Nemotron tied second place and therefore received the two required repetitions. Llama did not qualify.
