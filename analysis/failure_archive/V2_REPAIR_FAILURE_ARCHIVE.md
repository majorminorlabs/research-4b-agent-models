# V2 repair failure/methodology archive

This archive preserves methodology failures as evidence rather than treating them as model scores. It is the systems/methodology appendix for the canonical V2 study.

The classifications below distinguish model behavior, infrastructure behavior, resource limitation, and unresolved attribution. Hardware causality is not claimed where the evidence only establishes software or interface failure.

| Incident | Model | Stage | Observed failure | Classification | Impact |
|---|---|---|---|---|---|
| Shared runner/adapter batch | multiple candidates | original field execution | parser/transport and runner failures | `INVALID_INFRASTRUCTURE` | excluded from final capability score; raw evidence preserved |
| Nemotron repeated malformed tool calls | Nemotron-3-Nano-4B | original and resolution runs | calls ending around `{`, malformed arguments, HTTP 500/`finish_reason:length`, missing pre-parser token stream | infrastructure/interface interaction; unresolved where transport-invalid | nine noncanonical and three canonical Q01 observations cannot be reconstructed retrospectively |
| Nemotron short admission | Nemotron-3-Nano-4B | admission | 256-token admission did not expose long repeated-interaction failures | admission-test design defect | explains why later 768-token benchmark transport failures were not caught earlier |
| Q05 simulator contract | all models | historical V1 traces | old simulator did not enforce pause/load/affinity predicates | simulator-version mismatch | forward-only atoms cannot be imputed; observed no-movement scores remain conservative V2 zero |
| Resource eligibility | Qwen3 4B, Nemotron resolution | historical local runs | available-RAM/swap limits failed in the recorded cohort | resource qualification failure | behavioral evidence remains separate from eligibility |
| V2 repair Q01 replacements | Nemotron-3-Nano-4B | declared repair R1–R3 | corrected settings still produced one-turn malformed-argument/HTTP 500 transport failures; no pre-parser generations preserved | unresolved model/interface/transport interaction | canonical Q01 remains unresolved; no zero or success is imputed |

## Classification guide

- **MODEL BEHAVIOR:** malformed arguments or unsafe actions are attributed to the model only where the valid interface delivered an interpretable observation.
- **INFRASTRUCTURE BEHAVIOR:** parser, adapter, server, runner, or simulator defects that prevent the intended observation are not counted as model failures.
- **RESOURCE LIMITATION:** RAM, swap, or runtime eligibility failures are reported separately from behavioral points.
- **UNRESOLVED ATTRIBUTION:** preserved evidence cannot distinguish model generation from interface/transport termination; no score is imputed.

The historical raw logs, resource telemetry, Nemotron forensic manifest, Q05 qualification, and three replacement artifacts remain preserved. Future experiments are recorded in `docs/FUTURE_WORK.md` and are not required to close this study.

For complete provenance, retain the existing raw directories, server logs, resource telemetry, forensic audit, and V1 freeze. This file does not replace or rewrite them.
