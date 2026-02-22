from src.config import KEEP_COLUMNS
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "raw_hospital_data.csv"
OUT_PATH = ROOT / "data" / "processed" / "hospital_clean.csv"

DTYPES = {
    "Provider ID": "string",
    "ZIP Code": "string",
    "Phone Number": "string",
    "State": "string",
}

NA_STRINGS = ["Not Available", "Not Applicable", "N/A", "NA", ""]

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
        .str.replace(r"[^a-z0-9_]", "", regex=True)
    )
    return df

def clean_state(s: pd.Series) -> pd.Series:
    return s.astype("string").str.strip().str.upper()

def clean_zip(s: pd.Series) -> pd.Series:
    s = s.astype("string").str.strip().str.replace(r"[^0-9]", "", regex=True)
    s = s.str.slice(0, 5)
    return s

def clean_phone(s: pd.Series) -> pd.Series:
    s = s.astype("string").str.strip().str.replace(r"[^0-9]", "", regex=True)
    s = s.where(s.str.len() != 11, s.str.slice(1, 11))  # drop leading 1 if present
    s = s.where(s.str.len() == 10, pd.NA)
    return s

def drop_footnote_cols(df: pd.DataFrame) -> pd.DataFrame:
    cols = [c for c in df.columns if "footnote" in c]
    return df.drop(columns=cols)

def main():
    df = pd.read_csv(
        RAW_PATH,
        encoding="latin1",
        dtype=DTYPES,
        na_values=NA_STRINGS,
        keep_default_na=True,
    )

    df = standardize_columns(df)
        # normalize whitespace in common text fields (safe: no case changes)
    TEXT_COLS = [
    "hospital_name",
    "address",
    "city",
    "county_name",
    "hospital_type",
    "hospital_ownership",
]

    for c in TEXT_COLS:
        if c in df.columns:
            df[c] = (
                df[c].astype("string")
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
            )



    if "state" in df.columns:
        df["state"] = clean_state(df["state"])
    if "zip_code" in df.columns:
        df["zip_code"] = clean_zip(df["zip_code"])
    if "phone_number" in df.columns:
        df["phone_number"] = clean_phone(df["phone_number"])

    

    df = drop_footnote_cols(df)

    # schema lock (enforce exact output columns + order)
    df = df[KEEP_COLUMNS]

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    print(f"Saved: {OUT_PATH}")
    print(f"Rows, Cols: {df.shape}")

if __name__ == "__main__":
    main()