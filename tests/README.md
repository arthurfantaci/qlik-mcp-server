# Qlik MCP Server - Test Suite

This directory contains the comprehensive test suite for the Qlik MCP Server, built with pytest for professional testing capabilities.

## 🚀 Quick Start

### Prerequisites

1. Install test dependencies:
```bash
uv sync  # This installs both main and dev dependencies including pytest
```

> **Note:** Test files follow pytest conventions and cannot be run directly with Python. All tests must be executed using pytest.

2. Configure test environment:
```bash
cp .env.test.example .env.test
# Edit .env.test with your Qlik server details (when available)
```

### Running Tests

#### Run all tests
```bash
uv run pytest
```

#### Run with verbose output
```bash
uv run pytest -v
```

#### Run only unit tests (no Qlik server required)
```bash
uv run pytest -m unit
```

#### Run integration tests (requires Qlik server)
```bash
uv run pytest -m integration
```

#### Run with coverage report
```bash
uv run pytest --cov=src --cov-report=html
```

#### Run specific test file
```bash
uv run pytest tests/test_mcp_tool.py
```

#### Run specific test function
```bash
uv run pytest tests/test_mcp_tool.py::test_get_app_measures_mock
```

## 📁 Test Structure

```
tests/
├── conftest.py                  # Shared fixtures and configuration
├── test_qlik_connection.py      # Basic connection tests
├── test_mcp_tool.py              # MCP tool integration tests
├── test_list_apps.py             # Application listing tests
├── test_variables.py             # Variable retrieval tests
├── test_fields.py                # Field retrieval tests
├── test_sheets.py                # Sheet retrieval tests
├── test_dimensions.py            # Dimension retrieval tests
├── test_script.py                # Script analysis tests
├── test_data_sources.py          # Data source tests
├── test_binary_extraction.py     # BINARY LOAD extraction tests
├── test_vizlib_container.py      # VizlibContainer tests
└── test_both_tools.py            # Multi-tool integration tests
```

## 🏷️ Test Categories

### Unit Tests (`@pytest.mark.unit`)
- Run without Qlik server connection
- Test data validation and response structures
- Use mock data fixtures
- Always available for local development

### Integration Tests (`@pytest.mark.integration`)
- Require live Qlik server connection
- Test actual API interactions
- Automatically skipped when `SKIP_INTEGRATION_TESTS=true`
- Use `skip_without_qlik` fixture for automatic skipping

### Slow Tests (`@pytest.mark.slow`)
- Long-running tests
- Can be excluded with `pytest -m "not slow"`

## 🔧 Configuration

### Environment Variables (.env.test)

```bash
# Qlik Server Configuration
QLIK_SERVER_URL=your-qlik-server.com
QLIK_SERVER_PORT=4747
QLIK_USER_DIRECTORY=INTERNAL
QLIK_USER_ID=sa_engine

# Test Application IDs
TEST_APP_ID=your-test-app-id
TEST_SHEET_ID=your-test-sheet-id
TEST_CONTAINER_ID=your-container-id

# Test Control
SKIP_INTEGRATION_TESTS=true  # Set to false when Qlik is available
USE_MOCK_DATA=true           # Use mock data when Qlik unavailable
TEST_TIMEOUT=30              # Test timeout in seconds
```

## 🧩 Available Fixtures

### Configuration Fixtures
- `qlik_config` - Qlik server configuration
- `test_app_id` - Test application ID
- `test_sheet_id` - Test sheet ID
- `test_container_id` - Test container ID

### Client Fixtures
- `qlik_client` - Configured QlikClient instance (integration tests)
- `async_timeout` - Configurable async timeout wrapper

### Mock Data Fixtures
- `mock_measures_response` - Sample measures response
- `mock_applications_response` - Sample applications list
- `mock_script_response` - Sample script with analysis
- (Add more mock fixtures as needed)

### Utility Fixtures
- `skip_without_qlik` - Auto-skip when no Qlik server available
- `event_loop` - Async event loop for tests

## 📝 Writing New Tests

### Basic Test Structure

```python
"""Test module for your feature"""

import pytest
from src.tools import your_function


@pytest.mark.asyncio
@pytest.mark.unit
async def test_your_function_mock(mock_data_fixture):
    """Test with mock data (no server required)."""
    result = mock_data_fixture
    assert result is not None
    assert "expected_key" in result


@pytest.mark.asyncio
@pytest.mark.integration
async def test_your_function_live(test_app_id, skip_without_qlik):
    """Test with live Qlik server."""
    result = await your_function(app_id=test_app_id)
    assert result is not None
    assert result["app_id"] == test_app_id
```

> **Important:** Do not include shebangs (`#!/usr/bin/env python3`) or `if __name__ == "__main__":` blocks in test files. Tests should only be run via pytest.

### Adding Mock Fixtures

Edit `conftest.py` to add new mock fixtures:

```python
@pytest.fixture
def mock_your_data():
    """Provide mock data for your tests."""
    return {
        "key": "value",
        "data": [...]
    }
```

### Parametrized Tests

```python
@pytest.mark.asyncio
@pytest.mark.parametrize("param1,param2", [
    (True, True),
    (True, False),
    (False, True),
    (False, False),
])
async def test_with_parameters(param1, param2):
    """Test with multiple parameter combinations."""
    result = await function(option1=param1, option2=param2)
    assert result is not None
```

## 🔍 Debugging Tests

### Run specific test with output
```bash
uv run pytest tests/test_mcp_tool.py -v -s
```

### Run with debugging
```bash
uv run pytest --pdb  # Drop into debugger on failure
```

### Run with full traceback
```bash
uv run pytest --tb=long
```

## 📊 Coverage Reports

### Generate HTML coverage report
```bash
uv run pytest --cov=src --cov-report=html
open htmlcov/index.html  # View in browser
```

### Terminal coverage summary
```bash
uv run pytest --cov=src --cov-report=term-missing
```

## 🤖 CI/CD Integration

Tests are automatically run in GitHub Actions on:
- Every push to main branch
- Every pull request
- Manual workflow dispatch

See `.github/workflows/test.yml` for configuration.

## ⚠️ Troubleshooting

### Tests are skipped
- Check `SKIP_INTEGRATION_TESTS` in `.env.test`
- Verify Qlik server credentials are correct
- Ensure certificates are in place

### Connection errors
- Verify `QLIK_SERVER_URL` and `QLIK_SERVER_PORT`
- Check SSL certificates in `certs/` directory
- Ensure Qlik server is accessible

### Timeout errors
- Increase `TEST_TIMEOUT` in `.env.test`
- Check `WEBSOCKET_TIMEOUT` setting
- Verify network connectivity

## 🎯 Best Practices

1. **Follow pytest conventions**
   - No shebangs or main blocks in test files
   - Tests must be run via pytest, not directly with Python
   - Use proper test naming: `test_*.py` files, `test_*` functions

2. **Always write both unit and integration tests**
   - Unit tests ensure code quality without external dependencies
   - Integration tests verify actual Qlik interactions

3. **Use fixtures for shared setup**
   - Avoid duplicating setup code
   - Fixtures provide consistent test data

4. **Mark tests appropriately**
   - Use `@pytest.mark.unit` for offline tests
   - Use `@pytest.mark.integration` for Qlik-dependent tests
   - Use `@pytest.mark.slow` for long-running tests

5. **Test error cases**
   - Test invalid inputs
   - Test connection failures
   - Test empty responses

6. **Keep tests independent**
   - Each test should be runnable in isolation
   - Don't depend on test execution order

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)