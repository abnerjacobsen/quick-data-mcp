"""Tests for find_datasources prompt functionality."""

import pytest
import tempfile
import os
import json
import pandas as pd
from pathlib import Path

from mcp_server.prompts.find_datasources_prompt import find_datasources, format_file_size


class TestFindDatasources:
    """Test find_datasources prompt functionality."""
    
    @pytest.mark.asyncio
    async def test_find_datasources_with_files(self):
        """Test finding data sources in a directory with CSV and JSON files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            csv_file = temp_path / "sample_data.csv"
            pd.DataFrame({'id': [1, 2, 3]}).to_csv(csv_file, index=False)
            
            json_file = temp_path / "test_data.json"
            with open(json_file, 'w') as f:
                json.dump([{'id': 1}], f)
            
            result = await find_datasources(str(temp_path))
            
            assert isinstance(result, str)
            assert "Data Sources Found" in result
            assert "sample_data.csv" in result
            assert "test_data.json" in result
            assert "/load_dataset" in result
            assert "sample_data" in result
            assert "test_data" in result
    
    @pytest.mark.asyncio
    async def test_find_datasources_with_subdirectories(self):
        """Test finding data sources in subdirectories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            data_dir = temp_path / "data"
            data_dir.mkdir()
            
            csv_file = data_dir / "subdir_data.csv"
            pd.DataFrame({'x': [1, 2]}).to_csv(csv_file, index=False)
            
            result = await find_datasources(str(temp_path))
            
            assert isinstance(result, str)
            assert "Data Sources Found" in result
            assert str(Path("data") / "subdir_data.csv") in result
            assert "/load_dataset" in result
    
    @pytest.mark.asyncio
    async def test_find_datasources_no_files(self):
        """Test behavior when no data files are found."""
        with tempfile.TemporaryDirectory() as temp_dir:
            text_file = Path(temp_dir) / "readme.txt"
            text_file.write_text("This is not a data file")
            
            result = await find_datasources(temp_dir)
            
            assert isinstance(result, str)
            assert "No Data Sources Found" in result
            assert "Suggestion" in result
    
    @pytest.mark.asyncio
    async def test_find_datasources_current_directory(self):
        """Test finding data sources in current directory (default behavior)."""
        result = await find_datasources()
        
        assert isinstance(result, str)
        assert "Data Sources Found" in result
        assert ("data/" in result or "No Data Sources Found" in result)
    
    @pytest.mark.asyncio
    async def test_find_datasources_nonexistent_directory(self):
        """Test handling for non-existent directory."""
        result = await find_datasources("/nonexistent/directory/path")
        
        assert isinstance(result, str)
        assert "No Data Sources Found" in result
    
    @pytest.mark.asyncio
    async def test_find_datasources_special_characters_in_filename(self):
        """Test handling of files with special characters in names."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            csv_file = temp_path / "My Data-File.csv"
            pd.DataFrame({'a': [1]}).to_csv(csv_file, index=False)
            
            result = await find_datasources(str(temp_path))
            
            assert isinstance(result, str)
            assert "My Data-File.csv" in result
            assert "my_data_file" in result


class TestFormatFileSize:
    """Test format_file_size utility function."""
    
    def test_format_file_size_bytes(self):
        """Test formatting file sizes in bytes."""
        assert format_file_size(0) == "0 B"
        assert format_file_size(512) == "512 B"
        assert format_file_size(1023) == "1023 B"
    
    def test_format_file_size_kilobytes(self):
        """Test formatting file sizes in kilobytes."""
        assert format_file_size(1024) == "1.0 KB"
        assert format_file_size(2048) == "2.0 KB"
        assert format_file_size(1536) == "1.5 KB"
    
    def test_format_file_size_megabytes(self):
        """Test formatting file sizes in megabytes."""
        assert format_file_size(1024 * 1024) == "1.0 MB"
        assert format_file_size(1024 * 1024 * 2.5) == "2.5 MB"
    
    def test_format_file_size_gigabytes(self):
        """Test formatting file sizes in gigabytes."""
        assert format_file_size(1024 * 1024 * 1024) == "1.0 GB"
        assert format_file_size(1024 * 1024 * 1024 * 1.5) == "1.5 GB"


if __name__ == '__main__':
    pytest.main([__file__])