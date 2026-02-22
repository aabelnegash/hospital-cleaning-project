# hospital-cleaning-project

Data cleaning pipeline for the CMS “Hospital General Information” dataset.

## Goal
- Load raw hospital data
- Profile missingness, data types, and duplicates
- Clean key fields (Provider ID, ZIP Code, Phone Number, State)
- Output a processed dataset for analysis

## Data
- Source: CMS “Hospital General Information” dataset
- Raw file location (not tracked in Git): `data/raw/raw_hospital_data.csv`

## Project structure
- `src/`
  - `01_load_and_profile.py` — loads raw data and writes a profiling summary to `reports/`
- `reports/`
  - `profile_summary.txt` — profiling output (rows/cols, dtypes, missing values, duplicates)

## Setup (Windows)
```bash
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run profiling
```bash
.\.venv\Scripts\python.exe src/01_load_and_profile.py
```
## Run cleaning
```bash
.\.venv\Scripts\python.exe src/02_clean.py
```
Output schema (clean file)

The cleaned dataset schema is enforced to stay consistent across runs.

See src/config.py (KEEP_COLUMNS) for the exact output columns and order.

## Run validation
```bash
.\.venv\Scripts\python.exe src/03_validate.py
```