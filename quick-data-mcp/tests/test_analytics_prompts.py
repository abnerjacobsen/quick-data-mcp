"""Tests for analytics prompts functionality."""

import pytest
import pandas as pd
import tempfile
import os
from mcp_server import prompts
from mcp_server.models.schemas import DatasetManager, loaded_datasets, dataset_schemas

@pytest.fixture
def sample_dataset():
    data = {
        'order_id': [f'ord_00{i}' for i in range(1, 6)],
        'customer_id': [f'cust_12{i}' for i in range(3, 8)],
        'product_category': ['electronics', 'books', 'clothing', 'electronics', 'home_garden'],
        'order_value': [299.99, 29.99, 89.50, 599.99, 149.99],
        'order_date': pd.to_datetime(['2024-01-15', '2024-01-14', '2024-01-13', '2024-01-12', '2024-01-11']),
        'region': ['west_coast', 'midwest', 'east_coast', 'west_coast', 'south'],
        'customer_segment': ['premium', 'standard', 'premium', 'premium', 'standard']
    }
    df = pd.DataFrame(data)
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as f:
        df.to_csv(f.name, index=False)
        yield f.name
    os.unlink(f.name)

@pytest.fixture
def simple_dataset():
    data = {'id': range(5), 'name': [f'name_{i}' for i in range(5)]}
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
async def test_all_prompts_return_strings(sample_dataset):
    DatasetManager.load_dataset(sample_dataset, 'test_data')
    for prompt_func in [
        prompts.dataset_first_look, prompts.segmentation_workshop,
        prompts.data_quality_assessment, prompts.correlation_investigation,
        prompts.pattern_discovery_session
    ]:
        result = await prompt_func('test_data')
        assert isinstance(result, str) and len(result) > 0

@pytest.mark.asyncio
async def test_prompts_with_context(sample_dataset):
    DatasetManager.load_dataset(sample_dataset, 'test_data')
    for context in ['sales', 'marketing']:
        result = await prompts.insight_generation_workshop('test_data', context)
        assert isinstance(result, str) and context in result.lower()
    for audience in ['executive', 'analyst']:
        result = await prompts.dashboard_design_consultation('test_data', audience)
        assert isinstance(result, str) and audience in result.lower()

@pytest.mark.asyncio
async def test_nonexistent_dataset_errors():
    for prompt_func in [
        prompts.dataset_first_look, prompts.segmentation_workshop,
        prompts.data_quality_assessment, prompts.correlation_investigation,
        prompts.pattern_discovery_session, prompts.insight_generation_workshop,
        prompts.dashboard_design_consultation
    ]:
        result = await prompt_func('nonexistent_dataset')
        assert isinstance(result, str) and 'not found' in result.lower()

@pytest.mark.asyncio
async def test_first_look_prompt(sample_dataset):
    DatasetManager.load_dataset(sample_dataset, 'ecommerce')
    result = await prompts.dataset_first_look('ecommerce')
    assert 'First Look' in result and 'ecommerce' in result and '5 rows' in result

@pytest.mark.asyncio
async def test_segmentation_prompt(sample_dataset):
    DatasetManager.load_dataset(sample_dataset, 'ecommerce')
    result = await prompts.segmentation_workshop('ecommerce')
    assert 'Segmentation Workshop' in result and 'ecommerce' in result

@pytest.mark.asyncio
async def test_data_quality_prompt(sample_dataset):
    DatasetManager.load_dataset(sample_dataset, 'ecommerce')
    result = await prompts.data_quality_assessment('ecommerce')
    assert 'Data Quality Assessment' in result and 'ecommerce' in result

@pytest.mark.asyncio
async def test_correlation_prompt(sample_dataset):
    DatasetManager.load_dataset(sample_dataset, 'ecommerce')
    result = await prompts.correlation_investigation('ecommerce')
    assert 'Correlation Investigation' in result or 'Not Possible' in result

@pytest.mark.asyncio
async def test_pattern_discovery_prompt(sample_dataset):
    DatasetManager.load_dataset(sample_dataset, 'ecommerce')
    result = await prompts.pattern_discovery_session('ecommerce')
    assert 'Pattern Discovery Session' in result

@pytest.mark.asyncio
async def test_insight_workshop_prompt(sample_dataset):
    DatasetManager.load_dataset(sample_dataset, 'ecommerce')
    result = await prompts.insight_generation_workshop('ecommerce')
    assert 'Insight Generation Workshop' in result

@pytest.mark.asyncio
async def test_dashboard_design_prompt(sample_dataset):
    DatasetManager.load_dataset(sample_dataset, 'ecommerce')
    result = await prompts.dashboard_design_consultation('ecommerce')
    assert 'Dashboard Design Consultation' in result