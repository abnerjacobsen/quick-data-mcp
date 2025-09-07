"""
Main MCP Server Definition for the Generic Data Analytics Tool.

This script initializes the FastMCP server and registers all the analytics
tools, data resources, and guided prompts that form the server's capabilities.
It acts as the central integration point, importing functionality from the
`tools`, `resources`, and `prompts` packages and exposing them through the
MCP instance.

The server is configured to be stateless over HTTP, making it scalable and
robust. For detailed information on specific tools, resources, or prompts,
refer to the documentation within their respective implementation files.
"""

from fastmcp import FastMCP
from .config.settings import settings
from . import tools
from . import resources
from . import prompts
from typing import List, Optional, Dict, Any


# Create the FastMCP server instance
mcp = FastMCP(
    name=settings.server_name,
    host="0.0.0.0",
    port=8000,
    stateless_http=True
)

# ============================================================================
# DATASET MANAGEMENT TOOLS
# ============================================================================

@mcp.tool()
async def load_dataset(
    file_path: str, dataset_name: str, sample_size: Optional[int] = None
) -> Dict:
    """Loads a dataset from a JSON or CSV file into memory."""
    return await tools.load_dataset(file_path, dataset_name, sample_size)

@mcp.tool()
async def list_loaded_datasets() -> Dict:
    """Shows a summary of all datasets currently loaded in memory."""
    return await tools.list_loaded_datasets()

@mcp.tool()
async def clear_dataset(dataset_name: str) -> Dict:
    """Removes a specific dataset and its schema from memory."""
    from .models.schemas import DatasetManager
    return DatasetManager.clear_dataset(dataset_name)

@mcp.tool()
async def clear_all_datasets() -> Dict:
    """Removes all datasets and schemas from memory."""
    from .models.schemas import DatasetManager
    return DatasetManager.clear_all_datasets()

# ============================================================================
# CORE ANALYTICS TOOLS
# ============================================================================

@mcp.tool()
async def suggest_analysis(dataset_name: str) -> Dict:
    """Suggests relevant analysis tools based on the dataset's schema."""
    return await tools.suggest_analysis(dataset_name)

@mcp.tool()
async def analyze_distributions(dataset_name: str, column_name: str) -> Dict:
    """Analyzes and describes the distribution of a single column in a dataset."""
    return await tools.analyze_distributions(dataset_name, column_name)

@mcp.tool()
async def find_correlations(
    dataset_name: str, columns: Optional[List[str]] = None, threshold: float = 0.3
) -> Dict:
    """Finds correlations between numerical columns in a dataset."""
    return await tools.find_correlations(dataset_name, columns, threshold)

@mcp.tool()
async def segment_by_column(
    dataset_name: str, column_name: str, top_n: int = 10
) -> Dict:
    """Segments a dataset by a column and calculates aggregate statistics."""
    return await tools.segment_by_column(dataset_name, column_name, top_n)

@mcp.tool()
async def detect_outliers(
    dataset_name: str, columns: Optional[List[str]] = None, method: str = "iqr"
) -> Dict:
    """Detects outliers in numerical columns using configurable methods."""
    return await tools.detect_outliers(dataset_name, columns, method)

@mcp.tool()
async def time_series_analysis(
    dataset_name: str, date_column: str, value_column: str, frequency: Optional[str] = "auto"
) -> Dict:
    """Performs a basic time series analysis on a given dataset."""
    return await tools.time_series_analysis(dataset_name, date_column, value_column, frequency)

@mcp.tool()
async def validate_data_quality(dataset_name: str) -> Dict:
    """Performs a comprehensive data quality assessment on a dataset."""
    return await tools.validate_data_quality(dataset_name)

# ============================================================================
# ADVANCED OPERATION TOOLS
# ============================================================================

@mcp.tool()
async def compare_datasets(
    dataset_a: str, dataset_b: str, common_columns: Optional[List[str]] = None
) -> Dict:
    """Performs a side-by-side comparison of two datasets."""
    return await tools.compare_datasets(dataset_a, dataset_b, common_columns)

@mcp.tool()
async def merge_datasets(
    dataset_configs: List[Dict[str, Any]], join_strategy: str = "inner"
) -> Dict:
    """Merges multiple datasets based on provided configurations."""
    return await tools.merge_datasets(dataset_configs, join_strategy)

@mcp.tool()
async def calculate_feature_importance(
    dataset_name: str, target_column: str, feature_columns: Optional[List[str]] = None
) -> Dict:
    """Calculates feature importance based on correlation with a target column."""
    return await tools.calculate_feature_importance(dataset_name, target_column, feature_columns)

@mcp.tool()
async def memory_optimization_report(dataset_name: str) -> Dict:
    """Analyzes memory usage of a dataset and suggests optimizations."""
    return await tools.memory_optimization_report(dataset_name)

@mcp.tool()
async def execute_custom_analytics_code(dataset_name: str, python_code: str) -> str:
    """Executes custom Python code against a loaded dataset in an isolated environment."""
    return await tools.execute_custom_analytics_code(dataset_name, python_code)

# ============================================================================
# INPUT/OUTPUT TOOLS
# ============================================================================

@mcp.tool()
async def create_chart(
    dataset_name: str, chart_type: str, x_column: str, y_column: Optional[str] = None,
    groupby_column: Optional[str] = None, title: Optional[str] = None
) -> Dict:
    """Creates a chart from a dataset and saves it as an HTML file."""
    return await tools.create_chart(dataset_name, chart_type, x_column, y_column, groupby_column, title)

@mcp.tool()
async def generate_dashboard(dataset_name: str, chart_configs: List[Dict[str, Any]]) -> Dict:
    """Generates a set of charts intended for a dashboard."""
    return await tools.generate_dashboard(dataset_name, chart_configs)

@mcp.tool()
async def export_insights(
    dataset_name: str, format: str = "json", include_charts: bool = False
) -> Dict:
    """Generates and exports a summary of insights for a dataset to a file."""
    return await tools.export_insights(dataset_name, format, include_charts)

# ============================================================================
# ANALYTICS RESOURCES
# ============================================================================

@mcp.resource("datasets://loaded")
async def get_loaded_datasets_resource() -> Dict:
    """Lists all datasets currently loaded in memory with a brief summary."""
    return await resources.get_loaded_datasets()

@mcp.resource("datasets://{dataset_name}/schema")
async def get_dataset_schema(dataset_name: str) -> Dict:
    """Retrieves the dynamically discovered schema for a specific dataset."""
    return await resources.get_dataset_schema(dataset_name)

@mcp.resource("datasets://{dataset_name}/summary")
async def get_dataset_summary(dataset_name: str) -> Dict:
    """Provides a statistical summary of a dataset's numerical columns."""
    return await resources.get_dataset_summary(dataset_name)

@mcp.resource("datasets://{dataset_name}/sample")
async def get_dataset_sample(dataset_name: str, n_rows: int = 5) -> Dict:
    """Returns a small sample of rows from a dataset for preview."""
    return await resources.get_dataset_sample(dataset_name, n_rows)

@mcp.resource("analytics://current_dataset")
async def get_current_dataset() -> Dict:
    """Identifies the most recently loaded dataset as the current one."""
    return await resources.get_current_dataset()

@mcp.resource("analytics://available_analyses")
async def get_available_analyses() -> Dict:
    """Lists analysis types applicable to the current or specified dataset."""
    return await resources.get_available_analyses()

@mcp.resource("analytics://column_types")
async def get_column_types() -> Dict:
    """Gets the inferred role for each column in a dataset."""
    return await resources.get_column_types()

@mcp.resource("analytics://suggested_insights")
async def get_analysis_suggestions() -> Dict:
    """Provides a list of suggested next analysis steps for a dataset."""
    return await resources.get_analysis_suggestions()

@mcp.resource("analytics://memory_usage")
async def get_memory_usage() -> Dict:
    """Reports the total memory usage of all loaded datasets."""
    return await resources.get_memory_usage()

# ============================================================================
# SYSTEM & LEGACY RESOURCES
# ============================================================================

@mcp.resource("config://server")
async def get_server_config() -> Dict:
    """Provides the server's configuration and capabilities."""
    return await resources.get_server_config()

@mcp.resource("users://{user_id}/profile")
async def get_user_profile(user_id: str) -> Dict:
    """Retrieves a mock user profile."""
    return await resources.get_user_profile(user_id)

@mcp.resource("system://status")
async def get_system_status() -> Dict:
    """Provides the current status and health of the server."""
    return await resources.get_system_status()

# ============================================================================
# GUIDED WORKFLOW PROMPTS
# ============================================================================

@mcp.prompt()
async def dataset_first_look_prompt(dataset_name: str) -> str:
    """Generates an adaptive 'first look' prompt for a dataset."""
    return await prompts.dataset_first_look(dataset_name)

@mcp.prompt()
async def segmentation_workshop_prompt(dataset_name: str) -> str:
    """Generates a detailed prompt to guide a data segmentation workshop."""
    return await prompts.segmentation_workshop(dataset_name)

@mcp.prompt()
async def data_quality_assessment_prompt(dataset_name: str) -> str:
    """Generates a detailed prompt to guide a data quality assessment."""
    return await prompts.data_quality_assessment(dataset_name)

@mcp.prompt()
async def correlation_investigation_prompt(dataset_name: str) -> str:
    """Generates a detailed prompt to guide a correlation analysis workflow."""
    return await prompts.correlation_investigation(dataset_name)

@mcp.prompt()
async def pattern_discovery_session_prompt(dataset_name: str) -> str:
    """Generates a detailed prompt to guide a pattern discovery session."""
    return await prompts.pattern_discovery_session(dataset_name)

@mcp.prompt()
async def insight_generation_workshop_prompt(
    dataset_name: str, business_context: Optional[str] = "general"
) -> str:
    """Generates a detailed prompt to guide an insight generation workshop."""
    return await prompts.insight_generation_workshop(dataset_name, business_context)

@mcp.prompt()
async def dashboard_design_consultation_prompt(
    dataset_name: str, audience: Optional[str] = "general"
) -> str:
    """Generates a detailed prompt to guide a dashboard design session."""
    return await prompts.dashboard_design_consultation(dataset_name, audience)

@mcp.prompt()
async def find_datasources_prompt(directory_path: Optional[str] = None) -> str:
    """Discovers available data files and presents them as load options."""
    return await prompts.find_datasources(directory_path)

@mcp.prompt()
async def list_mcp_assets_prompt() -> str:
    """Returns a comprehensive, formatted list of all server capabilities."""
    return await prompts.list_mcp_assets()

# ============================================================================
# RESOURCE MIRROR TOOLS (for tool-only clients)
# ============================================================================

@mcp.tool()
async def resource_datasets_loaded() -> Dict:
    """Tool mirror of the `datasets://loaded` resource."""
    return await resources.get_loaded_datasets()

@mcp.tool()
async def resource_datasets_schema(dataset_name: str) -> Dict:
    """Tool mirror of the `datasets://{dataset_name}/schema` resource."""
    return await resources.get_dataset_schema(dataset_name)

@mcp.tool()
async def resource_datasets_summary(dataset_name: str) -> Dict:
    """Tool mirror of the `datasets://{dataset_name}/summary` resource."""
    return await resources.get_dataset_summary(dataset_name)

@mcp.tool()
async def resource_datasets_sample(dataset_name: str, n_rows: int = 5) -> Dict:
    """Tool mirror of the `datasets://{dataset_name}/sample` resource."""
    return await resources.get_dataset_sample(dataset_name, n_rows)

@mcp.tool()
async def resource_analytics_current_dataset() -> Dict:
    """Tool mirror of the `analytics://current_dataset` resource."""
    return await resources.get_current_dataset()

@mcp.tool()
async def resource_analytics_available_analyses() -> Dict:
    """Tool mirror of the `analytics://available_analyses` resource."""
    return await resources.get_available_analyses()

@mcp.tool()
async def resource_analytics_column_types() -> Dict:
    """Tool mirror of the `analytics://column_types` resource."""
    return await resources.get_column_types()

@mcp.tool()
async def resource_analytics_suggested_insights() -> Dict:
    """Tool mirror of the `analytics://suggested_insights` resource."""
    return await resources.get_analysis_suggestions()

@mcp.tool()
async def resource_analytics_memory_usage() -> Dict:
    """Tool mirror of the `analytics://memory_usage` resource."""
    return await resources.get_memory_usage()

@mcp.tool()
async def resource_config_server() -> Dict:
    """Tool mirror of the `config://server` resource."""
    return await resources.get_server_config()

@mcp.tool()
async def resource_users_profile(user_id: str) -> Dict:
    """Tool mirror of the `users://{user_id}/profile` resource."""
    return await resources.get_user_profile(user_id)

@mcp.tool()
async def resource_system_status() -> Dict:
    """Tool mirror of the `system://status` resource."""
    return await resources.get_system_status()

# ============================================================================
# SERVER ENTRY POINT
# ============================================================================

def get_server() -> FastMCP:
    """
    Returns the configured FastMCP server instance.

    Returns:
        FastMCP: The server instance.
    """
    return mcp

if __name__ == "__main__":
    mcp.run()
