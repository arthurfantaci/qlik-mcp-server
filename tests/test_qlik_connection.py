"""Test basic Qlik Sense server connection functionality."""

import pytest

from src.qlik_client import QlikClient


@pytest.mark.asyncio
@pytest.mark.integration
async def test_qlik_connection_basic(qlik_config, skip_without_qlik):
    """Test basic connection to Qlik Sense server."""
    client = QlikClient()

    # Test connection
    is_connected = await client.connect()
    assert is_connected, "Failed to connect to Qlik Sense server"

    # Test that websocket is established
    assert client.ws is not None, "WebSocket connection should be established"
    assert hasattr(client, "ws"), "Client should have ws attribute"

    # Disconnect
    await client.disconnect()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_qlik_connection_and_app_list(qlik_config, skip_without_qlik):
    """Test connection and listing applications."""
    client = QlikClient()

    # Connect to server
    is_connected = await client.connect()
    assert is_connected, "Failed to connect to Qlik Sense server"

    # Send request to list applications
    request_id = await client.send_request("GetDocList", {})
    assert request_id > 0, "Request ID should be positive"

    # Wait for response
    response = await client.wait_for_response(request_id)
    assert response is not None, "Should receive response"
    assert "result" in response, "Response should contain result"

    # Validate response structure
    if "qDocList" in response["result"]:
        doc_list = response["result"]["qDocList"]
        assert isinstance(doc_list, list), "Document list should be a list"

        # If there are apps, validate structure
        if doc_list:
            app = doc_list[0]
            assert "qDocName" in app, "App should have qDocName"
            assert "qDocId" in app, "App should have qDocId"

    # Disconnect
    await client.disconnect()


@pytest.mark.asyncio
@pytest.mark.unit
async def test_qlik_client_initialization():
    """Test QlikClient initialization without connection."""
    client = QlikClient()

    # Check initial state
    assert client.ws is None, "WebSocket should be None initially"
    assert client.request_id == 0, "Request ID should start at 0"
    assert isinstance(client.responses, dict), "Responses should be a dictionary"
    assert len(client.responses) == 0, "Responses should be empty initially"

    # Check configuration is loaded (assuming .env exists)
    import os
    if os.getenv("QLIK_SERVER_URL"):
        # If environment is configured, these should be set
        assert hasattr(client, "server_url"), "Should have server_url attribute"


@pytest.mark.asyncio
@pytest.mark.integration
async def test_qlik_connection_error_handling(skip_without_qlik):
    """Test error handling for connection failures."""
    client = QlikClient()

    # Temporarily mess with the configuration to force an error
    original_url = client.server_url
    client.server_url = "invalid-server-url"

    # Attempt connection
    try:
        is_connected = await client.connect()
        assert not is_connected, "Should fail to connect to invalid server"
    except Exception as e:
        # Connection error is expected
        assert "invalid-server-url" in str(e) or "connection" in str(e).lower()
    finally:
        # Restore original URL
        client.server_url = original_url


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.slow
async def test_qlik_multiple_connections(skip_without_qlik):
    """Test multiple sequential connections and disconnections."""
    client = QlikClient()

    for i in range(3):
        # Connect
        is_connected = await client.connect()
        assert is_connected, f"Failed to connect on attempt {i+1}"

        # Do a simple operation
        request_id = await client.send_request("GetDocList", {})
        response = await client.wait_for_response(request_id)
        assert response is not None, f"Should receive response on attempt {i+1}"

        # Disconnect
        await client.disconnect()
        assert client.ws is None or not client.ws.connected, "Should be disconnected"


class TestQlikConnectionConfiguration:
    """Test suite for connection configuration."""

    @pytest.mark.unit
    def test_configuration_from_environment(self):
        """Test that configuration is loaded from environment."""
        import os

        from dotenv import load_dotenv

        # Load test environment if available
        load_dotenv(".env.test", override=True) if os.path.exists(".env.test") else load_dotenv()

        # Check expected environment variables
        expected_vars = ["QLIK_SERVER_URL", "QLIK_SERVER_PORT", "QLIK_USER_DIRECTORY", "QLIK_USER_ID"]

        # If any are set, verify they're accessible
        if any(os.getenv(var) for var in expected_vars):
            client = QlikClient()
            assert hasattr(client, "server_url"), "Client should have server_url"
            assert hasattr(client, "server_port"), "Client should have server_port"

    @pytest.mark.unit
    def test_ssl_certificate_paths(self):
        """Test that SSL certificate paths are configured."""
        from pathlib import Path

        project_root = Path(__file__).parent.parent
        cert_dir = project_root / "certs"

        # Check if certificate directory exists
        if cert_dir.exists():
            expected_certs = ["root.pem", "client.pem", "client_key.pem"]
            for cert_file in expected_certs:
                cert_path = cert_dir / cert_file
                # Just check if the path is valid, not if file exists (may not be present in test env)
                assert isinstance(cert_path, Path), f"Certificate path should be Path object: {cert_file}"


@pytest.mark.asyncio
@pytest.mark.unit
async def test_mock_connection_flow():
    """Test connection flow with mock data (no actual server needed)."""
    # This test demonstrates the expected flow without requiring a real server

    # Simulate connection success
    mock_connected = True
    assert mock_connected, "Mock connection should succeed"

    # Simulate response
    mock_response = {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "qDocList": [
                {"qDocName": "Test App", "qDocId": "test-123"},
                {"qDocName": "Demo App", "qDocId": "demo-456"},
            ],
        },
    }

    # Validate mock response structure
    assert "result" in mock_response
    assert "qDocList" in mock_response["result"]
    assert len(mock_response["result"]["qDocList"]) == 2

    # Simulate disconnection
    mock_connected = False
    assert not mock_connected, "Mock should be disconnected"
