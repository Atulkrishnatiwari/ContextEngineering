#!/usr/bin/env python3

import json
import sys
import pandas as pd
from pathlib import Path

def validate_csv(filepath):
    errors = []
    warnings = []

    report = {
        "filepath": filepath,
        "format": "csv",
        "errors": errors,
        "warnings": warnings,
        "metadata": {}
    }

    if not Path(filepath).exists():
        errors.append(f"File not found: {filepath}")
        return report

    try:
        df = pd.read_csv(filepath)

        report["metadata"]["rows"] = len(df)
        report["metadata"]["columns"] = list(df.columns)
        report["metadata"]["dtypes"] = {
            k: str(v) for k, v in df.dtypes.items()
        }

        missing = df.isna().sum()
        if missing.any():
            report["metadata"]["missing_values"] = missing.to_dict()

        duplicates = df.duplicated().sum()
        if duplicates > 0:
            warnings.append(f"Found {duplicates} duplicate rows")

        for col in df.select_dtypes(include='object').columns:
            empty = (df[col].str.strip() == '').sum()
            if empty > 0:
                warnings.append(
                    f"Column '{col}' has {empty} empty strings"
                )

    except Exception as e:
        errors.append(f"Error reading file: {str(e)}")

    return report

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_dataset.py <file>")
        sys.exit(1)

    report = validate_csv(sys.argv[1])
    print(json.dumps(report, indent=2))

    if report["errors"]:
        sys.exit(1)

if __name__ == "__main__":
    main()
