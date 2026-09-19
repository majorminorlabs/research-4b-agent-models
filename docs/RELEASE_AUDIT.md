# Final release audit

Status: **BLOCKED — release candidate prepared, publication not authorized**.

## Completed

- Nemotron configuration resolution completed under one preregistered configuration; collection is closed.
- Scientific freeze prepared in V1.0_SCIENTIFIC_FREEZE.md.
- Six-model final table, resource distinction, compatibility exclusions, and superseded Nemotron evidence are documented.
- Standalone tests pass: 16 tests via python -m unittest discover -s tests -v.
- Model weights are absent from Git; exact external identities and hashes are recorded.
- License/attribution notice prepared in NOTICE.md for Mistral, Qwen, IBM Granite, NVIDIA Nemotron, and Meta Llama.
- Secret-pattern scan found no API keys, private keys, SSH material, passwords, or access tokens in non-raw tracked text.
- No live site or remote repository was modified.

## Blocking items before public distribution

- Raw logs and provenance include machine-local paths, usernames, host aliases, and hardware details. These are scientifically useful but require a final decision to publish raw evidence separately, redact it, or retain it behind an archival package.
- The repository has no external GitHub repository or release authorization. Suggested metadata is prepared in docs/WEBSITE_PLACEMENT.md, but no publication action is authorized.
- Upstream model terms remain applicable to any redistributed metadata or evidence; NOTICE.md supplies attribution pointers but is not legal advice or a substitute for license review by the distributor.

## Checks performed

- git grep secret-pattern scan over tracked non-raw content.
- Large-file scan: no model weights or giant binary artifacts in the repository; preserved JSON evidence is intentionally large.
- Processed-vs-raw resolution derivation regenerated successfully.
- Historical processed results were not overwritten.
- git diff --check passed at audit time.

## Release recommendation

Keep the repository in **BLOCKED** status until a human selects a raw-evidence redaction/distribution policy and explicitly authorizes publication. Proposed tag remains v1.0.0.

