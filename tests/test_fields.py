"""Test the get_app_fields functionality"""

import pytest

from src.tools import get_app_fields


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_fields_full():
    """Test field retrieval with all options enabled"""
    test_app_id = "12345678-abcd-1234-efgh-123456789abc"

    # Test with all options enabled
    result = await get_app_fields(
        app_id=test_app_id,
        show_system=True,
        show_hidden=True,
        show_derived_fields=True,
        show_semantic=True,
        show_src_tables=True,
        show_implicit=True,
    )

    # Verify response structure
    assert "error" not in result, f"Error retrieving fields: {result.get('error')}"
    assert "field_count" in result
    assert "table_count" in result
    assert "app_id" in result
    assert "retrieved_at" in result
    assert "options" in result
    assert "fields" in result
    assert "tables" in result

    # Verify field structure if fields exist
    if result["field_count"] > 0:
        field = result["fields"][0]
        assert "name" in field
        # Since we requested all options, these should be present
        assert "is_system" in field
        assert "is_hidden" in field
        assert "is_numeric" in field
        assert "cardinal" in field
        assert "source_tables" in field


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_fields_minimal():
    """Test field retrieval with minimal options"""
    test_app_id = "12345678-abcd-1234-efgh-123456789abc"

    result = await get_app_fields(
        app_id=test_app_id,
        show_system=False,
        show_hidden=False,
        show_derived_fields=False,
        show_semantic=False,
        show_src_tables=False,
        show_implicit=False,
    )

    # Verify response structure
    assert "error" not in result or result.get("error") == "App not found"
    if "error" not in result:
        assert "field_count" in result
        assert "fields" in result


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_fields_error_handling():
    """Test error handling with invalid app ID"""
    result = await get_app_fields(
        app_id="invalid-app-id",
        show_system=True,
    )

    # Should return an error for invalid app
    assert "error" in result
