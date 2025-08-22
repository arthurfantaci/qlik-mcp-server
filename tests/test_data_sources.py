#!/usr/bin/env python3
"""Test script for data sources lineage retrieval functionality"""

import asyncio
import sys
import os
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.tools import get_app_data_sources

async def test_data_sources():
    """Test the get_app_data_sources function"""
    print("🧪 Testing Qlik Sense Data Sources Retrieval")
    print("=" * 50)
    
    # Test app ID (replace with actual app ID)
    test_app_id = "fb41d1e1-38fb-4595-8391-2f1a536bceb1"
    
    try:
        print(f"📊 Testing data sources retrieval for app: {test_app_id}")
        print(f"🕒 Started at: {datetime.now().isoformat()}")
        print()
        
        # Test with all data source types included
        print("📊 Test 1: Full data sources retrieval with all types...")
        result = await get_app_data_sources(
            app_id=test_app_id,
            include_resident=True,
            include_file_sources=True,
            include_binary_sources=True,
            include_inline_sources=True
        )
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return False
        
        print(f"✅ Successfully retrieved {result['source_count']} data sources")
        print(f"📄 App ID: {result['app_id']}")
        print(f"🕒 Retrieved at: {result['retrieved_at']}")
        print(f"⚙️ Options: {result['options']}")
        
        # Show category breakdown
        categories = result.get('categories', {})
        print(f"\n📊 Data source categories:")
        print(f"  🔗 Binary sources: {categories.get('binary_count', 0)}")
        print(f"  📁 File sources: {categories.get('file_count', 0)}")
        print(f"  🏠 Resident sources: {categories.get('resident_count', 0)}")
        print(f"  📝 Inline sources: {categories.get('inline_count', 0)}")
        print(f"  ❓ Other sources: {categories.get('other_count', 0)}")
        
        if result['source_count'] > 0:
            print(f"\n📋 Sample data sources by category:")
            
            by_category = result.get('by_category', {})
            
            # Show binary sources (of particular interest)
            binary_sources = by_category.get('binary', [])
            if binary_sources:
                print(f"\n  🔗 Binary sources ({len(binary_sources)}):")
                for i, source in enumerate(binary_sources[:3]):
                    print(f"    {i+1}. {source['discriminator']}")
                    if source.get('statement'):
                        print(f"       Statement: {source['statement']}")
                if len(binary_sources) > 3:
                    print(f"       ... and {len(binary_sources) - 3} more")
            
            # Show file sources
            file_sources = by_category.get('file', [])
            if file_sources:
                print(f"\n  📁 File sources ({len(file_sources)}):")
                for i, source in enumerate(file_sources[:3]):
                    discriminator = source['discriminator']
                    # Truncate long paths for display
                    display_path = discriminator[:80] + "..." if len(discriminator) > 80 else discriminator
                    print(f"    {i+1}. {display_path}")
                if len(file_sources) > 3:
                    print(f"       ... and {len(file_sources) - 3} more")
            
            # Show resident sources
            resident_sources = by_category.get('resident', [])
            if resident_sources:
                print(f"\n  🏠 Resident sources ({len(resident_sources)}):")
                for i, source in enumerate(resident_sources[:5]):
                    print(f"    {i+1}. {source['discriminator']}")
                if len(resident_sources) > 5:
                    print(f"       ... and {len(resident_sources) - 5} more")
            
            # Show inline sources
            inline_sources = by_category.get('inline', [])
            if inline_sources:
                print(f"\n  📝 Inline sources ({len(inline_sources)}):")
                for i, source in enumerate(inline_sources):
                    print(f"    {i+1}. {source['discriminator']}")
        else:
            print("📄 No data sources found in this application")
        
        # Test with only binary sources
        print(f"\n📊 Test 2: Binary sources only...")
        result_binary = await get_app_data_sources(
            app_id=test_app_id,
            include_resident=False,
            include_file_sources=False,
            include_binary_sources=True,
            include_inline_sources=False
        )
        
        if "error" in result_binary:
            print(f"❌ Error in binary test: {result_binary['error']}")
        else:
            binary_count = result_binary['categories'].get('binary_count', 0)
            print(f"✅ Binary sources only test successful: {binary_count} binary sources")
        
        # Test with invalid app ID
        print(f"\n📊 Test 3: Error handling with invalid app ID...")
        result_error = await get_app_data_sources(
            app_id="invalid-app-id-12345",
            include_resident=True
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
    print("Starting data sources retrieval tests...")
    success = asyncio.run(test_data_sources())
    
    if success:
        print("\n✅ All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()