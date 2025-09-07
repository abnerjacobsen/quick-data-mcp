"""
Prompt-generating function for a dashboard design consultation.

This module provides a function that creates a detailed, context-aware prompt
to help a user or AI design a dashboard tailored to a specific audience.
"""

from typing import Optional
from ..models.schemas import dataset_schemas


async def dashboard_design_consultation(
    dataset_name: str,
    audience: Optional[str] = "general"
) -> str:
    """
    Generates a detailed prompt to guide a dashboard design session.

    This function inspects the dataset's schema to understand the available
    data types. It then constructs a markdown-formatted string that provides
    design principles and component recommendations tailored to the specified
    audience (e.g., 'executive', 'analyst').

    Args:
        dataset_name (str): The name of the loaded dataset for the dashboard.
        audience (Optional[str]): The target audience for the dashboard.
                                  Affects the recommendations. Defaults to "general".

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
        
        prompt = f"### Dashboard Design Consultation for '{dataset_name}'\n\n"
        prompt += f"**Audience:** {audience.title()}\n\n"
        prompt += "Let's design an effective dashboard. Here's a plan based on your data and target audience.\n\n"
        
        prompt += "**1. Available Data:**\n"
        prompt += f"- **Measures (Numerical):** {len(num_cols)} columns like `{num_cols[0]}`.\n"
        prompt += f"- **Dimensions (Categorical):** {len(cat_cols)} columns like `{cat_cols[0]}`.\n\n"

        prompt += "**2. Key Questions to Answer:**\n"
        if audience == "executive":
            prompt += "- What are the top-level KPIs? How are they trending?\n"
            prompt += "- Are we meeting our goals?\n"
            prompt += "- Where are the biggest risks or opportunities?\n\n"
        else:
            prompt += f"- How does `{num_cols[0]}` vary across `{cat_cols[0]}`?\n"
            prompt += "- What are the top segments? What are the outliers?\n"
            prompt += "- Is there a relationship between different measures?\n\n"

        prompt += "**3. Suggested Charts & Workflow:**\n"
        prompt += "A good dashboard tells a story. Here's a suggested flow:\n"
        prompt += "1. **High-Level KPIs**: Start with the most important numbers.\n"
        prompt += "2. **Trend Analysis**: Show performance over time.\n"
        prompt += "3. **Segmentation**: Break down the data by key categories.\n\n"

        prompt += "**Example Commands to Build Charts:**\n"
        prompt += f"- **KPI Bar Chart**: `/create_chart dataset_name:'{dataset_name}' chart_type:'bar' x_column:'{cat_cols[0]}' y_column:'{num_cols[0]}'`\n"
        prompt += f"- **Relationship Scatter Plot**: `/create_chart dataset_name:'{dataset_name}' chart_type:'scatter' x_column:'{num_cols[0]}' y_column:'{num_cols[1] if len(num_cols)>1 else num_cols[0]}'`\n\n"
        
        prompt += "**Next Step:**\n"
        prompt += "Use the `/generate_dashboard` tool with a list of the chart configurations you design.\n"
        
        return prompt
        
    except Exception as e:
        return f"**Error**: An unexpected error occurred while generating the prompt: {e}"