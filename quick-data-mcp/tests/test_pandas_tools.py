"""Tests for pandas tools functionality."""

import pytest
import pandas as pd
import json
import tempfile
import os
from mcp_server.tools import (
    load_dataset, list_loaded_datasets, segment_by_column,
    find_correlations, create_chart, analyze_distributions,
    detect_outliers, suggest_analysis
)
from mcp_server.models.schemas import DatasetManager, loaded_datasets, dataset_schemas

@pytest.fixture
def sample_csv_file():
    data = {'id': range(5), 'category': ['A', 'B', 'A', 'C', 'B'], 'value': [10.5, 20.0, 15.5, 30.0, 25.5]}
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
async def test_load_dataset(sample_csv_file):
    result = await load_dataset(sample_csv_file, 'test_csv')
    assert result['status'] == 'loaded'
    assert 'test_csv' in loaded_datasets

@pytest.mark.asyncio
async def test_load_with_sampling(sample_csv_file):
    result = await load_dataset(sample_csv_file, 'test_sample', sample_size=3)
    assert result['rows'] == 3
    assert result['sampled'] is True

@pytest.mark.asyncio
async def test_list_loaded_datasets(sample_csv_file):
    await load_dataset(sample_csv_file, 'test1')
    await load_dataset(sample_csv_file, 'test2')
    result = await list_loaded_datasets()
    assert result['total_datasets'] == 2

@pytest.mark.asyncio
async def test_segment_by_column(sample_csv_file):
    await load_dataset(sample_csv_file, 'test_data')
    result = await segment_by_column('test_data', 'category')
    assert 'segments' in result
    assert result['segment_count'] > 0

@pytest.mark.asyncio
async def test_find_correlations(sample_csv_file):
    await load_dataset(sample_csv_file, 'test_data')
    result = await find_correlations('test_data')
    assert 'correlation_matrix' in result

@pytest.mark.asyncio
async def test_find_correlations_insufficient_columns():
    df = pd.DataFrame({'a': range(5)})
    DatasetManager.load_dataset(df, 'test_data')
    result = await find_correlations('test_data')
    assert 'error' in result and 'two' in result['error']

@pytest.mark.asyncio
async def test_create_chart(sample_csv_file):
    await load_dataset(sample_csv_file, 'test_data')
    result = await create_chart('test_data', 'histogram', 'value')
    assert result['status'] == 'success' and 'chart_file' in result
    if result.get('chart_file'):
        os.unlink(result['chart_file'])

@pytest.mark.asyncio
async def test_analyze_distributions(sample_csv_file):
    await load_dataset(sample_csv_file, 'test_data')
    result = await analyze_distributions('test_data', 'value')
    assert result['distribution_type'] == 'numerical'

@pytest.mark.asyncio
async def test_detect_outliers(sample_csv_file):
    await load_dataset(sample_csv_file, 'test_data')
    result = await detect_outliers('test_data')
    assert 'outliers_by_column' in result

@pytest.mark.asyncio
async def test_suggest_analysis(sample_csv_file):
    await load_dataset(sample_csv_file, 'test_data')
    result = await suggest_analysis('test_data')
    assert 'suggestions' in result and len(result['suggestions']) > 0

@pytest.mark.asyncio
async def test_suggest_analysis_nonexistent_dataset():
    result = await suggest_analysis('nonexistent')
    assert 'error' in result and 'not found' in result['error']