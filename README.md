# Hospital Data Cleaning Project
![CI](../../actions/workflows/ci.yml/badge.svg)

Data cleaning pipeline for the CMS “Hospital General Information” dataset.

## Goal
- Load raw hospital data
- Profile missingness, data types, and duplicates
- Clean key fields (Provider ID, ZIP Code, Phone Number, State)
- Output a processed dataset for analysis

## Data
- Source: CMS “Hospital General Information” dataset
- Dataset Link: https://www.kaggle.com/datasets/cms/hospital-general-information
- Raw file location (not tracked in Git): `data/raw/raw_hospital_data.csv`

## Project structure
- `src/`
  - `load_and_profile.py` — loads raw data and writes a profiling summary to `reports/`
  - `clean.py` — cleans data and writes the cleaned output locally
  - `validate.py` — runs data quality checks and writes a validation report
  - `report_changes.py` — compares raw vs clean and writes a change report
  - `run_pipeline.py` — runs the full pipeline end-to-end
  - `config.py` — defines the enforced output schema (`KEEP_COLUMNS`)
  - `__init__.py` — marks `src` as a package
- `reports/`
  - `profile_summary.txt` — profiling output (rows/cols, dtypes, missing values, duplicates)
  - `validation_report.txt` — validation results
  - `change_report.txt` — what changed from raw → clean

## Setup (Windows)
```bash
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```
## Run full pipeline
```bash
.\.venv\Scripts\python.exe -m src.run_pipeline
```
## Run profiling 
```bash
.\.venv\Scripts\python.exe -m src.load_and_profile
```
## Run cleaning
```bash
.\.venv\Scripts\python.exe -m src.clean
```
**Output schema (clean file)**
- The cleaned dataset schema is enforced to stay consistent across runs.
- See `src/config.py` (`KEEP_COLUMNS`) for the exact output columns and order.

## Run validation
```bash
.\.venv\Scripts\python.exe -m src.validate
```
**CI runs validation against data/sample/hospital_clean_sample.csv (CLEAN_PATH env var).**

## Run change report
```bash
.\.venv\Scripts\python.exe -m src.report_changes
```
**Notes**
- Raw data is intentionally not committed to GitHub.
- Processed outputs are generated locally in data/processed/.
- Validation exits with a non-zero code if checks fail (pipeline will stop).
