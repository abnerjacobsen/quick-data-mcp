"""Tests for analytics tools functionality."""

import pytest
import pandas as pd
import os
import tempfile
from mcp_server import tools
from mcp_server.models.schemas import DatasetManager, loaded_datasets, dataset_schemas

@pytest.fixture
def sample_dataset():
    """Create a sample dataset for testing."""
    data = {'id': range(10), 'value': [i*2 for i in range(10)], 'category': ['A', 'B'] * 5}
    df = pd.DataFrame(data)
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as f:
        df.to_csv(f.name, index=False)
        yield f.name
    os.unlink(f.name)

@pytest.fixture(autouse=True)
def clear_datasets_fixture():
    loaded_datasets.clear()
    dataset_schemas.clear()
    yield
    loaded_datasets.clear()
    dataset_schemas.clear()

@pytest.mark.asyncio
async def test_validate_data_quality(sample_dataset):
    DatasetManager.load_dataset(sample_dataset, 'test_data')
    result = await tools.validate_data_quality('test_data')
    assert result['dataset_name'] == 'test_data'
    assert 'quality_score' in result

@pytest.mark.asyncio
async def test_compare_datasets(sample_dataset):
    DatasetManager.load_dataset(sample_dataset, 'dataset_a')
    DatasetManager.load_dataset(sample_dataset, 'dataset_b')
    result = await tools.compare_datasets('dataset_a', 'dataset_b')
    assert result['dataset_a'] == 'dataset_a'
    assert 'column_comparisons' in result

@pytest.mark.asyncio
async def test_merge_datasets(sample_dataset):
    DatasetManager.load_dataset(sample_dataset, 'dataset_a')
    df_b = pd.DataFrame({'id': range(5), 'value_b': [i*3 for i in range(5)]})
    DatasetManager.load_dataset(df_b, 'dataset_b')
    dataset_configs = [{'dataset_name': 'dataset_a'}, {'dataset_name': 'dataset_b', 'join_column': 'id'}]
    result = await tools.merge_datasets(dataset_configs)
    assert result['status'] == 'success'
    assert 'merged_dataset_name' in result

@pytest.mark.asyncio
async def test_merge_insufficient_datasets():
    result = await tools.merge_datasets([{'dataset_name': 'd1'}])
    assert 'error' in result and 'at least two' in result['error']

@pytest.mark.asyncio
async def test_generate_dashboard(sample_dataset):
    DatasetManager.load_dataset(sample_dataset, 'test_data')
    chart_configs = [{'chart_type': 'bar', 'x_column': 'category'}]
    result = await tools.generate_dashboard('test_data', chart_configs)
    assert 'summary' in result and result['summary']['successful_charts'] == 1

@pytest.mark.asyncio
async def test_export_insights(sample_dataset):
    DatasetManager.load_dataset(sample_dataset, 'test_data')
    result = await tools.export_insights('test_data', 'json')
    assert result['status'] == 'success' and 'export_file' in result
    if result.get('export_file'):
        os.unlink(result['export_file'])

@pytest.mark.asyncio
async def test_calculate_feature_importance(sample_dataset):
    DatasetManager.load_dataset(sample_dataset, 'test_data')
    result = await tools.calculate_feature_importance('test_data', 'value')
    assert 'feature_importance' in result

@pytest.mark.asyncio
async def test_memory_optimization_report(sample_dataset):
    DatasetManager.load_dataset(sample_dataset, 'test_data')
    result = await tools.memory_optimization_report('test_data')
    assert 'current_memory_mb' in result
    assert 'potential_savings_mb' in result