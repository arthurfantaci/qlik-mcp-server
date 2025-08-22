# Configuration Examples

This directory contains example configuration files for integrating the Qlik MCP Server with various MCP clients.

## Claude Desktop Configuration

The `claude_desktop_config.json` file shows how to configure the Qlik MCP Server with Claude Desktop.

### Setup Steps:

1. Copy the example configuration:
   ```bash
   cp examples/claude_desktop_config.json ~/.config/claude_desktop_config.json
   ```

2. Update the paths in the configuration file:
   - Replace `/path/to/your/qlik-mcp-server` with the actual path to this project
   - Ensure the Python path points to your Python 3.11 installation

3. Restart Claude Desktop

4. The Qlik Sense tools will be available in your Claude Desktop conversations

## Other MCP Clients

This server follows the standard MCP protocol and should work with any MCP-compatible client. Refer to your client's documentation for specific configuration requirements.

The server exposes the following tools:
- `list_qlik_applications`
- `get_app_measures`
- `get_app_variables`
- `get_app_fields`
- `get_app_sheets`
- `get_sheet_objects`
- `get_app_dimensions`
- `get_app_script`
- `get_app_data_sources`