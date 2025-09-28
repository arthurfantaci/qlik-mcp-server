"""Test application script retrieval functionality"""

import pytest

from src.tools import get_app_script


@pytest.mark.integration
@pytest.mark.asyncio
async def test_script_basic():
    """Test basic script retrieval"""
    test_app_id = "12345678-abcd-1234-efgh-123456789abc"

    result = await get_app_script(app_id=test_app_id)

    # Verify response structure
    assert "error" not in result, f"Error retrieving script: {result.get('error')}"
    assert "app_id" in result
    assert "script" in result
    assert "retrieved_at" in result


@pytest.mark.integration
@pytest.mark.asyncio
async def test_script_with_analysis():
    """Test script retrieval with full analysis"""
    test_app_id = "12345678-abcd-1234-efgh-123456789abc"

    result = await get_app_script(
        app_id=test_app_id,
        analyze_script=True,
        include_sections=True,
        mask_credentials=True,
    )

    # Verify response structure
    assert "error" not in result or result.get("error") == "App not found"

    if "error" not in result:
        assert "app_id" in result
        assert "script" in result
        assert "analysis" in result

        # Verify analysis structure when requested
        analysis = result.get("analysis", {})
        assert "total_lines" in analysis
        assert "sections" in analysis
        assert "load_statements" in analysis
        assert "store_statements" in analysis
        assert "drop_statements" in analysis
        assert "binary_load_statements" in analysis


@pytest.mark.integration
@pytest.mark.asyncio
async def test_script_error_handling():
    """Test error handling with invalid app ID"""
    result = await get_app_script(
        app_id="invalid-app-id",
        analyze_script=True,
    )

    # Should return an error for invalid app
    assert "error" in result
