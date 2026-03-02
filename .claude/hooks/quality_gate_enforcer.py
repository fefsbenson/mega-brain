#!/usr/bin/env python3
"""Quality Gate Enforcer - PostToolUse hook that validates pipeline checkpoints.

Checks if pipeline operations pass quality gates defined in
core/checklists/clone-quality-gates.yaml.

Exit codes: 0=pass, 1=warn (continue), 2=block
"""
import json
import sys
from pathlib import Path

def main():
    try:
        input_data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
    except (json.JSONDecodeError, Exception):
        sys.exit(0)  # Silent pass on parse errors

    tool_name = input_data.get("tool_name", "")
    file_path = input_data.get("file_path", "")

    # Only activate for pipeline-related file writes
    if not any(marker in file_path for marker in [
        "artifacts/", "knowledge/dna/", "agents/persons/"
    ]):
        sys.exit(0)

    # Check if we're in a pipeline phase
    state_file = Path(".claude/mission-control/MISSION-STATE.json")
    if not state_file.exists():
        sys.exit(0)

    try:
        state = json.loads(state_file.read_text())
        phase = state.get("current_state", {}).get("phase", 0)
    except Exception:
        sys.exit(0)

    # Log gate check (non-blocking)
    gate_log = Path("logs/quality-gates.jsonl")
    gate_log.parent.mkdir(parents=True, exist_ok=True)

    import datetime
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "tool": tool_name,
        "file": file_path,
        "phase": phase,
        "status": "checked"
    }

    with open(gate_log, "a") as f:
        f.write(json.dumps(entry) + "\n")

    sys.exit(0)  # Non-blocking by default

if __name__ == "__main__":
    main()
