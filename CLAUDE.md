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
```

### Testing
Test individual components:
```bash
python test_qlik_connection.py    # Test Qlik connection and measure retrieval
python test_list_apps.py          # Test application listing
python test_variables.py          # Test variable retrieval
python test_fields.py             # Test field list retrieval
python test_sheets.py             # Test sheet and visualization retrieval
python test_sheets_dashboard.py   # Test sheet retrieval with dashboard app
python test_dimensions.py         # Test dimension retrieval
python test_script.py             # Test script retrieval
python test_data_sources.py       # Test data sources lineage retrieval
python test_mcp_tool.py           # Test MCP tool functions directly
python test_both_tools.py         # Test both tools together
```

Test Qlik client directly:
```bash
python -m src.qlik_client
```

### Running the Server
Start the MCP server (requires Python 3.10+):
```bash
# Using Python 3.11 (recommended)
/opt/homebrew/bin/python3.11 -m src.server

# Or using the startup script
/opt/homebrew/bin/python3.11 start_server.py
```

**Note:** The project requires Python 3.10+ due to FastMCP dependencies. If you have Python 3.9 or older, install Python 3.11 via Homebrew:
```bash
brew install python@3.11
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

### Tool Parameter Handling

- `get_app_measures`: Requires `app_id`, optional `include_expression` and `include_tags` 
- `list_qlik_applications`: No parameters required
- `get_app_variables`: Requires `app_id`, optional `include_definition`, `include_tags`, `show_reserved`, `show_config`
- `get_app_fields`: Requires `app_id`, optional visibility flags for different field types and table information
- `get_app_sheets`: Requires `app_id`, optional `include_thumbnail` and `include_metadata`
- `get_sheet_objects`: Requires `app_id` and `sheet_id`, optional flags for properties, layout, and data definitions
- `get_app_dimensions`: Requires `app_id`, optional `include_title`, `include_tags`, `include_grouping`, `include_info`
- `get_app_script`: Requires `app_id` only
- `get_app_data_sources`: Requires `app_id`, optional flags for including different source types (resident, file, binary, inline)
- All tools return structured JSON with comprehensive error handling

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

## Recent Technical Improvements

### Complete Qlik Sense Application Analysis Suite

The MCP server has evolved into a comprehensive Qlik Sense analysis platform with three major development phases:

**Phase 1: Core Data Objects (Initial Development)**
- **Measures and Variables**: Using session objects (MeasureList, VariableList, DimensionList)
- **Fields and Tables**: Using FieldList for data model analysis
- **Applications**: Global context listing with GetDocList

**Phase 2: Sheet and Visualization Tools** 
- **Initial Challenge**: SheetList session objects didn't return sheet data
- **Solution**: Uses `GetAllInfos` → `GetObject` → `GetLayout` sequence for complete metadata
- **Object Retrieval**: Sheet-based visualization analysis with layout, properties, and data definitions
- **Advanced Features**: Comprehensive object type detection (charts, filters, containers, custom Vizlib components)

**Phase 3: Script and Data Sources (Latest Enhancement)**
- **Script Retrieval**: Direct `GetScript` API call for complete data loading scripts
- **Data Sources Lineage**: `GetLineage` API with intelligent categorization
- **Advanced Categorization**: Automatic sorting into binary, file, resident, inline, and other source types
- **Special Focus**: Binary source detection (qStatement: "binary") for app dependencies

**Key Technical Patterns:**
- **Three-Layer Architecture**: tools.py → qlik_client.py → server.py
- **Session Object Pattern**: For measures, variables, dimensions, fields
- **Handle-Based Access**: For sheets and visualization objects
- **Direct API Calls**: For scripts and lineage data
- **Intelligent Categorization**: For data sources with filtering options
- **Comprehensive Error Handling**: Graceful fallbacks and detailed logging

### Validation and Testing

All 9 tools have been extensively tested with real Qlik Sense applications:
- **Test Application**: `fb41d1e1-38fb-4595-8391-2f1a536bceb1`
- **Measures**: 19 measures with expressions and metadata
- **Variables**: Multiple variables with definitions and tags
- **Fields**: Comprehensive field and table information
- **Sheets**: 3 sheets with titles, dates, publication status
- **Visualization Objects**: 12+ objects with proper type classification
- **Dimensions**: 23 dimensions with metadata, grouping, and tags
- **Scripts**: Complete data loading script (39,439+ characters)
- **Data Sources**: 13+ sources categorized by type (1 binary, 3 file, 8 resident, 1 inline)

## Security Notes

- Certificate files in `certs/` are excluded from version control
- Never commit `.env` files or certificates
- All sensitive configuration is environment-based