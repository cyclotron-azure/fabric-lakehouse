"""
Data quality checks and reporting for data validation.
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class DataQualityReport:
    """Data quality check results."""
    table_name: str
    total_rows: int
    valid_rows: int
    issues: List[Dict[str, any]] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    @property
    def quality_score(self) -> float:
        """Calculate quality score as percentage of valid rows."""
        if self.total_rows == 0:
            return 0.0
        return (self.valid_rows / self.total_rows) * 100
    
    def add_issue(self, issue_type: str, column: str, count: int, details: Optional[str] = None):
        """Add a data quality issue."""
        self.issues.append({
            'type': issue_type,
            'column': column,
            'count': count,
            'details': details
        })
        logger.warning(f"Quality issue in {self.table_name}.{column}: {issue_type} ({count} rows)")
    
    def add_warning(self, message: str):
        """Add a warning message."""
        self.warnings.append(message)
        logger.warning(f"Quality warning for {self.table_name}: {message}")
    
    def to_dict(self) -> Dict:
        """Convert report to dictionary."""
        return {
            'table_name': self.table_name,
            'total_rows': self.total_rows,
            'valid_rows': self.valid_rows,
            'quality_score': round(self.quality_score, 2),
            'issues': self.issues,
            'warnings': self.warnings
        }


def check_data_quality(df: DataFrame, table_name: str, required_columns: List[str] = None) -> DataQualityReport:
    """
    Perform comprehensive data quality checks on a DataFrame.
    
    Args:
        df: Input DataFrame to check
        table_name: Name of the table being checked
        required_columns: List of columns that must not be null
        
    Returns:
        DataQualityReport with findings
    """
    logger.info(f"Starting data quality check for {table_name}")
    
    total_rows = df.count()
    report = DataQualityReport(
        table_name=table_name,
        total_rows=total_rows,
        valid_rows=total_rows  # Will be decremented as issues are found
    )
    
    if total_rows == 0:
        report.add_warning("Table is empty")
        return report
    
    # Check for null values in required columns
    if required_columns:
        for col in required_columns:
            if col not in df.columns:
                report.add_warning(f"Required column '{col}' not found in DataFrame")
                continue
                
            null_count = df.filter(F.col(col).isNull() | (F.col(col) == "")).count()
            if null_count > 0:
                report.add_issue("NULL_VALUES", col, null_count, 
                               f"{(null_count/total_rows)*100:.2f}% of rows")
                report.valid_rows -= null_count
    
    # Check for duplicates (if primary key column exists)
    if 'customer_id' in df.columns and table_name == 'customers':
        duplicate_count = df.groupBy('customer_id').count().filter(F.col('count') > 1).count()
        if duplicate_count > 0:
            report.add_issue("DUPLICATES", "customer_id", duplicate_count,
                           "Duplicate customer IDs found")
    
    if 'order_id' in df.columns and table_name == 'orders':
        duplicate_count = df.groupBy('order_id').count().filter(F.col('count') > 1).count()
        if duplicate_count > 0:
            report.add_issue("DUPLICATES", "order_id", duplicate_count,
                           "Duplicate order IDs found")
    
    # Check for negative values in numeric columns
    if 'quantity' in df.columns:
        negative_qty = df.filter(F.col('quantity') < 0).count()
        if negative_qty > 0:
            report.add_issue("INVALID_VALUE", "quantity", negative_qty,
                           "Negative quantities detected")
        
        zero_qty = df.filter(F.col('quantity') == 0).count()
        if zero_qty > 0:
            report.add_issue("INVALID_VALUE", "quantity", zero_qty,
                           "Zero quantities detected")
    
    if 'price' in df.columns:
        negative_price = df.filter(F.col('price') < 0).count()
        if negative_price > 0:
            report.add_issue("INVALID_VALUE", "price", negative_price,
                           "Negative prices detected")
        
        zero_price = df.filter(F.col('price') == 0).count()
        if zero_price > 0:
            report.add_issue("INVALID_VALUE", "price", zero_price,
                           "Zero prices detected")
    
    # Check for future dates
    if 'order_date' in df.columns:
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        future_dates = df.filter(F.col('order_date') > F.lit(today)).count()
        if future_dates > 0:
            report.add_issue("INVALID_VALUE", "order_date", future_dates,
                           "Future dates detected")
    
    # Statistical outliers for numeric columns
    if 'price' in df.columns:
        price_stats = df.select(
            F.mean('price').alias('mean'),
            F.stddev('price').alias('stddev'),
            F.max('price').alias('max')
        ).collect()[0]
        
        if price_stats['stddev']:
            outlier_threshold = price_stats['mean'] + (3 * price_stats['stddev'])
            outliers = df.filter(F.col('price') > outlier_threshold).count()
            if outliers > 0:
                report.add_issue("OUTLIER", "price", outliers,
                               f"Values > {outlier_threshold:.2f} (3 std dev)")
    
    logger.info(f"Quality check complete. Score: {report.quality_score:.2f}%")
    return report


def check_referential_integrity(orders_df: DataFrame, customers_df: DataFrame) -> Dict[str, int]:
    """
    Check referential integrity between orders and customers.
    
    Args:
        orders_df: Orders DataFrame
        customers_df: Customers DataFrame
        
    Returns:
        Dictionary with orphan counts
    """
    logger.info("Checking referential integrity...")
    
    # Find orders with customer_ids not in customers table
    customer_ids = customers_df.select('customer_id').distinct()
    orphan_orders = orders_df.join(
        customer_ids,
        orders_df.customer_id == customer_ids.customer_id,
        'left_anti'
    ).count()
    
    logger.info(f"Found {orphan_orders} orphan orders")
    
    return {
        'orphan_orders': orphan_orders
    }
