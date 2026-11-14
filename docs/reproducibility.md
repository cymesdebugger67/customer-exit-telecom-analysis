# Project Reproducibility Guide

## Project

The Customer Exit — Telecom Analytics

**Author:** Cyril James Lunzaga

## Purpose

This guide explains how to install, execute, test, and reproduce the analytics project.

## Validated Environment

- Python 3.15.2
- Pandas 3.1.1
- Matplotlib 3.11.2
- SciPy 1.18.1
- Pytest 9.2.0
- IPyKernel 7.4.0

## 1. Create the Python Environment

From the project root, run:

    py -3.15 -m venv .venv

## 2. Install Dependencies

    .\.venv\Scripts\python.exe -m pip install -r requirements.txt

## 3. Install the Local Analytics Package

    .\.venv\Scripts\python.exe -m pip install -e .

## 4. Prepare the Dataset

Download the genuine IBM Telco Customer Churn dataset.

Place the CSV at:

    data/raw/Telco-Customer-Churn.csv

The raw dataset is intentionally excluded from Git version control.

## 5. Execute the Analytics Pipeline

    .\.venv\Scripts\python.exe .\scripts\run_pipeline.py

The pipeline generates:

- 22 analytical tables
- 15 analytical charts
- 3 Markdown reports
- Data-quality diagnostics
- Cleaned analytical data

## 6. Generate README Graphics

    .\.venv\Scripts\python.exe .\scripts\build_readme_assets.py

This creates the project banner, KPI summary, and analytics workflow graphics.

## 7. Execute the Jupyter Notebooks

Open the notebooks folder in VS Code.

Select the project virtual environment as the Python kernel.

Run notebook cells from top to bottom.

## 8. Run Automated Tests

    .\.venv\Scripts\python.exe -m pytest -v

## 9. Validate Project Outputs

    .\.venv\Scripts\python.exe .\scripts\validate_project.py

## Reproducibility Notes

The pipeline uses a JSON configuration file located at:

    config/analysis_config.json

Bootstrap resampling uses a fixed random seed to support repeatable results.

Generated processed data remains local and is excluded from Git.

The project uses descriptive and statistical analysis, not predictive machine learning.

## Limitations

Reproduction requires access to the original dataset and a compatible Python environment.

The findings describe the historical sample and should not be interpreted as causal relationships.
