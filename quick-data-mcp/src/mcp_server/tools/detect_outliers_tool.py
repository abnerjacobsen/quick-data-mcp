"""
Tool for detecting outliers in numerical columns of a dataset.

This tool provides methods for identifying outliers in a dataset, which are
data points that differ significantly from other observations. It supports
two common detection methods: IQR (Interquartile Range) and Z-score.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from ..models.schemas import DatasetManager


async def detect_outliers(
    dataset_name: str, 
    columns: Optional[List[str]] = None,
    method: str = "iqr"
) -> Dict:
    """
    Detects outliers in numerical columns using configurable methods.

    This function can use either the Interquartile Range (IQR) method or the
    Z-score method to identify outliers. If no columns are specified, it will
    analyze all numerical columns in the dataset.

    Args:
        dataset_name (str): The name of the loaded dataset to analyze.
        columns (Optional[List[str]]): A list of numerical columns to check for
                                       outliers. If None, all numerical columns
                                       are used.
        method (str): The method to use for outlier detection. Supported methods
                      are 'iqr' (default) and 'zscore'.

    Returns:
        Dict: A dictionary containing a detailed report of the detected outliers
              for each column. If an error occurs, the dictionary will contain
              an 'error' key.
    """
    try:
        df = DatasetManager.get_dataset(dataset_name)
        
        if columns is None:
            columns = df.select_dtypes(include=np.number).columns.tolist()
        
        if not columns:
            return {"error": "No numerical columns found or specified for outlier detection."}
        
        existing_columns = [col for col in columns if col in df.columns and pd.api.types.is_numeric_dtype(df[col])]
        if not existing_columns:
            return {"error": "None of the specified columns are numerical or found in the dataset."}

        outliers_info = {}
        total_outliers = 0
        
        for col in existing_columns:
            series = df[col].dropna()
            
            if method == "iqr":
                Q1 = series.quantile(0.25)
                Q3 = series.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = series[(series < lower_bound) | (series > upper_bound)]
                
            elif method == "zscore":
                mean = series.mean()
                std = series.std()
                if std == 0: # Avoid division by zero for constant columns
                    outliers = pd.Series(dtype=series.dtype)
                    lower_bound, upper_bound = mean, mean
                else:
                    z_scores = np.abs((series - mean) / std)
                    outliers = series[z_scores > 3]
                    lower_bound = mean - 3 * std
                    upper_bound = mean + 3 * std
                
            else:
                return {"error": f"Unsupported method: '{method}'. Use 'iqr' or 'zscore'."}
            
            outlier_count = len(outliers)
            total_outliers += outlier_count
            
            outliers_info[col] = {
                "outlier_count": outlier_count,
                "outlier_percentage": round(outlier_count / len(df[col]) * 100, 2) if len(df[col]) > 0 else 0,
                "lower_bound": round(lower_bound, 4),
                "upper_bound": round(upper_bound, 4),
                "outlier_values": [round(v, 4) for v in outliers.head(10).tolist()],
                "method": method
            }
        
        return {
            "dataset": dataset_name,
            "method": method,
            "columns_analyzed": existing_columns,
            "total_outliers": total_outliers,
            "outliers_by_column": outliers_info
        }
        
    except Exception as e:
        return {"error": f"Outlier detection failed: {str(e)}"}