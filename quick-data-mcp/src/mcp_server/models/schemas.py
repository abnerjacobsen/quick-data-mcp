"""
Data models and schemas for the Generic Data Analytics MCP Server.

This module defines the Pydantic models used for data validation, serialization,
and schema representation throughout the application. It also includes the
`DatasetManager`, a crucial class for in-memory storage and management of
pandas DataFrames.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum
import pandas as pd
import numpy as np


class ColumnInfo(BaseModel):
    """
    Represents metadata and inferred characteristics of a single dataset column.

    Attributes:
        name (str): The name of the column.
        dtype (str): The data type of the column as a string (e.g., 'int64', 'object').
        unique_values (int): The number of unique values in the column.
        null_percentage (float): The percentage of null or missing values.
        sample_values (List[Any]): A small sample of non-null values from the column.
        suggested_role (str): The automatically inferred role of the column, such as
                              'categorical', 'numerical', 'temporal', or 'identifier'.
    """
    name: str
    dtype: str
    unique_values: int
    null_percentage: float
    sample_values: List[Any]
    suggested_role: str  # 'categorical', 'numerical', 'temporal', 'identifier'
    
    @classmethod
    def from_series(cls, series: pd.Series, name: str) -> 'ColumnInfo':
        """
        Creates a ColumnInfo instance by analyzing a pandas Series.

        This factory method automatically discovers column characteristics like data type,
        null percentage, and infers a functional role for the column.

        Args:
            series (pd.Series): The pandas Series to analyze.
            name (str): The name of the column.

        Returns:
            ColumnInfo: An instance populated with the series's metadata.
        """
        
        # Determine suggested role
        if pd.api.types.is_numeric_dtype(series):
            role = 'numerical'
        elif pd.api.types.is_datetime64_any_dtype(series):
            role = 'temporal'
        elif series.nunique() / len(series) < 0.5:  # Low cardinality = categorical
            role = 'categorical'
        elif series.nunique() == len(series):  # Unique values = identifier
            role = 'identifier'
        else:
            role = 'categorical'
            
        return cls(
            name=name,
            dtype=str(series.dtype),
            unique_values=series.nunique(),
            null_percentage=series.isnull().mean() * 100,
            sample_values=series.dropna().head(3).tolist(),
            suggested_role=role
        )


class DatasetSchema(BaseModel):
    """
    Represents the dynamically discovered schema of a loaded dataset.

    Attributes:
        name (str): The name of the dataset.
        columns (Dict[str, ColumnInfo]): A dictionary mapping column names to their
                                         ColumnInfo metadata.
        row_count (int): The total number of rows in the dataset.
        suggested_analyses (List[str]): A list of analysis types suggested based
                                        on the column roles present in the dataset.
    """
    name: str
    columns: Dict[str, ColumnInfo]
    row_count: int
    suggested_analyses: List[str]
    
    @classmethod
    def from_dataframe(cls, df: pd.DataFrame, name: str) -> 'DatasetSchema':
        """
        Creates a DatasetSchema instance by analyzing a pandas DataFrame.

        This factory method inspects all columns of a DataFrame to build a
        comprehensive schema, including suggesting relevant analyses.

        Args:
            df (pd.DataFrame): The DataFrame to analyze.
            name (str): The name to assign to the dataset's schema.

        Returns:
            DatasetSchema: An instance populated with the DataFrame's schema.
        """
        columns = {}
        for col in df.columns:
            columns[col] = ColumnInfo.from_series(df[col], col)
        
        # Generate analysis suggestions based on column types
        suggestions = []
        numerical_cols = [col for col, info in columns.items() if info.suggested_role == 'numerical']
        categorical_cols = [col for col, info in columns.items() if info.suggested_role == 'categorical']
        temporal_cols = [col for col, info in columns.items() if info.suggested_role == 'temporal']
        
        if len(numerical_cols) >= 2:
            suggestions.append("correlation_analysis")
        if categorical_cols:
            suggestions.append("segmentation_analysis")
        if temporal_cols:
            suggestions.append("time_series_analysis")
            
        return cls(
            name=name,
            columns=columns,
            row_count=len(df),
            suggested_analyses=suggestions
        )


# Global in-memory storage for datasets
loaded_datasets: Dict[str, pd.DataFrame] = {}
dataset_schemas: Dict[str, DatasetSchema] = {}


class DatasetManager:
    """
    A static class providing a simple in-memory store for managing datasets.

    This class handles loading, retrieving, and clearing datasets and their schemas
    from global dictionaries, acting as a centralized data manager for the server.
    """
    
    @staticmethod
    def load_dataset(file_path: str, dataset_name: str) -> dict:
        """
        Loads a dataset from a file into memory and discovers its schema.

        Supports JSON and CSV file formats. The loaded DataFrame and its discovered
        schema are stored in global dictionaries under the given dataset name.

        Args:
            file_path (str): The path to the data file (.json or .csv).
            dataset_name (str): The name to assign to the loaded dataset.

        Returns:
            dict: A summary of the load operation, including status, dimensions,
                  and memory usage.

        Raises:
            ValueError: If the file format is not supported.
        """
        
        # Determine format from file extension
        if file_path.endswith('.json'):
            df = pd.read_json(file_path)
            file_format = 'json'
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
            file_format = 'csv'
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
        
        # Store in global memory
        loaded_datasets[dataset_name] = df
        
        # Discover and cache schema
        schema = DatasetSchema.from_dataframe(df, dataset_name)
        dataset_schemas[dataset_name] = schema
        
        return {
            "status": "loaded",
            "dataset_name": dataset_name,
            "rows": len(df),
            "columns": list(df.columns),
            "format": file_format,
            "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024**2:.1f} MB"
        }
    
    @staticmethod
    def get_dataset(dataset_name: str) -> pd.DataFrame:
        """
        Retrieves a loaded dataset from memory.

        Args:
            dataset_name (str): The name of the dataset to retrieve.

        Returns:
            pd.DataFrame: The requested pandas DataFrame.

        Raises:
            ValueError: If the dataset is not found in memory.
        """
        if dataset_name not in loaded_datasets:
            raise ValueError(f"Dataset '{dataset_name}' not loaded. Use load_dataset() first.")
        return loaded_datasets[dataset_name]
    
    @staticmethod
    def list_datasets() -> List[str]:
        """
        Gets the names of all currently loaded datasets.

        Returns:
            List[str]: A list of dataset names.
        """
        return list(loaded_datasets.keys())
    
    @staticmethod
    def get_dataset_info(dataset_name: str) -> dict:
        """
        Gets basic information and schema for a loaded dataset.

        Args:
            dataset_name (str): The name of the dataset.

        Returns:
            dict: A dictionary containing the dataset's shape, columns, memory usage,
                  and full schema.

        Raises:
            ValueError: If the dataset is not found in memory.
        """
        if dataset_name not in loaded_datasets:
            raise ValueError(f"Dataset '{dataset_name}' not loaded")
            
        df = loaded_datasets[dataset_name]
        schema = dataset_schemas[dataset_name]
        
        return {
            "name": dataset_name,
            "shape": df.shape,
            "columns": list(df.columns),
            "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024**2,
            "schema": schema.model_dump()
        }
    
    @staticmethod
    def clear_dataset(dataset_name: str) -> dict:
        """
        Removes a specific dataset and its schema from memory.

        Args:
            dataset_name (str): The name of the dataset to clear.

        Returns:
            dict: A status message indicating success or failure.
        """
        if dataset_name not in loaded_datasets:
            return {"error": f"Dataset '{dataset_name}' not found"}
        
        del loaded_datasets[dataset_name]
        del dataset_schemas[dataset_name]
        
        return {"status": "success", "message": f"Dataset '{dataset_name}' cleared from memory"}
    
    @staticmethod
    def clear_all_datasets() -> dict:
        """
        Removes all datasets and schemas from memory.

        Returns:
            dict: A status message indicating how many datasets were cleared.
        """
        count = len(loaded_datasets)
        loaded_datasets.clear()
        dataset_schemas.clear()
        
        return {"status": "success", "message": f"Cleared {count} datasets from memory"}


class ChartConfig(BaseModel):
    """
    Defines the configuration for generating a chart.

    This model is used to pass all necessary parameters for creating a visualization
    with tools like `create_chart`.

    Attributes:
        dataset_name (str): The name of the dataset to use for the chart.
        chart_type (str): The type of chart to generate (e.g., 'bar', 'scatter').
        x_column (str): The column to use for the x-axis.
        y_column (Optional[str]): The column to use for the y-axis.
        groupby_column (Optional[str]): The column to use for grouping data.
        title (Optional[str]): An optional title for the chart.
    """
    dataset_name: str
    chart_type: str  # 'bar', 'histogram', 'scatter', 'line', 'box'
    x_column: str
    y_column: Optional[str] = None
    groupby_column: Optional[str] = None
    title: Optional[str] = None
    
    
class AnalysisResult(BaseModel):
    """
    A generic model for returning the result of an analysis tool.

    Attributes:
        dataset_name (str): The name of the dataset that was analyzed.
        analysis_type (str): The type of analysis performed.
        timestamp (datetime): The time the analysis was completed.
        results (Dict[str, Any]): The main results of the analysis.
        metadata (Dict[str, Any]): Additional metadata about the analysis.
    """
    dataset_name: str
    analysis_type: str
    timestamp: datetime = Field(default_factory=datetime.now)
    results: Dict[str, Any]
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DataQualityReport(BaseModel):
    """
    Represents a comprehensive data quality assessment report.

    Attributes:
        dataset_name (str): The name of the dataset assessed.
        total_rows (int): The total number of rows in the dataset.
        total_columns (int): The total number of columns.
        missing_data (Dict[str, float]): A mapping of column names to their percentage
                                         of missing values.
        duplicate_rows (int): The number of duplicate rows found.
        potential_issues (List[str]): A list of identified potential data quality issues.
        quality_score (float): An overall quality score from 0 to 100.
        recommendations (List[str]): A list of suggested actions to improve data quality.
    """
    dataset_name: str
    total_rows: int
    total_columns: int
    missing_data: Dict[str, float]  # column -> percentage missing
    duplicate_rows: int
    potential_issues: List[str]
    quality_score: float  # 0-100
    recommendations: List[str]


# Legacy models - kept for minimal backward compatibility if needed
class Status(str, Enum):
    """A simple status enum for tracking task states."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class UserProfile(BaseModel):
    """
    A simple model representing a user profile.

    Attributes:
        id (str): The unique identifier for the user.
        name (str): The user's name.
        email (str): The user's email address.
        status (str): The user's account status (e.g., 'active').
        preferences (Dict[str, Any]): A dictionary for storing user preferences.
    """
    id: str
    name: str
    email: str
    status: str = "active"
    preferences: Dict[str, Any] = Field(default_factory=dict)