"""
Prompts Package for the Generic Data Analytics MCP Server.

This package aggregates all the individual prompt-generating functions from
the various modules in this directory. These functions typically generate
dynamic, context-aware text that can be used to guide a user or an AI
through a specific data analysis workflow.
"""

from .dataset_first_look_prompt import dataset_first_look
from .segmentation_workshop_prompt import segmentation_workshop
from .data_quality_assessment_prompt import data_quality_assessment
from .correlation_investigation_prompt import correlation_investigation
from .pattern_discovery_session_prompt import pattern_discovery_session
from .insight_generation_workshop_prompt import insight_generation_workshop
from .dashboard_design_consultation_prompt import dashboard_design_consultation
from .find_datasources_prompt import find_datasources
from .list_mcp_assets_prompt import list_mcp_assets

__all__ = [
    "dataset_first_look",
    "segmentation_workshop", 
    "data_quality_assessment",
    "correlation_investigation",
    "pattern_discovery_session",
    "insight_generation_workshop",
    "dashboard_design_consultation",
    "find_datasources",
    "list_mcp_assets"
]