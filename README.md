# hospital-cleaning-project

Data cleaning pipeline for the CMS Hospital General Information dataset.

## Goal
- Load raw hospital data
- Profile missingness, types, and duplicates
- Clean key fields (IDs, ZIP, phone, state)
- Produce a processed dataset for analysis

## Data
- Source: CMS “Hospital General Information” dataset
- Raw file location (not tracked in Git): `data/raw/raw_hospital_data.csv`

## Project structure
- `src/`
  - `01_load_and_profile.py` — loads raw data and writes a profiling summary to `reports/`
- `reports/`
  - `profile_summary.txt` — profiling output (rows/cols, dtypes, missing values, duplicates)

## Setup
```bash
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

```md
## Run profiling
```bash
.\.venv\Scripts\python.exe src/01_load_and_profile.py