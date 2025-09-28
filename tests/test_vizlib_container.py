"""Test VizlibContainer functionality"""

import pytest

from src.tools import get_sheet_objects


@pytest.mark.integration
@pytest.mark.asyncio
async def test_vizlib_container_extraction():
    """Test VizlibContainer object extraction and Master Item resolution"""
    test_app_id = "12345678-abcd-1234-efgh-123456789abc"
    test_sheet_id = "11111111-2222-3333-4444-555555555555"

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

        # Look for VizlibContainer objects
        vizlib_containers = [
            obj for obj in result["objects"]
            if obj.get("type") == "VizlibContainer"
        ]

        # If VizlibContainer exists, verify extraction
        for container in vizlib_containers:
            assert "object_id" in container
            assert "type" in container
            assert container["type"] == "VizlibContainer"

            # Check if embedded objects were extracted
            if "embedded_objects" in container:
                for embedded in container["embedded_objects"]:
                    assert "object_id" in embedded
                    assert "type" in embedded
                    assert "visualization" in embedded


@pytest.mark.integration
@pytest.mark.asyncio
async def test_vizlib_container_master_item_resolution():
    """Test Master Item resolution in VizlibContainer"""
    test_app_id = "12345678-abcd-1234-efgh-123456789abc"
    test_sheet_id = "test-sheet-with-vizlib"

    result = await get_sheet_objects(
        app_id=test_app_id,
        sheet_id=test_sheet_id,
        include_expressions=True,
        resolve_master_items=True,
        extract_vizlib_objects=True,
    )

    if "error" not in result and result["object_count"] > 0:
        # Check for master item resolution in any object
        for obj in result["objects"]:
            if "master_item_resolved" in obj:
                assert obj["master_item_resolved"] is True
                assert "master_item_id" in obj
                assert "visualization" in obj


@pytest.mark.integration
@pytest.mark.asyncio
async def test_vizlib_container_error_handling():
    """Test error handling for VizlibContainer extraction"""
    result = await get_sheet_objects(
        app_id="invalid-app-id",
        sheet_id="invalid-sheet-id",
        extract_vizlib_objects=True,
    )

    # Should return an error for invalid IDs
    assert "error" in result
