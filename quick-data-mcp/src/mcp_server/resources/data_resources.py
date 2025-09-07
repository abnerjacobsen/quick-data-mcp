"""
Implementations for all data resources of the Generic Data Analytics MCP Server.

This module provides the core logic for the server's resources, which expose
read-only information about the server's state, loaded datasets, and system
configuration. Each function corresponds to a specific resource endpoint.
"""

from typing import Dict, Optional
from ..models.schemas import UserProfile, DatasetManager, dataset_schemas
from ..config.settings import settings


async def get_server_config() -> Dict:
    """
    Provides the server's configuration and capabilities.

    Returns:
        Dict: A dictionary with server name, version, and supported features.
    """
    return {
        "server_name": settings.server_name,
        "server_version": settings.version,
        "supported_formats": ["csv", "json"],
        "supported_analyses": [
            "data_quality", "distribution", "correlation", "segmentation",
            "time_series", "outlier_detection", "feature_importance"
        ]
    }


async def get_loaded_datasets() -> Dict:
    """
    Lists all datasets currently loaded in memory with a brief summary.

    Returns:
        Dict: A dictionary containing a list of loaded datasets, each with its
              name, dimensions, and memory usage.
    """
    datasets = []
    for name in DatasetManager.list_datasets():
        info = DatasetManager.get_dataset_info(name)
        datasets.append({
            "name": name,
            "rows": info.get("shape", (0, 0))[0],
            "columns": info.get("shape", (0, 0))[1],
            "memory_mb": round(info.get("memory_usage_mb", 0), 2)
        })
    return {
        "datasets": datasets,
        "total_datasets": len(datasets)
    }


async def get_dataset_schema(dataset_name: str) -> Dict:
    """
    Retrieves the dynamically discovered schema for a specific dataset.

    The schema includes column names, data types, inferred roles, and other metadata.

    Args:
        dataset_name (str): The name of the loaded dataset.

    Returns:
        Dict: The schema of the dataset as a dictionary.
    """
    if dataset_name not in dataset_schemas:
        return {"error": f"Dataset '{dataset_name}' not found."}
    return dataset_schemas[dataset_name].model_dump()


async def get_dataset_summary(dataset_name: str) -> Dict:
    """
    Provides a statistical summary of a dataset's numerical columns.

    This is equivalent to running `pandas.DataFrame.describe()`.

    Args:
        dataset_name (str): The name of the loaded dataset.

    Returns:
        Dict: A dictionary containing the statistical summary.
    """
    df = DatasetManager.get_dataset(dataset_name)
    return df.describe().to_dict()


async def get_dataset_sample(dataset_name: str, n_rows: int = 5) -> Dict:
    """
    Returns a small sample of rows from a dataset for preview.

    Args:
        dataset_name (str): The name of the loaded dataset.
        n_rows (int): The number of rows to return in the sample.

    Returns:
        Dict: A dictionary containing the sample data.
    """
    df = DatasetManager.get_dataset(dataset_name)
    return df.head(n_rows).to_dict('records')


async def get_current_dataset() -> Dict:
    """
    Identifies the most recently loaded dataset as the current one.

    Returns:
        Dict: Information about the current dataset, or a message if none are loaded.
    """
    datasets = DatasetManager.list_datasets()
    if not datasets:
        return {"current_dataset": None, "message": "No datasets loaded."}
    return {"current_dataset": datasets[-1]}


async def get_available_analyses(dataset_name: Optional[str] = None) -> Dict:
    """
    Lists analysis types applicable to the current or specified dataset.

    Args:
        dataset_name (Optional[str]): The dataset to check. If None, uses the
                                      most recently loaded one.

    Returns:
        Dict: A list of available analysis types.
    """
    if dataset_name is None:
        dataset_name = (await get_current_dataset()).get("current_dataset")
        if not dataset_name:
            return {"available_analyses": []}

    if dataset_name not in dataset_schemas:
        return {"error": f"Dataset '{dataset_name}' not found."}
    
    schema = dataset_schemas[dataset_name]
    return {"available_analyses": schema.suggested_analyses}


async def get_column_types(dataset_name: Optional[str] = None) -> Dict:
    """
    Gets the inferred role for each column in a dataset.

    Args:
        dataset_name (Optional[str]): The dataset to check. If None, uses the
                                      most recently loaded one.

    Returns:
        Dict: A mapping of column names to their inferred roles.
    """
    if dataset_name is None:
        dataset_name = (await get_current_dataset()).get("current_dataset")
        if not dataset_name:
            return {"column_types": {}}

    if dataset_name not in dataset_schemas:
        return {"error": f"Dataset '{dataset_name}' not found."}
    
    schema = dataset_schemas[dataset_name]
    return {
        "column_types": {name: col.suggested_role for name, col in schema.columns.items()}
    }


async def get_analysis_suggestions(dataset_name: Optional[str] = None) -> Dict:
    """
    Provides a list of suggested next analysis steps for a dataset.

    Args:
        dataset_name (Optional[str]): The dataset to get suggestions for. If None,
                                      uses the most recently loaded one.

    Returns:
        Dict: A list of suggested analyses.
    """
    if dataset_name is None:
        dataset_name = (await get_current_dataset()).get("current_dataset")
        if not dataset_name:
            return {"suggestions": []}

    from ..tools.suggest_analysis_tool import suggest_analysis
    return await suggest_analysis(dataset_name)


async def get_memory_usage() -> Dict:
    """
    Reports the total memory usage of all loaded datasets.

    Returns:
        Dict: A dictionary with the total memory usage in megabytes.
    """
    total_memory = 0
    for name in DatasetManager.list_datasets():
        info = DatasetManager.get_dataset_info(name)
        total_memory += info.get("memory_usage_mb", 0)
    return {"total_memory_mb": round(total_memory, 2)}


async def get_user_profile(user_id: str) -> Dict:
    """
    Retrieves a mock user profile.

    Args:
        user_id (str): The ID of the user to retrieve.

    Returns:
        Dict: A user profile object as a dictionary.
    """
    profile = UserProfile(id=user_id, name=f"User {user_id}", email=f"user.{user_id}@example.com")
    return profile.model_dump()


async def get_system_status() -> Dict:
    """
    Provides the current status and health of the server.

    Returns:
        Dict: A dictionary with system status information.
    """
    return {
        "status": "healthy",
        "version": settings.version,
        "datasets_loaded": len(DatasetManager.list_datasets()),
        "total_memory_mb": (await get_memory_usage())["total_memory_mb"]
    }