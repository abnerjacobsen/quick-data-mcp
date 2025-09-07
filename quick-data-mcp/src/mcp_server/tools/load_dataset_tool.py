"""
Tool for loading datasets from files into memory.

This tool handles the loading of data from CSV or JSON files into a pandas
DataFrame, which is then stored in memory for analysis by other tools.
It also supports taking a random sample of the data during loading.
"""

from typing import Dict, Optional
from ..models.schemas import DatasetManager, loaded_datasets, dataset_schemas


async def load_dataset(
    file_path: str,
    dataset_name: str,
    sample_size: Optional[int] = None
) -> Dict:
    """
    Loads a dataset from a JSON or CSV file into memory.

    This function uses the DatasetManager to load a file, create a pandas
    DataFrame, and store it in memory under a specified name. It automatically
    discovers the file format and the dataset's schema.

    Args:
        file_path (str): The local path to the data file (.json or .csv).
        dataset_name (str): A unique name to assign to the loaded dataset.
        sample_size (Optional[int]): If provided, a random sample of this many
                                     rows will be loaded instead of the full dataset.

    Returns:
        Dict: A dictionary summarizing the result of the load operation,
              including status, dimensions, and memory usage. If an error
              occurs, the dictionary will contain an 'error' key.
    """
    try:
        result = DatasetManager.load_dataset(file_path, dataset_name)
        
        # Apply sampling if requested
        if sample_size and sample_size > 0 and sample_size < result.get("rows", 0):
            df = DatasetManager.get_dataset(dataset_name)
            sampled_df = df.sample(n=sample_size, random_state=42)

            # Update the dataset in memory to the sampled version
            loaded_datasets[dataset_name] = sampled_df
            
            # Re-discover and cache the schema for the sampled data
            # This ensures schema and suggestions match the sampled data
            schema = dataset_schemas[dataset_name]
            schema.row_count = len(sampled_df)
            
            # Update result summary
            result["rows"] = len(sampled_df)
            result["sampled"] = True
            result["original_rows"] = len(df)
            result["memory_usage"] = f"{sampled_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
        else:
            result["sampled"] = False

        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to load dataset: {str(e)}"
        }