"""
Tools Package for the Generic Data Analytics MCP Server.

This package aggregates all the individual analytics and data manipulation tools
from the various modules in this directory. By importing them here, they can be
easily accessed from the main server file via the `tools` namespace.

The tools are organized into logical groups:
- Analytics Tools: High-level analyses and data quality checks.
- Pandas Tools: Core data manipulation, loading, and exploration functions
  powered by the pandas library.
"""

# Import modules for grouped access
from . import pandas_tools

# Analytics tools
from .validate_data_quality_tool import validate_data_quality
from .compare_datasets_tool import compare_datasets
from .merge_datasets_tool import merge_datasets
from .generate_dashboard_tool import generate_dashboard
from .export_insights_tool import export_insights
from .calculate_feature_importance_tool import calculate_feature_importance
from .memory_optimization_report_tool import memory_optimization_report
from .execute_custom_analytics_code_tool import execute_custom_analytics_code

# Pandas tools
from .load_dataset_tool import load_dataset
from .list_loaded_datasets_tool import list_loaded_datasets
from .segment_by_column_tool import segment_by_column
from .find_correlations_tool import find_correlations
from .create_chart_tool import create_chart
from .analyze_distributions_tool import analyze_distributions
from .detect_outliers_tool import detect_outliers
from .time_series_analysis_tool import time_series_analysis
from .suggest_analysis_tool import suggest_analysis

__all__ = [
    # Modules
    "pandas_tools",
    
    # Analytics tools
    "validate_data_quality",
    "compare_datasets",
    "merge_datasets",
    "generate_dashboard",
    "export_insights",
    "calculate_feature_importance",
    "memory_optimization_report",
    "execute_custom_analytics_code",
    
    # Pandas tools
    "load_dataset",
    "list_loaded_datasets",
    "segment_by_column",
    "find_correlations",
    "create_chart",
    "analyze_distributions",
    "detect_outliers",
    "time_series_analysis",
    "suggest_analysis"
]