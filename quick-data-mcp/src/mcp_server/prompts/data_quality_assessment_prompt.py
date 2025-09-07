"""
Prompt-generating function for a data quality assessment workflow.

This module provides a function that creates a detailed, context-aware prompt
to help a user or AI systematically review the data quality of a dataset.
"""

from ..models.schemas import DatasetManager, dataset_schemas


async def data_quality_assessment(dataset_name: str) -> str:
    """
    Generates a detailed prompt to guide a data quality assessment.

    This function inspects the dataset's schema and a sample of the data to
    highlight potential quality issues like missing values, inconsistent data
    types, and cardinality concerns. It then suggests a workflow with example
    tool commands to perform a comprehensive quality check.

    Args:
        dataset_name (str): The name of the loaded dataset to assess.

    Returns:
        str: A markdown-formatted string containing the guided prompt.
             Returns an error message if the dataset is not found.
    """
    try:
        if dataset_name not in dataset_schemas:
            return f"**Error**: Dataset '{dataset_name}' not found. Please load it first."
        
        schema = dataset_schemas[dataset_name]
        df = DatasetManager.get_dataset(dataset_name)

        prompt = f"### Data Quality Assessment for '{dataset_name}'\n\n"
        prompt += f"Let's review the quality of your dataset ({schema.row_count:,} rows).\n\n"

        # Missing Values
        missing_pct = df.isnull().sum().sum() / df.size * 100
        prompt += f"**1. Completeness:**\n"
        prompt += f"- Overall, your dataset is **{100-missing_pct:.1f}%** complete.\n"
        if missing_pct > 0:
            prompt += f"- Top columns with missing data: `{(df.isnull().sum().sort_values(ascending=False).index[0])}`.\n\n"
        else:
            prompt += "- No missing values found. Excellent!\n\n"

        # Duplicates
        dup_rows = df.duplicated().sum()
        prompt += f"**2. Uniqueness:**\n"
        if dup_rows > 0:
            prompt += f"- Found **{dup_rows} duplicate rows** ({dup_rows/len(df):.1%}).\n\n"
        else:
            prompt += "- No duplicate rows found. Great!\n\n"

        prompt += "**Suggested Workflow:**\n"
        prompt += "1. **Run Full Report**: Get a detailed quality score and breakdown.\n"
        prompt += f"   - `/validate_data_quality dataset_name:'{dataset_name}'`\n"
        prompt += "2. **Check for Outliers**: Identify unusual data points in numerical columns.\n"
        prompt += f"   - `/detect_outliers dataset_name:'{dataset_name}'`\n"
        prompt += "3. **Investigate Distributions**: Understand the shape of your data.\n"
        prompt += f"   - `/analyze_distributions dataset_name:'{dataset_name}' column_name:'COLUMN_NAME'`\n\n"
        
        prompt += "**Next Step:**\n"
        prompt += "Start with the full report to get a comprehensive list of issues and recommendations."

        return prompt
        
    except Exception as e:
        return f"**Error**: An unexpected error occurred while generating the prompt: {e}"