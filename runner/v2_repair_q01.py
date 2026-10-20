"""Run one predeclared V2 repair Q01 observation.

The frozen V2 collector and future simulator are imported from the pinned
measurement workspace. This wrapper changes only the already-authorized
Nemotron resolution sampling fields; it does not alter tasks, prompts,
simulator semantics, or scoring.
"""

import sys

V2_ROOT = "<WORKDIR>/tests/mm-8b-benchmark"
sys.path.insert(0, V2_ROOT + "/frozen_reference")
sys.path.insert(0, V2_ROOT)

from execution import frozen_replay  # noqa: E402
from scoring.v2.future_simulator import SimulatorV2  # noqa: E402
from scoring.v2.tool_schema import tool_defs_v2  # noqa: E402


frozen_replay.Simulator = SimulatorV2
frozen_replay.tool_defs = tool_defs_v2
# The controller runs on macOS while the inference server runs on the
# ThinkPad. Do not read or fabricate local /proc values; remote telemetry is
# captured independently on the inference host.
frozen_replay.sample = lambda pid, phase: {
    "epoch": __import__("time").time(),
    "phase": phase,
    "pid": pid,
    "rss_bytes": None,
    "mem": {"remote_telemetry": "captured_on_thinkpad"},
}

_post = frozen_replay.post


def post(base, payload):
    payload["temperature"] = 0.6
    payload["top_p"] = 0.95
    payload["chat_template_kwargs"] = {"enable_thinking": False}
    return _post(base, payload)


frozen_replay.post = post


if __name__ == "__main__":
    frozen_replay.main()
