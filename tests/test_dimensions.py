"""Test dimension retrieval functionality"""

import pytest

from src.tools import get_app_dimensions


@pytest.mark.integration
@pytest.mark.asyncio
async def test_dimensions_full_retrieval():
    """Test full dimension retrieval with all options"""
    test_app_id = "12345678-abcd-1234-efgh-123456789abc"

    # Test with all options enabled
    result = await get_app_dimensions(
        app_id=test_app_id,
        include_title=True,
        include_tags=True,
        include_grouping=True,
        include_info=True,
    )

    # Verify response structure
    assert "error" not in result, f"Error retrieving dimensions: {result.get('error')}"

    assert "dimension_count" in result
    assert "app_id" in result
    assert "retrieved_at" in result
    assert "options" in result
    assert "dimensions" in result

    # If dimensions exist, verify their structure
    if result["dimension_count"] > 0:
        dimension = result["dimensions"][0]
        assert "dimension_id" in dimension
        # Verify optional fields were included as requested
        assert "title" in dimension or "name" in dimension
        assert "tags" in dimension
        assert "grouping" in dimension



@pytest.mark.integration
@pytest.mark.asyncio
async def test_dimensions_minimal_options():
    """Test dimension retrieval with minimal options"""
    test_app_id = "12345678-abcd-1234-efgh-123456789abc"

    result = await get_app_dimensions(
        app_id=test_app_id,
        include_title=False,
        include_tags=False,
        include_grouping=False,
        include_info=False,
    )

    # Verify response structure
    assert "error" not in result or result.get("error") == "App not found"
    if "error" not in result:
        assert "dimension_count" in result
        assert "dimensions" in result


@pytest.mark.integration
@pytest.mark.asyncio
async def test_dimensions_error_handling():
    """Test error handling with invalid app ID"""
    result = await get_app_dimensions(
        app_id="invalid-app-id-12345",
        include_title=True,
    )

    # Should return an error for invalid app
    assert "error" in result
