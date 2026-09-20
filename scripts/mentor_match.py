#!/usr/bin/env python3
"""Development entry point for the portable Mentor Match storage helper."""

from pathlib import Path
import runpy


SKILL_SCRIPT = Path(__file__).resolve().parents[1] / "skills" / "mentor-match" / "scripts" / "mentor_match.py"


if __name__ == "__main__":
    runpy.run_path(str(SKILL_SCRIPT), run_name="__main__")
