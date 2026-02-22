import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "raw_hospital_data.csv"
CLEAN_PATH = ROOT / "data" / "processed" / "hospital_clean.csv"
OUT_PATH = ROOT / "reports" / "change_report.txt"

DTYPES_RAW = {
    "Provider ID": "string",
    "ZIP Code": "string",
    "Phone Number": "string",
    "State": "string",
}

NA_STRINGS = ["Not Available", "Not Applicable", "N/A", "NA", ""]


def standardize_columns(cols) -> pd.Index:
    """Match the same column naming scheme used in 02_clean.py."""
    return (
        pd.Index(cols)
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
        .str.replace(r"[^a-z0-9_]", "", regex=True)
    )


def missing_counts(df: pd.DataFrame, cols: list[str]) -> dict[str, int]:
    out = {}
    for c in cols:
        if c in df.columns:
            out[c] = int(df[c].isna().sum())
    return out


def main():
    raw = pd.read_csv(
        RAW_PATH,
        encoding="latin1",
        dtype=DTYPES_RAW,
        na_values=NA_STRINGS,
        keep_default_na=True,
    )

    clean = pd.read_csv(CLEAN_PATH, dtype=str)

    # Standardize raw column names BEFORE comparing to clean
    raw_std = raw.copy()
    raw_std.columns = standardize_columns(raw_std.columns)

    raw_cols = set(raw_std.columns)
    clean_cols = set(clean.columns)

    dropped = sorted(list(raw_cols - clean_cols))
    added = sorted(list(clean_cols - raw_cols))
    common = sorted(list(raw_cols & clean_cols))

    # Key fields: raw original names vs standardized clean names
    raw_key_cols = ["Provider ID", "ZIP Code", "Phone Number", "State"]
    clean_key_cols = ["provider_id", "zip_code", "phone_number", "state"]

    lines = []
    lines.append("=== CHANGE REPORT ===")
    lines.append(f"Raw file: {RAW_PATH}")
    lines.append(f"Clean file: {CLEAN_PATH}")
    lines.append("")
    lines.append(f"Raw shape: {raw.shape}")
    lines.append(f"Clean shape: {clean.shape}")
    lines.append("")
    lines.append(f"Common columns after standardization ({len(common)}): {common}")
    lines.append(f"Columns dropped ({len(dropped)}): {dropped}")
    lines.append(f"Columns added ({len(added)}): {added}")
    lines.append("")
    lines.append("Missing counts (raw key fields):")
    lines.append(str(missing_counts(raw, raw_key_cols)))
    lines.append("Missing counts (clean key fields):")
    lines.append(str(missing_counts(clean, clean_key_cols)))

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")

    print("\n".join(lines))
    print(f"\nSaved: {OUT_PATH}")


if __name__ == "__main__":
    main()