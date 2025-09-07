"""
Prompt-generating function for a pattern discovery session.

This module provides a function that creates a detailed, context-aware prompt
to help a user or AI run an open-ended exploratory analysis to find interesting
patterns in a dataset.
"""

from ..models.schemas import dataset_schemas


async def pattern_discovery_session(dataset_name: str) -> str:
    """
    Generates a detailed prompt to guide a pattern discovery session.

    This function inspects the dataset's schema and generates a markdown-formatted
    prompt that outlines different types of pattern analysis (e.g., distribution,
    segmentation, temporal) and provides relevant tool commands to begin
    the exploration.

    Args:
        dataset_name (str): The name of the loaded dataset to explore.

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

        prompt = f"### Pattern Discovery Session for '{dataset_name}'\n\n"
        prompt += "Let's uncover hidden patterns in your data. Here are some avenues for exploration:\n\n"

        prompt += "**1. Distribution Patterns (Shape of your data):**\n"
        prompt += "- Look for skewed distributions, multiple peaks, or gaps.\n"
        prompt += f"- **Tool**: `/analyze_distributions dataset_name:'{dataset_name}' column_name:'{num_cols[0]}'`\n\n"

        prompt += "**2. Relationship Patterns (How variables interact):**\n"
        prompt += "- Find strong correlations between numerical variables.\n"
        prompt += f"- **Tool**: `/find_correlations dataset_name:'{dataset_name}'`\n\n"

        prompt += "**3. Segmentation Patterns (Hidden groups):**\n"
        prompt += f"- Discover how numerical data behaves across different categories of `{cat_cols[0]}`.\n"
        prompt += f"- **Tool**: `/segment_by_column dataset_name:'{dataset_name}' column_name:'{cat_cols[0]}'`\n\n"
        
        prompt += "**Where would you like to start your search for patterns?**"

        return prompt
        
    except Exception as e:
        return f"**Error**: An unexpected error occurred while generating the prompt: {e}"