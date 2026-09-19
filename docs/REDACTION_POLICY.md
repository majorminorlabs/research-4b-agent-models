# Publication redaction policy

This policy defines the privacy pass applied after the scientific record was
frozen at commit `9dc8699`. It covers tracked source, provenance, processed
results, raw evidence, reports, and release metadata.

## Preserve

The release retains model IDs and hashes, task IDs and fixtures, prompts and
responses, tool-call arguments, malformed/catastrophic/completion outcomes,
timestamps and run IDs, hardware specifications, runtime and driver versions,
resource measurements, error messages, and all aggregate scores. These fields
are scientifically necessary and are not altered.

## Normalize

Only non-scientific identifying metadata is normalized:

- the local account name and account-bearing home paths become `<user>`;
- controller and remote personal hostnames/SSH labels become
  `<controller-host>` and `<remote-host>`;
- executable/model filesystem paths retain their structure and filenames while
  replacing the local account component.

The generic hardware class `Lenovo ThinkPad T14 Gen 2a` is retained because it
is part of the execution environment description. Synthetic benchmark values
such as `mreed@example.com`, `secret/warehouse-prod`, and task credential
fields are retained because they are fixture inputs and outputs, not personal
metadata.

## Procedure and invariants

The original frozen record remains recoverable in Git history at `9dc8699`.
Publication-tree replacements are deterministic and documented in
`docs/REDACTION_MANIFEST.md`; no historical evidence file is silently deleted.
Every replacement is checked to have scientific meaning changed: **NO**.
After redaction, tests and result-table comparisons must pass, and no model
run or scientific recomputation is permitted.
