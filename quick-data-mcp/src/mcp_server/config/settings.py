"""
Server configuration settings.

This module defines the configuration for the MCP server application using
a Settings class. It loads settings from environment variables,
providing default values for essential configurations.
"""

import os
from typing import Optional


class Settings:
    """
    Manages application settings for the MCP server.

    This class centralizes all configuration variables, loading them from
    environment variables where available, and providing sensible defaults.

    Attributes:
        server_name (str): The name of the MCP server.
        version (str): The version of the server application.
        log_level (str): The logging level for the application (e.g., 'INFO', 'DEBUG').
        api_key (Optional[str]): An optional API key for securing server access.
        database_url (Optional[str]): An optional database connection string.
    """
    
    def __init__(self):
        """Initializes the Settings object, loading values from environment variables."""
        self.server_name = "Modular MCP Server"
        self.version = "0.1.0"
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.api_key: Optional[str] = os.getenv("API_KEY")
        self.database_url: Optional[str] = os.getenv("DATABASE_URL")
    
    @property
    def server_info(self) -> dict:
        """
        Provides a dictionary with key server information.

        Returns:
            dict: A dictionary containing the server's name, version, and log level.
        """
        return {
            "name": self.server_name,
            "version": self.version,
            "log_level": self.log_level
        }

# Global instance of the Settings class to be used throughout the application.
settings = Settings()