# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Model Context Protocol (MCP) server providing comprehensive access to Qlik Sense applications via WebSocket API. FastMCP-based implementation with 9 tools for extracting app metadata, expressions, scripts, and visualizations.

## Commands

```bash
# Setup (UV recommended, requires Python 3.10+)
uv sync                               # Install dependencies and create venv
cp .env.example .env                  # Configure Qlik server details

# Run server
uv run python -m src.server           # Start MCP server

# Test with pytest (recommended)
uv run pytest                           # Run all tests
uv run pytest -v                        # Verbose output
uv run pytest -m unit                   # Unit tests only (no Qlik needed)
uv run pytest -m integration            # Integration tests (requires Qlik)
uv run pytest --cov=src                 # With coverage report

# Legacy: Test individual files directly
uv run python tests/test_qlik_connection.py    # Test basic connection
uv run python tests/test_list_apps.py          # Test app listing
uv run python tests/test_mcp_tool.py           # Test measures and MCP integration

# Debug WebSocket client
uv run python -m src.qlik_client
```

## Architecture

### Core Components
- `src/server.py` - FastMCP server registration and tool handlers
- `src/tools.py` - 9 tool implementations with Pydantic validation
- `src/qlik_client.py` - WebSocket client for Qlik Engine API

### Key Patterns
- **SSL certificate authentication** via `certs/` directory
- **WebSocket connection** to Qlik Engine API
- **Session objects** for metadata (measures, variables, fields, dimensions)
- **Handle-based access** for sheets and visualizations
- **Pydantic models** with FastMCP auto-schema generation
- **Enhanced script analysis** with BINARY LOAD extraction and section parsing

### Connection Flow
1. Load SSL certificates → WebSocket connect
2. App operations: `OpenDoc` → create session objects → `GetLayout`
3. Global operations: connect to `/app/` → `GetDocList`
4. Sheets: `GetAllInfos` → `GetObject` → `GetLayout`
5. Always disconnect to prevent resource leaks

### Tool Patterns

**Parameter Validation**: All tools use Pydantic models with field constraints, custom validators, and auto-generated schemas for FastMCP.

**API Access**:
- Session objects: measures, variables, dimensions, fields (`CreateSessionObject` + `GetLayout`)
- Handle-based: sheets and visualizations (`GetObject` + `GetLayout`)
- Direct API: scripts (`GetScript`), data sources (`GetLineage`)
- Global context: app listing (`GetDocList`)

**Script Analysis Features**:
- BINARY LOAD extraction with regex parsing
- Section parsing via ///$tab markers
- Statement counting (LOAD/STORE/DROP)
- Variable extraction (SET/LET with line numbers)
- Credential masking for security

## Configuration

Required `.env` variables (see `.env.example`):
```
QLIK_SERVER_URL=your-qlik-server.com
QLIK_SERVER_PORT=4747
QLIK_USER_DIRECTORY=INTERNAL
QLIK_USER_ID=sa_engine
```

SSL certificates in `certs/` directory:
- `root.pem`, `client.pem`, `client_key.pem`

## Development Guidelines

### Adding New Tools
1. Define Pydantic model in `tools.py` with Field annotations
2. Implement tool function using appropriate API pattern (session objects, handles, or direct API)
3. Register in `server.py` with `@mcp.tool()` decorator
4. Create corresponding test file in `tests/`

### Critical API Patterns
- **Sheet objects**: Use `GetAllInfos` → `GetObject` → `GetLayout` (SheetList session objects don't work)
- **Connection contexts**: App-specific `/app/{app_id}` vs global `/app/` for listing
- **Resource management**: Always disconnect WebSocket connections
- **Data source categorization**: `GetLineage` returns mixed types, categorize by statement patterns

### VizlibContainer Support
Enhanced object extraction from VizlibContainer visualizations:
- Detects embedded objects within VizlibContainer layouts
- Extracts child object properties and expressions
- Resolves master item references to full definitions
- Handles complex nested visualization structures

## Testing

Run individual test files to verify functionality:

- Connection: `uv run python tests/test_qlik_connection.py`
- Applications: `uv run python tests/test_list_apps.py`
- All tools: `uv run python tests/test_mcp_tool.py`
- Specific features: `uv run python tests/test_script.py`, `test_vizlib_container.py`, etc.

## Key Implementation Notes

- Always use `uv run` prefix for command execution
- SSL certificates required in `certs/` directory
- Environment configuration via `.env` file
- Python 3.10+ required for FastMCP compatibility
- WebSocket connections must be properly closed to prevent resource leaks
