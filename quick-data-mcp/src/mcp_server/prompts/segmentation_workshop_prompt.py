"""
Prompt-generating function for a data segmentation workshop.

This module provides a function that creates a detailed, context-aware prompt
to help a user or AI plan and execute a segmentation analysis on a dataset.
"""

from ..models.schemas import dataset_schemas


async def segmentation_workshop(dataset_name: str) -> str:
    """
    Generates a detailed prompt to guide a data segmentation workshop.

    This function inspects the dataset's schema to find available categorical
    and numerical columns. It then constructs a markdown-formatted string that
    lists the potential segmentation columns and provides a step-by-step
    workflow with example tool commands.

    Args:
        dataset_name (str): The name of the loaded dataset to segment.

    Returns:
        str: A markdown-formatted string containing the guided prompt.
             Returns an error message if the dataset is not found or has no
             categorical columns for segmentation.
    """
    try:
        if dataset_name not in dataset_schemas:
            return f"**Error**: Dataset '{dataset_name}' not found. Please load it first."
        
        schema = dataset_schemas[dataset_name]
        
        cat_cols = [name for name, info in schema.columns.items() if info.suggested_role == 'categorical']
        
        if not cat_cols:
            return (f"### Segmentation Not Possible\n\n"
                    f"The **{dataset_name}** dataset has no categorical columns, "
                    f"which are needed to create segments. "
                    f"Consider creating categorical features from numerical data.")

        prompt = f"### Segmentation Workshop for '{dataset_name}'\n\n"
        prompt += "Let's break down your data into meaningful groups (segments) to find insights.\n\n"
        
        prompt += "**Available Columns for Segmentation:**\n"
        for col in cat_cols:
            prompt += f"- `{col}` ({schema.columns[col].unique_values} unique values)\n"
        
        prompt += "\n**Suggested Workflow:**\n"
        prompt += f"1. **Choose a Segment**: Pick a column from the list above that represents a meaningful grouping (e.g., region, product category).\n"
        prompt += f"2. **Run Segmentation**: Use the `/segment_by_column` tool to see how numerical data differs across these groups.\n"
        prompt += f"   - `/segment_by_column dataset_name:'{dataset_name}' column_name:'{cat_cols[0]}'`\n"
        prompt += "3. **Visualize the Segments**: Create a bar chart to easily compare the segments.\n"
        prompt += f"   - `/create_chart dataset_name:'{dataset_name}' chart_type:'bar' x_column:'{cat_cols[0]}'`\n\n"
        
        prompt += "**Which column would you like to use to segment your data?**"

        return prompt
        
    except Exception as e:
        return f"**Error**: An unexpected error occurred while generating the prompt: {e}"