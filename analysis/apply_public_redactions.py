"""Apply the deterministic publication metadata redactions.

This script intentionally edits only tracked text files and does not touch
the frozen scientific fields or regenerate any result.
"""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
replacements = (
    ("/home/dippo", "/home/<user>"),
    ("/Users/dippo", "/Users/<user>"),
    ("dippo@", "<user>@"),
    ("Mac Studio", "<controller-host>"),
    ("pop-os", "<remote-host>"),
    ("hostname: dippos-Mac-Studio.local", "hostname: <controller-host>"),
    ("ssh_alias: thinkpad", "ssh_alias: <remote-host>"),
    ("remote_user: dippo", "remote_user: <user>"),
    ('"remote_user": "dippo"', '"remote_user": "<user>"'),
)

changed = []
for rel in tracked:
    path = ROOT / rel
    try:
        text = path.read_text()
    except (UnicodeDecodeError, OSError):
        continue
    new = text
    for old, replacement in replacements:
        new = new.replace(old, replacement)
    # Process snapshots and metadata also contain the account as a standalone
    # field. Avoid changing the repository's synthetic fixture values.
    if rel.startswith("runs/"):
        new = new.replace("dippo ", "<user> ")
        new = new.replace("dippo\t", "<user>\t")
    if new != text:
        path.write_text(new)
        changed.append(rel)
print(f"redacted {len(changed)} tracked files")
for rel in changed:
    print(rel)
