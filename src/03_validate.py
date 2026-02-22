import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLEAN_PATH = ROOT / "data" / "processed" / "hospital_clean.csv"
REPORT_PATH = ROOT / "reports" / "validation_report.txt"

def main():
    df = pd.read_csv(CLEAN_PATH, dtype=str)

    # Basic counts
    rows, cols = df.shape
    dup_rows = df.duplicated().sum()
    dup_provider = df["provider_id"].duplicated().sum() if "provider_id" in df.columns else "N/A"

    # Field checks
    bad_zip = 0
    if "zip_code" in df.columns:
        z = df["zip_code"].dropna()
        bad_zip = (~z.str.match(r"^\d{5}$")).sum()

    bad_phone = 0
    if "phone_number" in df.columns:
        p = df["phone_number"].dropna()
        bad_phone = (~p.str.match(r"^\d{10}$")).sum()

    bad_state = 0
    if "state" in df.columns:
        s = df["state"].dropna()
        bad_state = (~s.str.match(r"^[A-Z]{2}$")).sum()

    lines = [
        "=== VALIDATION REPORT ===",
        f"File: {CLEAN_PATH}",
        f"Rows, Cols: ({rows}, {cols})",
        f"Duplicate rows: {dup_rows}",
        f"Duplicate provider_id: {dup_provider}",
        f"bad_zip_count: {bad_zip}",
        f"bad_phone_count: {bad_phone}",
        f"bad_state_count: {bad_state}",
    ]

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(map(str, lines)), encoding="utf-8")
    print("\n".join(map(str, lines)))
    print(f"\nSaved: {REPORT_PATH}")

if __name__ == "__main__":
    main()