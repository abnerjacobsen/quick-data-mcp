"""
Tool for generating a dashboard by combining multiple charts.

This tool orchestrates the creation of a dashboard by generating several
individual charts based on a list of configurations. While it generates the
individual chart files, it does not yet combine them into a single HTML
dashboard file.
"""

from datetime import datetime
from typing import List, Dict, Any
from ..models.schemas import DatasetManager
from .create_chart_tool import create_chart


async def generate_dashboard(dataset_name: str, chart_configs: List[Dict[str, Any]]) -> Dict:
    """
    Generates a set of charts intended for a dashboard.

    This function iterates through a list of chart configurations, calling the
    `create_chart` tool for each one. It compiles the results of each chart
    generation into a summary report.

    Note: This tool currently generates individual chart files but does not
    combine them into a single dashboard view.

    Args:
        dataset_name (str): The name of the loaded dataset to use for the charts.
        chart_configs (List[Dict[str, Any]]): A list of dictionaries, where each
            dictionary is a configuration for a single chart (see `create_chart`
            for details).

    Returns:
        Dict: A dictionary containing a summary of the dashboard generation,
              including the status for each requested chart. If a setup error
              occurs, the dictionary will contain an 'error' key.
    """
    try:
        # Ensure dataset exists before starting
        DatasetManager.get_dataset(dataset_name)
        
        if not chart_configs:
            return {"error": "No chart configurations were provided."}
        
        chart_results = []
        
        for i, config in enumerate(chart_configs):
            chart_id = i + 1
            try:
                # Ensure required keys are present
                if "chart_type" not in config or "x_column" not in config:
                    chart_results.append({
                        "chart_id": chart_id, "config": config, "status": "failed",
                        "error": "Chart config must include 'chart_type' and 'x_column'."
                    })
                    continue

                chart_result = await create_chart(
                    dataset_name=dataset_name,
                    chart_type=config["chart_type"],
                    x_column=config["x_column"],
                    y_column=config.get("y_column"),
                    groupby_column=config.get("groupby_column"),
                    title=config.get("title", f"Chart {chart_id}: {config['chart_type']}"),
                )
                
                if "error" in chart_result:
                    chart_results.append({
                        "chart_id": chart_id, "config": config, "status": "failed",
                        "error": chart_result["error"]
                    })
                else:
                    chart_results.append({
                        "chart_id": chart_id, "config": config, "status": "success",
                        "result": chart_result
                    })
                    
            except Exception as chart_error:
                chart_results.append({
                    "chart_id": chart_id, "config": config, "status": "failed",
                    "error": f"Chart generation threw an exception: {str(chart_error)}"
                })
        
        successful_charts = sum(1 for c in chart_results if c["status"] == "success")
        
        return {
            "dataset": dataset_name,
            "dashboard_generated_at": datetime.now().isoformat(),
            "summary": {
                "total_charts_requested": len(chart_configs),
                "successful_charts": successful_charts,
                "failed_charts": len(chart_configs) - successful_charts,
            },
            "charts": chart_results,
        }
        
    except Exception as e:
        return {"error": f"Dashboard generation failed: {str(e)}"}