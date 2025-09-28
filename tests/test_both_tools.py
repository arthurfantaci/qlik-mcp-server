"""Test both MCP tools working together"""

import pytest

from src.tools import get_app_measures, list_qlik_applications


@pytest.mark.integration
@pytest.mark.asyncio
async def test_both_tools_integration():
    """Test both MCP tools working together in an integrated workflow"""
    # Step 1: List all applications
    apps_result = await list_qlik_applications()

    # Verify we can list applications
    assert "error" not in apps_result, f"Error listing apps: {apps_result.get('error')}"
    assert "count" in apps_result
    assert "applications" in apps_result
    assert apps_result["count"] >= 0

    # Skip test if no applications are available
    if apps_result["count"] == 0:
        pytest.skip("No Qlik applications available for testing")

    # Use the first available app for testing
    test_app = apps_result["applications"][0]
    test_app_id = test_app["app_id"]

    # Verify app structure
    assert "app_id" in test_app
    assert "name" in test_app
    assert "last_reload_time" in test_app

    # Step 2: Get measures from the selected app
    measures_result = await get_app_measures(
        app_id=test_app_id,
        include_expression=True,
        include_tags=True,
    )

    # Verify we can get measures
    assert "error" not in measures_result, f"Error getting measures: {measures_result.get('error')}"
    assert "count" in measures_result
    assert "measures" in measures_result
    assert measures_result["count"] >= 0

    # If measures exist, verify their structure
    if measures_result["count"] > 0:
        measure = measures_result["measures"][0]
        assert "id" in measure
        assert "title" in measure
        # If we requested expression and tags, they should be present
        assert "expression" in measure
        assert "tags" in measure


@pytest.mark.integration
@pytest.mark.asyncio
async def test_tools_workflow():
    """Test a complete workflow using both tools"""
    # First get list of applications
    apps_result = await list_qlik_applications()
    assert "error" not in apps_result

    # If apps exist, get measures from one of them
    if apps_result["count"] > 0:
        app = apps_result["applications"][0]
        measures_result = await get_app_measures(app_id=app["app_id"])
        assert "error" not in measures_result

        # Verify the workflow completed successfully
        assert isinstance(apps_result["count"], int)
        assert isinstance(measures_result["count"], int)
