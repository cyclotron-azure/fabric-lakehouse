"""
Test suite for schema validation.
"""

import pytest
import pandas as pd
from pyspark.sql import SparkSession
from src.schema_utils import validate_schema, get_required_columns


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


def test_customers_schema_validation(spark):
    """Test that customer schema validation works correctly."""
    # Create test data with correct schema
    data = pd.DataFrame({
        'customer_id': ['C001', 'C002'],
        'name': ['Alice', 'Bob'],
        'email': ['alice@test.com', 'bob@test.com'],
        'phone': ['555-0001', '555-0002'],
        'signup_date': ['2025-01-01', '2025-01-02']
    })
    
    df = spark.createDataFrame(data)
    expected_schema = get_required_columns('customers')
    
    result = validate_schema(df, expected_schema)
    
    assert result['valid'] == True, "Valid customer schema should pass validation"
    assert len(result['missing_columns']) == 0, "Should have no missing columns"


def test_orders_schema_validation(spark):
    """Test that order schema validation works correctly."""
    # Create test data with correct schema
    data = pd.DataFrame({
        'order_id': ['O001', 'O002'],
        'order_date': ['2025-11-01', '2025-11-02'],
        'customer_id': ['C001', 'C002'],
        'status': ['complete', 'complete'],
        'quantity': [2, 1],
        'price': [10.0, 15.0]
    })
    
    df = spark.createDataFrame(data)
    expected_schema = get_required_columns('orders')
    
    result = validate_schema(df, expected_schema)
    
    assert result['valid'] == True, "Valid order schema should pass validation"
    assert len(result['missing_columns']) == 0, "Should have no missing columns"


def test_missing_required_column(spark):
    """Test that validation fails when required columns are missing."""
    # Create data missing the 'email' column
    data = pd.DataFrame({
        'customer_id': ['C001'],
        'name': ['Alice'],
        'phone': ['555-0001'],
        'signup_date': ['2025-01-01']
    })
    
    df = spark.createDataFrame(data)
    expected_schema = get_required_columns('customers')
    
    result = validate_schema(df, expected_schema)
    
    assert result['valid'] == False, "Missing required column should fail validation"
    assert 'email' in result['missing_columns'], "Should detect missing email column"


def test_unexpected_columns_allowed(spark):
    """Test that extra columns don't cause validation failure."""
    # Create data with extra column
    data = pd.DataFrame({
        'customer_id': ['C001'],
        'name': ['Alice'],
        'email': ['alice@test.com'],
        'signup_date': ['2025-01-01'],
        'extra_field': ['some value']  # Extra column
    })
    
    df = spark.createDataFrame(data)
    expected_schema = get_required_columns('customers')
    
    result = validate_schema(df, expected_schema)
    
    # Extra columns should be noted but not cause failure
    assert 'extra_field' in result['unexpected_columns'], "Should detect unexpected columns"
    # Validation should still pass if all required columns are present
    assert len(result['missing_columns']) == 0, "Should have no missing required columns"
