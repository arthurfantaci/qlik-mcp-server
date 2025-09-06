# Script Tool Usage Guide

## Overview

The enhanced `get_app_script` tool provides comprehensive script retrieval and analysis capabilities for Qlik Sense applications. This guide covers all available features with detailed examples.

## Features

- **Basic Script Retrieval** - Get the complete application script
- **BINARY LOAD Detection** - Automatically extract all BINARY LOAD statements
- **Script Sectioning** - Parse scripts into logical sections based on ///$tab markers
- **Statement Analysis** - Count various statement types (LOAD, STORE, DROP)
- **Variable Extraction** - Identify SET and LET declarations
- **Line Numbering** - Add line numbers for easy reference
- **Script Preview** - Truncate large scripts for quick preview
- **Security Sanitization** - Automatic masking of sensitive information

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `app_id` | string | required | The Qlik Sense application ID |
| `analyze_script` | boolean | false | Enable comprehensive script analysis |
| `include_sections` | boolean | false | Parse script into sections/tabs |
| `include_line_numbers` | boolean | false | Add line numbers to output |
| `max_preview_length` | integer | null | Limit script to specified characters |

## Usage Examples

### 1. Basic Script Retrieval

**Prompt:**
```
"Get the script from application abc-demo-issuer"
```

**What happens:**
- Retrieves the complete script
- Sanitizes sensitive information
- Returns script content and length

**Response includes:**
```json
{
  "app_id": "12345678-abcd-1234-efgh-123456789abc",
  "script": "// Complete script content here...",
  "script_length": 33724,
  "retrieved_at": "2025-09-06T13:25:50.657026"
}
```

### 2. Script Analysis with BINARY LOAD Detection

**Prompt:**
```
"Analyze the script from app 12345678-abcd-1234-efgh-123456789abc and identify all BINARY LOAD statements"
```

**Parameters used:**
- `analyze_script: true`

**What happens:**
- Performs comprehensive script analysis
- Extracts all BINARY LOAD statements with source applications
- Counts all statement types
- Extracts variables and connections

**Response includes:**
```json
{
  "app_id": "12345678-abcd-1234-efgh-123456789abc",
  "script": "...",
  "analysis": {
    "total_lines": 1142,
    "empty_lines": 303,
    "comment_lines": 150,
    "load_statements": 48,
    "store_statements": 0,
    "drop_statements": 20,
    "binary_load_statements": [
      {
        "line_number": 7,
        "source_app": "lib://DataFiles/BaseApp.qvf",
        "full_statement": "BINARY [lib://DataFiles/BaseApp.qvf];"
      }
    ],
    "set_variables": [
      {"name": "ThousandSep", "value": ",", "line": 10},
      {"name": "DecimalSep", "value": ".", "line": 11}
    ],
    "let_variables": [
      {"name": "vDocumentTitle", "value": "DocumentTitle()", "line": 25}
    ]
  },
  "summary": {
    "binary_load_count": 1,
    "variables_count": 33,
    "connections_count": 2,
    "subroutines_count": 4
  }
}
```

### 3. Script with Section Breakdown

**Prompt:**
```
"Get the script from app 12345678-abcd-1234-efgh-123456789abc organized by sections"
```

**Parameters used:**
- `include_sections: true`

**What happens:**
- Parses script based on ///$tab markers
- Returns each section with line ranges
- Provides section content separately

**Response includes:**
```json
{
  "sections": [
    {
      "name": "Main",
      "start_line": 1,
      "end_line": 152,
      "content": "// Section content...",
      "line_count": 152
    },
    {
      "name": "Binary Load",
      "start_line": 154,
      "end_line": 160,
      "content": "BINARY [lib://DataFiles/BaseApp.qvf];",
      "line_count": 7
    }
  ],
  "sections_count": 38
}
```

### 4. Script Preview with Line Numbers

**Prompt:**
```
"Show me the first 500 characters of the script from app 12345678-abcd-1234-efgh-123456789abc with line numbers"
```

**Parameters used:**
- `max_preview_length: 500`
- `include_line_numbers: true`

**What happens:**
- Truncates script to 500 characters
- Adds line numbers to each line
- Indicates truncation in response

**Response includes:**
```json
{
  "script": "  1: ///$tab Main\n  2: SET ThousandSep=',';\n  3: SET DecimalSep='.';\n...",
  "script_length": 33724,
  "is_truncated": true,
  "truncated_at": 500,
  "truncation_note": "Script truncated to 500 characters (original: 33,724 characters)"
}
```

### 5. Complete Analysis with All Features

**Prompt:**
```
"Perform a comprehensive analysis of the script from app 12345678-abcd-1234-efgh-123456789abc. 
Include BINARY LOAD detection, section breakdown, and add line numbers. 
Show me the first 2000 characters."
```

**Parameters used:**
- `analyze_script: true`
- `include_sections: true`
- `include_line_numbers: true`
- `max_preview_length: 2000`

**What happens:**
- Performs full script analysis
- Extracts BINARY LOAD statements
- Parses sections
- Adds line numbers
- Truncates to 2000 characters

### 6. Finding Data Dependencies

**Prompt:**
```
"Check if app 12345678-abcd-1234-efgh-123456789abc has any BINARY LOAD dependencies on other applications"
```

**Parameters used:**
- `analyze_script: true`

**Use case:**
This is particularly useful for:
- Understanding app dependencies before migration
- Identifying data lineage
- Planning reload sequences
- Detecting circular dependencies

### 7. Variable Inventory

**Prompt:**
```
"Extract all variables from the script of app 12345678-abcd-1234-efgh-123456789abc"
```

**Parameters used:**
- `analyze_script: true`

**Returns:**
- All SET variables with values
- All LET variables with expressions
- Line numbers for each declaration

## Advanced Use Cases

### Migration Planning
```
"Analyze the script from our production app to identify all BINARY LOAD dependencies 
that need to be migrated together"
```

### Code Review
```
"Review the script structure of app 12345678-abcd-1234-efgh-123456789abc 
and show me the sections with line counts"
```

### Debugging Support
```
"Show me lines 500-600 of the script from app 12345678-abcd-1234-efgh-123456789abc 
with line numbers"
```
Note: Use max_preview_length and manual inspection for specific line ranges.

### Security Audit
```
"Analyze the script from app 12345678-abcd-1234-efgh-123456789abc 
and identify all connection strings"
```

## Response Structure

### Basic Response
```json
{
  "app_id": "string",
  "script": "string",
  "script_length": "integer",
  "retrieved_at": "ISO 8601 timestamp",
  "is_truncated": "boolean (if max_preview_length used)"
}
```

### With Analysis
Adds:
```json
{
  "analysis": {
    "total_lines": "integer",
    "empty_lines": "integer",
    "comment_lines": "integer",
    "sections": ["array of ScriptSection objects"],
    "binary_load_statements": ["array of BinaryLoadStatement objects"],
    "set_variables": ["array of variable objects"],
    "let_variables": ["array of variable objects"],
    "connections": ["array of connection strings"],
    "includes": ["array of include files"],
    "subroutines": ["array of subroutine names"]
  },
  "summary": {
    "sections_count": "integer",
    "binary_load_count": "integer",
    "variables_count": "integer",
    "connections_count": "integer"
  }
}
```

## Performance Considerations

1. **Large Scripts**: Use `max_preview_length` for scripts over 100KB
2. **Analysis Performance**: Full analysis adds ~100-200ms processing time
3. **Network**: Script retrieval depends on network latency to Qlik server
4. **Memory**: Large scripts (>10MB) may require additional memory

## Security Features

- **Automatic Password Masking**: Passwords in connection strings are replaced with [MASKED]
- **Credential Sanitization**: User IDs and sensitive data are sanitized
- **Safe BINARY LOAD Paths**: Source applications are validated and cleaned

## Troubleshooting

### Common Issues

1. **Empty Script Response**
   - Verify app_id is correct
   - Check user has script access permissions
   - Ensure app has a script (not all apps do)

2. **BINARY LOAD Not Detected**
   - Check script syntax is valid
   - Ensure BINARY statement is on its own line
   - Verify brackets/quotes are balanced

3. **Sections Not Found**
   - Sections require ///$tab markers
   - Without markers, entire script is one section
   - Check for typos in section markers

## Best Practices

1. **Start Simple**: Begin with basic retrieval, add analysis as needed
2. **Use Preview for Large Scripts**: Scripts over 1MB benefit from preview
3. **Combine Features Wisely**: Not all features are needed every time
4. **Cache Results**: Script content rarely changes during analysis sessions
5. **Security First**: Always use the tool's built-in sanitization

## Integration Examples

### With AI Assistants
```
"I need to understand the data flow in our sales dashboard app. 
Can you analyze the script and show me all data sources, 
especially any BINARY LOAD dependencies?"
```

### In Documentation Workflows
```
"Generate documentation for app 12345678-abcd-1234-efgh-123456789abc 
including script sections and BINARY LOAD dependencies"
```

### For Governance Reviews
```
"Audit the script of app 12345678-abcd-1234-efgh-123456789abc 
for hardcoded credentials and external data sources"
```

## Conclusion

The enhanced script tool transforms script analysis from a manual process to an automated, 
intelligent operation. Whether you're tracking BINARY LOAD dependencies, analyzing 
script structure, or performing security audits, the tool provides the insights you need 
in a format that's both human-readable and machine-processable.