#!/usr/bin/env python3

import sys
import pandas as pd
from pathlib import Path

def generate_report(filepath):
    report = []

    report.append("=" * 60)
    report.append("DATASET VALIDATION REPORT")
    report.append("=" * 60)

    if not Path(filepath).exists():
        return f"ERROR: File not found: {filepath}"

    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        return f"ERROR: Could not read file: {e}"

    report.append(f"\nFile: {filepath}")
    report.append("\nBASIC STATISTICS")
    report.append(f"Rows: {len(df)}")
    report.append(f"Columns: {len(df.columns)}")
    report.append(
        f"Memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
    )

    report.append("\nCOLUMN INFORMATION")

    for col in df.columns:
        report.append(
            f"{col}: {df[col].dtype} "
            f"({df[col].notna().sum()}/{len(df)} non-null)"
        )

    missing = df.isna().sum().sum()
    duplicates = df.duplicated().sum()

    report.append("\nDATA QUALITY")
    report.append(f"Missing values: {missing}")
    report.append(f"Duplicate rows: {duplicates}")

    report.append("\nRECOMMENDATIONS")

    if missing > 0:
        report.append("- Handle missing values")

    if duplicates > 0:
        report.append("- Remove duplicate rows")

    report.append("- Document dataset and preprocessing steps")
    report.append("- Add LICENSE and README.md files")

    report.append("\n" + "=" * 60)

    return "\n".join(report)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_report.py <file>")
        sys.exit(1)

    print(generate_report(sys.argv[1]))
