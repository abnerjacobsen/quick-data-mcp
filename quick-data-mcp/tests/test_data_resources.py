"""Tests for data resources."""

import pytest
from mcp_server.resources import data_resources
from mcp_server.config.settings import settings


@pytest.mark.asyncio
async def test_get_server_config():
    """Test getting server configuration."""
    config = await data_resources.get_server_config()
    
    assert isinstance(config, dict)
    assert config["server_name"] == settings.server_name
    assert config["server_version"] == settings.version
    assert "supported_formats" in config


@pytest.mark.asyncio
async def test_get_user_profile():
    """Test getting user profile by ID."""
    user_id = "test123"
    profile = await data_resources.get_user_profile(user_id)
    
    assert isinstance(profile, dict)
    assert profile["id"] == user_id
    assert profile["name"] == f"User {user_id}"
    assert profile["email"] == f"user.{user_id}@example.com"


@pytest.mark.asyncio
async def test_get_system_status():
    """Test getting system status information."""
    status = await data_resources.get_system_status()
    
    assert isinstance(status, dict)
    assert status["status"] == "healthy"
    assert status["version"] == settings.version
    assert "datasets_loaded" in status
    assert "total_memory_mb" in status


@pytest.mark.asyncio
async def test_user_profile_different_ids():
    """Test user profiles with different IDs."""
    user_ids = ["user1", "admin", "test_user_123"]
    
    for user_id in user_ids:
        profile = await data_resources.get_user_profile(user_id)
        assert profile["id"] == user_id
        assert profile["name"] == f"User {user_id}"
        assert profile["email"] == f"user.{user_id}@example.com"