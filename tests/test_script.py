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
    """Test the get_app_script function with enhanced features"""
    print("🧪 Testing Qlik Sense Script Retrieval with Enhanced Features")
    print("=" * 50)
    
    # Test app ID (replace with actual app ID from your Qlik Sense instance)
    test_app_id = "12345678-abcd-1234-efgh-123456789abc"
    
    try:
        print(f"📜 Testing script retrieval for app: {test_app_id}")
        print(f"🕒 Started at: {datetime.now().isoformat()}")
        print()
        
        # Test 1: Basic script retrieval
        print("📊 Test 1: Basic script retrieval...")
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
        
        # Test 2: Script with analysis
        print(f"\n📊 Test 2: Script retrieval with analysis...")
        result_analysis = await get_app_script(
            app_id=test_app_id,
            analyze_script=True,
            include_sections=True
        )
        
        if "error" in result_analysis:
            print(f"❌ Error: {result_analysis['error']}")
        else:
            print(f"✅ Successfully retrieved script with analysis")
            
            if "analysis" in result_analysis:
                analysis = result_analysis["analysis"]
                print(f"\n📈 Analysis Results:")
                print(f"  Total lines: {analysis['total_lines']:,}")
                print(f"  Empty lines: {analysis['empty_lines']:,}")
                print(f"  Comment lines: {analysis['comment_lines']:,}")
                print(f"  Sections: {len(analysis['sections'])}")
                print(f"  LOAD statements: {analysis['load_statements']}")
                print(f"  STORE statements: {analysis['store_statements']}")
                print(f"  DROP statements: {analysis['drop_statements']}")
                
                # Check for BINARY LOAD statements
                if analysis['binary_load_statements']:
                    print(f"\n📦 BINARY LOAD Statements Found:")
                    for binary in analysis['binary_load_statements']:
                        print(f"    Line {binary['line_number']}: {binary['source_app']}")
                        print(f"    Statement: {binary['full_statement']}")
                else:
                    print(f"  BINARY LOAD statements: None found")
                
                # Check for variables
                if analysis['set_variables']:
                    print(f"\n🔧 SET Variables ({len(analysis['set_variables'])}):")
                    for var in analysis['set_variables'][:3]:  # Show first 3
                        print(f"    {var['name']} = {var['value'][:50]}...")
                
                if analysis['let_variables']:
                    print(f"\n🔧 LET Variables ({len(analysis['let_variables'])}):")
                    for var in analysis['let_variables'][:3]:  # Show first 3
                        print(f"    {var['name']} = {var['value'][:50]}...")
        
        # Test 3: Script with line numbers
        print(f"\n📊 Test 3: Script with line numbers...")
        result_lines = await get_app_script(
            app_id=test_app_id,
            include_line_numbers=True,
            max_preview_length=500  # Get first 500 chars with line numbers
        )
        
        if "error" not in result_lines:
            print(f"✅ Successfully retrieved script with line numbers")
            if result_lines.get('is_truncated'):
                print(f"   Script truncated at {result_lines['truncated_at']} characters")
            # Show a snippet
            script_snippet = result_lines['script'][:200] if result_lines['script'] else "No script"
            print(f"\n📄 Script preview with line numbers:")
            print(script_snippet)
            print("...")
        
        # Test 4: Test sections parsing only
        print(f"\n📊 Test 4: Script sections parsing...")
        result_sections = await get_app_script(
            app_id=test_app_id,
            include_sections=True
        )
        
        if "error" not in result_sections and "sections" in result_sections:
            sections = result_sections['sections']
            print(f"✅ Found {len(sections)} sections")
            for section in sections[:5]:  # Show first 5 sections
                print(f"   • {section['name']} (lines {section['start_line']}-{section['end_line']}, {section['line_count']} lines)")
        
        # Test 5: Error handling with invalid app ID
        print(f"\n📊 Test 5: Error handling with invalid app ID...")
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
    print("Starting enhanced script retrieval tests...")
    print("Testing features: basic retrieval, analysis, BINARY LOAD extraction, sections, line numbers")
    print()
    success = asyncio.run(test_script())
    
    if success:
        print("\n✅ All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()