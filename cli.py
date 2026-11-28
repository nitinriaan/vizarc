"""
Backward-compatible root CLI wrapper for VizArc.
The installable entrypoint lives in `src/vizarc/cli.py`.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from vizarc.cli import main

if __name__ == "__main__":
    main()
