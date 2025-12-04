"""
Schema inference and validation utilities for data quality checks.
"""

from pyspark.sql import DataFrame
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DateType
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


def infer_schema(df: DataFrame, sample_size: int = 100) -> StructType:
    """
    Infer schema from a DataFrame by analyzing data types and patterns.
    
    Args:
        df: Input DataFrame
        sample_size: Number of rows to sample for inference
        
    Returns:
        Inferred StructType schema
    """
    logger.info(f"Inferring schema from DataFrame with {df.count()} rows")
    
    # Get current schema
    current_schema = df.schema
    
    # For this implementation, we return the existing schema
    # In a real scenario, you'd analyze data patterns to suggest improvements
    logger.info(f"Inferred schema with {len(current_schema.fields)} fields")
    
    return current_schema


def validate_schema(df: DataFrame, expected_schema: Dict[str, str]) -> Dict[str, any]:
    """
    Validate DataFrame schema against expected structure.
    
    Args:
        df: Input DataFrame
        expected_schema: Dictionary of column_name -> expected_type
        
    Returns:
        Dictionary with validation results
    """
    logger.info("Validating schema...")
    
    results = {
        'valid': True,
        'missing_columns': [],
        'unexpected_columns': [],
        'type_mismatches': [],
        'errors': []
    }
    
    actual_columns = {field.name: field.dataType.simpleString() for field in df.schema.fields}
    expected_columns = set(expected_schema.keys())
    actual_column_names = set(actual_columns.keys())
    
    # Check for missing columns
    missing = expected_columns - actual_column_names
    if missing:
        results['missing_columns'] = list(missing)
        results['valid'] = False
        logger.warning(f"Missing columns: {missing}")
    
    # Check for unexpected columns
    unexpected = actual_column_names - expected_columns
    if unexpected:
        results['unexpected_columns'] = list(unexpected)
        logger.info(f"Unexpected columns (may be valid): {unexpected}")
    
    # Check data types for common columns
    for col in expected_columns & actual_column_names:
        expected_type = expected_schema[col]
        actual_type = actual_columns[col]
        
        # Simplified type comparison (in real implementation, handle type hierarchies)
        if expected_type.lower() not in actual_type.lower():
            results['type_mismatches'].append({
                'column': col,
                'expected': expected_type,
                'actual': actual_type
            })
            results['valid'] = False
            logger.warning(f"Type mismatch for {col}: expected {expected_type}, got {actual_type}")
    
    if results['valid']:
        logger.info("Schema validation passed")
    else:
        logger.error("Schema validation failed")
    
    return results


def get_required_columns(table_name: str) -> Dict[str, str]:
    """
    Get required columns and their types for a given table.
    
    Args:
        table_name: Name of the table (customers, orders, etc.)
        
    Returns:
        Dictionary of column_name -> data_type
    """
    schemas = {
        'customers': {
            'customer_id': 'string',
            'name': 'string',
            'email': 'string',
            'signup_date': 'date'
        },
        'orders': {
            'order_id': 'string',
            'order_date': 'date',
            'customer_id': 'string',
            'status': 'string',
            'quantity': 'int',
            'price': 'double'
        }
    }
    
    return schemas.get(table_name, {})
