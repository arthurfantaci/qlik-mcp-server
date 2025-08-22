#!/usr/bin/env python3
"""Test script for dimension retrieval functionality"""

import asyncio
import sys
import os
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.tools import get_app_dimensions

async def test_dimensions():
    """Test the get_app_dimensions function"""
    print("🧪 Testing Qlik Sense Dimension Retrieval")
    print("=" * 50)
    
    # Test app ID (replace with actual app ID)
    test_app_id = "12345678-abcd-1234-efgh-123456789abc"
    
    try:
        print(f"📐 Testing dimension retrieval for app: {test_app_id}")
        print(f"🕒 Started at: {datetime.now().isoformat()}")
        print()
        
        # Test with all options enabled
        print("📊 Test 1: Full dimension data with all options...")
        result = await get_app_dimensions(
            app_id=test_app_id,
            include_title=True,
            include_tags=True,
            include_grouping=True,
            include_info=True
        )
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return False
        
        print(f"✅ Successfully retrieved {result['dimension_count']} dimensions")
        print(f"📄 App ID: {result['app_id']}")
        print(f"🕒 Retrieved at: {result['retrieved_at']}")
        print(f"⚙️ Options: {result['options']}")
        
        if result['dimension_count'] > 0:
            print(f"\n📋 First few dimensions:")
            for i, dimension in enumerate(result['dimensions'][:3]):
                print(f"\n  {i+1}. {dimension.get('title', dimension.get('name', 'Untitled'))}")
                print(f"     ID: {dimension['dimension_id']}")
                if dimension.get('description'):
                    print(f"     Description: {dimension['description']}")
                if dimension.get('tags'):
                    print(f"     Tags: {dimension['tags']}")
                print(f"     Grouping: {dimension.get('grouping', 'N/A')}")
                print(f"     Created: {dimension.get('created', 'Unknown')}")
                print(f"     Modified: {dimension.get('modified', 'Unknown')}")
                print(f"     Published: {dimension.get('published', False)}")
                print(f"     Approved: {dimension.get('approved', False)}")
        else:
            print("📄 No dimensions found in this application")
        
        # Test with minimal options
        print(f"\n📊 Test 2: Minimal dimension data...")
        result_minimal = await get_app_dimensions(
            app_id=test_app_id,
            include_title=False,
            include_tags=False,
            include_grouping=False,
            include_info=False
        )
        
        if "error" in result_minimal:
            print(f"❌ Error in minimal test: {result_minimal['error']}")
        else:
            print(f"✅ Minimal test successful: {result_minimal['dimension_count']} dimensions")
        
        # Test with invalid app ID
        print(f"\n📊 Test 3: Error handling with invalid app ID...")
        result_error = await get_app_dimensions(
            app_id="invalid-app-id-12345",
            include_title=True
        )
        
        if "error" in result_error:
            print(f"✅ Error handling works: {result_error['error']}")
        else:
            print(f"⚠️ Unexpected success with invalid app ID")
        
        print(f"\n🕒 Tests completed at: {datetime.now().isoformat()}")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test runner"""
    print("Starting dimension retrieval tests...")
    success = asyncio.run(test_dimensions())
    
    if success:
        print("\n✅ All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()