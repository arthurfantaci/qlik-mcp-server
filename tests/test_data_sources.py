"""Test data sources lineage retrieval functionality"""

import pytest

from src.tools import get_app_data_sources


@pytest.mark.integration
@pytest.mark.asyncio
async def test_data_sources_full_retrieval():
    """Test full data sources retrieval with all types"""
    # Test app ID
    test_app_id = "12345678-abcd-1234-efgh-123456789abc"

    # Test with all data source types included
    result = await get_app_data_sources(
        app_id=test_app_id,
        include_resident=True,
        include_file_sources=True,
        include_binary_sources=True,
        include_inline_sources=True,
    )

    # Verify response structure
    assert "error" not in result, f"Error retrieving data sources: {result.get('error')}"

    assert "source_count" in result
    assert "app_id" in result
    assert "retrieved_at" in result
    assert "options" in result
    assert "categories" in result

    # Verify category structure
    categories = result.get("categories", {})
    assert isinstance(categories, dict)

    # Verify data source structure if sources exist
    if result["source_count"] > 0:
        assert "by_category" in result
        by_category = result.get("by_category", {})
        assert isinstance(by_category, dict)

        # Verify each source has required fields
        for category, sources in by_category.items():
            for source in sources:
                assert "discriminator" in source
                assert "id" in source



@pytest.mark.integration
@pytest.mark.asyncio
async def test_data_sources_binary_only():
    """Test retrieving only binary sources"""
    test_app_id = "12345678-abcd-1234-efgh-123456789abc"

    result = await get_app_data_sources(
        app_id=test_app_id,
        include_resident=False,
        include_file_sources=False,
        include_binary_sources=True,
        include_inline_sources=False,
    )

    # Verify response structure
    assert "error" not in result or result.get("error") == "App not found"
    if "error" not in result:
        assert "categories" in result
        # Only binary sources should be included
        categories = result["categories"]
        assert categories.get("file_count", 0) == 0
        assert categories.get("resident_count", 0) == 0
        assert categories.get("inline_count", 0) == 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_data_sources_error_handling():
    """Test error handling with invalid app ID"""
    result = await get_app_data_sources(
        app_id="invalid-app-id-12345",
        include_resident=True,
    )

    # Should return an error for invalid app
    assert "error" in result
