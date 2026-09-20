# Final release audit (historical V1 preparation)

> This document records the superseded V1 publication-preparation state. It is preserved as historical evidence. The canonical public result is now V2; see `README.md`, `docs/REPORT.md`, `docs/V2_METHODOLOGY_CORRECTION.md`, and `runs/processed/canonical-v2-results-2026-09-20.json`.

Status: **SUPERSEDED — V1 preparation record retained for provenance**.

## Completed

- Nemotron configuration resolution completed under one preregistered configuration; collection is closed.
- Scientific freeze prepared in V1.0_SCIENTIFIC_FREEZE.md.
- Six-model final table, resource distinction, compatibility exclusions, and superseded Nemotron evidence are documented.
- Standalone tests pass: 16 tests via python -m unittest discover -s tests -v.
- Model weights are absent from Git; exact external identities and hashes are recorded.
- License/attribution notice prepared in NOTICE.md for Mistral, Qwen, IBM Granite, NVIDIA Nemotron, and Meta Llama.
- Secret-pattern scan found no API keys, private keys, SSH material, passwords, or access tokens in non-raw tracked text.
- No live site or remote repository was modified.
- Raw-evidence privacy review completed; 123 tracked evidence/provenance files
  received deterministic, non-scientific metadata normalization documented in
  docs/REDACTION_POLICY.md and docs/REDACTION_MANIFEST.md.
- Tracked-file scan after redaction found no local account name, account-bearing
  home path, personal hostname, SSH alias, private key, access token, password,
  or valid private network address. Synthetic fixture emails and credentials
  were retained and classified as scientific task data.

## Conditions for publication

- The repository has no external GitHub repository or release authorization. Suggested metadata is prepared in docs/WEBSITE_PLACEMENT.md; no publication action has been taken.
- Upstream model terms remain applicable to any redistributed metadata or evidence; NOTICE.md supplies attribution pointers but is not legal advice or a substitute for license review by the distributor.

## Checks performed

- Full tracked-file privacy scan, including raw evidence, before and after redaction.
- Large-file scan: no model weights or giant binary artifacts in the repository; preserved JSON evidence is intentionally large.
- Processed-vs-raw resolution derivation regenerated successfully.
- Historical processed results were not overwritten.
- git diff --check passed after redaction.
- `python -m unittest discover -s tests -v`: 16/16 passing after redaction.
- The historical V1 totals and resource classifications recorded above are
  not the canonical V2 result. V2 supersedes the capability table while
  preserving the V1 evidence.

## Release recommendation

This V1 preparation record is retained for provenance. The current public
canonical result is the V2 publication described in the repository README and
report.
