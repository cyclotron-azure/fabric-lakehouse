"""
Test suite for data quality checks including duplicate handling.
"""

import pytest
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from src.quality_checks import check_data_quality, check_referential_integrity
from src.silver import clean_customer_data, clean_order_data


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


def test_duplicate_detection_customers(spark):
    """Test that duplicate customer records are detected."""
    # Create data with duplicates
    data = pd.DataFrame({
        'customer_id': ['C001', 'C001', 'C002'],  # C001 is duplicate
        'name': ['Alice', 'Alice Duplicate', 'Bob'],
        'email': ['alice@test.com', 'alice2@test.com', 'bob@test.com'],
        'signup_date': ['2025-01-01', '2025-01-02', '2025-01-03']
    })
    
    df = spark.createDataFrame(data)
    report = check_data_quality(df, 'customers', required_columns=['customer_id', 'name', 'email'])
    
    # Check that duplicates were detected
    duplicate_issues = [issue for issue in report.issues if issue['type'] == 'DUPLICATES']
    assert len(duplicate_issues) > 0, "Should detect duplicate customer_ids"


def test_duplicate_removal_in_cleaning(spark):
    """Test that clean_customer_data removes duplicates."""
    # Create data with duplicates
    data = pd.DataFrame({
        'customer_id': ['C001', 'C001', 'C002'],  # C001 is duplicate
        'name': ['Alice', 'Alice Duplicate', 'Bob'],
        'email': ['alice@test.com', 'alice2@test.com', 'bob@test.com'],
        'phone': ['555-0001', '555-0002', '555-0003'],
        'signup_date': ['2025-01-01', '2025-01-02', '2025-01-03']
    })
    
    df = spark.createDataFrame(data)
    cleaned = clean_customer_data(df)
    
    # Should have only 2 customers after deduplication
    assert cleaned.count() == 2, "Should remove duplicate customer records"
    
    # Verify specific customer IDs
    customer_ids = [row.customer_id for row in cleaned.select('customer_id').collect()]
    assert sorted(customer_ids) == ['C001', 'C002'], "Should keep first occurrence of each customer"


def test_null_value_detection(spark):
    """Test that null values in required columns are detected."""
    # Create data with null values
    data = pd.DataFrame({
        'customer_id': ['C001', None, 'C003'],
        'name': ['Alice', 'Bob', None],
        'email': ['alice@test.com', 'bob@test.com', 'charlie@test.com'],
        'signup_date': ['2025-01-01', '2025-01-02', '2025-01-03']
    })
    
    df = spark.createDataFrame(data)
    report = check_data_quality(df, 'customers', required_columns=['customer_id', 'name'])
    
    # Check for null value issues
    null_issues = [issue for issue in report.issues if issue['type'] == 'NULL_VALUES']
    assert len(null_issues) >= 2, "Should detect null values in customer_id and name"


def test_invalid_quantity_detection(spark):
    """Test that negative and zero quantities are detected."""
    # Create data with invalid quantities
    data = pd.DataFrame({
        'order_id': ['O001', 'O002', 'O003'],
        'order_date': ['2025-11-01', '2025-11-02', '2025-11-03'],
        'customer_id': ['C001', 'C002', 'C003'],
        'status': ['complete', 'complete', 'complete'],
        'quantity': [2, -1, 0],  # Negative and zero
        'price': [10.0, 15.0, 20.0]
    })
    
    df = spark.createDataFrame(data)
    report = check_data_quality(df, 'orders', required_columns=['order_id', 'customer_id'])
    
    # Check for invalid values
    invalid_qty_issues = [issue for issue in report.issues 
                          if issue['type'] == 'INVALID_VALUE' and issue['column'] == 'quantity']
    assert len(invalid_qty_issues) >= 1, "Should detect invalid quantity values"


def test_referential_integrity(spark):
    """Test detection of orders referencing non-existent customers."""
    # Create customer data
    customers = pd.DataFrame({
        'customer_id': ['C001', 'C002'],
        'name': ['Alice', 'Bob'],
        'email': ['alice@test.com', 'bob@test.com'],
        'signup_date': ['2025-01-01', '2025-01-02']
    })
    
    # Create order data with orphan order
    orders = pd.DataFrame({
        'order_id': ['O001', 'O002', 'O003'],
        'order_date': ['2025-11-01', '2025-11-02', '2025-11-03'],
        'customer_id': ['C001', 'C002', 'C999'],  # C999 doesn't exist
        'status': ['complete', 'complete', 'complete'],
        'quantity': [1, 2, 3],
        'price': [10.0, 15.0, 20.0]
    })
    
    customers_df = spark.createDataFrame(customers)
    orders_df = spark.createDataFrame(orders)
    
    result = check_referential_integrity(orders_df, customers_df)
    
    assert result['orphan_orders'] == 1, "Should detect one orphan order (C999)"


def test_clean_order_data_removes_invalids(spark):
    """Test that clean_order_data removes rows with invalid data."""
    data = pd.DataFrame({
        'order_id': ['O001', 'O002', 'O003', 'O004'],
        'order_date': ['2025-11-01', '2025-11-02', '2025-11-03', '2026-01-01'],  # O004 is future
        'customer_id': ['C001', 'C002', 'C003', 'C004'],
        'status': ['complete', 'complete', 'complete', 'complete'],
        'quantity': [2, -1, 0, 1],  # O002 negative, O003 zero
        'price': [10.0, 15.0, 20.0, 25.0]
    })
    
    df = spark.createDataFrame(data)
    cleaned = clean_order_data(df)
    
    # Should remove O002 (negative qty), O003 (zero qty), O004 (future date)
    assert cleaned.count() == 1, "Should keep only valid orders"
    
    remaining_order = cleaned.select('order_id').collect()[0].order_id
    assert remaining_order == 'O001', "Should keep only O001"
