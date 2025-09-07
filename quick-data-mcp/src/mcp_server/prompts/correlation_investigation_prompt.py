"""
Prompt-generating function for guiding a correlation investigation workflow.

This module provides a function that creates a detailed, context-aware prompt
to help a user or AI explore correlations within a specified dataset.
"""

from ..models.schemas import dataset_schemas


async def correlation_investigation(dataset_name: str) -> str:
    """
    Generates a detailed prompt to guide a correlation analysis workflow.

    This function inspects the dataset's schema to find available numerical
    columns. It then constructs a markdown-formatted string that explains what
    correlation analysis is, lists the available columns, and suggests a
    step-by-step strategy with example tool commands.

    Args:
        dataset_name (str): The name of the loaded dataset to investigate.

    Returns:
        str: A markdown-formatted string containing the guided prompt.
             Returns an error message if the dataset is not found or has
             insufficient numerical data.
    """
    try:
        if dataset_name not in dataset_schemas:
            return f"**Error**: Dataset '{dataset_name}' not found. Please load it first."
        
        schema = dataset_schemas[dataset_name]
        numerical_cols = [name for name, info in schema.columns.items() if info.suggested_role == 'numerical']
        
        if len(numerical_cols) < 2:
            return (f"### Correlation Analysis Not Possible\n\n"
                    f"The **{dataset_name}** dataset has fewer than two numerical columns, "
                    f"which are required for correlation analysis.")

        prompt = f"### Correlation Investigation for '{dataset_name}'\n\n"
        prompt += "Let's explore the relationships between numerical variables in your dataset.\n\n"
        prompt += "**Available Numerical Columns:**\n"
        for col in numerical_cols:
            prompt += f"- `{col}`\n"

        prompt += "\n**Suggested Workflow:**\n"
        prompt += "1. **Overall Correlation Matrix**: Get a complete overview of all correlations.\n"
        prompt += f"   - `/find_correlations dataset_name:'{dataset_name}'`\n"
        prompt += "2. **Visualize Strongest Pairs**: Create scatter plots for interesting pairs.\n"
        prompt += f"   - `/create_chart dataset_name:'{dataset_name}' chart_type:'scatter' "
        prompt += f"x_column:'{numerical_cols[0]}' y_column:'{numerical_cols[1]}'`\n"
        prompt += "3. **Deeper Dive**: Analyze distributions of highly correlated variables.\n"
        prompt += f"   - `/analyze_distributions dataset_name:'{dataset_name}' column_name:'{numerical_cols[0]}'`\n\n"
        prompt += "**Key Concepts:**\n"
        prompt += "- **Correlation Coefficient**: A value between -1 and 1. "
        prompt += "`1` is total positive correlation, `-1` is total negative, and `0` is no correlation.\n"
        prompt += "- **Correlation vs. Causation**: Remember that a strong correlation does not imply one variable causes the other.\n"

        return prompt
        
    except Exception as e:
        return f"**Error**: An unexpected error occurred while generating the prompt: {e}"