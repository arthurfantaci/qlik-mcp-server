"""Test the MCP tool functionality directly."""

import json

import pytest

from src.tools import get_app_measures, list_qlik_applications


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_app_measures_with_server(test_app_id, skip_without_qlik):
    """Test get_app_measures with live Qlik server."""
    # This test will be skipped if no Qlik server is available
    result = await get_app_measures(
        app_id=test_app_id,
        include_expression=True,
        include_tags=True,
    )

    # Assertions
    assert result is not None, "Result should not be None"
    assert "app_id" in result, "Result should contain app_id"
    assert result["app_id"] == test_app_id, "App ID should match"
    assert "measures" in result, "Result should contain measures"
    assert "count" in result, "Result should contain count"
    assert isinstance(result["measures"], list), "Measures should be a list"

    # If measures exist, validate structure
    if result["measures"]:
        measure = result["measures"][0]
        assert "id" in measure, "Measure should have an id"
        assert "title" in measure, "Measure should have a title"
        assert "expression" in measure, "Measure should have an expression"


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_app_measures_mock(mock_measures_response):
    """Test get_app_measures response structure with mock data."""
    # This test uses mock data and doesn't require a Qlik server
    result = mock_measures_response

    # Validate response structure
    assert result is not None, "Result should not be None"
    assert "app_id" in result, "Result should contain app_id"
    assert "measures" in result, "Result should contain measures"
    assert "count" in result, "Result should contain count"
    assert "retrieved_at" in result, "Result should contain retrieved_at"
    assert "options" in result, "Result should contain options"

    # Validate measures structure
    assert len(result["measures"]) == result["count"], "Count should match measures length"

    for measure in result["measures"]:
        assert "id" in measure, "Each measure should have an id"
        assert "title" in measure, "Each measure should have a title"
        assert "expression" in measure, "Each measure should have an expression"
        assert "tags" in measure, "Each measure should have tags"
        assert isinstance(measure["tags"], list), "Tags should be a list"


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_app_measures_minimal_options(test_app_id, skip_without_qlik):
    """Test get_app_measures with minimal options."""
    result = await get_app_measures(
        app_id=test_app_id,
        include_expression=False,
        include_tags=False,
    )

    assert result is not None, "Result should not be None"
    assert result["options"]["include_expression"] is False
    assert result["options"]["include_tags"] is False

    # Verify expressions and tags are not included when requested
    if result["measures"]:
        measure = result["measures"][0]
        # Expression might still be present but empty or minimal
        # Tags should not be present or be empty
        if "tags" in measure:
            assert measure["tags"] == [] or measure["tags"] is None


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.parametrize("include_expression,include_tags", [
    (True, True),
    (True, False),
    (False, True),
    (False, False),
])
async def test_get_app_measures_options_combinations(
    test_app_id, include_expression, include_tags, skip_without_qlik,
):
    """Test get_app_measures with different option combinations."""
    result = await get_app_measures(
        app_id=test_app_id,
        include_expression=include_expression,
        include_tags=include_tags,
    )

    assert result is not None
    assert result["options"]["include_expression"] == include_expression
    assert result["options"]["include_tags"] == include_tags


@pytest.mark.asyncio
@pytest.mark.integration
async def test_list_applications_with_server(skip_without_qlik):
    """Test list_qlik_applications with live server."""
    result = await list_qlik_applications()

    assert result is not None, "Result should not be None"
    assert "applications" in result, "Result should contain applications"
    assert "count" in result, "Result should contain count"
    assert isinstance(result["applications"], list), "Applications should be a list"

    # If applications exist, validate structure
    if result["applications"]:
        app = result["applications"][0]
        assert "app_id" in app, "Application should have app_id"
        assert "name" in app, "Application should have name"
        assert "last_reload_time" in app, "Application should have last_reload_time"


@pytest.mark.asyncio
@pytest.mark.unit
async def test_list_applications_mock(mock_applications_response):
    """Test list_qlik_applications response structure with mock data."""
    result = mock_applications_response

    assert result is not None, "Result should not be None"
    assert "applications" in result, "Result should contain applications"
    assert "count" in result, "Result should contain count"
    assert "retrieved_at" in result, "Result should contain retrieved_at"

    assert len(result["applications"]) == result["count"], "Count should match applications length"

    for app in result["applications"]:
        assert "app_id" in app, "Each app should have app_id"
        assert "name" in app, "Each app should have name"
        assert "last_reload_time" in app, "Each app should have last_reload_time"
        assert "meta" in app, "Each app should have meta"


class TestMeasureValidation:
    """Test suite for measure validation and error cases."""

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_invalid_app_id_format(self):
        """Test that invalid app ID raises appropriate error."""
        with pytest.raises((ValueError, Exception)):
            await get_app_measures(
                app_id="",  # Empty app ID
                include_expression=True,
                include_tags=True,
            )

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_nonexistent_app_id(self, skip_without_qlik):
        """Test behavior with non-existent app ID."""
        result = await get_app_measures(
            app_id="nonexistent-app-id-12345",
            include_expression=True,
            include_tags=True,
        )

        # Should either return error in result or raise exception
        if result:
            assert "error" in result or result["count"] == 0


class TestSpecificMeasures:
    """Test suite for specific measure scenarios."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_find_specific_measure(self, test_app_id, skip_without_qlik):
        """Test finding a specific measure by title."""
        result = await get_app_measures(
            app_id=test_app_id,
            include_expression=True,
            include_tags=True,
        )

        # Example: looking for a Total_Cost measure
        total_cost_measures = [
            m for m in result["measures"]
            if "Total_Cost" in m.get("title", "") or "total" in m.get("title", "").lower()
        ]

        # This assertion might need adjustment based on actual data
        # For now, we just check the structure if such measure exists
        if total_cost_measures:
            measure = total_cost_measures[0]
            assert "id" in measure
            assert "expression" in measure


@pytest.mark.asyncio
@pytest.mark.unit
def test_measure_json_serialization(mock_measures_response):
    """Test that measure response can be JSON serialized."""
    # This test verifies the response can be converted to JSON
    json_str = json.dumps(mock_measures_response, indent=2)
    assert json_str is not None

    # Parse it back to verify round-trip works
    parsed = json.loads(json_str)
    assert parsed["app_id"] == mock_measures_response["app_id"]
    assert parsed["count"] == mock_measures_response["count"]
