#!/usr/bin/env python3
"""Test script for the get_app_fields functionality"""

import asyncio
import sys
import os

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

from src.tools import get_app_fields

async def test_get_fields():
    """Test the get_app_fields tool function"""
    
    # Use the same test app as other tests
    test_app_id = "12345678-abcd-1234-efgh-123456789abc"
    
    print("🚀 TESTING FIELD LIST FUNCTIONALITY")
    print("=" * 60)
    
    try:
        print(f"📊 Testing get_app_fields with app: {test_app_id}")
        
        # Test the tool function
        result = await get_app_fields(
            app_id=test_app_id,
            show_system=True,
            show_hidden=True,
            show_derived_fields=True,
            show_semantic=True,
            show_src_tables=True,
            show_implicit=True
        )
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return False
        
        print(f"✅ Retrieved {result['field_count']} fields from {result['table_count']} tables")
        
        # Show sample fields
        fields = result.get("fields", [])
        tables = result.get("tables", [])
        
        print(f"\n📊 Sample fields (first 10):")
        
        for i, field in enumerate(fields[:10]):
            print(f"\n   {i+1}. {field['name']}")
            if field.get('source_tables'):
                print(f"      Tables: {', '.join(field['source_tables'])}")
            print(f"      System: {field.get('is_system', False)}")
            print(f"      Hidden: {field.get('is_hidden', False)}")
            print(f"      Numeric: {field.get('is_numeric', False)}")
            print(f"      Cardinal: {field.get('cardinal', 0)}")
            if field.get('tags'):
                print(f"      Tags: {field['tags']}")
        
        print(f"\n📋 Tables found ({len(tables)}):")
        for i, table in enumerate(tables[:10]):  # Show first 10 tables
            print(f"   {i+1}. {table}")
        
        if len(tables) > 10:
            print(f"   ... and {len(tables) - 10} more tables")
        
        print(f"\n📄 Response metadata:")
        print(f"   App ID: {result['app_id']}")
        print(f"   Field Count: {result['field_count']}")
        print(f"   Table Count: {result['table_count']}")
        print(f"   Retrieved at: {result['retrieved_at']}")
        print(f"   Options: {result['options']}")
        
        # Show data model insights
        print(f"\n🔍 Data Model Insights:")
        
        # Count fields by type
        system_fields = sum(1 for f in fields if f.get('is_system', False))
        hidden_fields = sum(1 for f in fields if f.get('is_hidden', False))
        numeric_fields = sum(1 for f in fields if f.get('is_numeric', False))
        
        print(f"   System fields: {system_fields}")
        print(f"   Hidden fields: {hidden_fields}")
        print(f"   Numeric fields: {numeric_fields}")
        print(f"   Text fields: {result['field_count'] - numeric_fields}")
        
        # Show table with most fields
        if fields:
            table_field_count = {}
            for field in fields:
                if field.get('source_tables'):
                    for table in field['source_tables']:
                        table_field_count[table] = table_field_count.get(table, 0) + 1
            
            if table_field_count:
                largest_table = max(table_field_count.items(), key=lambda x: x[1])
                print(f"   Table with most fields: {largest_table[0]} ({largest_table[1]} fields)")
        
        print("\n" + "=" * 60)
        print("✅ FIELD LIST TEST PASSED!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    asyncio.run(test_get_fields())