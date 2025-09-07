"""
Tool for finding and analyzing correlations between numerical columns.

This tool calculates the Pearson correlation coefficient for all pairs of
numerical columns in a dataset. It provides the full correlation matrix and
also highlights pairs of columns with correlations exceeding a given threshold.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from ..models.schemas import DatasetManager


async def find_correlations(
    dataset_name: str, 
    columns: Optional[List[str]] = None,
    threshold: float = 0.3
) -> Dict:
    """
    Finds correlations between numerical columns in a dataset.

    This function computes a correlation matrix for the specified numerical
    columns. It also identifies and lists "strong" correlations (absolute
    value above the threshold) for easier interpretation.

    Args:
        dataset_name (str): The name of the loaded dataset to analyze.
        columns (Optional[List[str]]): A list of numerical columns to include
                                       in the correlation analysis. If None,
                                       all numerical columns are used.
        threshold (float): The minimum absolute correlation value to be
                           considered a "strong" correlation. Defaults to 0.3.

    Returns:
        Dict: A dictionary containing the full correlation matrix and a list
              of strong correlations. If an error occurs, the dictionary
              will contain an 'error' key.
    """
    try:
        df = DatasetManager.get_dataset(dataset_name)
        
        if columns is None:
            columns = df.select_dtypes(include=np.number).columns.tolist()
        
        if len(columns) < 2:
            return {"error": "Correlation analysis requires at least two numerical columns."}
        
        existing_columns = [col for col in columns if col in df.columns and pd.api.types.is_numeric_dtype(df[col])]
        if len(existing_columns) < 2:
            return {"error": f"Fewer than two existing numerical columns found for analysis."}
        
        corr_matrix = df[existing_columns].corr(numeric_only=True)
        
        # Find pairs with correlation above the threshold
        strong_correlations = []
        # Unstack the matrix to get a series of pairs, then filter
        corr_pairs = corr_matrix.unstack()
        # Remove self-correlations
        corr_pairs = corr_pairs[corr_pairs.index.get_level_values(0) != corr_pairs.index.get_level_values(1)]
        # Filter by threshold
        strong_pairs = corr_pairs[abs(corr_pairs) > threshold].drop_duplicates()

        for (col1, col2), corr_value in strong_pairs.items():
            strength = "strong" if abs(corr_value) > 0.7 else "moderate"
            direction = "positive" if corr_value > 0 else "negative"
            strong_correlations.append({
                "column_1": col1,
                "column_2": col2,
                "correlation": round(corr_value, 4),
                "strength": strength,
                "direction": direction,
            })
        
        # Sort by absolute correlation value
        strong_correlations.sort(key=lambda x: abs(x["correlation"]), reverse=True)
        
        return {
            "dataset": dataset_name,
            "correlation_matrix": {k: v.to_dict() for k, v in corr_matrix.to_dict().items()},
            "strong_correlations": strong_correlations,
            "columns_analyzed": existing_columns,
            "threshold": threshold
        }
        
    except Exception as e:
        return {"error": f"Correlation analysis failed: {str(e)}"}