"""Test the get_app_variables functionality"""

import pytest

from src.tools import get_app_variables


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_variables_full():
    """Test variable retrieval with all options"""
    test_app_id = "12345678-abcd-1234-efgh-123456789abc"

    result = await get_app_variables(
        app_id=test_app_id,
        include_definition=True,
        include_tags=True,
        include_comments=True,
    )

    # Verify response structure
    assert "error" not in result, f"Error retrieving variables: {result.get('error')}"
    assert "variable_count" in result
    assert "variables" in result
    assert "app_id" in result
    assert "retrieved_at" in result
    assert isinstance(result["variables"], list)

    # Verify variable structure if variables exist
    if result["variable_count"] > 0:
        variable = result["variables"][0]
        assert "name" in variable
        # Since we requested all options, these should be present
        assert "definition" in variable
        assert "tags" in variable
        assert "comment" in variable


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_variables_minimal():
    """Test variable retrieval with minimal options"""
    test_app_id = "12345678-abcd-1234-efgh-123456789abc"

    result = await get_app_variables(
        app_id=test_app_id,
        include_definition=False,
        include_tags=False,
        include_comments=False,
    )

    # Verify response structure
    assert "error" not in result or result.get("error") == "App not found"
    if "error" not in result:
        assert "variable_count" in result
        assert "variables" in result


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_variables_error_handling():
    """Test error handling with invalid app ID"""
    result = await get_app_variables(
        app_id="invalid-app-id",
        include_definition=True,
    )

    # Should return an error for invalid app
    assert "error" in result
