"""Test BINARY LOAD extraction functionality"""

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

    # Extract BINARY LOAD statements
    binary_loads = extract_binary_load_statements(test_script)

    # Test full analysis
    analysis = perform_script_analysis(test_script, include_sections=True)

    # Verify extraction worked correctly
    assert len(binary_loads) == 2, f"Expected 2 BINARY LOAD statements, found {len(binary_loads)}"
    assert binary_loads[0].source_app == "lib://DataFiles/BaseApp.qvf"
    assert binary_loads[1].source_app == "lib://Apps/SharedDataModel.qvf"

    # Additional assertions for full analysis
    assert analysis.total_lines > 0
    assert len(analysis.sections) > 0
    assert analysis.load_statements > 0
    assert len(analysis.binary_load_statements) == 2
