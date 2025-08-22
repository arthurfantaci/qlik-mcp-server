# Qlik MCP Server

A comprehensive MCP (Model Context Protocol) server that provides complete access to Qlik Sense applications and their detailed information for AI assistants and other MCP clients.

## Features

- 🔌 **Direct WebSocket connection** to Qlik Sense Enterprise
- 🔐 **Certificate-based authentication** with SSL security
- 📊 **9 comprehensive tools** covering all major Qlik Sense objects:
  - 📋 List all available applications with metadata
  - 📊 Retrieve measures with expressions and tags
  - 🔧 Retrieve variables with definitions and configurations
  - 📊 Retrieve fields and complete data model information
  - 📄 Retrieve sheets with metadata and properties
  - 🎨 Retrieve visualization objects from sheets with detailed properties
  - 📐 Retrieve dimensions with grouping and metadata
  - 📜 Retrieve complete data loading scripts
  - 🔗 Retrieve data sources and lineage information
- 🤖 **MCP-compatible** for use with Claude Desktop and other AI tools
- ⚡ **Production-ready** with comprehensive error handling
- 🧪 **Extensively tested** with real Qlik Sense applications

## Prerequisites

- **Python 3.10+** (required for FastMCP)
- Access to Qlik Sense Enterprise server
- Valid Qlik client certificates (see [Certificate Setup Guide](docs/CERTIFICATES.md))
- MCP-compatible client (e.g., Claude Desktop)

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/arthurfantaci/qlik-mcp-server.git
cd qlik-mcp-server

# Install dependencies (Python 3.10+ required)
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your Qlik Sense server details
# See .env.example for detailed configuration instructions
```

### 3. Certificate Setup

Obtain SSL certificates from your Qlik Sense administrator and place them in the `certs/` directory:

```
certs/
├── root.pem          # Server root certificate
├── client.pem        # Client certificate  
└── client_key.pem    # Client private key
```

📖 **Detailed certificate setup instructions**: [docs/CERTIFICATES.md](docs/CERTIFICATES.md)

### 4. Test Connection

```bash
# Test your Qlik Sense connection
python tests/test_qlik_connection.py

# Test application listing
python tests/test_list_apps.py
```

### 5. Configure with Claude Desktop

```bash
# Copy example configuration to Claude Desktop
cp examples/claude_desktop_config.json ~/.config/claude_desktop_config.json

# Edit the configuration file to update paths
# Then restart Claude Desktop
```

📖 **Detailed configuration examples**: [examples/README.md](examples/README.md)

## Usage

### Running as MCP Server

Start the MCP server:

```bash
# Using Python 3.11 (recommended)
/opt/homebrew/bin/python3.11 -m src.server

# Or using the startup script
/opt/homebrew/bin/python3.11 start_server.py
```

### Available Tools

The server provides **9 comprehensive tools** for Qlik Sense analysis:

| Tool | Description |
|------|-------------|
| `list_qlik_applications` | List all available applications with metadata |
| `get_app_measures` | Retrieve measures with expressions and tags |
| `get_app_variables` | Retrieve variables with definitions and configurations |
| `get_app_fields` | Retrieve fields and complete data model information |
| `get_app_sheets` | Retrieve sheets with metadata and properties |
| `get_sheet_objects` | Retrieve visualization objects with detailed properties |
| `get_app_dimensions` | Retrieve dimensions with grouping and metadata |
| `get_app_script` | Retrieve complete data loading scripts |
| `get_app_data_sources` | Retrieve data sources and lineage information |

### Using with Claude Desktop

Once configured, you can use natural language to access all tools:

**🔍 Explore Applications:**
```text
"Show me all available Qlik Sense applications"
```

**📊 Analyze Measures:**
```text
"Get all measures from Qlik app 12345678-abcd-1234-efgh-123456789abc with expressions and tags"
```

**🔧 Review Variables:**
```text
"Show me all variables in the application including their definitions"
```

**📊 Examine Data Model:**
```text
"Get all fields and table information to understand the data model structure"
```

**📄 Review Sheets:**
```text
"List all sheets in the application with their metadata"
```

**🎨 Analyze Visualizations:**
```text
"Get all visualization objects from sheet 'Overview' with their properties and layout"
```

**📐 Study Dimensions:**
```text
"Show me all dimensions with their grouping and metadata information"
```

**📜 Review Data Loading:**
```text
"Get the complete data loading script for this application"
```

**🔗 Understand Data Sources:**
```text
"Show me all data sources and their lineage, including binary and file sources"
```

The measures tool will return:

- Measure IDs and titles
- Measure descriptions
- Expressions (optional)
- Tags (optional)
- Total count of measures

The applications list tool will return:

- Application names and IDs
- Last reload timestamps
- Total count of applications

The variables tool will return:

- Variable names and definitions
- Variable tags (optional)
- Reserved and configuration flags
- Total count of variables

The fields tool will return:

- Field names and properties (numeric, system, hidden, etc.)
- Source table information for each field
- Complete list of tables in the application
- Field cardinality and tags
- Data model structure for analysis

## Tool Parameters

### `get_app_measures` Tool

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `app_id` | string | Yes | Qlik Sense application ID |
| `include_expression` | boolean | No | Include measure expressions (default: true) |
| `include_tags` | boolean | No | Include measure tags (default: true) |

### `list_qlik_applications` Tool

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| _(no parameters)_ | - | - | Returns all available applications |

### `get_app_variables` Tool

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `app_id` | string | Yes | Qlik Sense application ID |
| `include_definition` | boolean | No | Include variable definitions (default: true) |
| `include_tags` | boolean | No | Include variable tags (default: true) |
| `show_reserved` | boolean | No | Include reserved system variables (default: true) |
| `show_config` | boolean | No | Include configuration variables (default: true) |

### `get_app_fields` Tool

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `app_id` | string | Yes | Qlik Sense application ID |
| `show_system` | boolean | No | Include system fields (default: true) |
| `show_hidden` | boolean | No | Include hidden fields (default: true) |
| `show_derived_fields` | boolean | No | Include derived fields (default: true) |
| `show_semantic` | boolean | No | Include semantic fields (default: true) |
| `show_src_tables` | boolean | No | Include source table information (default: true) |
| `show_implicit` | boolean | No | Include implicit fields (default: true) |

## Response Formats

### `get_app_measures` Response

```json
{
  "app_id": "12345678-abcd-1234-efgh-123456789abc",
  "measures": [
    {
      "id": "measure_id",
      "title": "Revenue",
      "description": "Total revenue calculation",
      "expression": "Sum(Sales)",
      "label": "Total Revenue",
      "tags": ["finance", "kpi"]
    }
  ],
  "count": 25,
  "retrieved_at": "2024-01-20T10:30:00Z",
  "options": {
    "include_expression": true,
    "include_tags": true
  }
}
```

### `list_qlik_applications` Response

```json
{
  "applications": [
    {
      "app_id": "12345678-abcd-1234-efgh-123456789abc",
      "name": "Financial Dashboard",
      "last_reload_time": "2024-01-20T10:30:00Z",
      "meta": {},
      "doc_type": ""
    }
  ],
  "count": 148,
  "retrieved_at": "2024-01-20T10:30:00Z"
}
```

### `get_app_variables` Response

```json
{
  "app_id": "12345678-abcd-1234-efgh-123456789abc",
  "variables": [
    {
      "name": "vGoldSchema",
      "definition": "gold",
      "tags": [],
      "is_reserved": false,
      "is_config": false
    }
  ],
  "count": 65,
  "retrieved_at": "2024-01-20T10:30:00Z",
  "options": {
    "include_definition": true,
    "include_tags": true,
    "show_reserved": true,
    "show_config": true
  }
}
```

### `get_app_fields` Response

```json
{
  "app_id": "12345678-abcd-1234-efgh-123456789abc",
  "fields": [
    {
      "name": "interval_key",
      "source_tables": ["qv_financial_fact_derived", "qv_finance_placement_interval"],
      "is_system": false,
      "is_hidden": false,
      "is_numeric": true,
      "cardinal": 4818662,
      "tags": ["$key", "$numeric", "$integer"]
    }
  ],
  "tables": [
    "qv_financial_fact_derived",
    "qv_finance_placement_interval",
    "monthly_inventory_snapshot"
  ],
  "field_count": 88,
  "table_count": 14,
  "retrieved_at": "2024-01-20T10:30:00Z",
  "options": {
    "show_system": true,
    "show_hidden": true,
    "show_derived_fields": true,
    "show_semantic": true,
    "show_src_tables": true,
    "show_implicit": true
  }
}
```

### `get_app_sheets` Response

```json
{
  "app_id": "12345678-abcd-1234-efgh-123456789abc",
  "sheets": [
    {
      "id": "sheet_abc123",
      "title": "Overview Dashboard",
      "description": "Main overview of key metrics",
      "rank": 0,
      "columns": 24,
      "rows": 12,
      "meta": {
        "created": "2024-01-15T09:00:00Z",
        "modified": "2024-01-20T10:30:00Z",
        "published": true
      }
    }
  ],
  "count": 3,
  "retrieved_at": "2024-01-20T10:30:00Z",
  "options": {
    "include_thumbnail": false,
    "include_metadata": true
  }
}
```

### `get_sheet_objects` Response

```json
{
  "app_id": "12345678-abcd-1234-efgh-123456789abc",
  "sheet_id": "sheet_abc123",
  "objects": [
    {
      "id": "object_xyz789",
      "type": "barchart",
      "title": "Sales by Region",
      "subtitle": "Last 12 months",
      "position": {
        "x": 0,
        "y": 0,
        "width": 12,
        "height": 6
      },
      "properties": {
        "dimensions": ["Region"],
        "measures": ["Sum(Sales)"],
        "color": {
          "auto": true
        }
      },
      "layout": {
        "visualization": "barchart",
        "version": "1.0"
      }
    }
  ],
  "count": 12,
  "retrieved_at": "2024-01-20T10:30:00Z",
  "options": {
    "include_properties": true,
    "include_layout": true,
    "include_data": false
  }
}
```

### `get_app_dimensions` Response

```json
{
  "app_id": "12345678-abcd-1234-efgh-123456789abc",
  "dimensions": [
    {
      "id": "dim_product_category",
      "title": "Product Category",
      "description": "Product categorization hierarchy",
      "grouping": "N",
      "field_defs": ["Category"],
      "field_labels": ["Product Category"],
      "tags": ["product", "hierarchy"],
      "meta": {
        "created": "2024-01-10T14:30:00Z",
        "approved": true
      }
    }
  ],
  "count": 23,
  "retrieved_at": "2024-01-20T10:30:00Z",
  "options": {
    "include_title": true,
    "include_tags": true,
    "include_grouping": true,
    "include_info": true
  }
}
```

### `get_app_script` Response

```json
{
  "app_id": "12345678-abcd-1234-efgh-123456789abc",
  "script": "// Main data loading script\n\n// Load sales data\nSales:\nLOAD\n    OrderID,\n    CustomerID,\n    ProductID,\n    Quantity,\n    UnitPrice,\n    OrderDate\nFROM [lib://DataFiles/sales.qvd] (qvd);\n\n// Load customer data\nCustomers:\nLOAD\n    CustomerID,\n    CustomerName,\n    Region,\n    Country\nFROM [lib://DataFiles/customers.xlsx]\n(ooxml, embedded labels, table is Customers);\n",
  "script_length": 245,
  "retrieved_at": "2024-01-20T10:30:00Z"
}
```

### `get_app_data_sources` Response

```json
{
  "app_id": "12345678-abcd-1234-efgh-123456789abc",
  "data_sources": [
    {
      "name": "sales.qvd",
      "type": "file",
      "connection_string": "lib://DataFiles/sales.qvd",
      "statement": "LOAD * FROM [lib://DataFiles/sales.qvd] (qvd);",
      "discrimination": {
        "type": "DataConnection",
        "label": "QVD file source"
      }
    },
    {
      "name": "CustomerAnalytics.qvf",
      "type": "binary",
      "connection_string": "lib://Apps/CustomerAnalytics.qvf",
      "statement": "binary [lib://Apps/CustomerAnalytics.qvf];",
      "discrimination": {
        "type": "BinaryLoad",
        "label": "Binary application load"
      }
    },
    {
      "name": "TempTable",
      "type": "resident",
      "connection_string": "Resident SalesData",
      "statement": "LOAD CustomerID, Sum(Amount) as TotalSales RESIDENT SalesData GROUP BY CustomerID;",
      "discrimination": {
        "type": "ResidentLoad",
        "label": "Resident table transformation"
      }
    }
  ],
  "source_counts": {
    "binary": 1,
    "file": 3,
    "resident": 8,
    "inline": 1,
    "other": 0
  },
  "total_sources": 13,
  "retrieved_at": "2024-01-20T10:30:00Z",
  "options": {
    "include_resident": true,
    "include_file": true,
    "include_binary": true,
    "include_inline": true
  }
}
```

## Project Structure

```text
qlik-mcp-server/
├── src/                    # Core application code
│   ├── __init__.py         # Package initialization
│   ├── server.py           # FastMCP server implementation
│   ├── qlik_client.py      # Qlik Engine API WebSocket client
│   └── tools.py            # MCP tool definitions and implementations
├── tests/                  # Test suite
│   ├── test_qlik_connection.py    # Test basic connection
│   ├── test_list_apps.py          # Test application listing
│   ├── test_measures.py           # Test measure retrieval
│   ├── test_variables.py          # Test variable retrieval
│   ├── test_fields.py             # Test field retrieval
│   ├── test_sheets.py             # Test sheet retrieval
│   ├── test_dimensions.py         # Test dimension retrieval
│   ├── test_script.py             # Test script retrieval
│   ├── test_data_sources.py       # Test data source retrieval
│   ├── test_mcp_tool.py           # Test MCP tool functions
│   └── test_both_tools.py         # Test multiple tools together
├── examples/               # Configuration examples
│   ├── claude_desktop_config.json # Claude Desktop configuration
│   └── README.md           # Configuration instructions
├── docs/                   # Documentation
│   └── CERTIFICATES.md     # Certificate setup guide
├── certs/                  # SSL certificates (gitignored)
│   ├── root.pem           # Server root certificate
│   ├── client.pem         # Client certificate
│   └── client_key.pem     # Client private key
├── .env.example           # Example environment configuration
├── .env                   # Environment configuration (gitignored)
├── .gitignore            # Git ignore rules
├── requirements.txt       # Python dependencies
├── start_server.py       # Server startup script
├── CLAUDE.md             # Claude Code instructions
└── README.md             # This documentation
```

## Security

- Certificate files are excluded from version control via `.gitignore`
- Never commit `.env` files or certificates to repositories
- Use environment variables for sensitive configuration
- Certificates should be properly secured with appropriate file permissions

## Troubleshooting

### Connection Issues

1. **Certificate errors**: Verify certificates are in PEM format and readable
2. **Authentication fails**: Check QLIK_USER_DIRECTORY and QLIK_USER_ID settings
3. **Timeout errors**: Increase WEBSOCKET_TIMEOUT in `.env`
4. **App not found**: Verify app ID and user permissions in QMC

### MCP Issues

1. **Server won't start**: Check Python version (3.8+ required)
2. **Tool not found**: Restart Claude Desktop after configuration changes
3. **No response**: Check server logs for errors

## Development

### Running Tests

Comprehensive test suite for all tools:

```bash
# Test basic Qlik connection
python tests/test_qlik_connection.py

# Test individual tools
python tests/test_list_apps.py          # Application listing
python tests/test_variables.py          # Variable retrieval  
python tests/test_fields.py             # Field and table information
python tests/test_sheets.py             # Sheet metadata
python tests/test_dimensions.py         # Dimension analysis
python tests/test_script.py             # Script retrieval
python tests/test_data_sources.py       # Data source lineage

# Test MCP functionality
python tests/test_mcp_tool.py           # Direct tool functions
python tests/test_both_tools.py         # Multiple tools together

# Test Qlik client directly
python -m src.qlik_client
```

### Adding New Tools

To add more Qlik tools:

1. Define the tool function in `tools.py`
2. Add tool metadata to `TOOL_DEFINITIONS`
3. Register the tool in `server.py` using `@mcp.tool()`

### Available Tools

1. **list_qlik_applications**: Lists all available Qlik applications with names and IDs
2. **get_app_measures**: Retrieves all measures from a specific Qlik application
3. **get_app_variables**: Retrieves all variables from a specific Qlik application
4. **get_app_fields**: Retrieves all fields and table information from a specific Qlik application
5. **get_app_sheets**: Retrieves all sheets from a specific Qlik application with metadata
6. **get_sheet_objects**: Retrieves all visualization objects from a specific sheet with detailed properties
7. **get_app_dimensions**: Retrieves all dimensions from a specific Qlik application with metadata
8. **get_app_script**: Retrieves the complete data loading script from a specific Qlik application
9. **get_app_data_sources**: Retrieves data sources from the application's lineage (LOAD/STORE statements)

## Limitations

This is a lightweight pilot implementation with intentional limitations:

- Single app connection at a time
- No retry logic for failed connections
- Basic error handling
- No caching of results
- Sequential processing only
- Minimal logging

## Future Enhancements

Potential improvements for production use:

- Add tools for dimensions, sheets, and other Qlik objects
- Implement connection pooling
- Add comprehensive error handling and retry logic
- Cache frequently accessed data
- Support for multiple concurrent app connections
- Detailed logging and monitoring
- WebSocket reconnection handling

## License

This is a pilot project for individual use. Ensure compliance with your organization's Qlik Sense licensing terms.

## Support

This is a lightweight pilot implementation. For issues:

1. Check the troubleshooting section
2. Verify Qlik server connectivity
3. Review server logs for detailed error messages
4. Ensure certificates are valid and not expired
