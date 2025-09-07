"""
Tool for performing time series analysis on a dataset.

This tool analyzes a dataset with a date/time column, resampling the data to a
specified frequency and calculating basic trend and statistical information.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional
from ..models.schemas import DatasetManager


async def time_series_analysis(
    dataset_name: str, 
    date_column: str, 
    value_column: str,
    frequency: Optional[str] = "auto"
) -> Dict:
    """
    Performs a basic time series analysis on a given dataset.

    This function converts the date column to datetime objects, resamples the
    data to a specified or automatically determined frequency (daily, weekly,
    or monthly), and then calculates trend and descriptive statistics.

    Args:
        dataset_name (str): The name of the loaded dataset.
        date_column (str): The name of the column containing date/time information.
        value_column (str): The name of the numerical column to be analyzed over time.
        frequency (str): The frequency to resample the data to. Can be 'D' (daily),
                         'W' (weekly), 'M' (monthly), or 'auto'. Defaults to 'auto'.

    Returns:
        Dict: A dictionary containing the time series analysis results, including
              date range, trend, and statistics. If an error occurs, the
              dictionary will contain an 'error' key.
    """
    try:
        df = DatasetManager.get_dataset(dataset_name).copy()
        
        if date_column not in df.columns or value_column not in df.columns:
            return {"error": f"One or both specified columns not found in dataset."}
        
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
        df.dropna(subset=[date_column, value_column], inplace=True)
        
        if not pd.api.types.is_numeric_dtype(df[value_column]):
            return {"error": f"Value column '{value_column}' must be numerical."}

        df = df.sort_values(date_column).set_index(date_column)
        
        date_range = df.index.max() - df.index.min()
        
        if frequency == "auto":
            freq = 'M' if date_range.days > 365 else 'W' if date_range.days > 30 else 'D'
        else:
            freq = frequency
        
        ts_resampled = df[value_column].resample(freq).mean().dropna()
        
        if len(ts_resampled) < 2:
            return {"error": "Not enough data points to perform time series analysis after resampling."}

        # Simple linear trend
        x = np.arange(len(ts_resampled))
        y = ts_resampled.values
        slope, _ = np.polyfit(x, y, 1)
        
        return {
            "dataset": dataset_name,
            "time_series_summary": {
                "date_column": date_column,
                "value_column": value_column,
                "frequency": freq,
                "date_range_days": date_range.days,
                "data_points": len(ts_resampled),
            },
            "trend": {
                "slope": round(slope, 4),
                "direction": "increasing" if slope > 0.001 else "decreasing" if slope < -0.001 else "stable",
            },
            "statistics": ts_resampled.describe().round(4).to_dict(),
        }
        
    except Exception as e:
        return {"error": f"Time series analysis failed: {str(e)}"}