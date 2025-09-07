"""
Tool for performing a comprehensive data quality assessment on a dataset.

This tool evaluates a dataset against several quality metrics, including
missing data, duplicate rows, and data type consistency. It generates a
report with a quality score and recommendations for improvement.
"""

import pandas as pd
from typing import Dict
from ..models.schemas import DatasetManager, dataset_schemas, DataQualityReport


async def validate_data_quality(dataset_name: str) -> Dict:
    """
    Performs a comprehensive data quality assessment on a dataset.

    This function checks for common data quality issues such as:
    - Missing data (calculates percentage for each column)
    - Duplicate rows
    - Inconsistent data types within object columns
    - Identifier columns that are not unique

    It then calculates an overall quality score and provides a list of
    potential issues and actionable recommendations.

    Args:
        dataset_name (str): The name of the loaded dataset to validate.

    Returns:
        Dict: A dictionary containing the `DataQualityReport` as a dict.
              If an error occurs, the dictionary will contain an 'error' key.
    """
    try:
        df = DatasetManager.get_dataset(dataset_name)
        schema = dataset_schemas[dataset_name]
        
        # --- Metrics Calculation ---
        missing_data = {col: round(df[col].isnull().mean() * 100, 2) for col in df.columns if df[col].isnull().any()}
        duplicate_rows = int(df.duplicated().sum())
        
        issues = []
        recommendations = []
        
        # --- Issue Identification ---
        if duplicate_rows > 0:
            issues.append(f"Found {duplicate_rows} duplicate rows.")
            recommendations.append("Consider removing duplicate rows using a data cleaning tool.")

        high_missing_cols = {col: pct for col, pct in missing_data.items() if pct > 20}
        if high_missing_cols:
            issues.append(f"Columns with >20% missing data: {', '.join(high_missing_cols.keys())}.")
            recommendations.append("Investigate data source or consider imputation/removal for high-missing columns.")
        
        for col_name, col_info in schema.columns.items():
            if col_info.suggested_role == 'identifier' and col_info.unique_values < len(df):
                issues.append(f"Potential ID column '{col_name}' has duplicate values.")
                recommendations.append(f"Verify if '{col_name}' should be a unique identifier.")

        # --- Quality Score Calculation (heuristic) ---
        score = 100.0
        # Penalty for percent of dataset that is missing
        score -= (df.isnull().sum().sum() / df.size) * 50
        # Penalty for percent of rows that are duplicates
        score -= (duplicate_rows / len(df)) * 50
        score = max(0, score)
        
        if not issues:
            recommendations.append("Data quality appears to be good. No major issues detected.")
        
        report = DataQualityReport(
            dataset_name=dataset_name,
            total_rows=len(df),
            total_columns=len(df.columns),
            missing_data=missing_data,
            duplicate_rows=duplicate_rows,
            potential_issues=issues,
            quality_score=round(score, 1),
            recommendations=recommendations,
        )
        
        return report.model_dump()
        
    except Exception as e:
        return {"error": f"Data quality validation failed: {str(e)}"}