import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/raw_hospital_data.csv")  # your local raw file
OUT_PROFILE = Path("reports/profile_summary.txt")

# Force string types to preserve leading zeros
DTYPES = {
    "Provider ID": "string",
    "ZIP Code": "string",
    "Phone Number": "string",
    "State": "string",
}

NA_STRINGS = ["Not Available", "Not Applicable", "N/A", "NA", ""]

def main():
    df = pd.read_csv(
        RAW_PATH,
        encoding="latin1",
        dtype=DTYPES,
        na_values=NA_STRINGS,
        keep_default_na=True,
    )

    lines = []
    lines.append("=== BASIC PROFILE ===")
    lines.append(f"Rows, Cols: {df.shape}")
    lines.append("")
    lines.append("Columns:")
    lines.append(str(df.columns.tolist()))
    lines.append("")
    lines.append("Dtypes:")
    lines.append(str(df.dtypes))
    lines.append("")
    lines.append("Missing values (top 20):")
    lines.append(str(df.isna().sum().sort_values(ascending=False).head(20)))
    lines.append("")
    lines.append(f"Duplicate rows: {df.duplicated().sum()}")
    lines.append(f"Duplicate Provider ID: {df['Provider ID'].duplicated().sum()}")

    OUT_PROFILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_PROFILE.write_text("\n".join(lines), encoding="utf-8")

    print("\n".join(lines))
    print(f"\nSaved profile to: {OUT_PROFILE}")

if __name__ == "__main__":
    main()