import os
import sys
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLEAN_PATH = Path(os.getenv("CLEAN_PATH", str(ROOT / "data" / "processed" / "hospital_clean.csv")))
REPORT_PATH = ROOT / "reports" / "validation_report.txt"

# Treat these as missing when reading the cleaned file (belt + suspenders)
NA_STRINGS = ["Not Available", "Not Applicable", "N/A", "NA", ""]

# Common CMS-style comparison categories. If your dataset contains additional ones,
# we’ll add them after we see the outliers.
ALLOWED_COMPARISON = {
    "Above the national average",
    "Same as the national average",
    "Below the national average",
    "Not Available",
    "Number of Cases Too Small",
    "Not Applicable",
}

def fail(lines: list[str], msg: str) -> None:
    lines.append(f"FAIL: {msg}")

def ok(lines: list[str], msg: str) -> None:
    lines.append(f"OK: {msg}")

def main() -> None:
    df = pd.read_csv(
        CLEAN_PATH,
        dtype=str,
        na_values=NA_STRINGS,
        keep_default_na=True,
    )

    failures = 0
    lines: list[str] = []
    lines.append("=== VALIDATION REPORT (Phase 3) ===")
    lines.append(f"File: {CLEAN_PATH}")
    lines.append(f"Rows, Cols: {df.shape}")
    lines.append("")

    # ---------- provider_id ----------
    if "provider_id" not in df.columns:
        failures += 1
        fail(lines, "Missing required column: provider_id")
    else:
        pid = df["provider_id"]

        null_pid = int(pid.isna().sum())
        dup_pid = int(pid.duplicated().sum())

        bad_pid = pid.dropna()
        bad_pid = bad_pid[~bad_pid.str.match(r"^\d{6}$")]

        if null_pid == 0:
            ok(lines, "provider_id has 0 missing values")
        else:
            failures += 1
            fail(lines, f"provider_id missing values: {null_pid}")

        if dup_pid == 0:
            ok(lines, "provider_id is unique (0 duplicates)")
        else:
            failures += 1
            fail(lines, f"provider_id duplicates: {dup_pid}")

        if len(bad_pid) == 0:
            ok(lines, "provider_id format is 6 digits")
        else:
            failures += 1
            fail(lines, f"provider_id not 6 digits: {len(bad_pid)} examples={bad_pid.head(10).tolist()}")

    lines.append("")

    # ---------- ZIP / Phone / State formats ----------
    for col, pattern in [
        ("zip_code", r"^\d{5}$"),
        ("phone_number", r"^\d{10}$"),
        ("state", r"^[A-Z]{2}$"),
    ]:
        if col not in df.columns:
            failures += 1
            fail(lines, f"Missing required column: {col}")
            continue

        s = df[col].dropna()
        bad = s[~s.str.match(pattern)]
        if len(bad) == 0:
            ok(lines, f"{col} format valid (0 bad)")
        else:
            failures += 1
            fail(lines, f"{col} format invalid: {len(bad)} examples={bad.head(10).tolist()}")

    lines.append("")

    # ---------- hospital_overall_rating (1–5 or null) ----------
    if "hospital_overall_rating" not in df.columns:
        failures += 1
        fail(lines, "Missing required column: hospital_overall_rating")
    else:
        r = df["hospital_overall_rating"]

        # Convert to numeric where possible
        r_num = pd.to_numeric(r, errors="coerce")

        # Valid if null OR integer 1..5
        # (Some CMS extracts store as 1.0–5.0; coerce handles both)
        invalid_mask = (~r.isna()) & (~r_num.isin([1, 2, 3, 4, 5]))
        invalid = r[invalid_mask]

        if len(invalid) == 0:
            ok(lines, "hospital_overall_rating values are 1–5 or null")
        else:
            failures += 1
            fail(lines, f"hospital_overall_rating invalid values: {len(invalid)} examples={invalid.head(10).tolist()}")

    lines.append("")

    # ---------- emergency_services (Yes/No or null) ----------
    if "emergency_services" not in df.columns:
        failures += 1
        fail(lines, "Missing required column: emergency_services")
    else:
        es = df["emergency_services"].dropna().str.strip()
        # normalize common variants
        es_norm = (
            es.replace(
                {
                    "YES": "Yes",
                    "NO": "No",
                    "Yes": "Yes",
                    "No": "No",
                }
            )
        )

        bad_es = es_norm[~es_norm.isin(["Yes", "No"])]
        if len(bad_es) == 0:
            ok(lines, "emergency_services values are Yes/No or null")
        else:
            failures += 1
            top_bad = bad_es.value_counts().head(10).to_dict()
            fail(lines, f"emergency_services invalid values: {len(bad_es)} top={top_bad}")

    lines.append("")

    # ---------- national comparison columns (allowed categories or null) ----------
    comparison_cols = [c for c in df.columns if c.endswith("_national_comparison")]
    if len(comparison_cols) == 0:
        failures += 1
        fail(lines, "No *_national_comparison columns found (unexpected)")
    else:
        ok(lines, f"Found {len(comparison_cols)} *_national_comparison columns")

        for c in comparison_cols:
            s = df[c].dropna().str.strip()

            # Allow known categories; treat “Not Available” / “Not Applicable” as allowed if present
            bad = s[~s.isin(ALLOWED_COMPARISON)]
            if len(bad) == 0:
                ok(lines, f"{c}: allowed categories only")
            else:
                failures += 1
                top_bad = bad.value_counts().head(10).to_dict()
                fail(lines, f"{c}: invalid categories={len(bad)} top={top_bad}")

    lines.append("")
    lines.append(f"TOTAL FAILURES: {failures}")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")

    print("\n".join(lines))
    print(f"\nSaved: {REPORT_PATH}")

    if failures > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()