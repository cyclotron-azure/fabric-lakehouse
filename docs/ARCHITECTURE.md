# Medallion Architecture Guide

## Overview

The **Medallion Architecture** is a data design pattern that organizes data in a lakehouse using a three-layer approach: **Bronze**, **Silver**, and **Gold**. This pattern provides a clear pathway from raw data ingestion to analytics-ready datasets.

---

## Architecture Layers

### 🥉 Bronze Layer (Raw/Landing Zone)

**Purpose**: Store raw, immutable data exactly as received from source systems.

#### Characteristics

- **Schema-on-read**: Flexible schema, can evolve over time
- **Minimal transformation**: Only basic parsing (CSV → table format)
- **Historical archive**: Complete historical record of all ingested data
- **Metadata tracking**: Includes ingestion timestamps, source files, batch IDs
- **Fault tolerance**: Enables data replay if downstream errors occur

#### Implementation in This Project

```python
customers_bronze = customers_raw \
    .withColumn("ingestion_timestamp", F.current_timestamp()) \
    .withColumn("source_file", F.lit("customers.csv")) \
    .withColumn("bronze_layer_id", F.monotonically_increasing_id())
```

**Location**: `Tables/bronze/customers`, `Tables/bronze/orders`

#### Use Cases

- Data auditing and compliance
- Debugging data pipeline issues
- Reprocessing data with new business logic
- Historical analysis of data changes

---

### 🥈 Silver Layer (Cleaned/Curated)

**Purpose**: Provide validated, cleaned, and conformed data ready for business use.

#### Characteristics

- **Data quality applied**: Null handling, deduplication, validation rules
- **Schema enforcement**: Standardized data types and column names
- **Business logic**: Calculated fields, derived columns, enrichment
- **Referential integrity**: Joins between related datasets
- **Incremental updates**: Efficient merge operations for changing data

#### Implementation in This Project

**Data Cleaning**:
```python
def clean_customer_data(customers_df):
    cleaned = (
        customers_df
        .filter(F.col("customer_id").isNotNull())
        .filter(F.col("name").isNotNull())
        .withColumn("email", F.lower(F.trim(F.col("email"))))
        .dropDuplicates(["customer_id"])
    )
    return cleaned
```

**Data Enrichment**:
```python
orders_enriched = orders_clean.join(
    customers_clean,
    on="customer_id",
    how="left"
)
```

**Location**: `Tables/silver/customers`, `Tables/silver/orders`

#### Use Cases

- Feature engineering for ML models
- Ad-hoc analytics and exploration
- Data science workloads
- Input for Gold aggregations

---

### 🥇 Gold Layer (Analytics/Aggregated)

**Purpose**: Business-ready, optimized datasets for reporting and analytics.

#### Characteristics

- **Pre-aggregated**: KPIs and metrics calculated in advance
- **Denormalized**: Optimized for query performance (fewer joins)
- **Use-case specific**: Tailored to specific BI reports or dashboards
- **High performance**: Partitioned and optimized for fast reads
- **Business terminology**: Column names match business language

#### Implementation in This Project

**Monthly Revenue**:
```python
monthly_revenue = (
    orders_silver
    .filter(F.col("status") == "complete")
    .withColumn("month", F.date_format(F.col("order_date"), "yyyy-MM"))
    .groupBy("month")
    .agg(F.sum(F.col("line_total")).alias("revenue"))
)
```

**Customer Segmentation**:
```python
customer_metrics = (
    orders_silver
    .groupBy("customer_id", "name")
    .agg(
        F.sum("line_total").alias("total_spent"),
        F.count("order_id").alias("order_count")
    )
    .withColumn("customer_segment",
        F.when(F.col("order_count") >= 5, "VIP")
         .otherwise("Regular")
    )
)
```

**Location**: `Tables/gold/monthly_revenue`, `Tables/gold/customer_metrics`, `Tables/gold/repeat_customer_rate`

#### Use Cases

- Executive dashboards
- BI reports (Power BI, Tableau)
- Automated alerting
- Performance tracking

---

## Data Flow Diagram

```
┌─────────────────┐
│  Source Systems │
│  (CSV files)    │
└────────┬────────┘
         │
         │ Ingestion (minimal transformation)
         ▼
┌─────────────────────┐
│   🥉 Bronze Layer   │
│   Raw Delta Tables  │
│   - customers       │
│   - orders          │
└─────────┬───────────┘
          │
          │ Cleaning, Validation, Enrichment
          ▼
┌─────────────────────┐
│   🥈 Silver Layer   │
│  Curated Delta Tbls │
│   - customers       │
│   - orders          │
└─────────┬───────────┘
          │
          │ Aggregation, Denormalization
          ▼
┌─────────────────────────┐
│    🥇 Gold Layer        │
│  Analytics Delta Tables │
│   - monthly_revenue     │
│   - customer_metrics    │
│   - repeat_cust_rate    │
└─────────────────────────┘
          │
          │ Consumption
          ▼
┌─────────────────────────┐
│   BI Tools / Reports    │
│   - Power BI            │
│   - Notebooks           │
│   - ML Models           │
└─────────────────────────┘
```

---

## Design Principles

### 1. Immutability (Bronze)

Bronze tables are **append-only** - never delete or modify historical data. This ensures:
- Complete audit trail
- Ability to reprocess data
- Compliance with data retention policies

### 2. Idempotency (Silver & Gold)

Transformations should be **idempotent** - running the same pipeline multiple times produces the same result:
- Use `MERGE` operations for upserts
- Handle duplicates explicitly
- Design for incremental processing

### 3. Incremental Processing

Process only new/changed data for efficiency:
- Use watermarks for incremental loads
- Partition by date for easy filtering
- Implement change data capture (CDC) where applicable

### 4. Schema Evolution

Support evolving schemas without breaking downstream:
- Use `mergeSchema` option for Delta writes
- Handle new columns gracefully
- Version schema changes

---

## Performance Optimization

### Bronze Layer

```python
# Partition by ingestion date for efficient pruning
bronze_df.write \
    .partitionBy("ingestion_date") \
    .format("delta") \
    .save(path)
```

### Silver Layer

```python
# Z-order clustering for common filters
spark.sql(f"OPTIMIZE delta.`{silver_path}` ZORDER BY (customer_id, order_date)")
```

### Gold Layer

```python
# Materialize aggregations for fast queries
# Consider using Delta Live Tables for auto-optimization
```

---

## Delta Lake Benefits

All layers use **Delta Lake** format for:

1. **ACID Transactions**: Ensures data consistency
2. **Time Travel**: Query historical versions (`VERSION AS OF`)
3. **Schema Evolution**: Add columns without breaking queries
4. **Efficient Upserts**: `MERGE` operations for incremental updates
5. **Audit History**: Track all changes with transaction log

---

## Medallion vs. Traditional Data Warehouse

| Aspect | Medallion (Lakehouse) | Traditional DW |
|--------|----------------------|----------------|
| **Storage** | Cloud object storage (cheap) | Proprietary storage (expensive) |
| **Schema** | Flexible, schema-on-read | Rigid, schema-on-write |
| **Data Types** | Structured, semi-structured, unstructured | Structured only |
| **Scalability** | Elastic, pay-per-use | Fixed capacity |
| **Processing** | Spark, SQL, Python, R | SQL primarily |
| **Cost** | Low (storage cheap, compute on-demand) | High (always-on compute) |

---

## Best Practices

### ✅ Do

- Keep Bronze layer immutable
- Apply data quality checks in Silver
- Partition tables by commonly filtered columns (date, region)
- Use descriptive table and column names
- Document transformations and business logic
- Implement monitoring and alerting

### ❌ Don't

- Transform data in Bronze (keep raw)
- Skip data quality validation
- Create Gold tables without understanding use case
- Use SELECT * in production pipelines
- Ignore schema evolution planning

---

## Common Patterns

### Pattern 1: Slowly Changing Dimensions (SCD Type 2)

Track historical changes in customer data:

```python
# Silver layer - track customer changes
customers_scd = customers_bronze \
    .withColumn("effective_date", F.col("ingestion_timestamp")) \
    .withColumn("end_date", F.lit(None).cast("timestamp")) \
    .withColumn("is_current", F.lit(True))
```

### Pattern 2: Aggregation with Windows

Calculate running totals or rankings:

```python
# Gold layer - customer lifetime value with ranking
window_spec = Window.partitionBy("customer_segment").orderBy(F.desc("total_spent"))

customer_metrics_ranked = customer_metrics \
    .withColumn("rank_in_segment", F.row_number().over(window_spec))
```

### Pattern 3: Incremental Loads

Process only new data since last run:

```python
# Read with watermark
last_processed = spark.read.format("delta").load(checkpoint_path)
max_timestamp = last_processed.agg(F.max("ingestion_timestamp")).collect()[0][0]

# Process only new records
new_data = bronze_df.filter(F.col("ingestion_timestamp") > max_timestamp)
```

---

## Monitoring and Observability

### Key Metrics to Track

**Bronze Layer**:
- Records ingested per batch
- Ingestion latency
- Source file errors

**Silver Layer**:
- Data quality score
- Records rejected (failed validation)
- Transformation execution time

**Gold Layer**:
- Aggregation freshness
- Query performance
- Data completeness

### Implement in Code

```python
from src.logging_utils import setup_logger, log_dataframe_stats
from src.quality_checks import check_data_quality

# Log metrics
logger = setup_logger(__name__)
log_dataframe_stats(df, "customers", logger)

# Track quality
quality_report = check_data_quality(df, "customers", required_columns)
logger.info(f"Quality score: {quality_report.quality_score}%")
```

---

## Next Steps

1. **Run the Notebooks**: Follow the sequence Bronze → Silver → Gold
2. **Fix the Bugs**: Complete Task B to understand transformation challenges
3. **Implement New Features**: Add repeat_customer_rate metric (Task C)
4. **Review Governance**: Read [GOVERNANCE.md](GOVERNANCE.md) for compliance

---

## References

- [Databricks Medallion Architecture](https://www.databricks.com/glossary/medallion-architecture)
- [Microsoft Fabric Lakehouse](https://learn.microsoft.com/fabric/data-engineering/lakehouse-overview)
- [Delta Lake Documentation](https://docs.delta.io/)
- [Data Mesh Principles](https://www.datamesh-architecture.com/)
