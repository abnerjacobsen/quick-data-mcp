"""
Tool for analyzing dataset memory usage and suggesting optimizations.

This tool inspects the data types of each column in a DataFrame and provides
recommendations for converting them to more memory-efficient types, such as
downcasting integers and floats or converting strings to categoricals.
"""

import pandas as pd
import numpy as np
from typing import Dict
from ..models.schemas import DatasetManager


async def memory_optimization_report(dataset_name: str) -> Dict:
    """
    Analyzes memory usage of a dataset and suggests optimizations.

    This function calculates the current memory footprint of the dataset and
    then checks each column for potential optimizations. It suggests converting
    object columns with low cardinality to 'category', and downcasting 'int64'
    and 'float64' columns to smaller types where possible without data loss.

    Args:
        dataset_name (str): The name of the loaded dataset to analyze.

    Returns:
        Dict: A dictionary containing a detailed report with current memory usage,
              a list of specific optimization suggestions, and the total potential
              memory savings. If an error occurs, the dictionary will contain an
              'error' key.
    """
    try:
        df = DatasetManager.get_dataset(dataset_name)
        
        memory_usage = df.memory_usage(deep=True)
        total_memory = memory_usage.sum()
        
        suggestions = []
        total_potential_savings = 0
        
        for col in df.columns:
            col_mem = memory_usage[col]
            dtype = df[col].dtype
            
            # Suggest converting object to category for low-cardinality strings
            if dtype == 'object':
                if df[col].nunique() / len(df) < 0.5:
                    optimized_mem = df[col].astype('category').memory_usage(deep=True)
                    savings = col_mem - optimized_mem
                    if savings > 0:
                        suggestions.append({
                            "column": col, "suggestion": "Convert to 'category'",
                            "savings_kb": round(savings / 1024, 2)
                        })
                        total_potential_savings += savings

            # Suggest downcasting numerical types
            elif np.issubdtype(dtype, np.integer):
                new_type = pd.to_numeric(df[col], downcast='integer')
                if new_type.dtype != dtype:
                    optimized_mem = df[col].astype(new_type.dtype).memory_usage(deep=True)
                    savings = col_mem - optimized_mem
                    if savings > 0:
                        suggestions.append({
                            "column": col, "suggestion": f"Downcast to '{new_type.dtype}'",
                            "savings_kb": round(savings / 1024, 2)
                        })
                        total_potential_savings += savings
            
            elif np.issubdtype(dtype, np.floating):
                new_type = pd.to_numeric(df[col], downcast='float')
                if new_type.dtype != dtype:
                    optimized_mem = df[col].astype(new_type.dtype).memory_usage(deep=True)
                    savings = col_mem - optimized_mem
                    if savings > 0:
                        suggestions.append({
                            "column": col, "suggestion": f"Downcast to '{new_type.dtype}'",
                            "savings_kb": round(savings / 1024, 2)
                        })
                        total_potential_savings += savings

        return {
            "dataset": dataset_name,
            "current_memory_mb": round(total_memory / 1024**2, 2),
            "potential_savings_mb": round(total_potential_savings / 1024**2, 2),
            "potential_savings_pct": round(total_potential_savings / total_memory * 100, 2) if total_memory > 0 else 0,
            "optimization_suggestions": suggestions,
        }
        
    except Exception as e:
        return {"error": f"Memory optimization analysis failed: {str(e)}"}