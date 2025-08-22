# Qlik MCP Server

A lightweight MCP (Model Context Protocol) server that exposes Qlik Sense measure information to AI assistants and other MCP clients.

## Features

- 🔌 Direct WebSocket connection to Qlik Sense Enterprise
- 🔐 Certificate-based authentication
- 📊 Retrieve all measures from any Qlik Sense application
- 📋 List all available Qlik applications with names and IDs
- 🔧 Retrieve all variables from any Qlik Sense application
- 📊 Retrieve all fields and table information for data model analysis
- 📄 Retrieve all sheets from any Qlik Sense application
- 🎨 Retrieve visualization objects with detailed metadata from sheets
- 🤖 MCP-compatible for use with Claude and other AI tools
- ⚡ Lightweight and focused implementation

## Prerequisites

- Python 3.8+
- Access to Qlik Sense Enterprise server
- Valid Qlik client certificates
- MCP-compatible client (e.g., Claude Desktop)

## Installation

1. **Clone or download this repository**:

   ```bash
   cd qlik-mcp-server
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure certificates**:
   - Ensure your Qlik certificates are in the `certs/` directory:
     - `root.pem` - Root certificate
     - `client.pem` - Client certificate
     - `client_key.pem` - Client private key

4. **Configure environment**:
   - Edit `.env` file with your Qlik server details:

   ```env
   QLIK_SERVER_URL=your.qlik.server.ip
   QLIK_SERVER_PORT=4747
   QLIK_USER_DIRECTORY=INTERNAL
   QLIK_USER_ID=sa_engine
   ```

## Usage

### Testing the Connection

Test the Qlik connection directly:

```bash
python -m src.qlik_client
```

### Running as MCP Server

Start the MCP server:

```bash
python -m src.server
```

### Configuring with Claude Desktop

Add to your Claude Desktop configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "qlik-sense": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/qlik-mcp-server"
    }
  }
}
```

### Using the Tools

Once configured, you can use all six tools in Claude:

**Get Application Measures:**

```text
"Can you get all measures from Qlik app fb41d1e1-38fb-4595-8391-2f1a536bceb1?"
```

**List All Applications:**

```text
"Can you get a list of all Qlik Sense applications along with the app ids?"
```

**Get Application Variables:**

```text
"Can you get all variables from Qlik app fb41d1e1-38fb-4595-8391-2f1a536bceb1?"
```

**Get Application Fields:**

```text
"Can you get all fields and table information from Qlik app fb41d1e1-38fb-4595-8391-2f1a536bceb1?"
```

**Get Application Sheets:**

```text
"Can you get all sheets from Qlik app fb41d1e1-38fb-4595-8391-2f1a536bceb1?"
```

**Get Sheet Objects:**

```text
"Can you get all visualization objects from sheet 'sheet123' in Qlik app fb41d1e1-38fb-4595-8391-2f1a536bceb1?"
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
  "app_id": "fb41d1e1-38fb-4595-8391-2f1a536bceb1",
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
      "app_id": "fb41d1e1-38fb-4595-8391-2f1a536bceb1",
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
  "app_id": "fb41d1e1-38fb-4595-8391-2f1a536bceb1",
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
  "app_id": "fb41d1e1-38fb-4595-8391-2f1a536bceb1",
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

## Project Structure

```text
qlik-mcp-server/
├── src/
│   ├── __init__.py         # Package initialization
│   ├── server.py           # MCP server implementation
│   ├── qlik_client.py      # Qlik WebSocket client
│   └── tools.py            # MCP tool definitions
├── certs/                  # Qlik certificates (gitignored)
├── .env                    # Configuration (gitignored)
├── .gitignore             # Git ignore rules
├── requirements.txt        # Python dependencies
└── README.md              # This file
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

Test the Qlik connection and measure retrieval:

```bash
python test_qlik_connection.py
```

Test application listing:

```bash
python test_list_apps.py
```

Test variable retrieval:

```bash
python test_variables.py
```

Test field list retrieval:

```bash
python test_fields.py
```

Test MCP tool functions directly:

```bash
python test_mcp_tool.py
```

### Adding New Tools

To add more Qlik tools:

1. Define the tool function in `tools.py`
2. Add tool metadata to `TOOL_DEFINITIONS`
3. Register the tool in `server.py` using `@mcp.tool()`

### Available Tools

1. **get_app_measures**: Retrieves all measures from a specific Qlik application
2. **list_qlik_applications**: Lists all available Qlik applications with names and IDs
3. **get_app_variables**: Retrieves all variables from a specific Qlik application
4. **get_app_fields**: Retrieves all fields and table information from a specific Qlik application

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
