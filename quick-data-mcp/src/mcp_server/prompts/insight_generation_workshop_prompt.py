"""
Prompt-generating function for an insight generation workshop.

This module provides a function that creates a detailed, context-aware prompt
to help a user or AI run a workshop-style analysis to derive business insights
from a dataset.
"""

from typing import Optional
from ..models.schemas import dataset_schemas


async def insight_generation_workshop(
    dataset_name: str,
    business_context: Optional[str] = "general"
) -> str:
    """
    Generates a detailed prompt to guide an insight generation workshop.

    This function creates a markdown-formatted prompt that provides a framework
    for translating data analysis into actionable business insights. It tailors
    its suggestions based on the provided business context (e.g., 'sales', 'marketing').

    Args:
        dataset_name (str): The name of the loaded dataset to analyze.
        business_context (Optional[str]): The business context for the analysis,
                                          which helps tailor the suggestions.
                                          Defaults to "general".

    Returns:
        str: A markdown-formatted string containing the guided prompt.
             Returns an error message if the dataset is not found.
    """
    try:
        if dataset_name not in dataset_schemas:
            return f"**Error**: Dataset '{dataset_name}' not found. Please load it first."
        
        schema = dataset_schemas[dataset_name]

        prompt = f"### Insight Generation Workshop for '{dataset_name}'\n\n"
        prompt += f"**Business Context:** {business_context.title()}\n\n"
        prompt += "Let's turn data into actionable insights! Here is a framework to guide our workshop.\n\n"

        prompt += "**1. Define Key Business Questions:**\n"
        prompt += f"- Based on a '{business_context}' context, what are we trying to achieve?\n"
        prompt += "- Which columns in your dataset are the most important Key Performance Indicators (KPIs)?\n\n"

        prompt += "**2. Analysis & Pattern Discovery:**\n"
        prompt += "Let's find meaningful patterns. Here are some ideas:\n"
        prompt += f"- `/suggest_analysis dataset_name:'{dataset_name}'` - Get AI-powered suggestions.\n"
        prompt += f"- `/segment_by_column ...` - Compare performance across different segments.\n"
        prompt += f"- `/find_correlations ...` - Discover unexpected relationships.\n\n"

        prompt += "**3. Synthesize & Recommend:**\n"
        prompt += "Once we find a pattern, we need to ask:\n"
        prompt += "- **So what?** Why does this pattern matter to the business?\n"
        prompt += "- **Now what?** What specific action can we take based on this insight?\n\n"

        prompt += "**Example for a 'Sales' context:**\n"
        prompt += "- **Finding:** `Sales in Region 'A' are 50% lower than in 'B'.`\n"
        prompt += "- **Insight (So what?):** `We are missing a major market opportunity in Region 'A'.`\n"
        prompt += "- **Recommendation (Now what?):** `Launch a targeted marketing campaign in Region 'A'.`\n\n"

        prompt += "**Let's begin! What is the primary goal of your analysis today?**"
        
        return prompt
        
    except Exception as e:
        return f"**Error**: An unexpected error occurred while generating the prompt: {e}"