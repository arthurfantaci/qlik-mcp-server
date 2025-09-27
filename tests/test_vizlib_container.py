#!/usr/bin/env python3
"""Test script specifically for VizlibContainer functionality"""

import asyncio
import sys
import os

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)

from src.tools import get_sheet_objects  # noqa: E402

async def test_vizlib_container():
    """Test VizlibContainer object extraction and Master Item resolution"""

    # Use a generic test case for VizlibContainer testing
    test_app_id = "12345678-abcd-1234-efgh-123456789abc"  # Replace with your app ID
    test_sheet_id = "11111111-2222-3333-4444-555555555555"  # Replace with your sheet ID
    test_container_id = "container1"  # Replace with actual container ID

    print("🚀 TESTING VIZLIB CONTAINER FUNCTIONALITY")
    print("=" * 60)
    print(f"\n📱 Test Application: {test_app_id}")
    print(f"📄 Test Sheet: {test_sheet_id}")
    print(f"📦 Expected Container: {test_container_id}")
    print("=" * 60)

    try:
        # Test with all features enabled
        print("\n📊 Retrieving all objects from sheet (with container processing)...")
        print("-" * 40)

        result = await get_sheet_objects(
            app_id=test_app_id,
            sheet_id=test_sheet_id,
            include_properties=True,
            include_layout=True,
            include_data_definition=True,
            resolve_master_items=True  # Enable Master Item resolution
        )

        if "error" in result:
            print(f"❌ Error getting sheet objects: {result['error']}")
            return False

        print(f"✅ Retrieved {result['object_count']} objects from sheet: {result.get('sheet_title', 'Untitled')}")

        # Analyze the results
        objects = result.get("objects", [])
        containers_found = []
        embedded_objects_total = 0
        master_items_resolved = 0

        print("\n📊 Object Analysis:")
        print("-" * 40)

        # Count object types
        object_types = {}
        for obj in objects:
            obj_type = obj.get('object_type', 'unknown')
            object_types[obj_type] = object_types.get(obj_type, 0) + 1

            # Check if it's a container
            if obj.get("is_container"):
                containers_found.append(obj['object_id'])
                embedded_count = obj.get("embedded_object_count", 0)
                embedded_objects_total += embedded_count

                print(f"\n🗂️ Found Container: {obj['object_id']}")
                print(f"   Type: {obj['object_type']}")
                print(f"   Embedded Objects: {embedded_count}")

                # Show container structure
                if obj.get("container_structure"):
                    structure = obj["container_structure"]
                    print(f"   Tabs/Panels: {structure.get('tab_count', 0)}")
                    for tab in structure.get('tabs', []):
                        print(f"      - {tab.get('label', 'Unnamed')} (Objects: {tab.get('object_count', 0)})")

                # List embedded objects
                if obj.get("embedded_objects"):
                    print("   Embedded Visualizations:")
                    for embedded_obj in obj["embedded_objects"]:
                        obj_id = embedded_obj.get('object_id')
                        obj_type = embedded_obj.get('object_type')
                        container_tab = embedded_obj.get('container_tab', 'Main')
                        print(f"      - {obj_id}: {obj_type} in {container_tab}")

                        # Check for Master Item resolution
                        if embedded_obj.get("measures"):
                            for measure in embedded_obj["measures"]:
                                if measure.get("is_master_item"):
                                    master_items_resolved += 1
                                    print(f"        📊 Master Measure Resolved: {measure.get('master_item_title')}")
                                    print(f"           Expression: {measure.get('resolved_expression', '')[:100]}...")

                        if embedded_obj.get("dimensions"):
                            for dimension in embedded_obj["dimensions"]:
                                if dimension.get("is_master_item"):
                                    master_items_resolved += 1
                                    print(f"        📏 Master Dimension Resolved: {dimension.get('master_item_title')}")
                                    print(f"           Field: {dimension.get('field')}")

        print("\n📋 Summary:")
        print("   Object types found:")
        for obj_type, count in sorted(object_types.items()):
            print(f"      {obj_type}: {count}")

        print("\n   Container Analysis:")
        print(f"      Containers Found: {len(containers_found)}")
        print(f"      Total Embedded Objects: {embedded_objects_total}")
        print(f"      Master Items Resolved: {master_items_resolved}")

        # Check if we found the expected container
        success = False
        if test_container_id in containers_found:
            print(f"\n✅ SUCCESS: Found expected VizlibContainer {test_container_id}")
            success = True
        else:
            print(f"\n⚠️ WARNING: Expected container {test_container_id} not found")
            print(f"   Found containers: {containers_found}")

        # Check for regular (non-embedded) objects that use Master Items
        print("\n📊 Regular Objects with Master Items:")
        for obj in objects:
            if not obj.get("is_container") and not obj.get("is_embedded"):
                has_master_items = False

                # Check measures
                if obj.get("measures"):
                    for measure in obj["measures"]:
                        if measure.get("is_master_item"):
                            if not has_master_items:
                                print(f"\n   Object: {obj['object_id']} ({obj['object_type']})")
                                has_master_items = True
                            print(f"      Master Measure: {measure.get('master_item_title')}")

                # Check dimensions
                if obj.get("dimensions"):
                    for dimension in obj["dimensions"]:
                        if dimension.get("is_master_item"):
                            if not has_master_items:
                                print(f"\n   Object: {obj['object_id']} ({obj['object_type']})")
                                has_master_items = True
                            print(f"      Master Dimension: {dimension.get('master_item_title')}")

        # Optionally save output for debugging (commented out by default)
        # output_file = "test_output.json"
        # with open(output_file, "w") as f:
        #     json.dump(result, f, indent=2)
        # print(f"\n💾 Full output saved to: {output_file}")

        # Show response metadata
        print("\n📄 Response Metadata:")
        print(f"   Retrieved at: {result['retrieved_at']}")
        print(f"   Options: {result['options']}")

        print("\n" + "=" * 60)
        if success and embedded_objects_total > 0:
            print("✅ VIZLIB CONTAINER TEST PASSED!")
            print("   - Container objects are properly detected")
            print("   - Embedded objects are successfully extracted")
            if master_items_resolved > 0:
                print("   - Master Items are resolved to full expressions")
        else:
            print("⚠️ TEST PARTIALLY SUCCESSFUL")
            if not success:
                print("   - Expected container was not found")
            if embedded_objects_total == 0:
                print("   - No embedded objects were extracted")
        print("=" * 60)

        return success and embedded_objects_total > 0

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_vizlib_container())
    sys.exit(0 if result else 1)
