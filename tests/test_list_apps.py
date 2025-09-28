"""Test listing Qlik applications"""

import pytest

from src.qlik_client import QlikClient
from src.tools import list_qlik_applications


@pytest.mark.integration
def test_qlik_client_list_apps():
    """Test the QlikClient get_doc_list method directly"""
    client = QlikClient()

    # Connect to global context
    assert client.connect_global(), "Failed to connect to Qlik Engine"

    try:
        # Get app list
        result = client.get_doc_list()
        assert result is not None, "Failed to get document list"
        assert isinstance(result, list)

        # Verify structure if apps exist
        if len(result) > 0:
            app = result[0]
            assert "qDocId" in app
            assert "qDocName" in app
            assert "qLastReloadTime" in app

    finally:
        client.disconnect()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_list_applications_tool():
    """Test the list_qlik_applications MCP tool function"""
    result = await list_qlik_applications()

    # Verify response structure
    assert "error" not in result, f"Error listing applications: {result.get('error')}"
    assert "count" in result
    assert "applications" in result
    assert isinstance(result["applications"], list)

    # Verify app structure if apps exist
    if result["count"] > 0:
        app = result["applications"][0]
        assert "app_id" in app
        assert "name" in app
        assert "last_reload_time" in app
        assert "file_size" in app
        assert "published" in app
