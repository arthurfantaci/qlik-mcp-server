#!/usr/bin/env python3
"""Test script for listing Qlik applications"""

import sys
import os
import asyncio
import json

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.qlik_client import QlikClient
from src.tools import list_qlik_applications


def test_qlik_client_list_apps():
    """Test the QlikClient get_doc_list method directly"""

    print("="*60)
    print("TESTING QLIK CLIENT - APPLICATION LISTING")
    print("="*60)

    client = QlikClient()

    try:
        print("\n🔌 Connecting to Qlik Engine global context...")
        if not client.connect_global():
            print("❌ Failed to connect to Qlik Engine")
            return False

        print("✅ Connected successfully!")

        print("\n📋 Fetching application list...")
        result = client.get_doc_list()

        print(f"✅ Retrieved {result['count']} applications")

        # Show applications
        if result['applications']:
            print("\n📱 Applications found:")
            for i, app in enumerate(result['applications'][:10], 1):  # Show first 10
                print(f"\n   {i}. {app['name']}")
                print(f"      ID: {app['app_id']}")
                print(f"      Last Reload: {app['last_reload_time']}")
                if app.get('doc_type'):
                    print(f"      Type: {app['doc_type']}")

        client.disconnect()
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        client.disconnect()
        return False


async def test_mcp_tool_list_apps():
    """Test the MCP tool function directly"""

    print("="*60)
    print("TESTING MCP TOOL - APPLICATION LISTING")
    print("="*60)

    try:
        print("\n🔧 Testing list_qlik_applications tool...")

        result = await list_qlik_applications()

        if "error" in result:
            print(f"❌ Tool returned error: {result['error']}")
            return False

        print("✅ Tool executed successfully!")
        print(f"   Count: {result['count']} applications")
        print(f"   Retrieved at: {result['retrieved_at']}")

        # Show sample applications
        if result['applications']:
            print("\n📱 Sample applications (first 5):")
            for i, app in enumerate(result['applications'][:5], 1):
                print(f"\n   {i}. {app['name']}")
                print(f"      ID: {app['app_id']}")
                print(f"      Last Reload: {app['last_reload_time']}")

        # Test JSON serialization
        print("\n📄 JSON output sample:")
        sample_output = {
            "count": result['count'],
            "sample_apps": result['applications'][:3] if result['applications'] else []
        }
        json_output = json.dumps(sample_output, indent=2)
        if len(json_output) > 500:
            print(json_output[:500] + "...")
        else:
            print(json_output)

        return True

    except Exception as e:
        print(f"❌ Tool test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run both tests"""

    print("🚀 TESTING APPLICATION LISTING FUNCTIONALITY")
    print("="*60)

    # Test 1: Direct client test
    success1 = test_qlik_client_list_apps()

    if success1:
        print("\n" + "="*60)

        # Test 2: MCP tool test
        success2 = asyncio.run(test_mcp_tool_list_apps())

        if success1 and success2:
            print("\n" + "="*60)
            print("✅ ALL TESTS PASSED!")
            print("="*60)
            return True

    print("\n" + "="*60)
    print("❌ SOME TESTS FAILED!")
    print("="*60)
    return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
