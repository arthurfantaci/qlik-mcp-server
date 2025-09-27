#!/usr/bin/env python3
"""Test BINARY LOAD extraction functionality"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.tools import extract_binary_load_statements, perform_script_analysis

def test_binary_extraction():
    """Test extraction of BINARY LOAD statements from script"""

    # Test script with BINARY LOAD statements
    test_script = """///$tab Main
SET ThousandSep=',';
SET DecimalSep='.';

///$tab Binary Load
// Load data from another application
BINARY [lib://DataFiles/BaseApp.qvf];

///$tab Additional Data
// Load additional data
Products:
LOAD
    ProductID,
    ProductName,
    Category
FROM [lib://DataFiles/products.csv]
(txt, utf8, embedded labels, delimiter is ',');

// Another binary load example
BINARY LOAD FROM 'lib://Apps/SharedDataModel.qvf';

///$tab Cleanup
DROP TABLE TempTable;"""

    print("🧪 Testing BINARY LOAD Extraction")
    print("=" * 50)

    # Extract BINARY LOAD statements
    binary_loads = extract_binary_load_statements(test_script)

    print(f"\n📦 Found {len(binary_loads)} BINARY LOAD statements:")
    for binary in binary_loads:
        print(f"  Line {binary.line_number}: {binary.source_app}")
        print(f"    Full statement: {binary.full_statement}")

    # Test full analysis
    print("\n📊 Testing Full Script Analysis with BINARY LOAD:")
    analysis = perform_script_analysis(test_script, include_sections=True)

    print(f"  Total lines: {analysis.total_lines}")
    print(f"  Sections: {len(analysis.sections)}")
    print(f"  LOAD statements: {analysis.load_statements}")
    print(f"  BINARY LOAD statements: {len(analysis.binary_load_statements)}")

    if analysis.binary_load_statements:
        print("\n  BINARY LOAD Details:")
        for binary in analysis.binary_load_statements:
            print(f"    • Line {binary.line_number}: {binary.source_app}")

    # Verify extraction worked correctly
    assert len(binary_loads) == 2, f"Expected 2 BINARY LOAD statements, found {len(binary_loads)}"
    assert binary_loads[0].source_app == "lib://DataFiles/BaseApp.qvf"
    assert binary_loads[1].source_app == "lib://Apps/SharedDataModel.qvf"

    print("\n✅ All BINARY LOAD extraction tests passed!")
    return True

if __name__ == "__main__":
    success = test_binary_extraction()
    sys.exit(0 if success else 1)
