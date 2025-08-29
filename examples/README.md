# Configuration Examples

This directory contains example configuration files for integrating the Qlik MCP Server with various MCP clients.

## Cursor IDE Configuration

The `cursor_config.json` file shows how to configure the Qlik MCP Server with Cursor IDE.

### Setup Steps:

1. Create the configuration directory and file:
   ```bash
   # For project-specific configuration (recommended)
   mkdir -p .cursor
   cp examples/cursor_config.json .cursor/mcp.json
   
   # OR for global configuration
   cp examples/cursor_config.json ~/.cursor/mcp.json
   ```

2. Update the paths in the configuration file:
   - Replace `/path/to/your/qlik-mcp-server` with the actual path to this project
   - Ensure the Python path points to your Python 3.11 installation

3. Enable MCP in Cursor:
   - Open Cursor Settings (Settings → Cursor Settings)
   - Find and enable the MCP servers option

4. Restart Cursor IDE or reload the window

5. Use in Agent Mode:
   - **Important**: Switch to Agent Mode (not Ask Mode) to access MCP tools
   - The Qlik Sense tools will be available through natural language commands

### Cursor-Specific Notes:
- Cursor uses `"mcpServers"` (camelCase) as the root key
- Tools are only accessible in Agent Mode
- Cursor will ask for permission before executing tools (can be disabled with YOLO mode in settings)

## VS Code Configuration

The `vscode_config.json` file shows how to configure the Qlik MCP Server with VS Code.

### Setup Steps:

1. Copy the example configuration:
   ```bash
   cp examples/vscode_config.json ~/.vscode/settings.json
   ```
   
   Or if you have existing VS Code settings, merge the configuration manually.

2. Update the paths in the configuration file:
   - Replace `/path/to/your/qlik-mcp-server` with the actual path to this project
   - Ensure the Python path points to your Python 3.11 installation

3. Restart VS Code or reload the window (Command Palette → "Developer: Reload Window")

4. The Qlik Sense tools will be available through the MCP extension in VS Code

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