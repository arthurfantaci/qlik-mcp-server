# API Reference

Complete reference for all 9 MCP tools provided by the Qlik MCP Server.

## Tool Overview

| Tool | Purpose | Required Parameters | Optional Parameters |
|------|---------|-------------------|-------------------|
| `list_qlik_applications` | List all applications | None | None |
| `get_app_measures` | Get measures from app | `app_id` | `include_expression`, `include_tags` |
| `get_app_variables` | Get variables from app | `app_id` | `include_definition`, `include_tags`, `show_reserved`, `show_config` |
| `get_app_fields` | Get fields and tables | `app_id` | Various visibility flags |
| `get_app_sheets` | Get sheets from app | `app_id` | `include_thumbnail`, `include_metadata` |
| `get_sheet_objects` | Get objects from sheet | `app_id`, `sheet_id` | `include_properties`, `include_layout`, `include_data_definition`, `resolve_master_items` |
| `get_app_dimensions` | Get dimensions from app | `app_id` | `include_title`, `include_tags`, `include_grouping`, `include_info` |
| `get_app_script` | Get data loading script | `app_id` | None |
| `get_app_data_sources` | Get data sources lineage | `app_id` | Source type filters |

## Detailed Tool Documentation

### `list_qlik_applications`

Lists all available Qlik Sense applications.

**Parameters**: None

**Response**:
```json
{
  "applications": [
    {
      "app_id": "12345678-abcd-1234-efgh-123456789abc",
      "name": "Financial Dashboard",
      "last_reload_time": "2025-08-29T10:30:00Z",
      "meta": {},
      "doc_type": ""
    }
  ],
  "count": 148,
  "retrieved_at": "2025-08-29T10:30:00Z"
}
```

---

### `get_app_measures`

Retrieves all measures from a specific Qlik Sense application.

**Parameters**:
- `app_id` (string, required): Qlik Sense application ID
- `include_expression` (boolean, optional): Include measure expressions (default: true)
- `include_tags` (boolean, optional): Include measure tags (default: true)

**Response**:
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

---

### `get_app_variables`

Retrieves all variables from a specific Qlik Sense application.

**Parameters**:
- `app_id` (string, required): Qlik Sense application ID
- `include_definition` (boolean, optional): Include variable definitions (default: true)
- `include_tags` (boolean, optional): Include variable tags (default: true)
- `show_reserved` (boolean, optional): Include reserved system variables (default: true)
- `show_config` (boolean, optional): Include configuration variables (default: true)

**Response**:
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
  "retrieved_at": "2025-08-29T10:30:00Z",
  "options": {
    "include_definition": true,
    "include_tags": true,
    "show_reserved": true,
    "show_config": true
  }
}
```

---

### `get_app_fields`

Retrieves all fields and table information from a specific Qlik Sense application.

**Parameters**:
- `app_id` (string, required): Qlik Sense application ID
- `show_system` (boolean, optional): Include system fields (default: true)
- `show_hidden` (boolean, optional): Include hidden fields (default: true)
- `show_derived_fields` (boolean, optional): Include derived fields (default: true)
- `show_semantic` (boolean, optional): Include semantic fields (default: true)
- `show_src_tables` (boolean, optional): Include source table information (default: true)
- `show_implicit` (boolean, optional): Include implicit fields (default: true)

**Response**:
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
    "qv_finance_placement_interval"
  ],
  "field_count": 88,
  "table_count": 14,
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

---

### `get_app_sheets`

Retrieves all sheets from a specific Qlik Sense application.

**Parameters**:
- `app_id` (string, required): Qlik Sense application ID
- `include_thumbnail` (boolean, optional): Include sheet thumbnails (default: false)
- `include_metadata` (boolean, optional): Include detailed metadata (default: true)

**Response**:
```json
{
  "app_id": "12345678-abcd-1234-efgh-123456789abc",
  "sheets": [
    {
      "id": "sheet_id",
      "title": "Overview Dashboard",
      "description": "Main overview of key metrics",
      "rank": 0,
      "columns": 24,
      "rows": 12,
      "meta": {
        "created": "2025-08-15T09:00:00Z",
        "modified": "2025-08-29T10:30:00Z",
        "published": true
      }
    }
  ],
  "count": 3,
  "retrieved_at": "2025-08-29T10:30:00Z",
  "options": {
    "include_thumbnail": false,
    "include_metadata": true
  }
}
```

---

### `get_sheet_objects`

Retrieves all visualization objects from a specific sheet.

**Parameters**:
- `app_id` (string, required): Qlik Sense application ID
- `sheet_id` (string, required): Sheet ID
- `include_properties` (boolean, optional): Include object properties (default: true)
- `include_layout` (boolean, optional): Include object layout (default: true)
- `include_data_definition` (boolean, optional): Include data definitions (default: true)
- `resolve_master_items` (boolean, optional): Resolve Master Item references to full expressions (default: true)

**Response**:
```json
{
  "app_id": "12345678-abcd-1234-efgh-123456789abc",
  "sheet_id": "sheet_id",
  "objects": [
    {
      "id": "object_id",
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
        "measures": ["Sum(Sales)"]
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

---

### `get_app_dimensions`

Retrieves all dimensions from a specific Qlik Sense application.

**Parameters**:
- `app_id` (string, required): Qlik Sense application ID
- `include_title` (boolean, optional): Include dimension titles (default: true)
- `include_tags` (boolean, optional): Include dimension tags (default: true)
- `include_grouping` (boolean, optional): Include grouping information (default: true)
- `include_info` (boolean, optional): Include additional info (default: true)

**Response**:
```json
{
  "app_id": "12345678-abcd-1234-efgh-123456789abc",
  "dimensions": [
    {
      "id": "dimension_id",
      "title": "Product Category",
      "description": "Product categorization",
      "grouping": "N",
      "field_defs": ["Category"],
      "field_labels": ["Product Category"],
      "tags": ["product", "hierarchy"]
    }
  ],
  "count": 23,
  "retrieved_at": "2025-08-29T10:30:00Z",
  "options": {
    "include_title": true,
    "include_tags": true,
    "include_grouping": true,
    "include_info": true
  }
}
```

---

### `get_app_script`

Retrieves and optionally analyzes the complete data loading script from a specific Qlik Sense application.

**Parameters**:
- `app_id` (string, required): Qlik Sense application ID
- `analyze_script` (boolean, optional): Enable comprehensive script analysis including BINARY LOAD extraction (default: false)
- `include_sections` (boolean, optional): Parse script into sections/tabs based on ///$tab markers (default: false)
- `include_line_numbers` (boolean, optional): Add line numbers to script output (default: false)
- `max_preview_length` (integer, optional): Maximum characters to return for script preview (minimum: 100)

**Basic Response**:
```json
{
  "app_id": "12345678-abcd-1234-efgh-123456789abc",
  "script": "// Main data loading script\nLOAD * FROM 'data.qvd' (qvd);\n",
  "script_length": 39439,
  "retrieved_at": "2025-08-29T10:30:00Z"
}
```

**Enhanced Analysis Response** (when `analyze_script: true`):
```json
{
  "app_id": "12345678-abcd-1234-efgh-123456789abc",
  "script": "// Main data loading script\nLOAD * FROM 'data.qvd' (qvd);\n",
  "script_length": 39439,
  "retrieved_at": "2025-08-29T10:30:00Z",
  "analysis": {
    "total_lines": 245,
    "empty_lines": 12,
    "comment_lines": 8,
    "sections": [
      {
        "name": "Main",
        "start_line": 1,
        "end_line": 245,
        "content": "...",
        "line_count": 245
      }
    ],
    "load_statements": 15,
    "store_statements": 2,
    "drop_statements": 1,
    "binary_load_statements": [
      {
        "line_number": 5,
        "source_app": "CustomerAnalytics.qvf",
        "full_statement": "BINARY [lib://Apps/CustomerAnalytics.qvf];"
      }
    ],
    "set_variables": [
      {
        "name": "vEnvironment",
        "value": "dev",
        "line": 10
      }
    ],
    "let_variables": [],
    "connections": ["lib://DataFiles"],
    "includes": ["lib://Scripts/common.qvs"],
    "subroutines": ["LoadCustomerData"]
  },
  "summary": {
    "total_lines": 245,
    "sections_count": 1,
    "load_statements": 15,
    "store_statements": 2,
    "binary_load_count": 1,
    "variables_count": 1,
    "connections_count": 1,
    "subroutines_count": 1
  }
}
```

---

### `get_app_data_sources`

Retrieves data sources and lineage information from a specific Qlik Sense application.

**Parameters**:
- `app_id` (string, required): Qlik Sense application ID
- `include_resident` (boolean, optional): Include resident sources (default: true)
- `include_file_sources` (boolean, optional): Include file sources (default: true)
- `include_binary_sources` (boolean, optional): Include binary sources (default: true)
- `include_inline_sources` (boolean, optional): Include inline sources (default: true)

**Response**:
```json
{
  "app_id": "12345678-abcd-1234-efgh-123456789abc",
  "data_sources": [
    {
      "name": "data_source_name",
      "type": "file",
      "connection_string": "lib://DataFiles/sales.qvd",
      "statement": "LOAD * FROM [lib://DataFiles/sales.qvd] (qvd);",
      "discrimination": {
        "type": "DataConnection",
        "label": "File source"
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
    "include_file_sources": true,
    "include_binary_sources": true,
    "include_inline_sources": true
  }
}
```

## Error Responses

All tools return consistent error responses when issues occur:

```json
{
  "error": "Connection failed",
  "details": "Unable to connect to Qlik server at server.example.com:4747",
  "timestamp": "2025-08-29T10:30:00Z",
  "app_id": "12345678-abcd-1234-efgh-123456789abc"
}
```

Common error types:
- **Connection errors**: Network or certificate issues
- **Authentication errors**: Invalid credentials or permissions
- **App errors**: Application not found or access denied
- **Data errors**: Unexpected data format or structure

## Usage Tips

1. **Start with `list_qlik_applications`** to get available app IDs
2. **Use optional parameters** to control response size and detail level
3. **Test with known applications** before using with production apps
4. **Check user permissions** if tools return empty results
5. **Monitor response times** with large applications