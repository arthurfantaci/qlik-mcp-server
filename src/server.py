#!/usr/bin/env python3
"""MCP Server for Qlik Sense measure retrieval"""

import os
import sys
import asyncio
from typing import Dict, Any
from datetime import datetime
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load environment variables - ensure we load from the correct directory
import pathlib
project_root = pathlib.Path(__file__).parent.parent
env_path = project_root / '.env'
load_dotenv(env_path)

# Import tools
from .tools import (
    get_app_measures, list_qlik_applications, get_app_variables, 
    get_app_fields, get_app_sheets, get_sheet_objects, get_app_dimensions, get_app_script, get_app_data_sources, TOOL_DEFINITIONS
)

# Create MCP server instance
mcp = FastMCP(
    name=os.getenv("MCP_SERVER_NAME", "qlik-sense"),
    version=os.getenv("MCP_SERVER_VERSION", "0.1.0")
)

# Register the get_app_measures tool
@mcp.tool()
async def handle_get_app_measures(
    app_id: str,
    include_expression: bool = True,
    include_tags: bool = True
) -> Dict[str, Any]:
    """
    MCP tool handler for retrieving Qlik Sense measures.
    
    This tool connects to a Qlik Sense server, opens the specified application,
    creates a MeasureList session object, retrieves all measure metadata,
    and returns the results as structured JSON.
    """
    print(f"📊 Retrieving measures for app: {app_id}", file=sys.stderr)
    print(f"📊 Environment check: QLIK_SERVER_URL={os.getenv('QLIK_SERVER_URL')}", file=sys.stderr)
    
    try:
        # Call the actual implementation
        result = await get_app_measures(
            app_id=app_id,
            include_expression=include_expression,
            include_tags=include_tags
        )
        
        if "error" in result:
            print(f"❌ Error: {result['error']}", file=sys.stderr)
        else:
            print(f"✅ Retrieved {result['count']} measures", file=sys.stderr)
        
        return result
        
    except Exception as e:
        error_response = {
            "error": f"Unexpected error: {str(e)}",
            "app_id": app_id
        }
        print(f"❌ Unexpected error in MCP handler: {e}", file=sys.stderr)
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}", file=sys.stderr)
        return error_response


# Register the list_qlik_applications tool
@mcp.tool()
async def handle_list_qlik_applications() -> Dict[str, Any]:
    """
    MCP tool handler for listing all Qlik Sense applications.
    
    This tool connects to Qlik Sense server global context and retrieves
    a list of all available applications with their names and IDs.
    """
    print("📋 Retrieving list of Qlik applications...", file=sys.stderr)
    print(f"📋 Environment check: QLIK_SERVER_URL={os.getenv('QLIK_SERVER_URL')}", file=sys.stderr)
    
    try:
        # Call the actual implementation
        result = await list_qlik_applications()
        
        if "error" in result:
            print(f"❌ Error: {result['error']}", file=sys.stderr)
        else:
            print(f"✅ Retrieved {result['count']} applications", file=sys.stderr)
        
        return result
        
    except Exception as e:
        error_response = {
            "error": f"Unexpected error: {str(e)}",
            "timestamp": datetime.utcnow().isoformat()
        }
        print(f"❌ Unexpected error in MCP handler: {e}", file=sys.stderr)
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}", file=sys.stderr)
        return error_response


# Register the get_app_variables tool
@mcp.tool()
async def handle_get_app_variables(
    app_id: str,
    include_definition: bool = True,
    include_tags: bool = True,
    show_reserved: bool = True,
    show_config: bool = True
) -> Dict[str, Any]:
    """
    MCP tool handler for retrieving Qlik Sense variables.
    
    This tool connects to a Qlik Sense server, opens the specified application,
    creates a VariableList session object, retrieves all variable metadata,
    and returns the results as structured JSON.
    """
    print(f"📋 Retrieving variables for app: {app_id}", file=sys.stderr)
    print(f"📋 Environment check: QLIK_SERVER_URL={os.getenv('QLIK_SERVER_URL')}", file=sys.stderr)
    
    try:
        # Call the actual implementation
        result = await get_app_variables(
            app_id=app_id,
            include_definition=include_definition,
            include_tags=include_tags,
            show_reserved=show_reserved,
            show_config=show_config
        )
        
        if "error" in result:
            print(f"❌ Error: {result['error']}", file=sys.stderr)
        else:
            print(f"✅ Retrieved {result['count']} variables", file=sys.stderr)
        
        return result
        
    except Exception as e:
        error_response = {
            "error": f"Unexpected error: {str(e)}",
            "app_id": app_id
        }
        print(f"❌ Unexpected error in MCP handler: {e}", file=sys.stderr)
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}", file=sys.stderr)
        return error_response


# Register the get_app_fields tool
@mcp.tool()
async def handle_get_app_fields(
    app_id: str,
    show_system: bool = True,
    show_hidden: bool = True,
    show_derived_fields: bool = True,
    show_semantic: bool = True,
    show_src_tables: bool = True,
    show_implicit: bool = True
) -> Dict[str, Any]:
    """
    MCP tool handler for retrieving Qlik Sense fields and table information.
    
    This tool connects to a Qlik Sense server, opens the specified application,
    creates a FieldList session object, retrieves all field metadata and table information,
    and returns the results as structured JSON for data model analysis.
    """
    print(f"📊 Retrieving fields for app: {app_id}", file=sys.stderr)
    print(f"📊 Environment check: QLIK_SERVER_URL={os.getenv('QLIK_SERVER_URL')}", file=sys.stderr)
    
    try:
        # Call the actual implementation
        result = await get_app_fields(
            app_id=app_id,
            show_system=show_system,
            show_hidden=show_hidden,
            show_derived_fields=show_derived_fields,
            show_semantic=show_semantic,
            show_src_tables=show_src_tables,
            show_implicit=show_implicit
        )
        
        if "error" in result:
            print(f"❌ Error: {result['error']}", file=sys.stderr)
        else:
            print(f"✅ Retrieved {result['field_count']} fields from {result['table_count']} tables", file=sys.stderr)
        
        return result
        
    except Exception as e:
        error_response = {
            "error": f"Unexpected error: {str(e)}",
            "app_id": app_id
        }
        print(f"❌ Unexpected error in MCP handler: {e}", file=sys.stderr)
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}", file=sys.stderr)
        return error_response


# Register the get_app_sheets tool
@mcp.tool()
async def handle_get_app_sheets(
    app_id: str,
    include_thumbnail: bool = False,
    include_metadata: bool = True
) -> Dict[str, Any]:
    """
    MCP tool handler for retrieving Qlik Sense sheets.
    
    This tool connects to a Qlik Sense server, opens the specified application,
    creates a SheetList session object, retrieves all sheet metadata,
    and returns the results as structured JSON.
    """
    print(f"📄 Retrieving sheets for app: {app_id}", file=sys.stderr)
    print(f"📄 Environment check: QLIK_SERVER_URL={os.getenv('QLIK_SERVER_URL')}", file=sys.stderr)
    
    try:
        # Call the actual implementation
        result = await get_app_sheets(
            app_id=app_id,
            include_thumbnail=include_thumbnail,
            include_metadata=include_metadata
        )
        
        if "error" in result:
            print(f"❌ Error: {result['error']}", file=sys.stderr)
        else:
            print(f"✅ Retrieved {result['sheet_count']} sheets", file=sys.stderr)
        
        return result
        
    except Exception as e:
        error_response = {
            "error": f"Unexpected error: {str(e)}",
            "app_id": app_id
        }
        print(f"❌ Unexpected error in MCP handler: {e}", file=sys.stderr)
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}", file=sys.stderr)
        return error_response


# Register the get_sheet_objects tool
@mcp.tool()
async def handle_get_sheet_objects(
    app_id: str,
    sheet_id: str,
    include_properties: bool = True,
    include_layout: bool = True,
    include_data_definition: bool = True
) -> Dict[str, Any]:
    """
    MCP tool handler for retrieving visualization objects from a sheet.
    
    This tool connects to a Qlik Sense server, opens the specified application,
    retrieves the sheet and all its visualization objects with detailed metadata,
    and returns the results as structured JSON for analysis.
    """
    print(f"📊 Retrieving objects for sheet: {sheet_id} in app: {app_id}", file=sys.stderr)
    print(f"📊 Environment check: QLIK_SERVER_URL={os.getenv('QLIK_SERVER_URL')}", file=sys.stderr)
    
    try:
        # Call the actual implementation
        result = await get_sheet_objects(
            app_id=app_id,
            sheet_id=sheet_id,
            include_properties=include_properties,
            include_layout=include_layout,
            include_data_definition=include_data_definition
        )
        
        if "error" in result:
            print(f"❌ Error: {result['error']}", file=sys.stderr)
        else:
            print(f"✅ Retrieved {result['object_count']} objects from sheet", file=sys.stderr)
        
        return result
        
    except Exception as e:
        error_response = {
            "error": f"Unexpected error: {str(e)}",
            "app_id": app_id,
            "sheet_id": sheet_id
        }
        print(f"❌ Unexpected error in MCP handler: {e}", file=sys.stderr)
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}", file=sys.stderr)
        return error_response


@mcp.tool()
async def handle_get_app_dimensions(
    app_id: str,
    include_title: bool = True,
    include_tags: bool = True,
    include_grouping: bool = True,
    include_info: bool = True
) -> Dict[str, Any]:
    """
    MCP tool handler for retrieving dimensions from a Qlik Sense application.
    
    This tool connects to a Qlik Sense server, opens the specified application,
    retrieves all dimensions with their metadata and configuration details,
    and returns the results as structured JSON for analysis.
    """
    print(f"📐 Retrieving dimensions for app: {app_id}", file=sys.stderr)
    print(f"📐 Environment check: QLIK_SERVER_URL={os.getenv('QLIK_SERVER_URL')}", file=sys.stderr)
    
    try:
        # Call the actual implementation
        result = await get_app_dimensions(
            app_id=app_id,
            include_title=include_title,
            include_tags=include_tags,
            include_grouping=include_grouping,
            include_info=include_info
        )
        
        if "error" in result:
            print(f"❌ Error: {result['error']}", file=sys.stderr)
        else:
            print(f"✅ Retrieved {result['dimension_count']} dimensions from app", file=sys.stderr)
        
        return result
        
    except Exception as e:
        error_response = {
            "error": f"Unexpected error: {str(e)}",
            "app_id": app_id
        }
        print(f"❌ Unexpected error in MCP handler: {e}", file=sys.stderr)
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}", file=sys.stderr)
        return error_response


@mcp.tool()
async def handle_get_app_script(
    app_id: str,
    analyze_script: bool = False,
    include_sections: bool = False,
    include_line_numbers: bool = False,
    max_preview_length: int = None
) -> Dict[str, Any]:
    """
    MCP tool handler for retrieving and analyzing the script from a Qlik Sense application.
    
    This tool connects to a Qlik Sense server, opens the specified application,
    retrieves the complete application script used for data loading and transformation,
    optionally performs detailed analysis including BINARY LOAD extraction,
    and returns it as structured JSON.
    
    Args:
        app_id: The Qlik Sense application ID
        analyze_script: Enable detailed script analysis and parsing
        include_sections: Parse and return script sections/tabs
        include_line_numbers: Add line numbers to script output
        max_preview_length: Maximum characters to return for script preview
    """
    print(f"📜 Retrieving script for app: {app_id}", file=sys.stderr)
    print(f"📜 Environment check: QLIK_SERVER_URL={os.getenv('QLIK_SERVER_URL')}", file=sys.stderr)
    
    if analyze_script:
        print(f"🔍 Script analysis enabled", file=sys.stderr)
    if include_sections:
        print(f"📑 Section parsing enabled", file=sys.stderr)
    if max_preview_length:
        print(f"✂️ Preview limited to {max_preview_length:,} characters", file=sys.stderr)
    
    try:
        # Call the actual implementation with all parameters
        result = await get_app_script(
            app_id=app_id,
            analyze_script=analyze_script,
            include_sections=include_sections,
            include_line_numbers=include_line_numbers,
            max_preview_length=max_preview_length
        )
        
        if "error" in result:
            print(f"❌ Error: {result['error']}", file=sys.stderr)
        else:
            script_length = result.get('script_length', 0)
            print(f"✅ Retrieved script from app ({script_length:,} characters)", file=sys.stderr)
            
            if "analysis" in result:
                analysis = result["analysis"]
                print(f"📊 Script Analysis:", file=sys.stderr)
                print(f"   • Total lines: {analysis['total_lines']:,}", file=sys.stderr)
                print(f"   • Sections: {len(analysis['sections'])}", file=sys.stderr)
                print(f"   • LOAD statements: {analysis['load_statements']}", file=sys.stderr)
                print(f"   • BINARY LOAD statements: {len(analysis['binary_load_statements'])}", file=sys.stderr)
                
                if analysis['binary_load_statements']:
                    print(f"   📦 BINARY LOAD sources:", file=sys.stderr)
                    for binary in analysis['binary_load_statements']:
                        print(f"      - Line {binary['line_number']}: {binary['source_app']}", file=sys.stderr)
            
            if result.get('is_truncated'):
                print(f"⚠️ Script truncated to {max_preview_length:,} characters", file=sys.stderr)
        
        return result
        
    except Exception as e:
        error_response = {
            "error": f"Unexpected error: {str(e)}",
            "app_id": app_id
        }
        print(f"❌ Unexpected error in MCP handler: {e}", file=sys.stderr)
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}", file=sys.stderr)
        return error_response


@mcp.tool()
async def handle_get_app_data_sources(
    app_id: str,
    include_resident: bool = True,
    include_file_sources: bool = True,
    include_binary_sources: bool = True,
    include_inline_sources: bool = True
) -> Dict[str, Any]:
    """
    MCP tool handler for retrieving data sources from a Qlik Sense application.
    
    This tool connects to a Qlik Sense server, opens the specified application,
    retrieves the lineage information to identify all data sources used in LOAD
    and STORE statements, and returns categorized results for analysis.
    """
    print(f"📊 Retrieving data sources for app: {app_id}", file=sys.stderr)
    print(f"📊 Environment check: QLIK_SERVER_URL={os.getenv('QLIK_SERVER_URL')}", file=sys.stderr)
    
    try:
        # Call the actual implementation
        result = await get_app_data_sources(
            app_id=app_id,
            include_resident=include_resident,
            include_file_sources=include_file_sources,
            include_binary_sources=include_binary_sources,
            include_inline_sources=include_inline_sources
        )
        
        if "error" in result:
            print(f"❌ Error: {result['error']}", file=sys.stderr)
        else:
            source_count = result.get('source_count', 0)
            categories = result.get('categories', {})
            print(f"✅ Retrieved {source_count} data sources from app", file=sys.stderr)
            print(f"   Binary: {categories.get('binary_count', 0)}, Files: {categories.get('file_count', 0)}, Resident: {categories.get('resident_count', 0)}", file=sys.stderr)
        
        return result
        
    except Exception as e:
        error_response = {
            "error": f"Unexpected error: {str(e)}",
            "app_id": app_id
        }
        print(f"❌ Unexpected error in MCP handler: {e}", file=sys.stderr)
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}", file=sys.stderr)
        return error_response


def main():
    """Main entry point for the MCP server"""
    print("🚀 Starting Qlik Sense MCP Server", file=sys.stderr)
    print(f"   Name: {os.getenv('MCP_SERVER_NAME', 'qlik-sense')}", file=sys.stderr)
    print(f"   Version: {os.getenv('MCP_SERVER_VERSION', '0.1.0')}", file=sys.stderr)
    print(f"   Server: {os.getenv('QLIK_SERVER_URL')}:{os.getenv('QLIK_SERVER_PORT')}", file=sys.stderr)
    print(f"   Working Directory: {os.getcwd()}", file=sys.stderr)
    print(f"   .env file exists: {os.path.exists('.env')}", file=sys.stderr)
    print("\n📡 Server is running. Waiting for MCP client connections...", file=sys.stderr)
    
    # Run the MCP server
    mcp.run()


if __name__ == "__main__":
    main()