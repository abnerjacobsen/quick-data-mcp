"""
Tool for exporting a summary of dataset insights to a file.

This tool generates a report containing key insights about a dataset—such as
its shape, data quality metrics, and schema summary—and exports it to a file
in various formats (JSON, CSV, HTML).
"""

import pandas as pd
import json
from datetime import datetime
from pathlib import Path
from typing import Dict
from ..models.schemas import DatasetManager, dataset_schemas


async def export_insights(
    dataset_name: str,
    format: str = "json",
    include_charts: bool = False
) -> Dict:
    """
    Generates and exports a summary of insights for a dataset to a file.

    The insights report includes dataset info, schema summary, data quality
    metrics, and statistical summaries for numerical and categorical columns.

    Args:
        dataset_name (str): The name of the loaded dataset to export insights for.
        format (str): The format to export the insights in. Supported formats:
                      'json', 'csv', 'html'. Defaults to 'json'.
        include_charts (bool): If True, attempts to include charts in the export.
                               (Currently not implemented). Defaults to False.

    Returns:
        Dict: A dictionary containing the status of the export and the path to
              the created file. If an error occurs, the dictionary will contain
              an 'error' key.
    """
    try:
        df = DatasetManager.get_dataset(dataset_name)
        schema = dataset_schemas[dataset_name]
        
        insights = {
            "dataset_name": dataset_name,
            "export_timestamp": datetime.now().isoformat(),
            "dataset_info": {
                "rows": df.shape[0],
                "columns": df.shape[1],
                "memory_usage_mb": round(df.memory_usage(deep=True).sum() / 1024**2, 2),
            },
            "schema_summary": {
                "numerical_columns": sum(1 for c in schema.columns.values() if c.suggested_role == 'numerical'),
                "categorical_columns": sum(1 for c in schema.columns.values() if c.suggested_role == 'categorical'),
                "temporal_columns": sum(1 for c in schema.columns.values() if c.suggested_role == 'temporal'),
            },
            "data_quality": {
                "duplicate_rows": int(df.duplicated().sum()),
                "total_missing_values": int(df.isnull().sum().sum()),
            },
            "suggested_analyses": schema.suggested_analyses,
        }
        
        outputs_dir = Path("outputs/reports")
        outputs_dir.mkdir(parents=True, exist_ok=True)
        export_file_path = outputs_dir / f"insights_{dataset_name}.{format.lower()}"

        if format.lower() == "json":
            with open(export_file_path, 'w') as f:
                json.dump(insights, f, indent=2, default=str)
                
        elif format.lower() == "csv":
            summary_list = [
                {"metric": "Dataset Name", "value": dataset_name},
                {"metric": "Export Date", "value": insights["export_timestamp"]},
                {"metric": "Total Rows", "value": insights["dataset_info"]["rows"]},
            ]
            pd.DataFrame(summary_list).to_csv(export_file_path, index=False)
            
        elif format.lower() == "html":
            html_content = f"<h1>Insights for {dataset_name}</h1>"
            html_content += pd.DataFrame.from_dict(insights, orient='index').to_html()
            with open(export_file_path, 'w') as f:
                f.write(html_content)
        else:
            return {"error": f"Unsupported export format: '{format}'. Use 'json', 'csv', or 'html'."}
        
        return {
            "dataset": dataset_name,
            "export_format": format,
            "export_file": str(export_file_path.resolve()),
            "status": "success"
        }
        
    except Exception as e:
        return {"error": f"Export failed: {str(e)}"}