"""
Logging utilities for data pipeline operations.
"""

import logging
import sys
from typing import Optional
from pyspark.sql import DataFrame


def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Set up a logger with consistent formatting.
    
    Args:
        name: Logger name (typically __name__)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler with formatting
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, level.upper()))
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    return logger


def log_dataframe_stats(df: DataFrame, name: str, logger: Optional[logging.Logger] = None):
    """
    Log basic statistics about a DataFrame.
    
    Args:
        df: DataFrame to analyze
        name: Name/description of the DataFrame
        logger: Logger instance (creates default if None)
    """
    if logger is None:
        logger = logging.getLogger(__name__)
    
    row_count = df.count()
    col_count = len(df.columns)
    
    logger.info(f"DataFrame '{name}' statistics:")
    logger.info(f"  - Rows: {row_count:,}")
    logger.info(f"  - Columns: {col_count}")
    logger.info(f"  - Column names: {', '.join(df.columns)}")
    
    # Log null counts for each column
    null_counts = df.select([
        (F.sum(F.col(c).isNull().cast("int")).alias(c)) 
        for c in df.columns
    ]).collect()[0].asDict()
    
    has_nulls = any(count > 0 for count in null_counts.values())
    if has_nulls:
        logger.info("  - Null counts:")
        for col, count in null_counts.items():
            if count > 0:
                logger.info(f"    {col}: {count:,} ({(count/row_count)*100:.2f}%)")
    else:
        logger.info("  - No null values detected")


# Import for null count calculation
from pyspark.sql import functions as F
