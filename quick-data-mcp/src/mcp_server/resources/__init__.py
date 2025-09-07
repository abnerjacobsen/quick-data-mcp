"""
Resources Package for the Generic Data Analytics MCP Server.

This package aggregates all the individual resource functions from the
various modules in this directory. By importing them here, they can be
easily accessed from the main server file via the `resources` namespace.

These resources provide read-only access to data and metadata about the
server's state, such as loaded datasets, schema information, and system status.
"""
from .data_resources import (
    get_server_config,
    get_loaded_datasets,
    get_dataset_schema,
    get_dataset_summary,
    get_dataset_sample,
    get_current_dataset,
    get_available_analyses,
    get_column_types,
    get_analysis_suggestions,
    get_memory_usage,
    get_user_profile,
    get_system_status,
)

__all__ = [
    "get_server_config",
    "get_loaded_datasets",
    "get_dataset_schema",
    "get_dataset_summary",
    "get_dataset_sample",
    "get_current_dataset",
    "get_available_analyses",
    "get_column_types",
    "get_analysis_suggestions",
    "get_memory_usage",
    "get_user_profile",
    "get_system_status"
]