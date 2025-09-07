"""
Tool for segmenting a dataset based on the values in a specified column.

This tool groups a dataset by a categorical column and calculates aggregate
statistics for the numerical columns within each segment.
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from ..models.schemas import DatasetManager


async def segment_by_column(
    dataset_name: str, 
    column_name: str, 
    top_n: int = 10
) -> Dict:
    """
    Segments a dataset by a column and calculates aggregate statistics.

    This function groups the dataset by the unique values in the `column_name`.
    For each group (segment), it calculates the count, mean, sum, and standard
    deviation for all available numerical columns.

    Args:
        dataset_name (str): The name of the loaded dataset to segment.
        column_name (str): The name of the categorical column to group by.
        top_n (int): The maximum number of segments (top by count) to return.
                     Defaults to 10.

    Returns:
        Dict: A dictionary containing the segmentation results, with aggregate
              statistics for each segment. If an error occurs, the dictionary
              will contain an 'error' key.
    """
    try:
        df = DatasetManager.get_dataset(dataset_name)
        
        if column_name not in df.columns:
            return {"error": f"Column '{column_name}' not found in dataset '{dataset_name}'."}
        
        if df[column_name].nunique() > 100:
            return {"error": f"Column '{column_name}' has too many unique values (>100) for effective segmentation."}

        # First, get the top N segments by count
        top_segments = df[column_name].value_counts().nlargest(top_n).index
        df_filtered = df[df[column_name].isin(top_segments)]

        numerical_cols = df_filtered.select_dtypes(include=np.number).columns.tolist()
        
        if not numerical_cols:
            # If no numerical columns, just perform a value count
            segments = df_filtered[column_name].value_counts().to_frame('count')
        else:
            # Define aggregations for numerical columns
            agg_dict = {col: ['mean', 'sum', 'std'] for col in numerical_cols}
            agg_dict['count'] = (column_name, 'size') # Add count of items in each group

            segments = df_filtered.groupby(column_name).agg(agg_dict)
            segments.columns = ['_'.join(col).strip() for col in segments.columns.values]
            segments.rename(columns={f"{column_name}_size": "count"}, inplace=True)

        segments = segments.sort_values('count', ascending=False)
        segments['percentage_of_total'] = (segments['count'] / len(df) * 100).round(2)
        
        return {
            "dataset": dataset_name,
            "segmented_by": column_name,
            "segment_count": len(segments),
            "segments": segments.to_dict('index'),
        }
        
    except Exception as e:
        return {"error": f"Segmentation failed: {str(e)}"}