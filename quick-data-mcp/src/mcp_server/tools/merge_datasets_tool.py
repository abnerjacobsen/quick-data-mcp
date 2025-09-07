"""
Tool for merging multiple datasets into a single DataFrame.

This tool can combine two or more datasets using either a specified join key
or by concatenation. The resulting merged dataset is then loaded back into
memory for further analysis.
"""

import pandas as pd
from typing import List, Dict, Any
from ..models.schemas import DatasetManager, loaded_datasets, dataset_schemas, DatasetSchema


async def merge_datasets(
    dataset_configs: List[Dict[str, Any]], 
    join_strategy: str = "inner"
) -> Dict:
    """
    Merges multiple datasets based on provided configurations.

    This function starts with the first dataset in the list and iteratively
    merges or concatenates the subsequent datasets. If a 'join_column' is
    specified in a dataset's config, it performs a merge; otherwise, it
    concatenates. The final merged DataFrame is saved as a new dataset.

    Args:
        dataset_configs (List[Dict[str, Any]]): A list of dictionaries, where
            each dictionary specifies a dataset to merge. It must contain
            'dataset_name' and may contain 'join_column'.
        join_strategy (str): The type of join to perform for merges (e.g.,
                             'inner', 'outer', 'left', 'right'). Defaults to 'inner'.

    Returns:
        Dict: A dictionary containing a report of the merge operations and the
              name of the newly created merged dataset. If an error occurs,
              the dictionary will contain an 'error' key.
    """
    try:
        if len(dataset_configs) < 2:
            return {"error": "Merge operation requires at least two datasets."}
        
        # Load the base DataFrame
        base_config = dataset_configs[0]
        merged_df = DatasetManager.get_dataset(base_config["dataset_name"]).copy()
        
        merge_steps = []
        
        for config in dataset_configs[1:]:
            dataset_name = config["dataset_name"]
            join_column = config.get("join_column")
            
            df_to_merge = DatasetManager.get_dataset(dataset_name)
            
            if not join_column:
                return {"error": f"Configuration for dataset '{dataset_name}' must provide a 'join_column'."}
            
            if join_column not in merged_df.columns or join_column not in df_to_merge.columns:
                return {"error": f"Join column '{join_column}' not found in one or both datasets."}

            before_shape = merged_df.shape
            merged_df = pd.merge(
                merged_df, df_to_merge, on=join_column, how=join_strategy,
                suffixes=('', f'_{dataset_name}')
            )
            after_shape = merged_df.shape

            merge_steps.append({
                "merged_with": dataset_name,
                "join_column": join_column,
                "rows_gained": after_shape[0] - before_shape[0],
            })
        
        # Save the newly merged dataset
        merged_name = f"merged_{'_'.join(d['dataset_name'] for d in dataset_configs)}"
        loaded_datasets[merged_name] = merged_df
        dataset_schemas[merged_name] = DatasetSchema.from_dataframe(merged_df, merged_name)
        
        return {
            "status": "success",
            "merged_dataset_name": merged_name,
            "final_shape": merged_df.shape,
            "merge_strategy": join_strategy,
            "merge_steps": merge_steps
        }
        
    except Exception as e:
        return {"error": f"Dataset merge failed: {str(e)}"}