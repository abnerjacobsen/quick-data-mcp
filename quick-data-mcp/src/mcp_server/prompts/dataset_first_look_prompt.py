"""
Prompt-generating function for providing an initial overview of a dataset.

This module provides a function that creates a detailed, context-aware prompt
to give a user or AI a "first look" at a newly loaded dataset, guiding them
on how to start their analysis.
"""

from ..models.schemas import dataset_schemas


async def dataset_first_look(dataset_name: str) -> str:
    """
    Generates an adaptive "first look" prompt for a dataset.

    This function inspects the dataset's schema to identify the types of
    columns available (numerical, categorical, etc.). It then constructs a
    markdown-formatted string that summarizes the dataset's structure and
    provides tailored recommendations and example commands for starting an analysis.

    Args:
        dataset_name (str): The name of the loaded dataset to analyze.

    Returns:
        str: A markdown-formatted string containing the guided prompt.
             Returns an error message if the dataset is not found.
    """
    try:
        if dataset_name not in dataset_schemas:
            return f"**Error**: Dataset '{dataset_name}' not found. Please load it first."
        
        schema = dataset_schemas[dataset_name]
        
        num_cols = [name for name, info in schema.columns.items() if info.suggested_role == 'numerical']
        cat_cols = [name for name, info in schema.columns.items() if info.suggested_role == 'categorical']
        
        prompt = f"### First Look at '{dataset_name}'\n\n"
        prompt += f"I've loaded your dataset! It has **{schema.row_count:,} rows** and **{len(schema.columns)} columns**.\n\n"
        
        prompt += "**Column Types:**\n"
        prompt += f"- **Numerical ({len(num_cols)}):** `{', '.join(num_cols)}`\n"
        prompt += f"- **Categorical ({len(cat_cols)}):** `{', '.join(cat_cols)}`\n\n"
        
        prompt += "**Recommended Starting Points:**\n"
        
        if len(num_cols) >= 2:
            prompt += f"- **Explore Relationships**: See how numerical columns relate.\n"
            prompt += f"  - `/find_correlations dataset_name:'{dataset_name}'`\n"
        
        if cat_cols and num_cols:
            prompt += f"- **Segment Your Data**: Analyze `{num_cols[0]}` across different categories of `{cat_cols[0]}`.\n"
            prompt += f"  - `/segment_by_column dataset_name:'{dataset_name}' column_name:'{cat_cols[0]}'`\n"
        
        prompt += f"- **Check Data Quality**: Get a report on missing data and other issues.\n"
        prompt += f"  - `/validate_data_quality dataset_name:'{dataset_name}'`\n\n"

        prompt += "**What would you like to investigate first?**"
        
        return prompt
        
    except Exception as e:
        return f"**Error**: An unexpected error occurred while generating the prompt: {e}"