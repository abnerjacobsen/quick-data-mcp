"""Tests for list_mcp_assets prompt functionality."""

import pytest

from mcp_server.prompts.list_mcp_assets_prompt import list_mcp_assets


class TestListMcpAssets:
    """Test list_mcp_assets prompt functionality."""
    
    @pytest.mark.asyncio
    async def test_list_mcp_assets_returns_string(self):
        """Test that list_mcp_assets returns a string."""
        result = await list_mcp_assets()
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    @pytest.mark.asyncio
    async def test_list_mcp_assets_contains_sections(self):
        """Test that the output contains the expected sections."""
        result = await list_mcp_assets()
        
        assert "## 📝 Prompts" in result
        assert "## 🔧 Tools" in result
        assert "## 📊 Resources" in result
    
    @pytest.mark.asyncio
    async def test_list_mcp_assets_contains_key_prompts(self):
        """Test that key prompts are listed."""
        result = await list_mcp_assets()
        
        assert "dataset_first_look" in result
        assert "find_datasources" in result
    
    @pytest.mark.asyncio
    async def test_list_mcp_assets_contains_key_tools(self):
        """Test that key tools are listed."""
        result = await list_mcp_assets()
        
        assert "load_dataset" in result
        assert "create_chart" in result
        assert "execute_custom_analytics_code" in result
    
    @pytest.mark.asyncio
    async def test_list_mcp_assets_contains_key_resources(self):
        """Test that key resources are listed."""
        result = await list_mcp_assets()
        
        assert "datasets://loaded" in result
        assert "datasets://{dataset_name}/schema" in result
    
    @pytest.mark.asyncio
    async def test_list_mcp_assets_formatting(self):
        """Test that the output is properly formatted."""
        result = await list_mcp_assets()
        
        assert result.strip().startswith("#")
        assert "🚀" in result
        assert "- **/" in result  # Check for prompt/tool list format
        
    @pytest.mark.asyncio
    async def test_list_mcp_assets_subsections(self):
        """Test that tool subsections are present."""
        result = await list_mcp_assets()
        
        assert "### Data Management" in result
        assert "### Core Analytics" in result
        assert "### Advanced Operations" in result
        assert "### Input/Output" in result


if __name__ == '__main__':
    pytest.main([__file__])