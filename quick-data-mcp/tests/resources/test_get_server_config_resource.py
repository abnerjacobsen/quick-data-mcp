"""Tests for get_server_config resource functionality."""

import pytest
from mcp_server.resources.data_resources import get_server_config
from mcp_server.config.settings import settings


class TestGetServerConfig:
    """Test get_server_config resource functionality."""
    
    @pytest.mark.asyncio
    async def test_get_server_config(self):
        """Test getting server configuration."""
        config = await get_server_config()
        
        assert isinstance(config, dict)
        assert config["server_name"] == settings.server_name
        assert config["server_version"] == settings.version
        assert "supported_formats" in config
        assert "csv" in config["supported_formats"]
        assert "json" in config["supported_formats"]


if __name__ == '__main__':
    pytest.main([__file__])