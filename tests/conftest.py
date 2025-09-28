"""Pytest configuration and shared fixtures for Qlik MCP Server tests."""

import os
import sys
import pytest
import asyncio
from typing import Optional, Dict, Any
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load test environment variables
test_env_path = project_root / ".env.test"
if test_env_path.exists():
    load_dotenv(test_env_path, override=True)
else:
    # Fall back to regular .env if test env doesn't exist
    load_dotenv(override=True)


# Check if Qlik server is available
def qlik_server_available() -> bool:
    """Check if Qlik server connection is available."""
    skip_integration = os.getenv("SKIP_INTEGRATION_TESTS", "true").lower() == "true"
    return not skip_integration


# Skip decorator for integration tests
skip_without_qlik = pytest.mark.skipif(
    not qlik_server_available(),
    reason="Qlik Sense server not available or SKIP_INTEGRATION_TESTS=true"
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_app_id() -> str:
    """Provide test application ID from environment or default."""
    return os.getenv("TEST_APP_ID", "12345678-abcd-1234-efgh-123456789abc")


@pytest.fixture
def test_sheet_id() -> str:
    """Provide test sheet ID from environment or default."""
    return os.getenv("TEST_SHEET_ID", "sheet-123-abc")


@pytest.fixture
def test_container_id() -> str:
    """Provide test container ID from environment or default."""
    return os.getenv("TEST_CONTAINER_ID", "container1")


@pytest.fixture
def qlik_config() -> Dict[str, Any]:
    """Provide Qlik server configuration."""
    return {
        "server_url": os.getenv("QLIK_SERVER_URL", "test-server.example.com"),
        "server_port": int(os.getenv("QLIK_SERVER_PORT", "4747")),
        "user_directory": os.getenv("QLIK_USER_DIRECTORY", "INTERNAL"),
        "user_id": os.getenv("QLIK_USER_ID", "sa_engine"),
        "timeout": int(os.getenv("WEBSOCKET_TIMEOUT", "10000"))
    }


@pytest.fixture
async def qlik_client(qlik_config):
    """Provide QlikClient instance if server is available."""
    if not qlik_server_available():
        pytest.skip("Qlik server not available")

    from src.qlik_client import QlikClient

    client = QlikClient()
    # Note: Connection will be established when needed
    yield client
    # Cleanup if needed
    if hasattr(client, 'ws') and client.ws:
        try:
            client.disconnect()
        except Exception:
            pass


@pytest.fixture
def mock_measures_response():
    """Provide mock measures response for testing without Qlik server."""
    return {
        "app_id": "12345678-abcd-1234-efgh-123456789abc",
        "measures": [
            {
                "id": "measure1",
                "title": "Total Sales",
                "description": "Sum of all sales",
                "expression": "Sum(Sales)",
                "label": "Total Sales",
                "tags": ["kpi", "sales"]
            },
            {
                "id": "measure2",
                "title": "Average Order Value",
                "description": "Average value per order",
                "expression": "Sum(Sales)/Count(DISTINCT OrderID)",
                "label": "AOV",
                "tags": ["kpi", "sales", "average"]
            }
        ],
        "count": 2,
        "retrieved_at": "2025-01-01T12:00:00Z",
        "options": {
            "include_expression": True,
            "include_tags": True
        }
    }


@pytest.fixture
def mock_applications_response():
    """Provide mock applications list for testing without Qlik server."""
    return {
        "applications": [
            {
                "app_id": "12345678-abcd-1234-efgh-123456789abc",
                "name": "Sales Dashboard",
                "last_reload_time": "2025-01-01T10:00:00Z",
                "meta": {},
                "doc_type": ""
            },
            {
                "app_id": "87654321-dcba-4321-hgfe-cba987654321",
                "name": "Finance Dashboard",
                "last_reload_time": "2025-01-01T11:00:00Z",
                "meta": {},
                "doc_type": ""
            }
        ],
        "count": 2,
        "retrieved_at": "2025-01-01T12:00:00Z"
    }


@pytest.fixture
def mock_script_response():
    """Provide mock script response for testing without Qlik server."""
    return {
        "app_id": "12345678-abcd-1234-efgh-123456789abc",
        "script": """///$tab Main
SET ThousandSep=',';
SET DecimalSep='.';

// Binary load from base app
Binary [lib://Apps/BaseApp.qvf];

///$tab Sales Data
Sales:
LOAD
    OrderID,
    CustomerID,
    ProductID,
    Quantity,
    UnitPrice,
    OrderDate
FROM [lib://DataFiles/sales.qvd] (qvd);

///$tab Variables
SET vCurrentYear = Year(Today());
LET vLastReloadTime = Now();
""",
        "script_length": 350,
        "analysis": {
            "total_lines": 20,
            "empty_lines": 3,
            "comment_lines": 4,
            "sections": [
                {"name": "Main", "start_line": 1, "end_line": 6},
                {"name": "Sales Data", "start_line": 8, "end_line": 16},
                {"name": "Variables", "start_line": 18, "end_line": 20}
            ],
            "binary_loads": [
                {
                    "statement": "Binary [lib://Apps/BaseApp.qvf];",
                    "source_app": "lib://Apps/BaseApp.qvf",
                    "line_number": 6
                }
            ],
            "load_statements": 1,
            "store_statements": 0,
            "drop_statements": 0,
            "variables": {
                "SET": [
                    {"name": "ThousandSep", "value": "','", "line": 2},
                    {"name": "DecimalSep", "value": "'.'", "line": 3},
                    {"name": "vCurrentYear", "value": "Year(Today())", "line": 19}
                ],
                "LET": [
                    {"name": "vLastReloadTime", "value": "Now()", "line": 20}
                ]
            }
        },
        "retrieved_at": "2025-01-01T12:00:00Z"
    }


# Markers for test categorization
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as requiring Qlik Sense connection"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test (no external dependencies)"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "skip_without_qlik: skip test if Qlik server unavailable"
    )


# Helper function for async timeout
@pytest.fixture
def async_timeout():
    """Provide configurable async timeout."""
    timeout_seconds = int(os.getenv("TEST_TIMEOUT", "30"))

    async def _timeout(coro, timeout=timeout_seconds):
        """Execute coroutine with timeout."""
        try:
            return await asyncio.wait_for(coro, timeout=timeout)
        except asyncio.TimeoutError:
            pytest.fail(f"Test timed out after {timeout} seconds")

    return _timeout