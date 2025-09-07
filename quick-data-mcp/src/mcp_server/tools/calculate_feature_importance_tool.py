"""
Tool for calculating feature importance relative to a target variable.

This tool uses a correlation-based method to determine the importance of
numerical features in predicting a numerical target column. It is a simple yet
effective way to get a first-pass understanding of which features might be
most influential in a predictive model.
"""

import pandas as pd
from typing import List, Dict, Optional
from ..models.schemas import DatasetManager


async def calculate_feature_importance(
    dataset_name: str, 
    target_column: str, 
    feature_columns: Optional[List[str]] = None
) -> Dict:
    """
    Calculates feature importance based on correlation with a target column.

    This function computes the Pearson correlation between each specified numerical
    feature column and the numerical target column. The absolute value of the
    correlation is used as the importance score.

    Args:
        dataset_name (str): The name of the loaded dataset to analyze.
        target_column (str): The name of the numerical column to be used as the target.
        feature_columns (Optional[List[str]]): A list of feature columns to evaluate.
            If None, all columns other than the target will be considered.

    Returns:
        Dict: A dictionary containing the importance scores for each feature,
              ranked by importance. If an error occurs, the dictionary will
              contain an 'error' key.
    """
    try:
        df = DatasetManager.get_dataset(dataset_name)
        
        if target_column not in df.columns:
            return {"error": f"Target column '{target_column}' not found"}
        
        # Auto-select feature columns if not provided
        if feature_columns is None:
            feature_columns = [col for col in df.columns if col != target_column]
        
        # Filter to numerical columns only for correlation-based importance
        numerical_features = []
        for col in feature_columns:
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                numerical_features.append(col)
        
        if not numerical_features:
            return {"error": "No numerical feature columns found to analyze."}
        
        if not pd.api.types.is_numeric_dtype(df[target_column]):
            return {"error": "Target column must be numerical for correlation-based feature importance."}
        
        # Calculate correlations with target
        correlations = df[numerical_features + [target_column]].corr(numeric_only=True)[target_column]
        
        # Calculate feature importance (absolute correlation)
        feature_importance = {}
        for feature in numerical_features:
            correlation = correlations.get(feature, 0.0)
            importance = abs(correlation) if not pd.isna(correlation) else 0
            feature_importance[feature] = {
                "correlation": round(correlation, 4),
                "importance": round(importance, 4),
                "rank": 0  # Will be set below
            }
        
        # Rank features by importance
        sorted_features = sorted(feature_importance.items(), key=lambda x: x[1]["importance"], reverse=True)
        for rank, (feature, info) in enumerate(sorted_features, 1):
            feature_importance[feature]["rank"] = rank
        
        return {
            "dataset": dataset_name,
            "target_column": target_column,
            "method": "correlation_based",
            "feature_importance": feature_importance,
            "top_features": [f[0] for f in sorted_features[:5]],
            "features_analyzed": len(numerical_features)
        }
        
    except Exception as e:
        return {"error": f"Feature importance calculation failed: {str(e)}"}