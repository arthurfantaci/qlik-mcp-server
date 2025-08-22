#!/usr/bin/env python3
"""Test script demonstrating both MCP tools working together"""

import sys
import os
import asyncio
import json

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.tools import get_app_measures, list_qlik_applications


async def demonstrate_both_tools():
    """Demonstrate both MCP tools working together"""
    
    print("🚀 DEMONSTRATING BOTH MCP TOOLS")
    print("="*60)
    
    try:
        # Step 1: List all applications
        print("\n📋 Step 1: Getting list of all Qlik applications...")
        
        apps_result = await list_qlik_applications()
        
        if "error" in apps_result:
            print(f"❌ Error listing apps: {apps_result['error']}")
            return False
        
        print(f"✅ Found {apps_result['count']} applications")
        
        # Find our test app
        test_app_id = "fb41d1e1-38fb-4595-8391-2f1a536bceb1"
        test_app = None
        
        for app in apps_result['applications']:
            if app['app_id'] == test_app_id:
                test_app = app
                break
        
        if test_app:
            print(f"\n🎯 Found test app: '{test_app['name']}'")
            print(f"   ID: {test_app['app_id']}")
            print(f"   Last Reload: {test_app['last_reload_time']}")
        else:
            # Use the first available app as fallback
            test_app = apps_result['applications'][0]
            test_app_id = test_app['app_id']
            print(f"\n🎯 Using first available app: '{test_app['name']}'")
            print(f"   ID: {test_app['app_id']}")
        
        # Step 2: Get measures from the selected app
        print(f"\n📊 Step 2: Getting measures from app '{test_app['name']}'...")
        
        measures_result = await get_app_measures(
            app_id=test_app_id,
            include_expression=True,
            include_tags=True
        )
        
        if "error" in measures_result:
            print(f"❌ Error getting measures: {measures_result['error']}")
            return False
        
        print(f"✅ Found {measures_result['count']} measures")
        
        # Show sample workflow results
        print(f"\n📈 Workflow Results:")
        print(f"   Total Applications: {apps_result['count']}")
        print(f"   Selected App: {test_app['name']}")
        print(f"   App Measures: {measures_result['count']}")
        
        if measures_result['measures']:
            print(f"\n📊 Sample measures from '{test_app['name']}':")
            for i, measure in enumerate(measures_result['measures'][:3], 1):
                print(f"   {i}. {measure['title']}")
                if measure.get('expression'):
                    expr = measure['expression'][:50] + "..." if len(measure['expression']) > 50 else measure['expression']
                    print(f"      Expression: {expr}")
        
        # Show JSON structure for both responses
        print(f"\n📄 Combined Response Structure:")
        combined_response = {
            "workflow": "List apps then get measures",
            "applications_summary": {
                "total_count": apps_result['count'],
                "sample_apps": [
                    {"name": app['name'], "app_id": app['app_id']} 
                    for app in apps_result['applications'][:3]
                ]
            },
            "measures_summary": {
                "app_name": test_app['name'],
                "app_id": test_app_id,
                "measures_count": measures_result['count'],
                "sample_measures": [
                    {"title": m['title'], "expression": m.get('expression', '')[:30] + "..." if m.get('expression') and len(m.get('expression', '')) > 30 else m.get('expression', '')}
                    for m in measures_result['measures'][:2]
                ]
            }
        }
        
        print(json.dumps(combined_response, indent=2))
        
        print(f"\n{'='*60}")
        print("✅ BOTH TOOLS WORKING PERFECTLY!")
        print("🎉 Ready for MCP client integration!")
        print(f"{'='*60}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(demonstrate_both_tools())
    sys.exit(0 if success else 1)