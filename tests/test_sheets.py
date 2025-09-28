"""Test sheet and visualization object functionality"""

import pytest

from src.tools import get_app_sheets, get_sheet_objects


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_sheets():
    """Test sheet retrieval"""
    test_app_id = "12345678-abcd-1234-efgh-123456789abc"

    result = await get_app_sheets(
        app_id=test_app_id,
        include_thumbnail=False,
        include_objects=True,
    )

    # Verify response structure
    assert "error" not in result, f"Error retrieving sheets: {result.get('error')}"
    assert "sheet_count" in result
    assert "sheets" in result
    assert isinstance(result["sheets"], list)

    # Verify sheet structure if sheets exist
    if result["sheet_count"] > 0:
        sheet = result["sheets"][0]
        assert "sheet_id" in sheet
        assert "title" in sheet
        assert "description" in sheet
        assert "object_count" in sheet

        # Since we requested objects, they should be included
        if sheet["object_count"] > 0:
            assert "objects" in sheet


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_sheet_objects():
    """Test retrieving objects from a specific sheet"""
    test_app_id = "12345678-abcd-1234-efgh-123456789abc"
    test_sheet_id = "test-sheet-id"

    result = await get_sheet_objects(
        app_id=test_app_id,
        sheet_id=test_sheet_id,
        include_expressions=True,
        resolve_master_items=True,
        extract_vizlib_objects=True,
    )

    # Verify response structure
    assert "error" not in result or result.get("error") == "Sheet not found"

    if "error" not in result:
        assert "sheet_id" in result
        assert "object_count" in result
        assert "objects" in result
        assert isinstance(result["objects"], list)

        # Verify object structure if objects exist
        if result["object_count"] > 0:
            obj = result["objects"][0]
            assert "object_id" in obj
            assert "type" in obj
            assert "title" in obj
            assert "visualization" in obj


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sheets_error_handling():
    """Test error handling with invalid app ID"""
    result = await get_app_sheets(
        app_id="invalid-app-id",
        include_objects=True,
    )

    # Should return an error for invalid app
    assert "error" in result
