#!/usr/bin/env python3
"""Test script for the sheet and visualization object functionality"""

import asyncio
import sys
import os
import json

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

from src.tools import get_app_sheets, get_sheet_objects

async def test_sheet_functionality():
    """Test the sheet and visualization object retrieval"""
    
    # Use the same test app as other tests
    test_app_id = "fb41d1e1-38fb-4595-8391-2f1a536bceb1"
    
    print("🚀 TESTING SHEET AND VISUALIZATION FUNCTIONALITY")
    print("=" * 60)
    
    try:
        # First, get all sheets
        print(f"\n📄 Testing get_app_sheets with app: {test_app_id}")
        print("-" * 40)
        
        sheets_result = await get_app_sheets(
            app_id=test_app_id,
            include_thumbnail=False,
            include_metadata=True
        )
        
        if "error" in sheets_result:
            print(f"❌ Error getting sheets: {sheets_result['error']}")
            return False
        
        print(f"✅ Retrieved {sheets_result['sheet_count']} sheets")
        
        # Show sheet information
        sheets = sheets_result.get("sheets", [])
        print(f"\n📄 Sheets found:")
        
        test_sheet_id = None
        for i, sheet in enumerate(sheets[:10]):  # Show first 10 sheets
            print(f"\n   {i+1}. {sheet.get('title', 'Untitled')}")
            print(f"      ID: {sheet['sheet_id']}")
            if sheet.get('description'):
                print(f"      Description: {sheet['description']}")
            if sheet.get('created'):
                print(f"      Created: {sheet['created']}")
            if sheet.get('modified'):
                print(f"      Modified: {sheet['modified']}")
            print(f"      Published: {sheet.get('published', False)}")
            print(f"      Approved: {sheet.get('approved', False)}")
            
            # Store first sheet ID for object testing
            if i == 0 and sheet.get('sheet_id'):
                test_sheet_id = sheet['sheet_id']
        
        if len(sheets) > 10:
            print(f"\n   ... and {len(sheets) - 10} more sheets")
        
        # Test getting objects from a sheet if we have one
        if test_sheet_id:
            print(f"\n\n📊 Testing get_sheet_objects with sheet: {test_sheet_id}")
            print("-" * 40)
            
            objects_result = await get_sheet_objects(
                app_id=test_app_id,
                sheet_id=test_sheet_id,
                include_properties=True,
                include_layout=True,
                include_data_definition=True
            )
            
            if "error" in objects_result:
                print(f"❌ Error getting sheet objects: {objects_result['error']}")
                return False
            
            print(f"✅ Retrieved {objects_result['object_count']} objects from sheet: {objects_result.get('sheet_title', 'Untitled')}")
            
            # Show object information
            objects = objects_result.get("objects", [])
            print(f"\n📊 Visualization objects found:")
            
            # Count object types
            object_types = {}
            for obj in objects:
                obj_type = obj.get('object_type', 'unknown')
                object_types[obj_type] = object_types.get(obj_type, 0) + 1
            
            print(f"\n   Object types summary:")
            for obj_type, count in sorted(object_types.items()):
                print(f"      {obj_type}: {count}")
            
            # Show detailed info for first few objects
            print(f"\n   Detailed object information (first 5):")
            
            for i, obj in enumerate(objects[:5]):
                print(f"\n   {i+1}. {obj.get('title', obj.get('object_type', 'Unknown'))}")
                print(f"      ID: {obj['object_id']}")
                print(f"      Type: {obj['object_type']}")
                
                if obj.get('subtitle'):
                    print(f"      Subtitle: {obj['subtitle']}")
                
                if obj.get('layout'):
                    layout = obj['layout']
                    print(f"      Position: ({layout.get('x', 0)}, {layout.get('y', 0)})")
                    print(f"      Size: {layout.get('width', 0)} x {layout.get('height', 0)}")
                
                if obj.get('measures'):
                    print(f"      Measures:")
                    for measure in obj['measures'][:3]:  # Show first 3 measures
                        print(f"         - {measure.get('label', 'Unnamed')}: {measure.get('expression', '')[:50]}...")
                
                if obj.get('dimensions'):
                    print(f"      Dimensions:")
                    for dimension in obj['dimensions'][:3]:  # Show first 3 dimensions
                        print(f"         - {dimension.get('label', 'Unnamed')}: {dimension.get('field', '')}")
                
                if obj.get('properties'):
                    print(f"      Properties: {list(obj['properties'].keys())}")
            
            if len(objects) > 5:
                print(f"\n   ... and {len(objects) - 5} more objects")
        
        else:
            print("\n⚠️ No sheets found to test object retrieval")
        
        # Show response metadata
        print(f"\n\n📄 Response Metadata:")
        print(f"   Sheets retrieved at: {sheets_result['retrieved_at']}")
        print(f"   Sheets options: {sheets_result['options']}")
        
        if test_sheet_id and 'retrieved_at' in objects_result:
            print(f"   Objects retrieved at: {objects_result['retrieved_at']}")
            print(f"   Objects options: {objects_result['options']}")
        
        print("\n" + "=" * 60)
        print("✅ SHEET AND VISUALIZATION TEST PASSED!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    asyncio.run(test_sheet_functionality())