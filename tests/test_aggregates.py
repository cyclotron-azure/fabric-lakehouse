"""
Test suite for aggregate calculations (BUGGY VERSION FOR INTERVIEW).

This test will FAIL until the bugs in src/silver.py are fixed.
"""

import pytest
import pandas as pd
from pyspark.sql import SparkSession
from src.silver import compute_monthly_revenue


@pytest.fixture(scope="module")
def spark():
    """Create a Spark session for testing."""
    spark = SparkSession.builder \
        .appName("pytest") \
        .master("local[2]") \
        .config("spark.sql.shuffle.partitions", "2") \
        .getOrCreate()
    yield spark
    spark.stop()


def test_compute_monthly_revenue_uses_qty_times_price(spark):
    """
    Test that monthly revenue correctly multiplies quantity * price.
    
    ⚠️ THIS TEST WILL FAIL until bugs are fixed in src/silver.py
    
    Bugs to fix:
    1. Case-sensitive status filter ('complete' vs 'Complete'/'COMPLETE')
    2. Revenue calculation using price instead of quantity * price
    """
    # Create test data with mixed-case status values
    data = pd.DataFrame({
        'order_id': ['O001', 'O002', 'O003'],
        'order_date': ['2025-11-01', '2025-11-15', '2025-11-20'],
        'customer_id': ['C001', 'C002', 'C003'],
        'status': ['Complete', 'COMPLETE', 'cancelled'],  # Mixed case
        'quantity': [2, 1, 10],
        'price': [10.0, 5.0, 1.0]
    })
    
    df = spark.createDataFrame(data)
    result = compute_monthly_revenue(df).toPandas()
    
    # Expected calculation:
    # O001: 2 * 10.0 = 20.0 (Complete)
    # O002: 1 * 5.0 = 5.0 (COMPLETE)
    # O003: excluded (cancelled)
    # Total for 2025-11: 25.0
    
    assert len(result) == 1, "Should have exactly one month (2025-11)"
    assert result.iloc[0]['month'] == '2025-11', "Should be November 2025"
    
    expected_revenue = 25.0
    actual_revenue = result.iloc[0]['revenue']
    
    # This assertion will FAIL until bugs are fixed
    assert actual_revenue == expected_revenue, \
        f"Expected revenue ${expected_revenue}, but got ${actual_revenue}. " \
        f"Hints: 1) Check case-sensitive status filter, 2) Verify quantity * price calculation"


def test_monthly_revenue_case_insensitive_status(spark):
    """
    Test that status filtering is case-insensitive.
    
    ⚠️ THIS TEST WILL FAIL until case-sensitivity bug is fixed.
    """
    data = pd.DataFrame({
        'order_id': ['O001', 'O002', 'O003', 'O004'],
        'order_date': ['2025-11-01', '2025-11-02', '2025-11-03', '2025-11-04'],
        'customer_id': ['C001', 'C002', 'C003', 'C004'],
        'status': ['complete', 'Complete', 'COMPLETE', 'cancelled'],
        'quantity': [1, 1, 1, 1],
        'price': [10.0, 10.0, 10.0, 10.0]
    })
    
    df = spark.createDataFrame(data)
    result = compute_monthly_revenue(df).toPandas()
    
    # All three 'complete' variations should be included
    expected_revenue = 30.0  # 3 orders * 1 * 10.0
    actual_revenue = result.iloc[0]['revenue'] if len(result) > 0 else 0.0
    
    assert actual_revenue == expected_revenue, \
        f"Status filter should be case-insensitive. Expected ${expected_revenue}, got ${actual_revenue}"


def test_monthly_aggregation_correctness(spark):
    """Test that revenue is correctly aggregated by month."""
    data = pd.DataFrame({
        'order_id': ['O001', 'O002', 'O003'],
        'order_date': ['2025-10-15', '2025-11-10', '2025-11-20'],
        'customer_id': ['C001', 'C002', 'C003'],
        'status': ['complete', 'complete', 'complete'],  # All lowercase for this test
        'quantity': [2, 3, 1],
        'price': [10.0, 15.0, 20.0]
    })
    
    df = spark.createDataFrame(data)
    result = compute_monthly_revenue(df).toPandas()
    
    assert len(result) == 2, "Should have two months (2025-10 and 2025-11)"
    
    # October: 2 * 10.0 = 20.0
    oct_revenue = result[result['month'] == '2025-10']['revenue'].values[0]
    assert oct_revenue == 20.0, f"October revenue should be $20.00, got ${oct_revenue}"
    
    # November: 3 * 15.0 + 1 * 20.0 = 65.0
    nov_revenue = result[result['month'] == '2025-11']['revenue'].values[0]
    assert nov_revenue == 65.0, f"November revenue should be $65.00, got ${nov_revenue}"


def test_excludes_non_complete_orders(spark):
    """Test that only 'complete' orders are included in revenue."""
    data = pd.DataFrame({
        'order_id': ['O001', 'O002', 'O003', 'O004'],
        'order_date': ['2025-11-01', '2025-11-02', '2025-11-03', '2025-11-04'],
        'customer_id': ['C001', 'C002', 'C003', 'C004'],
        'status': ['complete', 'pending', 'cancelled', 'COMPLETE'],
        'quantity': [1, 1, 1, 1],
        'price': [10.0, 10.0, 10.0, 10.0]
    })
    
    df = spark.createDataFrame(data)
    result = compute_monthly_revenue(df).toPandas()
    
    # Only O001 (complete) and O004 (COMPLETE) should be included = $20.0
    expected_revenue = 20.0
    actual_revenue = result.iloc[0]['revenue'] if len(result) > 0 else 0.0
    
    assert actual_revenue == expected_revenue, \
        f"Should only include complete orders. Expected ${expected_revenue}, got ${actual_revenue}"
