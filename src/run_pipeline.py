import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MODULES = [
    "src.load_and_profile",
    "src.clean",
    "src.validate",
    "src.report_changes",
]

def run(module: str) -> None:
    cmd = [sys.executable, "-m", module]
    print(f"\n>>> Running: {' '.join(cmd)}")
    subprocess.check_call(cmd, cwd=ROOT)

def main() -> None:
    for module in MODULES:
        run(module)
    print("\n✅ Pipeline complete.")

if __name__ == "__main__":
    main()