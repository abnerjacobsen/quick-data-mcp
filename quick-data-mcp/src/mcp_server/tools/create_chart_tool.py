"""
Tool for creating and saving a variety of charts from a dataset.

This tool uses the Plotly Express library to generate common chart types like
histograms, bar charts, scatter plots, line plots, and box plots. It can
save the generated interactive charts as HTML files.
"""

import pandas as pd
import plotly.express as px
from pathlib import Path
from typing import Dict, Optional
from ..models.schemas import DatasetManager


async def create_chart(
    dataset_name: str,
    chart_type: str,
    x_column: str,
    y_column: Optional[str] = None,
    groupby_column: Optional[str] = None,
    title: Optional[str] = None,
    save_path: Optional[str] = None
) -> Dict:
    """
    Creates a chart from a dataset and saves it as an HTML file.

    This function supports generating 'histogram', 'bar', 'scatter', 'line',
    and 'box' plots. It automatically handles chart titles and can group
    data by a specified column.

    Args:
        dataset_name (str): The name of the loaded dataset to use.
        chart_type (str): The type of chart to create. Supported types are:
                          'histogram', 'bar', 'scatter', 'line', 'box'.
        x_column (str): The name of the column for the x-axis.
        y_column (Optional[str]): The name of the column for the y-axis.
                                  Required for 'scatter' and 'line' plots.
        groupby_column (Optional[str]): The column to use for color-based grouping.
        title (Optional[str]): The title of the chart. If None, a title is
                               generated automatically.
        save_path (Optional[str]): The path to save the HTML file. If None, it
                                   saves to 'outputs/charts/' with a generated name.

    Returns:
        Dict: A dictionary with the status of the chart creation, including the
              path to the saved file. If an error occurs, the dictionary will
              contain an 'error' key.
    """
    try:
        df = DatasetManager.get_dataset(dataset_name)
        
        # Validate columns exist
        required_cols = [x_column]
        if y_column:
            required_cols.append(y_column)
        if groupby_column:
            required_cols.append(groupby_column)
            
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            return {"error": f"Columns not found: {', '.join(missing_cols)}"}
        
        # Generate title if not provided
        if title is None:
            title = f"{chart_type.title()} Chart: {x_column}"
            if y_column:
                title += f" vs {y_column}"
            if groupby_column:
                title += f" (grouped by {groupby_column})"
        
        fig = None
        
        if chart_type == "histogram":
            fig = px.histogram(df, x=x_column, color=groupby_column, title=title)
            
        elif chart_type == "bar":
            if y_column:
                # Aggregated bar chart
                agg_data = df.groupby(x_column, as_index=False)[y_column].mean()
                fig = px.bar(agg_data, x=x_column, y=y_column, color=groupby_column, title=title)
            else:
                # Count plot
                fig = px.bar(df, x=x_column, color=groupby_column, title=title)
                    
        elif chart_type == "scatter":
            if not y_column:
                return {"error": "Scatter plot requires both x_column and y_column."}
            fig = px.scatter(df, x=x_column, y=y_column, color=groupby_column, title=title)
            
        elif chart_type == "line":
            if not y_column:
                return {"error": "Line plot requires both x_column and y_column."}
            
            df_sorted = df.sort_values(x_column)
            fig = px.line(df_sorted, x=x_column, y=y_column, color=groupby_column, title=title)
            
        elif chart_type == "box":
            fig = px.box(df, x=x_column, y=y_column, color=groupby_column, title=title)
            
        else:
            return {"error": f"Unsupported chart type: '{chart_type}'. Supported: histogram, bar, scatter, line, box"}
        
        # Save chart
        if save_path is None:
            outputs_dir = Path("outputs/charts")
            outputs_dir.mkdir(parents=True, exist_ok=True)
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '_')).rstrip()
            filename = f"{safe_title}.html".replace(" ", "_")
            save_path = outputs_dir / filename

        chart_file = str(Path(save_path).resolve())
        fig.write_html(chart_file)
        
        return {
            "dataset": dataset_name,
            "chart_type": chart_type,
            "chart_config": {
                "x_column": x_column,
                "y_column": y_column,
                "groupby_column": groupby_column,
                "title": title
            },
            "chart_file": chart_file,
            "status": "success"
        }
        
    except Exception as e:
        return {"error": f"Chart creation failed: {str(e)}"}