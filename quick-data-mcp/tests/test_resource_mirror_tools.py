"""Tests for resource mirror tools that provide tool-only client compatibility."""

import pytest
from mcp_server.server import mcp
from mcp_server.resources import data_resources
from fastmcp import Client


@pytest.mark.asyncio
class TestResourceMirrorTools:
    """Test resource mirror tools provide identical functionality to resources."""
    
    async def test_resource_datasets_loaded_matches_resource(self):
        """Ensure tool matches resource output for loaded datasets."""
        async with Client(mcp) as client:
            tool_result = await client.call_tool('resource_datasets_loaded')
            resource_result = await data_resources.get_loaded_datasets()
            assert tool_result.data == resource_result

    async def test_resource_config_server_matches_resource(self):
        """Ensure tool matches resource output for server config."""
        async with Client(mcp) as client:
            tool_result = await client.call_tool('resource_config_server')
            resource_result = await data_resources.get_server_config()
            assert tool_result.data == resource_result

    async def test_resource_users_profile_matches_resource(self):
        """Ensure tool matches resource output for user profiles."""
        user_id = "test123"
        async with Client(mcp) as client:
            tool_result = await client.call_tool('resource_users_profile', {'user_id': user_id})
            resource_result = await data_resources.get_user_profile(user_id)
            assert tool_result.data == resource_result

    async def test_resource_system_status_matches_resource(self):
        """Ensure tool matches resource output for system status."""
        async with Client(mcp) as client:
            tool_result = await client.call_tool('resource_system_status')
            resource_result = await data_resources.get_system_status()
            assert tool_result.data == resource_result