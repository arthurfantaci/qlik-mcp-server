#!/usr/bin/env python3
"""Test script for application script retrieval functionality"""

import asyncio
import sys
import os
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.tools import get_app_script

async def test_script():
    """Test the get_app_script function"""
    print("🧪 Testing Qlik Sense Script Retrieval")
    print("=" * 50)
    
    # Test app ID (replace with actual app ID)
    test_app_id = "12345678-abcd-1234-efgh-123456789abc"
    
    try:
        print(f"📜 Testing script retrieval for app: {test_app_id}")
        print(f"🕒 Started at: {datetime.now().isoformat()}")
        print()
        
        # Test script retrieval
        print("📊 Test 1: Retrieving application script...")
        result = await get_app_script(app_id=test_app_id)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return False
        
        print(f"✅ Successfully retrieved script")
        print(f"📄 App ID: {result['app_id']}")
        print(f"🕒 Retrieved at: {result['retrieved_at']}")
        print(f"📏 Script length: {result['script_length']:,} characters")
        
        if result['script_length'] > 0:
            script = result['script']
            
            # Show first few lines of the script
            lines = script.split('\n')
            print(f"\n📋 Script preview (first 10 lines):")
            for i, line in enumerate(lines[:10]):
                line_preview = line[:100] + "..." if len(line) > 100 else line
                print(f"  {i+1:2d}: {line_preview}")
            
            if len(lines) > 10:
                print(f"     ... and {len(lines) - 10} more lines")
            
            # Basic script analysis
            print(f"\n📊 Script analysis:")
            print(f"  Total lines: {len(lines):,}")
            print(f"  Empty lines: {sum(1 for line in lines if not line.strip()):,}")
            print(f"  Contains 'LOAD': {'✅' if 'LOAD' in script.upper() else '❌'}")
            print(f"  Contains 'FROM': {'✅' if 'FROM' in script.upper() else '❌'}")
            print(f"  Contains 'LET': {'✅' if 'LET' in script.upper() else '❌'}")
            print(f"  Contains 'SET': {'✅' if 'SET' in script.upper() else '❌'}")
            
        else:
            print("📄 Script is empty or not found")
        
        # Test with invalid app ID
        print(f"\n📊 Test 2: Error handling with invalid app ID...")
        result_error = await get_app_script(app_id="invalid-app-id-12345")
        
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
    print("Starting script retrieval tests...")
    success = asyncio.run(test_script())
    
    if success:
        print("\n✅ All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()