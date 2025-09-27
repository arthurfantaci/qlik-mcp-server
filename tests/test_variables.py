#!/usr/bin/env python3
"""Test script for the get_app_variables functionality"""

import asyncio
import sys
import os

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)

from src.tools import get_app_variables  # noqa: E402

async def test_get_variables():
    """Test the get_app_variables tool function"""

    # Use the same test app as other tests
    test_app_id = "12345678-abcd-1234-efgh-123456789abc"

    print("🚀 TESTING VARIABLE RETRIEVAL FUNCTIONALITY")
    print("=" * 60)

    try:
        print(f"📋 Testing get_app_variables with app: {test_app_id}")

        # Test the tool function
        result = await get_app_variables(
            app_id=test_app_id,
            include_definition=True,
            include_tags=True,
            show_reserved=True,
            show_config=True
        )

        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return False

        print(f"✅ Retrieved {result['count']} variables")

        # Show sample variables
        variables = result.get("variables", [])
        print("\n📋 Sample variables (first 5):")

        for i, variable in enumerate(variables[:5]):
            print(f"\n   {i+1}. {variable['name']}")
            if variable.get('definition'):
                definition = variable['definition']
                truncated = definition[:50] + '...' if len(definition) > 50 else definition
                print(f"      Definition: {truncated}")
            if variable.get('is_reserved') is not None:
                print(f"      Reserved: {variable['is_reserved']}")
            if variable.get('is_config') is not None:
                print(f"      Config: {variable['is_config']}")
            if variable.get('tags'):
                print(f"      Tags: {variable['tags']}")

        print("\n📄 Response metadata:")
        print(f"   App ID: {result['app_id']}")
        print(f"   Count: {result['count']}")
        print(f"   Retrieved at: {result['retrieved_at']}")
        print(f"   Options: {result['options']}")

        print("\n" + "=" * 60)
        print("✅ VARIABLE TEST PASSED!")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    asyncio.run(test_get_variables())
