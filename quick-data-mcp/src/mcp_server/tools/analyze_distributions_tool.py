"""
Tool for analyzing the statistical distribution of a dataset column.

This tool inspects a specified column and provides a detailed statistical summary.
It automatically detects whether the column is numerical or categorical and
returns the appropriate descriptive statistics.
"""

import pandas as pd
from typing import Dict
from ..models.schemas import DatasetManager


async def analyze_distributions(dataset_name: str, column_name: str) -> Dict:
    """
    Analyzes and describes the distribution of a single column in a dataset.

    For numerical columns, it calculates standard statistical measures like mean,
    median, standard deviation, quartiles, skewness, and kurtosis.

    For categorical columns, it provides frequency counts for the most common values.

    Args:
        dataset_name (str): The name of the loaded dataset to analyze.
        column_name (str): The name of the column whose distribution is to be analyzed.

    Returns:
        Dict: A dictionary containing the detailed distribution analysis. If an
              error occurs, the dictionary will contain an 'error' key.
    """
    try:
        df = DatasetManager.get_dataset(dataset_name)
        
        if column_name not in df.columns:
            return {"error": f"Column '{column_name}' not found in dataset"}
        
        series = df[column_name]
        
        result = {
            "dataset": dataset_name,
            "column": column_name,
            "dtype": str(series.dtype),
            "total_values": len(series),
            "unique_values": series.nunique(),
            "null_values": int(series.isnull().sum()),
            "null_percentage": round(series.isnull().mean() * 100, 2)
        }
        
        if pd.api.types.is_numeric_dtype(series):
            # Numerical distribution
            result.update({
                "distribution_type": "numerical",
                "mean": round(series.mean(), 3),
                "median": round(series.median(), 3),
                "std": round(series.std(), 3),
                "min": series.min(),
                "max": series.max(),
                "quartiles": {
                    "q25": round(series.quantile(0.25), 3),
                    "q50": round(series.quantile(0.50), 3),
                    "q75": round(series.quantile(0.75), 3)
                },
                "skewness": round(series.skew(), 3),
                "kurtosis": round(series.kurtosis(), 3)
            })
        else:
            # Categorical distribution
            value_counts = series.value_counts().head(10)
            result.update({
                "distribution_type": "categorical",
                "most_frequent": value_counts.index[0] if len(value_counts) > 0 else None,
                "frequency_of_most_common": int(value_counts.iloc[0]) if len(value_counts) > 0 else 0,
                "top_10_values": {str(k): int(v) for k, v in value_counts.to_dict().items()}
            })
        
        return result
        
    except Exception as e:
        return {"error": f"Distribution analysis failed: {str(e)}"}