"""MCP tool definitions for Qlik measure retrieval"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
import re


class GetAppMeasuresArgs(BaseModel):
    """Arguments for the get_app_measures tool"""
    app_id: str = Field(description="Qlik Sense application ID")
    include_expression: bool = Field(
        default=True,
        description="Include measure expressions in the response"
    )
    include_tags: bool = Field(
        default=True,
        description="Include measure tags in the response"
    )


class GetAppVariablesArgs(BaseModel):
    """Arguments for the get_app_variables tool"""
    app_id: str = Field(description="Qlik Sense application ID")
    include_definition: bool = Field(
        default=True,
        description="Include variable definitions in the response"
    )
    include_tags: bool = Field(
        default=True,
        description="Include variable tags in the response"
    )
    show_reserved: bool = Field(
        default=True,
        description="Include reserved system variables"
    )
    show_config: bool = Field(
        default=True,
        description="Include configuration variables"
    )


class GetAppFieldsArgs(BaseModel):
    """Arguments for the get_app_fields tool"""
    app_id: str = Field(description="Qlik Sense application ID")
    show_system: bool = Field(
        default=True,
        description="Include system fields"
    )
    show_hidden: bool = Field(
        default=True,
        description="Include hidden fields"
    )
    show_derived_fields: bool = Field(
        default=True,
        description="Include derived fields"
    )
    show_semantic: bool = Field(
        default=True,
        description="Include semantic fields"
    )
    show_src_tables: bool = Field(
        default=True,
        description="Include source table information"
    )
    show_implicit: bool = Field(
        default=True,
        description="Include implicit fields"
    )


class GetAppSheetsArgs(BaseModel):
    """Arguments for the get_app_sheets tool"""
    app_id: str = Field(description="Qlik Sense application ID")
    include_thumbnail: bool = Field(
        default=False,
        description="Include sheet thumbnails"
    )
    include_metadata: bool = Field(
        default=True,
        description="Include sheet metadata"
    )


class GetSheetObjectsArgs(BaseModel):
    """Arguments for the get_sheet_objects tool"""
    app_id: str = Field(description="Qlik Sense application ID")
    sheet_id: str = Field(description="Sheet ID to analyze")
    include_properties: bool = Field(
        default=True,
        description="Include object properties"
    )
    include_layout: bool = Field(
        default=True,
        description="Include position/size info"
    )
    include_data_definition: bool = Field(
        default=True,
        description="Include measures/dimensions"
    )
    resolve_master_items: bool = Field(
        default=True,
        description="Resolve Master Item references to their full expressions"
    )


class GetAppDimensionsArgs(BaseModel):
    """Arguments for the get_app_dimensions tool"""
    app_id: str = Field(description="Qlik Sense application ID")
    include_title: bool = Field(
        default=True,
        description="Include dimension titles"
    )
    include_tags: bool = Field(
        default=True,
        description="Include dimension tags"
    )
    include_grouping: bool = Field(
        default=True,
        description="Include dimension grouping information"
    )
    include_info: bool = Field(
        default=True,
        description="Include detailed dimension information"
    )


class ScriptSection(BaseModel):
    """Represents a section/tab in the Qlik script"""
    name: str = Field(description="Section/tab name")
    start_line: int = Field(description="Starting line number")
    end_line: int = Field(description="Ending line number")
    content: str = Field(description="Section content")
    line_count: int = Field(description="Number of lines in section")


class BinaryLoadStatement(BaseModel):
    """Represents a BINARY LOAD statement in the script"""
    line_number: int = Field(description="Line number where statement appears")
    source_app: str = Field(description="Source application path or name")
    full_statement: str = Field(description="Complete BINARY LOAD statement")


class ScriptAnalysis(BaseModel):
    """Analysis and statistics of the script"""
    total_lines: int = Field(description="Total number of lines")
    empty_lines: int = Field(description="Number of empty lines")
    comment_lines: int = Field(description="Number of comment lines")
    sections: List[ScriptSection] = Field(default_factory=list, description="Script sections/tabs")
    load_statements: int = Field(description="Count of LOAD statements")
    store_statements: int = Field(description="Count of STORE statements")
    drop_statements: int = Field(description="Count of DROP statements")
    binary_load_statements: List[BinaryLoadStatement] = Field(default_factory=list, description="BINARY LOAD statements found")
    set_variables: List[Dict[str, Any]] = Field(default_factory=list, description="SET variable declarations")
    let_variables: List[Dict[str, Any]] = Field(default_factory=list, description="LET variable declarations")
    connections: List[str] = Field(default_factory=list, description="Connection strings found")
    includes: List[str] = Field(default_factory=list, description="Include/Must_Include files")
    subroutines: List[str] = Field(default_factory=list, description="Subroutine definitions")


class GetAppScriptArgs(BaseModel):
    """Arguments for the get_app_script tool"""
    app_id: str = Field(description="Qlik Sense application ID")
    analyze_script: bool = Field(
        default=False,
        description="Enable detailed script analysis and parsing"
    )
    include_sections: bool = Field(
        default=False,
        description="Parse and return script sections/tabs"
    )
    include_line_numbers: bool = Field(
        default=False,
        description="Add line numbers to script output"
    )
    max_preview_length: Optional[int] = Field(
        default=None,
        description="Maximum characters to return for script preview (None for full script)"
    )


class GetAppDataSourcesArgs(BaseModel):
    """Arguments for the get_app_data_sources tool"""
    app_id: str = Field(description="Qlik Sense application ID")
    include_resident: bool = Field(
        default=True,
        description="Include RESIDENT data sources"
    )
    include_file_sources: bool = Field(
        default=True,
        description="Include file-based data sources"
    )
    include_binary_sources: bool = Field(
        default=True,
        description="Include binary data sources"
    )
    include_inline_sources: bool = Field(
        default=True,
        description="Include inline data sources"
    )


async def get_app_measures(
    app_id: str,
    include_expression: bool = True,
    include_tags: bool = True
) -> Dict[str, Any]:
    """
    Retrieve all measures from a Qlik Sense application.
    
    Args:
        app_id: The Qlik Sense application ID
        include_expression: Whether to include measure expressions
        include_tags: Whether to include measure tags
    
    Returns:
        JSON object containing measure information
    """
    from .qlik_client import QlikClient
    
    client = QlikClient()
    
    try:
        # Connect to Qlik and open app
        if not client.connect(app_id):
            return {
                "error": "Failed to connect to Qlik Sense",
                "app_id": app_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Get measures
        result = client.get_measures(
            include_expression=include_expression,
            include_tags=include_tags
        )
        
        # Add metadata to response
        response = {
            "app_id": app_id,
            "measures": result["measures"],
            "count": result["count"],
            "retrieved_at": datetime.utcnow().isoformat(),
            "options": {
                "include_expression": include_expression,
                "include_tags": include_tags
            }
        }
        
        return response
        
    except Exception as e:
        return {
            "error": str(e),
            "app_id": app_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    finally:
        # Always disconnect
        client.disconnect()


async def list_qlik_applications() -> Dict[str, Any]:
    """
    Retrieve a list of all available Qlik Sense applications.
    
    Returns:
        JSON object containing application list with names and IDs
    """
    from .qlik_client import QlikClient
    
    client = QlikClient()
    
    try:
        # Connect to Qlik global context
        if not client.connect_global():
            return {
                "error": "Failed to connect to Qlik Sense",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Get application list
        result = client.get_doc_list()
        
        # Add metadata to response
        response = {
            "applications": result["applications"],
            "count": result["count"],
            "retrieved_at": datetime.utcnow().isoformat()
        }
        
        return response
        
    except Exception as e:
        return {
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    finally:
        # Always disconnect
        client.disconnect()


async def get_app_variables(
    app_id: str,
    include_definition: bool = True,
    include_tags: bool = True,
    show_reserved: bool = True,
    show_config: bool = True
) -> Dict[str, Any]:
    """
    Retrieve all variables from a Qlik Sense application.
    
    Args:
        app_id: The Qlik Sense application ID
        include_definition: Whether to include variable definitions
        include_tags: Whether to include variable tags
        show_reserved: Whether to include reserved system variables
        show_config: Whether to include configuration variables
    
    Returns:
        JSON object containing variable information
    """
    from .qlik_client import QlikClient
    
    client = QlikClient()
    
    try:
        # Connect to Qlik and open app
        if not client.connect(app_id):
            return {
                "error": "Failed to connect to Qlik Sense",
                "app_id": app_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Get variables
        result = client.get_variables(
            include_definition=include_definition,
            include_tags=include_tags,
            show_reserved=show_reserved,
            show_config=show_config
        )
        
        # Add metadata to response
        response = {
            "app_id": app_id,
            "variables": result["variables"],
            "count": result["count"],
            "retrieved_at": datetime.utcnow().isoformat(),
            "options": {
                "include_definition": include_definition,
                "include_tags": include_tags,
                "show_reserved": show_reserved,
                "show_config": show_config
            }
        }
        
        return response
        
    except Exception as e:
        return {
            "error": str(e),
            "app_id": app_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    finally:
        # Always disconnect
        client.disconnect()


async def get_app_fields(
    app_id: str,
    show_system: bool = True,
    show_hidden: bool = True,
    show_derived_fields: bool = True,
    show_semantic: bool = True,
    show_src_tables: bool = True,
    show_implicit: bool = True
) -> Dict[str, Any]:
    """
    Retrieve all fields from a Qlik Sense application.
    
    Args:
        app_id: The Qlik Sense application ID
        show_system: Whether to include system fields
        show_hidden: Whether to include hidden fields
        show_derived_fields: Whether to include derived fields
        show_semantic: Whether to include semantic fields
        show_src_tables: Whether to include source table information
        show_implicit: Whether to include implicit fields
    
    Returns:
        JSON object containing field information and data model insights
    """
    from .qlik_client import QlikClient
    
    client = QlikClient()
    
    try:
        # Connect to Qlik and open app
        if not client.connect(app_id):
            return {
                "error": "Failed to connect to Qlik Sense",
                "app_id": app_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Get fields
        result = client.get_fields(
            show_system=show_system,
            show_hidden=show_hidden,
            show_derived_fields=show_derived_fields,
            show_semantic=show_semantic,
            show_src_tables=show_src_tables,
            show_implicit=show_implicit
        )
        
        # Add metadata to response
        response = {
            "app_id": app_id,
            "fields": result["fields"],
            "tables": result.get("tables", []),
            "field_count": result["field_count"],
            "table_count": result.get("table_count", 0),
            "retrieved_at": datetime.utcnow().isoformat(),
            "options": {
                "show_system": show_system,
                "show_hidden": show_hidden,
                "show_derived_fields": show_derived_fields,
                "show_semantic": show_semantic,
                "show_src_tables": show_src_tables,
                "show_implicit": show_implicit
            }
        }
        
        return response
        
    except Exception as e:
        return {
            "error": str(e),
            "app_id": app_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    finally:
        # Always disconnect
        client.disconnect()


async def get_app_sheets(
    app_id: str,
    include_thumbnail: bool = False,
    include_metadata: bool = True
) -> Dict[str, Any]:
    """
    Retrieve all sheets from a Qlik Sense application.
    
    Args:
        app_id: The Qlik Sense application ID
        include_thumbnail: Whether to include sheet thumbnails
        include_metadata: Whether to include sheet metadata
    
    Returns:
        JSON object containing sheet information
    """
    from .qlik_client import QlikClient
    
    client = QlikClient()
    
    try:
        # Connect to Qlik and open app
        if not client.connect(app_id):
            return {
                "error": "Failed to connect to Qlik Sense",
                "app_id": app_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Get sheets
        result = client.get_sheets(
            include_thumbnail=include_thumbnail,
            include_metadata=include_metadata
        )
        
        # Add metadata to response
        response = {
            "app_id": app_id,
            "sheets": result["sheets"],
            "sheet_count": result["sheet_count"],
            "retrieved_at": datetime.utcnow().isoformat(),
            "options": {
                "include_thumbnail": include_thumbnail,
                "include_metadata": include_metadata
            }
        }
        
        return response
        
    except Exception as e:
        return {
            "error": str(e),
            "app_id": app_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    finally:
        # Always disconnect
        client.disconnect()


async def get_sheet_objects(
    app_id: str,
    sheet_id: str,
    include_properties: bool = True,
    include_layout: bool = True,
    include_data_definition: bool = True,
    resolve_master_items: bool = True
) -> Dict[str, Any]:
    """
    Retrieve all visualization objects from a specific sheet.
    
    Args:
        app_id: The Qlik Sense application ID
        sheet_id: The sheet ID to analyze
        include_properties: Whether to include object properties
        include_layout: Whether to include position/size info
        include_data_definition: Whether to include measures/dimensions
        resolve_master_items: Whether to resolve Master Item references
    
    Returns:
        JSON object containing visualization object details
    """
    from .qlik_client import QlikClient
    
    client = QlikClient()
    
    try:
        # Connect to Qlik and open app
        if not client.connect(app_id):
            return {
                "error": "Failed to connect to Qlik Sense",
                "app_id": app_id,
                "sheet_id": sheet_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Get sheet objects
        result = client.get_sheet_objects(
            sheet_id=sheet_id,
            include_properties=include_properties,
            include_layout=include_layout,
            include_data_definition=include_data_definition,
            resolve_master_items=resolve_master_items
        )
        
        # Add metadata to response
        response = {
            "app_id": app_id,
            "sheet_id": sheet_id,
            "sheet_title": result.get("sheet_title", ""),
            "objects": result["objects"],
            "object_count": result["object_count"],
            "retrieved_at": datetime.utcnow().isoformat(),
            "options": {
                "include_properties": include_properties,
                "include_layout": include_layout,
                "include_data_definition": include_data_definition,
                "resolve_master_items": resolve_master_items
            }
        }
        
        return response
        
    except Exception as e:
        return {
            "error": str(e),
            "app_id": app_id,
            "sheet_id": sheet_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    finally:
        # Always disconnect
        client.disconnect()


async def get_app_dimensions(
    app_id: str,
    include_title: bool = True,
    include_tags: bool = True,
    include_grouping: bool = True,
    include_info: bool = True
) -> Dict[str, Any]:
    """Retrieve all dimensions from a Qlik Sense application"""
    from .qlik_client import QlikClient
    
    client = QlikClient()
    
    try:
        # Connect to Qlik and open the specified app
        if not client.connect(app_id):
            return {
                "error": "Failed to connect to Qlik Engine",
                "app_id": app_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Get dimensions from the app
        dimensions_data = client.get_dimensions(
            include_title=include_title,
            include_tags=include_tags,
            include_grouping=include_grouping,
            include_info=include_info
        )
        
        # Build response
        response = {
            "app_id": app_id,
            "retrieved_at": datetime.utcnow().isoformat(),
            "dimension_count": dimensions_data["dimension_count"],
            "dimensions": dimensions_data["dimensions"],
            "options": {
                "include_title": include_title,
                "include_tags": include_tags,
                "include_grouping": include_grouping,
                "include_info": include_info
            }
        }
        
        return response
        
    except Exception as e:
        return {
            "error": str(e),
            "app_id": app_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    finally:
        # Always disconnect
        client.disconnect()


def parse_script_sections(script: str) -> List[ScriptSection]:
    """Parse script into sections/tabs based on ///$tab markers"""
    sections = []
    lines = script.split('\n')
    current_section = None
    current_content = []
    current_start = 0
    
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('///$tab'):
            # Save previous section if exists
            if current_section:
                sections.append(ScriptSection(
                    name=current_section,
                    start_line=current_start,
                    end_line=i - 1,
                    content='\n'.join(current_content),
                    line_count=len(current_content)
                ))
            
            # Start new section
            parts = line.strip().split(None, 1)
            current_section = parts[1] if len(parts) > 1 else f"Section_{len(sections) + 1}"
            current_content = []
            current_start = i + 1
        elif current_section is not None:
            current_content.append(line)
    
    # Save last section
    if current_section and current_content:
        sections.append(ScriptSection(
            name=current_section,
            start_line=current_start,
            end_line=len(lines),
            content='\n'.join(current_content),
            line_count=len(current_content)
        ))
    
    # If no sections found, treat entire script as one section
    if not sections and script.strip():
        sections.append(ScriptSection(
            name="Main",
            start_line=1,
            end_line=len(lines),
            content=script,
            line_count=len(lines)
        ))
    
    return sections


def extract_binary_load_statements(script: str) -> List[BinaryLoadStatement]:
    """Extract BINARY LOAD statements from the script"""
    binary_loads = []
    lines = script.split('\n')
    
    # Pattern to match BINARY LOAD statements (case-insensitive)
    # Matches: BINARY [path];  or  BINARY LOAD FROM [path];
    binary_pattern = re.compile(
        r'^\s*BINARY\s+(?:LOAD\s+FROM\s+)?([^;]+);?\s*$',
        re.IGNORECASE | re.MULTILINE
    )
    
    for i, line in enumerate(lines, 1):
        match = binary_pattern.match(line)
        if match:
            # Clean up the source app path - remove quotes, brackets, and whitespace
            source_app = match.group(1).strip()
            # Remove surrounding brackets if present
            if source_app.startswith('[') and source_app.endswith(']'):
                source_app = source_app[1:-1]
            # Remove surrounding quotes
            source_app = source_app.strip('"').strip("'")
            
            binary_loads.append(BinaryLoadStatement(
                line_number=i,
                source_app=source_app,
                full_statement=line.strip()
            ))
    
    return binary_loads


def perform_script_analysis(script: str, include_sections: bool = False) -> ScriptAnalysis:
    """Perform comprehensive analysis of the Qlik script"""
    lines = script.split('\n')
    
    # Initialize counters
    empty_lines = sum(1 for line in lines if not line.strip())
    comment_lines = sum(1 for line in lines if line.strip().startswith('//') or line.strip().startswith('/*'))
    
    # Parse sections if requested
    sections = parse_script_sections(script) if include_sections else []
    
    # Extract BINARY LOAD statements
    binary_loads = extract_binary_load_statements(script)
    
    # Count statement types (case-insensitive)
    script_upper = script.upper()
    load_statements = len(re.findall(r'\bLOAD\b', script_upper))
    store_statements = len(re.findall(r'\bSTORE\b', script_upper))
    drop_statements = len(re.findall(r'\bDROP\b', script_upper))
    
    # Extract SET and LET variables
    set_pattern = re.compile(r'^\s*SET\s+(\w+)\s*=\s*(.+?);?\s*$', re.IGNORECASE | re.MULTILINE)
    let_pattern = re.compile(r'^\s*LET\s+(\w+)\s*=\s*(.+?);?\s*$', re.IGNORECASE | re.MULTILINE)
    
    set_variables = []
    for match in set_pattern.finditer(script):
        set_variables.append({
            'name': match.group(1),
            'value': match.group(2).strip(),
            'line': script[:match.start()].count('\n') + 1
        })
    
    let_variables = []
    for match in let_pattern.finditer(script):
        let_variables.append({
            'name': match.group(1),
            'value': match.group(2).strip(),
            'line': script[:match.start()].count('\n') + 1
        })
    
    # Extract connection strings (simplified - matches CONNECT TO statements)
    connection_pattern = re.compile(r'^\s*(?:LIB\s+)?CONNECT\s+TO\s+(.+?);?\s*$', re.IGNORECASE | re.MULTILINE)
    connections = [match.group(1).strip().strip('"').strip("'") for match in connection_pattern.finditer(script)]
    
    # Extract includes
    include_pattern = re.compile(r'^\s*\$\((?:Must_)?Include\s*=\s*(.+?)\);?\s*$', re.IGNORECASE | re.MULTILINE)
    includes = [match.group(1).strip().strip('"').strip("'") for match in include_pattern.finditer(script)]
    
    # Extract subroutines
    sub_pattern = re.compile(r'^\s*SUB\s+(\w+)', re.IGNORECASE | re.MULTILINE)
    subroutines = [match.group(1) for match in sub_pattern.finditer(script)]
    
    return ScriptAnalysis(
        total_lines=len(lines),
        empty_lines=empty_lines,
        comment_lines=comment_lines,
        sections=sections,
        load_statements=load_statements,
        store_statements=store_statements,
        drop_statements=drop_statements,
        binary_load_statements=binary_loads,
        set_variables=set_variables,
        let_variables=let_variables,
        connections=connections,
        includes=includes,
        subroutines=subroutines
    )


def add_line_numbers(script: str) -> str:
    """Add line numbers to script content"""
    lines = script.split('\n')
    numbered_lines = []
    max_line_num = len(lines)
    padding = len(str(max_line_num))
    
    for i, line in enumerate(lines, 1):
        numbered_lines.append(f"{i:>{padding}}: {line}")
    
    return '\n'.join(numbered_lines)


def sanitize_script(script: str) -> str:
    """Sanitize sensitive information from script"""
    # Mask passwords in connection strings
    script = re.sub(
        r'(PASSWORD\s*=\s*)[\'"]?[^\'";\s]+[\'"]?',
        r'\1[MASKED]',
        script,
        flags=re.IGNORECASE
    )
    
    # Mask user credentials
    script = re.sub(
        r'(USER\s+ID\s*=\s*)[\'"]?[^\'";\s]+[\'"]?',
        r'\1[MASKED]',
        script,
        flags=re.IGNORECASE
    )
    
    return script


async def get_app_script(
    app_id: str,
    analyze_script: bool = False,
    include_sections: bool = False,
    include_line_numbers: bool = False,
    max_preview_length: Optional[int] = None
) -> Dict[str, Any]:
    """
    Retrieve and optionally analyze the script from a Qlik Sense application.
    
    Args:
        app_id: The Qlik Sense application ID
        analyze_script: Enable detailed script analysis and parsing
        include_sections: Parse and return script sections/tabs
        include_line_numbers: Add line numbers to script output
        max_preview_length: Maximum characters to return for script preview
    
    Returns:
        JSON object containing script content and optional analysis
    """
    from .qlik_client import QlikClient
    
    client = QlikClient()
    
    try:
        # Connect to Qlik and open the specified app
        if not client.connect(app_id):
            return {
                "error": "Failed to connect to Qlik Engine",
                "app_id": app_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Get script from the app
        script_data = client.get_script()
        
        if "error" in script_data:
            return {
                "error": script_data["error"],
                "app_id": app_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        script_content = script_data["script"]
        
        # Sanitize sensitive information
        script_content = sanitize_script(script_content)
        
        # Apply preview length limit if specified
        original_length = len(script_content)
        if max_preview_length and len(script_content) > max_preview_length:
            script_content = script_content[:max_preview_length]
            is_truncated = True
        else:
            is_truncated = False
        
        # Add line numbers if requested
        if include_line_numbers:
            script_content = add_line_numbers(script_content)
        
        # Build response
        response = {
            "app_id": app_id,
            "retrieved_at": datetime.utcnow().isoformat(),
            "script": script_content,
            "script_length": original_length,
            "is_truncated": is_truncated
        }
        
        # Add truncation info if applicable
        if is_truncated:
            response["truncated_at"] = max_preview_length
            response["truncation_note"] = f"Script truncated to {max_preview_length:,} characters (original: {original_length:,} characters)"
        
        # Perform analysis if requested
        if analyze_script or include_sections:
            analysis_result = perform_script_analysis(script_data["script"], include_sections=include_sections)
            
            # Convert Pydantic models to dict for JSON serialization
            analysis_dict = analysis_result.model_dump() if hasattr(analysis_result, 'model_dump') else analysis_result.dict()
            
            # Add analysis to response
            response["analysis"] = analysis_dict
            
            # Add summary statistics
            response["summary"] = {
                "total_lines": analysis_result.total_lines,
                "sections_count": len(analysis_result.sections),
                "load_statements": analysis_result.load_statements,
                "store_statements": analysis_result.store_statements,
                "binary_load_count": len(analysis_result.binary_load_statements),
                "variables_count": len(analysis_result.set_variables) + len(analysis_result.let_variables),
                "connections_count": len(analysis_result.connections),
                "subroutines_count": len(analysis_result.subroutines)
            }
        
        # Add sections separately if requested (for easier access)
        if include_sections and not analyze_script:
            sections = parse_script_sections(script_data["script"])
            response["sections"] = [section.dict() for section in sections]
            response["sections_count"] = len(sections)
        
        return response
        
    except Exception as e:
        import traceback
        return {
            "error": str(e),
            "error_type": type(e).__name__,
            "app_id": app_id,
            "timestamp": datetime.utcnow().isoformat(),
            "traceback": traceback.format_exc()
        }
    
    finally:
        # Always disconnect
        client.disconnect()


async def get_app_data_sources(
    app_id: str,
    include_resident: bool = True,
    include_file_sources: bool = True,
    include_binary_sources: bool = True,
    include_inline_sources: bool = True
) -> Dict[str, Any]:
    """Retrieve data sources from a Qlik Sense application's lineage"""
    from .qlik_client import QlikClient
    
    client = QlikClient()
    
    try:
        # Connect to Qlik and open the specified app
        if not client.connect(app_id):
            return {
                "error": "Failed to connect to Qlik Engine",
                "app_id": app_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Get lineage data from the app
        lineage_data = client.get_lineage(
            include_resident=include_resident,
            include_file_sources=include_file_sources,
            include_binary_sources=include_binary_sources,
            include_inline_sources=include_inline_sources
        )
        
        # Build response
        response = {
            "app_id": app_id,
            "retrieved_at": datetime.utcnow().isoformat(),
            "source_count": lineage_data["source_count"],
            "data_sources": lineage_data["data_sources"],
            "categories": lineage_data["categories"],
            "by_category": lineage_data["by_category"],
            "options": {
                "include_resident": include_resident,
                "include_file_sources": include_file_sources,
                "include_binary_sources": include_binary_sources,
                "include_inline_sources": include_inline_sources
            }
        }
        
        return response
        
    except Exception as e:
        return {
            "error": str(e),
            "app_id": app_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    finally:
        # Always disconnect
        client.disconnect()


# Tool metadata for MCP registration
TOOL_DEFINITIONS = {
    "get_app_measures": {
        "description": "Retrieve all measures from a Qlik Sense application",
        "inputSchema": {
            "type": "object",
            "properties": {
                "app_id": {
                    "type": "string",
                    "description": "Qlik Sense application ID"
                },
                "include_expression": {
                    "type": "boolean",
                    "description": "Include measure expressions in the response",
                    "default": True
                },
                "include_tags": {
                    "type": "boolean", 
                    "description": "Include measure tags in the response",
                    "default": True
                }
            },
            "required": ["app_id"]
        }
    },
    "list_qlik_applications": {
        "description": "Get a list of all available Qlik Sense applications with their names and IDs",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    "get_app_variables": {
        "description": "Retrieve all variables from a Qlik Sense application",
        "inputSchema": {
            "type": "object",
            "properties": {
                "app_id": {
                    "type": "string",
                    "description": "Qlik Sense application ID"
                },
                "include_definition": {
                    "type": "boolean",
                    "description": "Include variable definitions in the response",
                    "default": True
                },
                "include_tags": {
                    "type": "boolean", 
                    "description": "Include variable tags in the response",
                    "default": True
                },
                "show_reserved": {
                    "type": "boolean",
                    "description": "Include reserved system variables",
                    "default": True
                },
                "show_config": {
                    "type": "boolean",
                    "description": "Include configuration variables",
                    "default": True
                }
            },
            "required": ["app_id"]
        }
    },
    "get_app_fields": {
        "description": "Retrieve all fields and table information from a Qlik Sense application",
        "inputSchema": {
            "type": "object",
            "properties": {
                "app_id": {
                    "type": "string",
                    "description": "Qlik Sense application ID"
                },
                "show_system": {
                    "type": "boolean",
                    "description": "Include system fields",
                    "default": True
                },
                "show_hidden": {
                    "type": "boolean",
                    "description": "Include hidden fields",
                    "default": True
                },
                "show_derived_fields": {
                    "type": "boolean",
                    "description": "Include derived fields",
                    "default": True
                },
                "show_semantic": {
                    "type": "boolean",
                    "description": "Include semantic fields",
                    "default": True
                },
                "show_src_tables": {
                    "type": "boolean",
                    "description": "Include source table information",
                    "default": True
                },
                "show_implicit": {
                    "type": "boolean",
                    "description": "Include implicit fields",
                    "default": True
                }
            },
            "required": ["app_id"]
        }
    },
    "get_app_sheets": {
        "description": "Retrieve all sheets from a Qlik Sense application",
        "inputSchema": {
            "type": "object",
            "properties": {
                "app_id": {
                    "type": "string",
                    "description": "Qlik Sense application ID"
                },
                "include_thumbnail": {
                    "type": "boolean",
                    "description": "Include sheet thumbnails",
                    "default": False
                },
                "include_metadata": {
                    "type": "boolean",
                    "description": "Include sheet metadata",
                    "default": True
                }
            },
            "required": ["app_id"]
        }
    },
    "get_sheet_objects": {
        "description": "Retrieve all visualization objects from a specific sheet, including embedded objects in containers",
        "inputSchema": {
            "type": "object",
            "properties": {
                "app_id": {
                    "type": "string",
                    "description": "Qlik Sense application ID"
                },
                "sheet_id": {
                    "type": "string",
                    "description": "Sheet ID to analyze"
                },
                "include_properties": {
                    "type": "boolean",
                    "description": "Include object properties",
                    "default": True
                },
                "include_layout": {
                    "type": "boolean",
                    "description": "Include position/size info",
                    "default": True
                },
                "include_data_definition": {
                    "type": "boolean",
                    "description": "Include measures/dimensions",
                    "default": True
                },
                "resolve_master_items": {
                    "type": "boolean",
                    "description": "Resolve Master Item references to their full expressions",
                    "default": True
                }
            },
            "required": ["app_id", "sheet_id"]
        }
    },
    "get_app_dimensions": {
        "description": "Retrieve all dimensions from a Qlik Sense application",
        "inputSchema": {
            "type": "object",
            "properties": {
                "app_id": {
                    "type": "string",
                    "description": "Qlik Sense application ID"
                },
                "include_title": {
                    "type": "boolean",
                    "description": "Include dimension titles",
                    "default": True
                },
                "include_tags": {
                    "type": "boolean",
                    "description": "Include dimension tags",
                    "default": True
                },
                "include_grouping": {
                    "type": "boolean",
                    "description": "Include dimension grouping information",
                    "default": True
                },
                "include_info": {
                    "type": "boolean",
                    "description": "Include detailed dimension information",
                    "default": True
                }
            },
            "required": ["app_id"]
        }
    },
    "get_app_script": {
        "description": "Retrieve and optionally analyze the script from a Qlik Sense application, including BINARY LOAD statement extraction",
        "inputSchema": {
            "type": "object",
            "properties": {
                "app_id": {
                    "type": "string",
                    "description": "Qlik Sense application ID"
                },
                "analyze_script": {
                    "type": "boolean",
                    "description": "Enable detailed script analysis including BINARY LOAD extraction, variable declarations, and statement counts",
                    "default": False
                },
                "include_sections": {
                    "type": "boolean",
                    "description": "Parse and return script sections/tabs based on ///$tab markers",
                    "default": False
                },
                "include_line_numbers": {
                    "type": "boolean",
                    "description": "Add line numbers to script output for easier reference",
                    "default": False
                },
                "max_preview_length": {
                    "type": "integer",
                    "description": "Maximum characters to return for script preview (useful for very large scripts)",
                    "default": None
                }
            },
            "required": ["app_id"]
        }
    },
    "get_app_data_sources": {
        "description": "Retrieve data sources from a Qlik Sense application's lineage",
        "inputSchema": {
            "type": "object",
            "properties": {
                "app_id": {
                    "type": "string",
                    "description": "Qlik Sense application ID"
                },
                "include_resident": {
                    "type": "boolean",
                    "description": "Include RESIDENT data sources",
                    "default": True
                },
                "include_file_sources": {
                    "type": "boolean",
                    "description": "Include file-based data sources",
                    "default": True
                },
                "include_binary_sources": {
                    "type": "boolean",
                    "description": "Include binary data sources",
                    "default": True
                },
                "include_inline_sources": {
                    "type": "boolean",
                    "description": "Include inline data sources",
                    "default": True
                }
            },
            "required": ["app_id"]
        }
    }
}