#!/usr/bin/env python3
"""Test the MCP tool functionality directly"""

import sys
import os
import asyncio
import json

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.tools import get_app_measures


async def test_mcp_tool():
    """Test the MCP tool function directly"""

    print("="*60)
    print("TESTING MCP TOOL FUNCTION")
    print("="*60)

    app_id = "12345678-abcd-1234-efgh-123456789abc"

    print(f"\n🔧 Testing get_app_measures tool with app: {app_id}")

    try:
        # Test the tool function
        result = await get_app_measures(
            app_id=app_id,
            include_expression=True,
            include_tags=True
        )

        print("\n✅ Tool executed successfully!")

        if "error" in result:
            print(f"❌ Tool returned error: {result['error']}")
            return False

        print("\n📊 Results:")
        print(f"   App ID: {result['app_id']}")
        print(f"   Count: {result['count']} measures")
        print(f"   Retrieved at: {result['retrieved_at']}")
        print(f"   Options: {result['options']}")

        # Show first few measures
        if result['measures']:
            print("\n📈 First 3 measures:")
            for i, measure in enumerate(result['measures'][:3], 1):
                print(f"\n   {i}. {measure['title']}")
                print(f"      ID: {measure['id']}")
                if measure.get('description'):
                    print(f"      Description: {measure['description']}")
                if measure.get('expression'):
                    expr_len = len(measure['expression'])
                    expr = measure['expression'][:60] + "..." if expr_len > 60 else measure['expression']
                    print(f"      Expression: {expr}")

        # Verify the Total_Cost measure is present
        total_cost_measures = [m for m in result['measures'] if m['title'] == 'Total_Cost']
        if total_cost_measures:
            total_cost = total_cost_measures[0]
            print("\n🎯 Found Total_Cost measure:")
            print(f"      ID: {total_cost['id']}")
            print(f"      Expression: {total_cost['expression']}")
        else:
            print("\n⚠️  Total_Cost measure not found")

        print("\n📄 JSON output sample:")
        sample_output = {
            "app_id": result['app_id'],
            "count": result['count'],
            "sample_measure": result['measures'][0] if result['measures'] else None
        }
        print(json.dumps(sample_output, indent=2))

        print(f"\n{'='*60}")
        print("✅ MCP TOOL TEST PASSED!")
        print(f"{'='*60}")

        return True

    except Exception as e:
        print(f"\n❌ Tool test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Run the async test
    success = asyncio.run(test_mcp_tool())
    sys.exit(0 if success else 1)
