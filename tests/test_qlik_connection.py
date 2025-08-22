#!/usr/bin/env python3
"""Standalone test script for Qlik connection and measure retrieval"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.qlik_client import QlikClient
import json


def test_qlik_connection(app_id: str = None):
    """Test the Qlik connection and measure retrieval"""
    
    # Use provided app_id or default test app
    if not app_id:
        app_id = "12345678-abcd-1234-efgh-123456789abc"
        print(f"No app_id provided, using test app: {app_id}")
    
    print("\n" + "="*60)
    print("QLIK MCP SERVER - CONNECTION TEST")
    print("="*60)
    
    # Create client
    client = QlikClient()
    
    print(f"\n📋 Configuration:")
    print(f"   Server: {client.server_url}:{client.server_port}")
    print(f"   User: {client.user_directory}\\{client.user_id}")
    print(f"   Certificates: {os.path.exists(client.cert_root) and 'Found' or 'Missing'}")
    
    try:
        # Test connection
        print(f"\n🔌 Connecting to app: {app_id}")
        if not client.connect(app_id):
            print("❌ Failed to connect to Qlik Sense")
            return False
        
        print("✅ Connection successful!")
        
        # Test measure retrieval
        print("\n📊 Retrieving measures...")
        result = client.get_measures(include_expression=True, include_tags=True)
        
        print(f"✅ Retrieved {result['count']} measures")
        
        # Display sample measures
        if result['measures']:
            print("\n📈 Sample measures (first 3):")
            for i, measure in enumerate(result['measures'][:3], 1):
                print(f"\n   {i}. {measure['title']}")
                print(f"      ID: {measure['id']}")
                if measure.get('description'):
                    print(f"      Description: {measure['description']}")
                if measure.get('expression'):
                    expr = measure['expression']
                    if len(expr) > 60:
                        expr = expr[:57] + "..."
                    print(f"      Expression: {expr}")
                if measure.get('tags'):
                    print(f"      Tags: {', '.join(measure['tags'])}")
        
        # Test JSON serialization
        print("\n📄 Testing JSON serialization...")
        json_output = json.dumps({
            "app_id": app_id,
            "measures": result['measures'][:1],  # Just first measure
            "count": result['count']
        }, indent=2)
        print("✅ JSON serialization successful")
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        client.disconnect()
        print("\n🔌 Disconnected from Qlik Engine")


if __name__ == "__main__":
    # Get app_id from command line if provided
    app_id = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Run test
    success = test_qlik_connection(app_id)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)