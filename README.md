# Student Performance Predictor

A modular machine learning project that predicts a student's **math score** based on demographic and academic attributes using a fully automated pipeline — from raw data ingestion through preprocessing and model training.

---

## Problem Statement

Given student information such as gender, race/ethnicity, parental education level, lunch type, test preparation course, reading score, and writing score — predict the student's **math score**.

---

## Project Structure

```
ML_Projects/
├── artifacts/                   # Auto-generated outputs (CSVs, pickle files)
│   ├── data.csv                 # Raw dataset copy
│   ├── train.csv                # Training split
│   ├── test.csv                 # Test split
│   └── preprocessor_obj.pkl     # Serialised preprocessing pipeline
├── logs/                        # Auto-generated daily log files
├── notebook/
│   ├── data/
│   │   └── stud.csv             # Source dataset
│   └── 01_EDA_Student_Performance.ipynb
├── src/
│   ├── component/
│   │   ├── data_ingestion.py        # Reads raw CSV, splits into train/test
│   │   ├── data_transformation.py   # Builds and applies sklearn preprocessing pipeline
│   │   └── model_trainer.py         # (in progress) Model selection and training
│   ├── pipeline/
│   │   ├── train_pipeline.py        # Orchestrates the full training flow
│   │   └── predict_pipeline.py      # Loads artifacts and runs inference
│   ├── exception.py             # Custom exception with traceback detail
│   ├── logger.py                # Rotating daily file logger
│   └── utils.py                 # save_object / load_object helpers (dill)
├── main.py
├── setup.py
└── requirement.txt
```

---

## Features Used

| Feature | Type |
|---|---|
| gender | Categorical |
| race_ethnicity | Categorical |
| parental_level_of_education | Categorical |
| lunch | Categorical |
| test_preparation_course | Categorical |
| reading_score | Numerical |
| writing_score | Numerical |

**Target:** `math_score` (continuous)

---

## Pipeline

### 1. Data Ingestion (`data_ingestion.py`)
- Reads `notebook/data/stud.csv`
- Saves a raw copy to `artifacts/data.csv`
- Splits into 80/20 train-test and saves to `artifacts/train.csv` / `artifacts/test.csv`

### 2. Data Transformation (`data_transformation.py`)
- **Numerical features** → Median imputation → Standard scaling
- **Categorical features** → Most-frequent imputation → One-Hot encoding
- Combined via `sklearn.compose.ColumnTransformer`
- Fitted preprocessor serialised to `artifacts/preprocessor_obj.pkl` using `dill`

### 3. Model Trainer (`model_trainer.py`)
- In progress

---

## Setup

### Prerequisites
- Python 3.8+

### Install

```bash
# Clone the repository
git clone <repo-url>
cd ML_Projects

# Create and activate a virtual environment
python -m venv myenv
source myenv/bin/activate        # macOS/Linux
myenv\Scripts\activate           # Windows

# Install dependencies (also installs the package in editable mode)
pip install -r requirement.txt
```

### Dependencies

| Package | Purpose |
|---|---|
| pandas | Data loading and manipulation |
| numpy | Array operations |
| scikit-learn | Preprocessing pipelines and ML models |
| dill | Serialising complex Python objects (pipelines) |
| seaborn / matplotlib | EDA visualisations |

---

## Run

```bash
# Run the full ingestion + transformation pipeline
python src/component/data_ingestion.py
```

On success, `artifacts/preprocessor_obj.pkl` will be created along with the train/test CSVs.

---

## Logging

Logs are written to `logs/<YYYY-MM-DD>.log` and include timestamps, module names, and log levels.

---

## Author

**Tejasvi** — `hustlers037@gmail.com`
