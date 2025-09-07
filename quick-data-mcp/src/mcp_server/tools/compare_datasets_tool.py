"""
Tool for comparing two datasets side-by-side.

This tool provides a comparative analysis of two loaded datasets, focusing on
their shapes and the statistical properties of their common columns.
"""

import pandas as pd
from typing import List, Dict, Optional
from ..models.schemas import DatasetManager


async def compare_datasets(
    dataset_a: str,
    dataset_b: str,
    common_columns: Optional[List[str]] = None
) -> Dict:
    """
    Performs a side-by-side comparison of two datasets.

    The comparison includes a look at the shapes (rows, columns) of both
    datasets and a detailed statistical comparison of their common columns.
    For numerical columns, it compares means and standard deviations. For all
    common columns, it compares data types, unique value counts, and null percentages.

    Args:
        dataset_a (str): The name of the first loaded dataset.
        dataset_b (str): The name of the second loaded dataset.
        common_columns (Optional[List[str]]): A list of columns to compare.
            If None, the intersection of columns from both datasets will be used.

    Returns:
        Dict: A dictionary containing the detailed comparison report. If an
              error occurs, the dictionary will contain an 'error' key.
    """
    try:
        df_a = DatasetManager.get_dataset(dataset_a)
        df_b = DatasetManager.get_dataset(dataset_b)
        
        # Find common columns if not specified
        if common_columns is None:
            common_columns = list(set(df_a.columns) & set(df_b.columns))
        
        if not common_columns:
            return {"error": "No common columns found between datasets to compare."}
        
        comparison = {
            "dataset_a": dataset_a,
            "dataset_b": dataset_b,
            "shape_comparison": {
                "dataset_a_shape": df_a.shape,
                "dataset_b_shape": df_b.shape,
                "row_difference": df_a.shape[0] - df_b.shape[0],
                "column_difference": df_a.shape[1] - df_b.shape[1]
            },
            "common_columns": common_columns,
            "column_comparisons": {}
        }
        
        # Compare each common column
        for col in common_columns:
            col_comparison = {
                "column": col,
                "dtype_a": str(df_a[col].dtype),
                "dtype_b": str(df_b[col].dtype),
                "unique_values_a": int(df_a[col].nunique()),
                "unique_values_b": int(df_b[col].nunique()),
                "null_pct_a": round(df_a[col].isnull().mean() * 100, 2),
                "null_pct_b": round(df_b[col].isnull().mean() * 100, 2)
            }
            
            # Numerical comparison
            if pd.api.types.is_numeric_dtype(df_a[col]) and pd.api.types.is_numeric_dtype(df_b[col]):
                col_comparison.update({
                    "mean_a": round(df_a[col].mean(), 3),
                    "mean_b": round(df_b[col].mean(), 3),
                    "mean_difference": round(df_a[col].mean() - df_b[col].mean(), 3),
                    "std_a": round(df_a[col].std(), 3),
                    "std_b": round(df_b[col].std(), 3)
                })
            
            comparison["column_comparisons"][col] = col_comparison
        
        return comparison
        
    except Exception as e:
        return {"error": f"Dataset comparison failed: {str(e)}"}