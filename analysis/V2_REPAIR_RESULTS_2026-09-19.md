# Corrected V2 repair results

The manifest-authorized repair executed exactly three Nemotron Q01 replacement measurements. No other model, task, or exploratory run was launched.

## Replacement outcomes

| Replacement | Historical case | Outcome | V2 score | Resource telemetry |
|---|---|---|---:|---|
| N-REPAIR-R1-Q01 | resolution R1/Q01 | transport-invalid after one turn | unresolved | 0 swap; minimum available 9.33 GiB; peak server RSS 0.43 GiB |
| N-REPAIR-R2-Q01 | resolution R2/Q01 | transport-invalid after one turn | unresolved | 0 swap; same server/host telemetry |
| N-REPAIR-R3-Q01 | resolution R3/Q01 | transport-invalid after one turn | unresolved | 0 swap; same server/host telemetry |

The server log records the frozen model loading with one slot and a 16,384-token slot context, followed by three JSON tool-argument parse failures and HTTP 500 responses. The raw returned bodies and requests are preserved. No V2 task score is imputed: the missing pre-parser generation means the Q01 outcome cannot be separated into model-side malformed generation versus transport/parser termination under the fail-closed rule.

## Canonical V2 state

The canonical non-Nemotron table remains the immutable V2 rescore result:

| Model | Per-run V2 total(s) | Per-task V2 scores | Provenance |
|---|---:|---|---|
| Ministral-3-3B-Instruct-2512 | 2, 2, 2 | 0, 0, 2, 0, 0, 0, 0 | `V2_RETROSPECTIVE_RESCORE` |
| Qwen3-4B | 0, 0, 0 | 0, 0, 0, 0, 0, 0, 0 | `V2_RETROSPECTIVE_RESCORE` |
| Qwen2.5-3B-Instruct | 4 | 0, 0, 0, 0, 0, 0, 0 | `V2_RETROSPECTIVE_RESCORE` |
| Granite-4.1-3B | 6 | 4, 0, 2, 0, 0, 0, 0 | `V2_RETROSPECTIVE_RESCORE` |
| Llama-3.2-3B-Instruct | 2 | 2, 0, 0, 0, 0, 0, 0 | `V2_RETROSPECTIVE_RESCORE` |
| Nemotron-3-Nano-4B | 0–10 each repetition | Q01 unresolved; Q02–Q07 = 0 | Q01 `V2_REPLACEMENT_MEASUREMENT` unresolved; Q02–Q07 retrospective |

Nemotron therefore does not have a complete canonical V2 total. The three replacement runs reproduce the unresolved transport/interface failure; they do not justify treating Q01 as zero or as successful. This is the corrected research result, not a failure of the repair to choose a number.

## Resource status

The replacement host run itself had zero swap throughout, minimum sampled available RAM 9.33 GiB, and peak server RSS approximately 0.43 GiB. These observations satisfy the RAM/swap telemetry predicates for the replacement execution. They do not make the unresolved behavioral observation scoreable, and they do not alter the historical Nemotron resolution resource FAIL (minimum available RAM approximately 0.72 GiB and 6.43 GiB swap delta).

## V1 → V2 and conclusions

The V1-to-V2 changes remain those in the immutable V2 rescore artifact: 100 decisions were reconstructed; 12 remain unresolved. The three new replacements do not reduce that unresolved count because they reproduce the same evidence gap under the corrected Nemotron settings. Historical V1 headline claims based on proxy credit, unchanged state, or Q05's old simulator contract do not survive as V2 capability claims. The resource-eligibility conclusions remain separate from behavioral scores.

The former Nemotron 20/18/18 configuration-resolution totals remain preserved historical V1 evidence and are not silently converted into V2 totals. The original 17/17/17 observations remain preserved and superseded as previously documented. No model ranking or scale conclusion should use Nemotron as a complete V2 point estimate.

