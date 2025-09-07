"""
Tool for suggesting relevant analyses based on dataset characteristics.

This tool inspects the schema of a loaded dataset and recommends appropriate
analysis tools to use based on the types of columns available (e.g., suggesting
correlation analysis if there are numerical columns).
"""

from typing import Dict
from ..models.schemas import dataset_schemas


async def suggest_analysis(dataset_name: str) -> Dict:
    """
    Suggests relevant analysis tools based on the dataset's schema.

    This function analyzes the column types and other metadata from the dataset's
    schema to generate a prioritized list of suggested analysis tools. Each suggestion
    includes a description, the relevant columns, and an example command.

    Args:
        dataset_name (str): The name of the loaded dataset for which to generate
                            suggestions.

    Returns:
        Dict: A dictionary containing a list of analysis suggestions. If an
              error occurs, the dictionary will contain an 'error' key.
    """
    try:
        if dataset_name not in dataset_schemas:
            return {"error": f"Schema for dataset '{dataset_name}' not found. Please load it first."}
            
        schema = dataset_schemas[dataset_name]
        
        num_cols = [c.name for c in schema.columns.values() if c.suggested_role == 'numerical']
        cat_cols = [c.name for c in schema.columns.values() if c.suggested_role == 'categorical']
        time_cols = [c.name for c in schema.columns.values() if c.suggested_role == 'temporal']
        
        suggestions = []
        
        if len(num_cols) >= 2:
            suggestions.append({
                "priority": "high", "type": "correlation",
                "description": f"Find relationships between the {len(num_cols)} numerical columns.",
                "tool_command": f"/find_correlations dataset_name:'{dataset_name}'"
            })
        
        if cat_cols and num_cols:
            suggestions.append({
                "priority": "high", "type": "segmentation",
                "description": f"Segment data by '{cat_cols[0]}' to analyze numerical trends.",
                "tool_command": f"/segment_by_column dataset_name:'{dataset_name}' column_name:'{cat_cols[0]}'"
            })
        
        if time_cols and num_cols:
            suggestions.append({
                "priority": "medium", "type": "time_series",
                "description": f"Analyze trends over time using '{time_cols[0]}' and '{num_cols[0]}'.",
                "tool_command": f"/time_series_analysis dataset_name:'{dataset_name}' date_column:'{time_cols[0]}' value_column:'{num_cols[0]}'"
            })

        if num_cols:
            suggestions.append({
                "priority": "medium", "type": "distribution_analysis",
                "description": f"Explore the distribution of numerical column '{num_cols[0]}'.",
                "tool_command": f"/analyze_distributions dataset_name:'{dataset_name}' column_name:'{num_cols[0]}'"
            })
            suggestions.append({
                "priority": "low", "type": "outlier_detection",
                "description": f"Check for outliers in the {len(num_cols)} numerical columns.",
                "tool_command": f"/detect_outliers dataset_name:'{dataset_name}'"
            })

        suggestions.append({
            "priority": "low", "type": "data_quality",
            "description": "Get a comprehensive data quality report.",
            "tool_command": f"/validate_data_quality dataset_name:'{dataset_name}'"
        })
        
        return {
            "dataset_name": dataset_name,
            "suggestions": suggestions,
        }
        
    except Exception as e:
        return {"error": f"Analysis suggestion failed: {str(e)}"}