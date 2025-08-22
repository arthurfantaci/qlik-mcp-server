#!/usr/bin/env python3
"""Test sheet functionality with a dashboard app"""

import asyncio
import sys
import os

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

from src.tools import get_app_sheets

async def test_dashboard_sheets():
    """Test sheets with a dashboard app"""
    
    # Try with the main dashboard app
    test_app_id = "e8b58c47-080a-4b0f-ab8b-df760bbdf7bc"  # abc-demo-issuer-main-dashboard
    
    print(f"Testing sheets for dashboard app: {test_app_id}")
    
    result = await get_app_sheets(
        app_id=test_app_id,
        include_thumbnail=False,
        include_metadata=True
    )
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return False
    
    print(f"✅ Found {result['sheet_count']} sheets")
    
    sheets = result.get("sheets", [])
    for i, sheet in enumerate(sheets[:5]):
        print(f"\n{i+1}. {sheet.get('title', 'Untitled')}")
        print(f"   ID: {sheet['sheet_id']}")
    
    return True

if __name__ == "__main__":
    asyncio.run(test_dashboard_sheets())