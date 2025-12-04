"""
Silver transformation functions with seeded bugs for interview assessment.

This module contains data transformation logic for the Silver layer.
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def compute_monthly_revenue(orders_df: DataFrame) -> DataFrame:
    """
    Compute monthly revenue from orders.
    
    ⚠️ BUG ALERT (For Interview Assessment):
    - BUG 1: Uses SUM(price) instead of SUM(quantity * price)
    - BUG 2: Filters by status == 'complete' (case-sensitive) causing valid rows 
             like 'Complete'/'COMPLETE' to be dropped
    
    Args:
        orders_df: Orders DataFrame with columns: order_date, status, quantity, price
        
    Returns:
        DataFrame with columns: month, revenue
    """
    result = (
        orders_df
        .filter(F.col("status") == "complete")  # BUG 1: case-sensitive filter
        .withColumn("month", F.date_format(F.col("order_date"), "yyyy-MM"))
        .groupBy("month")
        .agg(F.sum("price").alias("revenue"))   # BUG 2: wrong aggregation - should be quantity * price
        .orderBy("month")
    )
    return result


def clean_customer_data(customers_df: DataFrame) -> DataFrame:
    """
    Clean and normalize customer data.
    
    Args:
        customers_df: Raw customers DataFrame
        
    Returns:
        Cleaned customers DataFrame
    """
    logger.info("Cleaning customer data...")
    
    cleaned = (
        customers_df
        # Remove rows with missing customer_id or name
        .filter(F.col("customer_id").isNotNull() & (F.col("customer_id") != ""))
        .filter(F.col("name").isNotNull() & (F.col("name") != ""))
        # Normalize email to lowercase
        .withColumn("email", F.lower(F.trim(F.col("email"))))
        # Remove duplicate customer records (keep first occurrence)
        .dropDuplicates(["customer_id"])
        # Add data quality flag
        .withColumn("has_email", F.col("email").isNotNull() & (F.col("email") != ""))
        .withColumn("has_phone", F.col("phone").isNotNull() & (F.col("phone") != ""))
    )
    
    logger.info(f"Cleaned {cleaned.count()} customer records")
    return cleaned


def clean_order_data(orders_df: DataFrame) -> DataFrame:
    """
    Clean and normalize order data.
    
    Args:
        orders_df: Raw orders DataFrame
        
    Returns:
        Cleaned orders DataFrame
    """
    logger.info("Cleaning order data...")
    
    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')
    
    cleaned = (
        orders_df
        # Remove rows with missing critical fields
        .filter(F.col("order_id").isNotNull() & (F.col("order_id") != ""))
        .filter(F.col("customer_id").isNotNull() & (F.col("customer_id") != ""))
        .filter(F.col("order_date").isNotNull())
        # Normalize status to lowercase for consistency
        .withColumn("status", F.lower(F.trim(F.col("status"))))
        # Remove invalid quantities and prices
        .filter(F.col("quantity") > 0)
        .filter(F.col("price") >= 0)
        # Remove future dates
        .filter(F.col("order_date") <= F.lit(today))
        # Remove duplicate orders
        .dropDuplicates(["order_id"])
        # Calculate line total
        .withColumn("line_total", F.col("quantity") * F.col("price"))
    )
    
    logger.info(f"Cleaned {cleaned.count()} order records")
    return cleaned


def join_orders_with_customers(orders_df: DataFrame, customers_df: DataFrame) -> DataFrame:
    """
    Join orders with customer data to create enriched dataset.
    
    Args:
        orders_df: Cleaned orders DataFrame
        customers_df: Cleaned customers DataFrame
        
    Returns:
        Joined DataFrame with order and customer information
    """
    logger.info("Joining orders with customers...")
    
    enriched = (
        orders_df
        .join(
            customers_df.select("customer_id", "name", "email", "city", "state"),
            on="customer_id",
            how="left"
        )
        # Add flag for orphan orders
        .withColumn("has_customer_data", F.col("name").isNotNull())
    )
    
    total_orders = enriched.count()
    orphan_orders = enriched.filter(~F.col("has_customer_data")).count()
    
    if orphan_orders > 0:
        logger.warning(f"Found {orphan_orders} orphan orders ({(orphan_orders/total_orders)*100:.2f}%)")
    
    logger.info(f"Enriched {total_orders} orders with customer data")
    return enriched
