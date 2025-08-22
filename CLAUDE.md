# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Model Context Protocol (MCP) server that provides comprehensive access to Qlik Sense applications and their detailed information. Originally focused on measures, it now offers complete Qlik Sense data access functionality. Current tools:

1. `get_app_measures` - Retrieves all measures from a specific Qlik Sense application
2. `list_qlik_applications` - Lists all available Qlik applications with names and IDs
3. `get_app_variables` - Retrieves all variables from a specific Qlik Sense application
4. `get_app_fields` - Retrieves all fields and table information from a specific Qlik Sense application
5. `get_app_sheets` - Retrieves all sheets from a specific Qlik Sense application with metadata
6. `get_sheet_objects` - Retrieves all visualization objects from a specific sheet with detailed properties
7. `get_app_dimensions` - Retrieves all dimensions from a specific Qlik Sense application with metadata
8. `get_app_script` - Retrieves the complete data loading script from a specific Qlik Sense application
9. `get_app_data_sources` - Retrieves data sources from the application's lineage (LOAD/STORE statements)

The server is named `qlik-sense` to reflect its expanding scope beyond just measures.

## Development Commands

### Setup and Installation
```bash
pip install -r requirements.txt
cp .env.example .env  # Configure with your Qlik server details
```

### Testing
```bash
# Test individual tools (most commonly used)
python tests/test_qlik_connection.py    # Basic connection validation
python tests/test_list_apps.py          # Application listing
python tests/test_measures.py           # Measure retrieval
python tests/test_mcp_tool.py           # MCP tool functions directly

# Test all tools comprehensively
python tests/test_variables.py          # Variables
python tests/test_fields.py             # Fields and data model
python tests/test_sheets.py             # Sheets and visualizations
python tests/test_dimensions.py         # Dimensions
python tests/test_script.py             # Data loading scripts
python tests/test_data_sources.py       # Data source lineage

# Test multiple tools together
python tests/test_both_tools.py
```

### Running the Server
```bash
# Requires Python 3.10+ for FastMCP
/opt/homebrew/bin/python3.11 -m src.server
# Alternative: /opt/homebrew/bin/python3.11 start_server.py
```

### Debugging
```bash
# Test Qlik client connection directly
python -m src.qlik_client
```

## Architecture

### Core Components

- **`src/server.py`** - FastMCP server that registers and handles tool calls
- **`src/tools.py`** - MCP tool definitions and implementations
- **`src/qlik_client.py`** - WebSocket client for Qlik Engine API communication

### Key Architecture Patterns

- **Certificate-based authentication** - Uses SSL certificates for Qlik Sense connection
- **WebSocket communication** - Direct connection to Qlik Engine API via WebSocket
- **Session object pattern** - Creates MeasureList session objects to retrieve measures
- **Environment-based configuration** - All connection details configured via `.env` file

### Connection Flow

1. Load SSL certificates from `certs/` directory
2. Establish WebSocket connection to Qlik Engine API
3. For app-specific operations: Open specific app using `OpenDoc`
4. For app listing: Connect to global context, call `GetDocList`
5. For sheets: Use `GetAllInfos` to find sheets, then `GetObject` + `GetLayout` for metadata
6. For sheet objects: Get sheet object, retrieve child objects with layout and properties
7. Always disconnect after operations

### Tool Implementation Patterns

**Parameter Validation**: All tools use Pydantic models (defined in `tools.py`) for parameter validation and type safety.

**Common Parameters**:
- All tools except `list_qlik_applications` require `app_id`
- Most tools have optional boolean flags to control response detail level
- `get_sheet_objects` uniquely requires both `app_id` and `sheet_id`

**API Access Patterns**:
- **Session Objects**: Measures, variables, dimensions, fields use `CreateSessionObject` + `GetLayout`
- **Handle-Based**: Sheets and sheet objects use `GetObject` by handle + `GetLayout`
- **Direct API**: Scripts use `GetScript`, data sources use `GetLineage`
- **Global Context**: Application listing uses global connection + `GetDocList`

**Error Handling**: All tools return structured JSON with comprehensive error handling and graceful fallbacks.

### Environment Configuration

Required `.env` variables:
- `QLIK_SERVER_URL` - Qlik server hostname/IP
- `QLIK_SERVER_PORT` - Port (default: 4747)
- `QLIK_USER_DIRECTORY` - User directory (default: INTERNAL)
- `QLIK_USER_ID` - User ID (default: sa_engine)

Certificate paths (relative to project root):
- `QLIK_CERT_ROOT` - Root certificate (default: certs/root.pem)
- `QLIK_CERT_CLIENT` - Client certificate (default: certs/client.pem)
- `QLIK_CERT_KEY` - Client private key (default: certs/client_key.pem)

## Key Development Considerations

### Adding New Tools

When adding new Qlik tools, follow this pattern:

1. **Define Pydantic model** in `tools.py` for parameter validation
2. **Implement tool function** in `tools.py` using appropriate Qlik API pattern:
   - Session objects for metadata retrieval (measures, variables, dimensions, fields)
   - Handle-based access for sheet objects
   - Direct API calls for scripts and lineage
3. **Register tool** in `server.py` using `@mcp.tool()` decorator
4. **Add to TOOL_DEFINITIONS** for metadata
5. **Create test file** in `tests/` following existing patterns

### Critical Qlik API Patterns

**Sheet Objects Challenge**: SheetList session objects don't return sheet data. Must use `GetAllInfos` → `GetObject` → `GetLayout` sequence.

**Connection Patterns**:
- App-specific: Connect to `/app/{app_id}` for most operations
- Global context: Connect to `/app/` for application listing
- Always disconnect after operations to prevent resource leaks

**Data Source Categorization**: The `GetLineage` API returns mixed source types. Use intelligent categorization to sort into binary, file, resident, and inline sources based on statement patterns.

### Testing Strategy

All 9 tools are validated against real Qlik Sense applications. Each test file in `tests/` corresponds to a specific tool and includes connection validation, parameter testing, and response format verification.

**Key Test Patterns**:
- Individual tool tests validate specific functionality
- `test_mcp_tool.py` tests MCP integration directly
- `test_both_tools.py` validates multiple tools together
- `test_qlik_connection.py` provides basic connectivity validation

## Security Notes

- Certificate files in `certs/` are excluded from version control
- Never commit `.env` files or certificates
- All sensitive configuration is environment-based
- Example configuration files (.env.example) are provided for setup guidance
- Comprehensive documentation helps users configure securely

## Public Repository Considerations

This project is designed for public sharing with:
- **Example configurations** instead of actual sensitive files
- **Comprehensive documentation** for setup and troubleshooting
- **Security-first approach** with proper .gitignore exclusions
- **Clear separation** between public code and private configuration
- **Production-ready** error handling and validation