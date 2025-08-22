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
| `get_sheet_objects` | Get objects from sheet | `app_id`, `sheet_id` | `include_properties`, `include_layout`, `include_data` |
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
    "qv_finance_placement_interval"
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
  "app_id": "fb41d1e1-38fb-4595-8391-2f1a536bceb1",
  "sheets": [
    {
      "id": "sheet_id",
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

---

### `get_sheet_objects`

Retrieves all visualization objects from a specific sheet.

**Parameters**:
- `app_id` (string, required): Qlik Sense application ID
- `sheet_id` (string, required): Sheet ID
- `include_properties` (boolean, optional): Include object properties (default: true)
- `include_layout` (boolean, optional): Include object layout (default: true)
- `include_data` (boolean, optional): Include data definitions (default: false)

**Response**:
```json
{
  "app_id": "fb41d1e1-38fb-4595-8391-2f1a536bceb1",
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
  "retrieved_at": "2024-01-20T10:30:00Z",
  "options": {
    "include_properties": true,
    "include_layout": true,
    "include_data": false
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
  "app_id": "fb41d1e1-38fb-4595-8391-2f1a536bceb1",
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
  "retrieved_at": "2024-01-20T10:30:00Z",
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

Retrieves the complete data loading script from a specific Qlik Sense application.

**Parameters**:
- `app_id` (string, required): Qlik Sense application ID

**Response**:
```json
{
  "app_id": "fb41d1e1-38fb-4595-8391-2f1a536bceb1",
  "script": "// Main data loading script\nLOAD * FROM 'data.qvd' (qvd);\n",
  "script_length": 39439,
  "retrieved_at": "2024-01-20T10:30:00Z"
}
```

---

### `get_app_data_sources`

Retrieves data sources and lineage information from a specific Qlik Sense application.

**Parameters**:
- `app_id` (string, required): Qlik Sense application ID
- `include_resident` (boolean, optional): Include resident sources (default: true)
- `include_file` (boolean, optional): Include file sources (default: true)
- `include_binary` (boolean, optional): Include binary sources (default: true)
- `include_inline` (boolean, optional): Include inline sources (default: true)

**Response**:
```json
{
  "app_id": "fb41d1e1-38fb-4595-8391-2f1a536bceb1",
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
  "retrieved_at": "2024-01-20T10:30:00Z",
  "options": {
    "include_resident": true,
    "include_file": true,
    "include_binary": true,
    "include_inline": true
  }
}
```

## Error Responses

All tools return consistent error responses when issues occur:

```json
{
  "error": "Connection failed",
  "details": "Unable to connect to Qlik server at server.example.com:4747",
  "timestamp": "2024-01-20T10:30:00Z",
  "app_id": "fb41d1e1-38fb-4595-8391-2f1a536bceb1"
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