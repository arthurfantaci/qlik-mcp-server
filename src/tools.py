"""MCP tool definitions for Qlik measure retrieval"""

from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


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


class GetAppScriptArgs(BaseModel):
    """Arguments for the get_app_script tool"""
    app_id: str = Field(description="Qlik Sense application ID")


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
    include_data_definition: bool = True
) -> Dict[str, Any]:
    """
    Retrieve all visualization objects from a specific sheet.
    
    Args:
        app_id: The Qlik Sense application ID
        sheet_id: The sheet ID to analyze
        include_properties: Whether to include object properties
        include_layout: Whether to include position/size info
        include_data_definition: Whether to include measures/dimensions
    
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
            include_data_definition=include_data_definition
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
                "include_data_definition": include_data_definition
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


async def get_app_script(app_id: str) -> Dict[str, Any]:
    """Retrieve the script from a Qlik Sense application"""
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
        
        # Build response
        response = {
            "app_id": app_id,
            "retrieved_at": datetime.utcnow().isoformat(),
            "script": script_data["script"],
            "script_length": script_data["script_length"]
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
        "description": "Retrieve all visualization objects from a specific sheet",
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
        "description": "Retrieve the script from a Qlik Sense application",
        "inputSchema": {
            "type": "object",
            "properties": {
                "app_id": {
                    "type": "string",
                    "description": "Qlik Sense application ID"
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