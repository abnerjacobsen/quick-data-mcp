"""
Tool for listing all datasets currently loaded in memory.

This tool provides a summary of all active datasets, including their names,
dimensions (rows and columns), and memory footprint.
"""

from typing import Dict
from ..models.schemas import DatasetManager


async def list_loaded_datasets() -> Dict:
    """
    Shows a summary of all datasets currently loaded in memory.

    This function retrieves the list of active datasets from the DatasetManager
    and compiles a report including the total number of datasets and their
    combined memory usage.

    Returns:
        Dict: A dictionary containing a list of loaded datasets with their
              summaries, and overall totals. If an error occurs, the dictionary
              will contain an 'error' key.
    """
    try:
        datasets = []
        total_memory = 0
        
        for name in DatasetManager.list_datasets():
            info = DatasetManager.get_dataset_info(name)
            memory_mb = info.get("memory_usage_mb", 0)
            total_memory += memory_mb
            
            datasets.append({
                "name": name,
                "rows": info.get("shape", (0, 0))[0],
                "columns": info.get("shape", (0, 0))[1],
                "memory_mb": round(memory_mb, 2)
            })
        
        return {
            "loaded_datasets": datasets,
            "total_datasets": len(datasets),
            "total_memory_mb": round(total_memory, 2)
        }
        
    except Exception as e:
        return {"error": f"Failed to list datasets: {str(e)}"}