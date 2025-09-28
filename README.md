# Qlik MCP Server

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![MCP](https://img.shields.io/badge/MCP-compatible-brightgreen)

A comprehensive MCP (Model Context Protocol) server that provides complete access to Qlik Sense applications and their detailed information for AI assistants and other MCP clients.

## Features

- 🔌 **Direct WebSocket connection** to Qlik Sense Enterprise
- 🔐 **Certificate-based authentication** with SSL security
- 📦 **VizlibContainer support** with embedded object extraction
- 🔗 **Master Item resolution** automatically resolves references to full expressions
- 🔍 **BINARY LOAD detection** automatically extracts and analyzes BINARY dependencies
- 📊 **Advanced Script Analysis** with section parsing, variable extraction, and statement counting
- 📊 **9 comprehensive tools** covering all major Qlik Sense objects:
  - 📋 List all available applications with metadata
  - 📊 Retrieve measures with expressions and tags
  - 🔧 Retrieve variables with definitions and configurations
  - 📊 Retrieve fields and complete data model information
  - 📄 Retrieve sheets with metadata and properties
  - 🎨 Retrieve visualization objects from sheets with detailed properties
  - 📐 Retrieve dimensions with grouping and metadata
  - 📜 Retrieve and analyze data loading scripts with BINARY LOAD extraction
  - 🔗 Retrieve data sources and lineage information
- 🤖 **MCP-compatible** for use with Claude Desktop and other AI tools
- ⚡ **Production-ready** with comprehensive error handling
- 🧪 **Extensively tested** with real Qlik Sense applications

## Why This Matters

🎯 **Business Impact**: This MCP server bridges the gap between Qlik Sense's powerful analytics and modern AI assistants, enabling:

- **10x faster insights** - Natural language queries replace complex Qlik Sense expressions
- **Democratized analytics** - Non-technical users can explore Qlik data through conversation
- **Automated documentation** - AI can instantly analyze and document your entire Qlik application structure
- **Enterprise-ready integration** - Production-grade WebSocket connections with certificate-based security

💡 **Use Cases**:

- **Automated QA**: AI assistants can validate measures, dimensions, and data models
- **Documentation Generation**: Automatically create comprehensive app documentation
- **Migration Analysis**: Assess complexity before Qlik app migrations or upgrades
- **Governance Auditing**: Review variables, scripts, and data sources for compliance

## 🛠️ Modern Development Stack

This project uses industry-standard tools for reliability and maintainability:

- **🚀 UV**: Fast, reliable Python package management and virtual environment handling
- **🧹 Ruff**: Lightning-fast Python linter and formatter with automated code quality
- **🧪 Pytest**: Professional testing framework with unit/integration test separation
- **🤖 GitHub Actions**: Automated CI/CD with matrix testing across Python versions
- **📦 FastMCP**: Modern MCP server framework with Pydantic validation

## Prerequisites

- **Python 3.10+** (required for FastMCP)
- **UV package manager** (strongly recommended - handles everything automatically)
- Access to Qlik Sense Enterprise server
- Valid Qlik client certificates (see [Certificate Setup Guide](docs/CERTIFICATES.md))
- MCP-compatible client (e.g., Cursor IDE, VS Code, Claude Desktop)

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/arthurfantaci/qlik-mcp-server.git
cd qlik-mcp-server

# Install with UV (strongly recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh  # Install UV if not already installed
uv sync  # Creates virtual environment and installs all dependencies automatically
```

> **Why UV?** UV provides faster, more reliable dependency management with automatic virtual environment handling, lockfile generation for reproducible builds, and seamless integration with modern Python development workflows.

### 2. Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your Qlik Sense server details
# See .env.example for detailed configuration instructions
```

### 3. Certificate Setup

Obtain SSL certificates from your Qlik Sense administrator and place them in the `certs/` directory:

```bash
certs/
├── root.pem          # Server root certificate
├── client.pem        # Client certificate  
└── client_key.pem    # Client private key
```

📖 **Detailed certificate setup instructions**: [docs/CERTIFICATES.md](docs/CERTIFICATES.md)

### 4. Test Connection

```bash
# Test basic Qlik connection
uv run pytest tests/test_qlik_connection.py -v

# Test application listing
uv run pytest tests/test_list_apps.py -v

# Run all unit tests (no Qlik server required)
uv run pytest -m unit

# Run integration tests (requires Qlik server)
uv run pytest -m integration
```

### 5. Configure with Cursor IDE

```bash
# For project-specific configuration (recommended)
mkdir -p .cursor
cp examples/cursor_config.json .cursor/mcp.json

# OR for global configuration
cp examples/cursor_config.json ~/.cursor/mcp.json

# Update the paths in the configuration to match your setup
# Enable MCP in Cursor Settings and restart Cursor
```

### 6. Configure with VS Code

```bash
# Copy example configuration to VS Code settings
cp examples/vscode_config.json ~/.vscode/settings.json

# Or merge with existing VS Code settings
# Update the paths in the configuration to match your setup
```

### 7. Configure with Claude Desktop

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
| `get_app_script` | Retrieve and analyze scripts with BINARY LOAD extraction |
| `get_app_data_sources` | Retrieve data sources and lineage information |

### Enhanced Script Tool Examples

The `get_app_script` tool now includes powerful analysis capabilities. Here are examples of how to use it:

#### Basic Script Retrieval

```text
"Get the script from app 12345678-abcd-1234-efgh-123456789abc"
```

#### Script with Full Analysis and BINARY LOAD Detection

```text
"Analyze the script from app 12345678-abcd-1234-efgh-123456789abc and show me all BINARY LOAD statements"

Parameters used:
- analyze_script: true
- Result includes: BINARY LOAD statements with source apps, variable declarations, statement counts
```

#### Script with Section Parsing

```text
"Get the script from app 12345678-abcd-1234-efgh-123456789abc and break it down by sections"

Parameters used:
- include_sections: true  
- Result: Script organized by ///$tab sections with line ranges
```

#### Script Preview with Line Numbers

```text
"Show me the first 1000 characters of the script from app 12345678-abcd-1234-efgh-123456789abc with line numbers"

Parameters used:
- max_preview_length: 1000
- include_line_numbers: true
- Result: Truncated script with line numbers for easy reference
```

#### Complete Analysis with All Features

```text
"Perform a comprehensive analysis of the script from app 12345678-abcd-1234-efgh-123456789abc including BINARY LOAD detection, sections, and show line numbers"

Parameters used:
- analyze_script: true
- include_sections: true  
- include_line_numbers: true
- Result: Full analysis with BINARY LOAD extraction, sections, variables, and formatted output
```

**Script Analysis Response Includes:**

- Total lines, empty lines, comment lines
- Script sections/tabs with line ranges
- BINARY LOAD statements with source applications and line numbers
- Count of LOAD, STORE, DROP statements
- SET and LET variable declarations
- Connection strings (sanitized)
- Include file references
- Subroutine definitions

📚 **[Complete Script Tool Usage Guide](docs/SCRIPT_TOOL_USAGE.md)** - Comprehensive documentation with all parameters and advanced examples

### Using with Different MCP Clients

#### Cursor IDE

- **Important**: Switch to Agent Mode (not Ask Mode) to access MCP tools
- Tools are available through natural language commands
- Cursor will ask for permission before executing tools (configurable in settings)
- Example: "Use the Qlik tools to list all available applications"

#### VS Code

- Access tools through the MCP extension
- Use the command palette or natural language interface
- Tools execute with appropriate permissions

#### Claude Desktop

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

The sheets tool will return:

- Sheet IDs and titles
- Sheet descriptions and metadata
- Layout information (columns, rows)
- Publication status and creation dates
- Total count of sheets

The sheet objects tool will return:

- Visualization object IDs and types
- Object titles and subtitles
- Position and sizing information
- Object properties and layout details
- Dimension and measure configurations with Master Item resolution
- VizlibContainer objects with embedded visualizations
- Container structure with tabs/panels and nested objects
- Total count of objects on the sheet

The dimensions tool will return:

- Dimension IDs and titles
- Dimension descriptions and definitions
- Field definitions and labels
- Grouping information and hierarchy
- Tags and metadata
- Total count of dimensions

The script tool will return:

- Complete data loading script content
- Script length in characters
- All LOAD statements and transformations
- Data connection strings and sources
- Variable definitions and SET statements

The data sources tool will return:

- Data source names and types
- Connection strings and statements
- Source categorization (file, binary, resident, inline)
- Source counts by type
- Lineage and dependency information
- Total count of all data sources

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

### `get_app_sheets` Tool

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `app_id` | string | Yes | Qlik Sense application ID |
| `include_thumbnail` | boolean | No | Include sheet thumbnail images (default: false) |
| `include_metadata` | boolean | No | Include detailed metadata (default: true) |

### `get_sheet_objects` Tool

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `app_id` | string | Yes | Qlik Sense application ID |
| `sheet_id` | string | Yes | Sheet ID to retrieve objects from |
| `include_properties` | boolean | No | Include object properties (default: true) |
| `include_layout` | boolean | No | Include object layout information (default: true) |
| `include_data_definition` | boolean | No | Include measure/dimension definitions (default: true) |
| `resolve_master_items` | boolean | No | Resolve Master Item references to full expressions (default: true) |

### `get_app_dimensions` Tool

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `app_id` | string | Yes | Qlik Sense application ID |
| `include_title` | boolean | No | Include dimension titles (default: true) |
| `include_tags` | boolean | No | Include dimension tags (default: true) |
| `include_grouping` | boolean | No | Include grouping information (default: true) |
| `include_info` | boolean | No | Include additional metadata (default: true) |

### `get_app_script` Tool

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `app_id` | string | Yes | Qlik Sense application ID |
| `analyze_script` | boolean | No | Enable comprehensive script analysis including BINARY LOAD extraction (default: false) |
| `include_sections` | boolean | No | Parse script into sections/tabs based on ///$tab markers (default: false) |
| `include_line_numbers` | boolean | No | Add line numbers to script output (default: false) |
| `max_preview_length` | integer | No | Maximum characters to return for script preview (minimum: 100) |

### `get_app_data_sources` Tool

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `app_id` | string | Yes | Qlik Sense application ID |
| `include_resident` | boolean | No | Include resident table sources (default: true) |
| `include_file_sources` | boolean | No | Include file-based sources (default: true) |
| `include_binary_sources` | boolean | No | Include binary load sources (default: true) |
| `include_inline_sources` | boolean | No | Include inline data sources (default: true) |

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
  "retrieved_at": "2025-08-29T10:30:00Z",
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
      "name": "CRM Dashboard",
      "last_reload_time": "2025-08-29T10:30:00Z",
      "meta": {},
      "doc_type": ""
    }
  ],
  "count": 50,
  "retrieved_at": "2025-08-29T10:30:00Z"
}
```

### `get_app_variables` Response

```json
{
  "app_id": "12345678-abcd-1234-efgh-123456789abc",
  "variables": [
    {
      "name": "vDataSource",
      "definition": "dev",
      "tags": [],
      "is_reserved": false,
      "is_config": false
    }
  ],
  "count": 25,
  "retrieved_at": "2025-08-29T10:30:00Z",
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
      "name": "customer_id",
      "source_tables": ["fact_crm", "dim_customer"],
      "is_system": false,
      "is_hidden": false,
      "is_numeric": true,
      "cardinal": 4818662,
      "tags": ["$key", "$numeric", "$integer"]
    }
  ],
  "tables": [
    "fact_transactions",
    "dim_customer_details"
  ],
  "field_count": 60,
  "table_count": 10,
  "retrieved_at": "2025-08-29T10:30:00Z",
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
      "title": "Summary View",
      "description": "Summary of OKRs",
      "rank": 0,
      "columns": 14,
      "rows": 10,
      "meta": {
        "created": "2025-08-15T09:00:00Z",
        "modified": "2025-08-29T10:30:00Z",
        "published": true
      }
    }
  ],
  "count": 5,
  "retrieved_at": "2025-08-29T10:30:00Z",
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
  "retrieved_at": "2025-08-29T10:30:00Z",
  "options": {
    "include_properties": true,
    "include_layout": true,
    "include_data_definition": true,
    "resolve_master_items": true
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
        "created": "2025-08-10T14:30:00Z",
        "approved": true
      }
    }
  ],
  "count": 30,
  "retrieved_at": "2025-08-29T10:30:00Z",
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
  "retrieved_at": "2025-08-29T10:30:00Z"
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
  "retrieved_at": "2025-08-29T10:30:00Z",
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
├── .github/workflows/      # CI/CD automation
│   └── test.yml           # GitHub Actions test pipeline
├── .claude/                # Claude Code configuration
│   └── settings.local.json # Local Claude settings
├── src/                    # Core application code
│   ├── __init__.py         # Package initialization
│   ├── server.py           # FastMCP server implementation
│   ├── qlik_client.py      # Qlik Engine API WebSocket client
│   └── tools.py            # MCP tool definitions and implementations
├── tests/                  # Comprehensive test suite (pytest)
│   ├── conftest.py         # Pytest configuration and fixtures
│   ├── README.md           # Testing documentation and guidelines
│   ├── test_qlik_connection.py    # Test basic connection
│   ├── test_list_apps.py          # Test application listing
│   ├── test_mcp_tool.py           # Test MCP tool functions (includes measures)
│   ├── test_variables.py          # Test variable retrieval
│   ├── test_fields.py             # Test field retrieval
│   ├── test_sheets.py             # Test sheet retrieval
│   ├── test_dimensions.py         # Test dimension retrieval
│   ├── test_script.py             # Test script retrieval and analysis
│   ├── test_data_sources.py       # Test data source retrieval
│   ├── test_binary_extraction.py  # Test BINARY LOAD extraction
│   ├── test_vizlib_container.py   # Test VizlibContainer functionality
│   └── test_both_tools.py         # Test multiple tools together
├── examples/               # Configuration examples
│   ├── cursor_config.json         # Cursor IDE configuration
│   ├── vscode_config.json         # VS Code configuration
│   ├── claude_desktop_config.json # Claude Desktop configuration
│   └── README.md           # Configuration instructions
├── docs/                   # Documentation
│   ├── CERTIFICATES.md     # Certificate setup guide
│   ├── API_REFERENCE.md    # Complete API documentation
│   ├── SCRIPT_TOOL_USAGE.md # Script tool usage guide
│   └── TROUBLESHOOTING.md  # Troubleshooting guide
├── certs/                  # SSL certificates (gitignored)
│   ├── root.pem           # Server root certificate
│   ├── client.pem         # Client certificate
│   └── client_key.pem     # Client private key
├── .env.example           # Example environment configuration
├── .env.test.example      # Test environment configuration template
├── .env                   # Environment configuration (gitignored)
├── .gitignore            # Git ignore rules
├── pyproject.toml         # Python project configuration and dependencies
├── pytest.ini            # Pytest configuration and markers
├── uv.lock               # UV dependency lockfile for reproducible builds
├── start_server.py       # Server startup script
├── CLAUDE.md             # Claude Code instructions
├── CONTRIBUTING.md       # Contribution guidelines
├── LICENSE               # MIT license
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

1. **Server won't start**: Check Python version (3.10+ required)
2. **Tool not found**: Restart Claude Desktop after configuration changes
3. **No response**: Check server logs for errors

## Development

### Running Tests

The project uses **pytest** exclusively for professional-grade testing with clear separation between unit and integration tests.

#### Setup Test Environment

```bash
# Install test dependencies (automatically handled by UV)
uv sync  # Installs both main and dev dependencies including pytest

# Configure test environment for integration tests
cp .env.test.example .env.test
# Edit .env.test with your Qlik server details (when available)
```

#### Pytest Testing Commands

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run only unit tests (no Qlik server required - perfect for development)
uv run pytest -m unit

# Run integration tests (requires Qlik server connection)
uv run pytest -m integration

# Run with coverage report
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/test_mcp_tool.py

# Run specific test function
uv run pytest tests/test_mcp_tool.py::test_get_app_measures_mock
```

#### Test Categories

The test suite uses pytest markers for clear organization:

- **`@pytest.mark.unit`**: Fast tests that don't require external dependencies
- **`@pytest.mark.integration`**: Tests requiring live Qlik Sense server connection
- **`@pytest.mark.slow`**: Long-running tests (can be excluded with `-m "not slow"`)

> **Pro Tip**: Use `uv run pytest -m unit` during development for fast feedback loops, then run integration tests when you have Qlik server access.

#### Test Specific Functionality

```bash
# Test specific components with pytest
uv run pytest tests/test_mcp_tool.py -v           # MCP tool functions (includes measures)
uv run pytest tests/test_variables.py -v          # Variable retrieval
uv run pytest tests/test_fields.py -v             # Field and table information
uv run pytest tests/test_sheets.py -v             # Sheet metadata
uv run pytest tests/test_dimensions.py -v         # Dimension analysis
uv run pytest tests/test_script.py -v             # Script retrieval and analysis
uv run pytest tests/test_data_sources.py -v       # Data source lineage
uv run pytest tests/test_binary_extraction.py -v  # BINARY LOAD extraction
uv run pytest tests/test_vizlib_container.py -v   # VizlibContainer functionality
uv run pytest tests/test_both_tools.py -v         # Multiple tools together

# Debug Qlik client directly
uv run python -m src.qlik_client
```

See [tests/README.md](tests/README.md) for comprehensive testing documentation.

### Code Quality & Formatting

The project maintains high code quality standards with automated tooling:

```bash
# Run Ruff linting and formatting
uv run ruff check                    # Check for style and quality issues
uv run ruff check --fix              # Auto-fix issues where possible
uv run ruff format                   # Format code according to standards

# The project is configured with:
# - pyproject.toml: Ruff configuration for consistent code style
# - Automatic import sorting and code formatting
# - Integration with development workflow
```

### Continuous Integration (CI/CD)

The project includes a comprehensive GitHub Actions workflow (`.github/workflows/test.yml`) that automatically:

**🔄 Automated Testing**:
- Runs on every push to `main` and `develop` branches
- Executes on all pull requests
- Matrix testing across multiple Python versions (3.10, 3.11, 3.12, 3.13)
- Separate unit test and integration test execution

**🛠️ Quality Assurance**:
- UV dependency management and caching
- Ruff linting and formatting verification
- Pytest execution with coverage reporting
- Test result reporting and failure notifications

**🚀 Manual Triggers**:
- Workflow can be manually triggered via GitHub Actions UI
- Optional integration test execution (when Qlik server access is available)

The CI/CD pipeline ensures code quality and prevents regressions, making the project reliable for production use.

### Adding New Tools

To add more Qlik tools:

1. Define a Pydantic model in `tools.py` for parameter validation with Field annotations
2. Implement the tool function in `tools.py`
3. Register the tool in `server.py` using `@mcp.tool()` accepting the Pydantic model
4. FastMCP automatically generates schemas from Pydantic models

### Tool Definitions

The server provides 9 comprehensive tools for complete Qlik Sense analysis. See the main tools table above for complete details and parameters.

## Limitations

Current implementation considerations:

- Single app connection at a time
- No retry logic for failed connections
- Basic error handling
- No caching of results
- Sequential processing only
- Minimal logging

## Future Enhancements

The project has achieved a modern, production-ready foundation. Potential enhancements:

**📈 Scalability & Performance**:
- Connection pooling for multiple concurrent app connections
- Intelligent caching of frequently accessed data
- WebSocket reconnection handling with retry logic

**🔧 Additional Functionality**:
- Tools for additional Qlik objects (bookmarks, stories, etc.)
- Advanced filtering and pagination for large datasets
- Bulk operations for enterprise-scale deployments

**🔍 Observability & Monitoring**:
- Structured logging with configurable levels
- Performance metrics and monitoring endpoints
- Distributed tracing for complex operations

> **Note**: The core development infrastructure (UV, Ruff, Pytest, GitHub Actions) is already enterprise-ready, providing a solid foundation for these future enhancements.

## Recent Enhancements

### Script Tool v2.0 (Latest)

- ✨ **BINARY LOAD Detection**: Automatically extracts all BINARY LOAD statements with source applications
- 📑 **Section Parsing**: Organizes scripts by ///$tab markers with line ranges
- 📊 **Comprehensive Analysis**: Statement counting, variable extraction, connection detection
- 🔒 **Security Enhancements**: Automatic password and credential sanitization
- 📏 **Line Numbering**: Optional line numbers for easy reference
- ✂️ **Script Preview**: Configurable truncation for large scripts
- 📚 **Enhanced Documentation**: Complete usage guide with examples

## License

This project is licensed under MIT. Ensure compliance with your organization's Qlik Sense licensing terms.

## Support

For technical support:

1. Check the troubleshooting section
2. Verify Qlik server connectivity
3. Review server logs for detailed error messages
4. Ensure certificates are valid and not expired
