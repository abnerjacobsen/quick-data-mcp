"""
Prompt-generating function that lists all available server assets.

This module provides a function that returns a static, formatted string
listing all the prompts, tools, and resources available on the server.
"""

# Note: In a more advanced implementation, this list could be generated
# dynamically by introspecting the MCP server object to prevent it from
# becoming outdated.

async def list_mcp_assets() -> str:
    """
    Returns a comprehensive, formatted list of all server capabilities.

    This function provides a static but detailed list of all available prompts,
    tools (organized by category), and resources. It serves as a handy reference
    for users to understand the full scope of what the server can do.

    Returns:
        str: A markdown-formatted string listing all server assets.
    """
    return \"\"\"
# 🚀 Quick-Data MCP Server Assets

This is a complete list of all available prompts, tools, and resources.

## 📝 Prompts
*Interactive conversation starters and analysis guides.*

- **/dataset_first_look** `(dataset_name)`: Initial exploration guide for a new dataset.
- **/segmentation_workshop** `(dataset_name)`: Plan a segmentation strategy.
- **/data_quality_assessment** `(dataset_name)`: Start a data quality review.
- **/correlation_investigation** `(dataset_name)`: Guide a correlation analysis.
- **/insight_generation_workshop** `(dataset_name, business_context)`: Generate business insights.
- **/dashboard_design_consultation** `(dataset_name, audience)`: Plan a dashboard.
- **/find_datasources** `(directory_path)`: Discover data files in your project.
- **/list_mcp_assets**: You are here!

## 🔧 Tools
*Functions for data analysis and manipulation.*

### Data Management
- **/load_dataset** `(file_path, dataset_name)`: Load a JSON/CSV dataset.
- **/list_loaded_datasets**: Show all datasets in memory.
- **/clear_dataset** `(dataset_name)`: Remove a specific dataset from memory.
- **/clear_all_datasets**: Clear all datasets from memory.

### Core Analytics
- **/suggest_analysis** `(dataset_name)`: Get AI-powered analysis recommendations.
- **/analyze_distributions** `(dataset_name, column_name)`: Analyze a column's distribution.
- **/find_correlations** `(dataset_name)`: Find correlations between numerical columns.
- **/segment_by_column** `(dataset_name, column_name)`: Segment data by a categorical column.
- **/detect_outliers** `(dataset_name)`: Detect outliers in numerical columns.
- **/time_series_analysis** `(dataset_name, date_column, value_column)`: Analyze trends over time.
- **/validate_data_quality** `(dataset_name)`: Get a comprehensive data quality report.

### Advanced Operations
- **/compare_datasets** `(dataset_a, dataset_b)`: Compare two datasets.
- **/merge_datasets** `(dataset_configs)`: Join multiple datasets.
- **/calculate_feature_importance** `(dataset_name, target_column)`: Calculate feature importance.
- **/memory_optimization_report** `(dataset_name)`: Get memory usage optimization tips.
- **/execute_custom_analytics_code** `(dataset_name, python_code)`: Run custom Python code.

### Input/Output
- **/create_chart** `(dataset_name, ...)`: Create a chart and save it as HTML.
- **/generate_dashboard** `(dataset_name, ...)`: Create multiple charts for a dashboard.
- **/export_insights** `(dataset_name, format)`: Export an analysis report.

## 📊 Resources
*Read-only endpoints for real-time data and metadata.*

- `datasets://loaded`: List of all loaded datasets.
- `datasets://{dataset_name}/schema`: The schema of a specific dataset.
- `datasets://{dataset_name}/summary`: Statistical summary of a dataset.
- `analytics://available_analyses`: List of analyses applicable to the current dataset.
\"\"\"