# 🎯 Azure Fabric Lakehouse Medallion Architecture

A comprehensive 60-minute hands-on assessment for Azure Fabric & Data Engineering candidates.

## 📋 Overview

This repository provides a complete **Medallion Architecture** implementation on Azure Fabric Lakehouse with:
- **Bronze → Silver → Gold** data transformation pipeline
- Seeded bugs for debugging assessment
- Feature implementation challenges
- Governance documentation tasks
- Agentic AI helper (mock mode)

**Business Scenario**: Retail orders data ingestion, transformation, and analytics.

---

## 🏗️ Repository Structure

```
inteview/
├── data/                       # Sample CSV files
│   ├── customers.csv           # Customer master data (with quality issues)
│   └── orders.csv              # Order transactions (mixed-case status)
├── infra/                      # Infrastructure setup
│   └── setup-lakehouse.ps1     # PowerShell script for Fabric Lakehouse creation (mock)
├── notebooks/                  # PySpark notebooks
│   ├── 01_Bronze_Ingest.ipynb  # Raw data ingestion
│   ├── 02_Silver_Transform.ipynb  # Data cleaning (contains bugs!)
│   └── 03_Gold_Aggregates.ipynb   # Analytics aggregation
├── src/                        # Python utilities
│   ├── __init__.py
│   ├── schema_utils.py         # Schema inference and validation
│   ├── quality_checks.py       # Data quality checks
│   ├── logging_utils.py        # Logging helpers
│   ├── silver.py               # Silver layer transformations (BUGGY!)
│   └── agent_helper.py         # Semantic Kernel mock agent
├── tests/                      # Pytest test suite
│   ├── test_schema.py          # Schema validation tests
│   ├── test_quality.py         # Data quality tests
│   └── test_aggregates.py      # Aggregate calculation tests (will fail until fixed)
├── docs/                       # Documentation
│   ├── ARCHITECTURE.md         # Medallion architecture explanation
│   └── GOVERNANCE.md           # Data governance guidelines
├── .devcontainer/              # VS Code dev container config
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
└── README.md                   # This file
```

---

## 🚀 Quick Start (15 minutes)

### Prerequisites

- **Azure Fabric workspace** (already exists - see assumptions)
- **Python 3.11+**
- **VS Code** (recommended) or Jupyter environment
- **Git**

### Step 1: Clone Repository

```bash
git clone <your-repo-url>
cd inteview
```

### Step 2: Set Up Environment

**Option A: Using Dev Container (Recommended)**
```bash
# Open in VS Code
code .
# Press Ctrl+Shift+P → "Dev Containers: Reopen in Container"
```

**Option B: Local Python Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

### Step 3: Create Lakehouse (Mock Mode)

```powershell
cd infra
./setup-lakehouse.ps1 -WorkspaceName "InterviewWorkspace" -LakehouseName "RetailLakehouse"
```

**Note**: This script is in mock mode. For real deployment, uncomment API calls in the script.

### Step 4: Verify Setup

```bash
# Run tests to confirm environment
pytest tests/ -v
```

**Expected**: Most tests pass, but `test_aggregates.py` will **FAIL** (this is intentional - see Task B).

---

## 📝 Interview Tasks (60 minutes)

### Task A: Setup & Data Ingestion (15 minutes)

**Objective**: Load raw CSV files into Bronze Delta tables.

1. Open `notebooks/01_Bronze_Ingest.ipynb`
2. Update `DATA_PATH` if not using local development setup
3. Run all cells to ingest customers and orders
4. Verify Bronze tables created successfully

**Deliverable**: Bronze tables with metadata columns added.

**Evaluation Criteria**:
- Correct Delta table creation
- Metadata columns present (ingestion_timestamp, source_file)
- Understanding of Bronze layer purpose

---

### Task B: Debug Silver Transformation (20 minutes)

**Objective**: Fix bugs in the `compute_monthly_revenue()` function.

#### 🐛 Known Bugs

The function in `src/silver.py` has two critical bugs:

1. **Case-sensitive status filter**: Filters only `status == 'complete'`, missing `'Complete'` and `'COMPLETE'`
2. **Incorrect revenue calculation**: Uses `SUM(price)` instead of `SUM(quantity * price)`

#### Steps

1. Open `notebooks/02_Silver_Transform.ipynb`
2. Run cells until you reach the "TASK B" section
3. Observe incorrect monthly revenue results
4. Open `src/silver.py` and locate `compute_monthly_revenue()`
5. Fix both bugs:
   - Normalize status to lowercase before filtering
   - Calculate revenue as `quantity * price`
6. Re-run the notebook cell to verify fix
7. Run `pytest tests/test_aggregates.py` - all tests should now **PASS**

#### Expected Corrected Code

```python
from pyspark.sql import functions as F

def compute_monthly_revenue(orders_df):
    """
    FIX:
    - Normalize status to lowercase and compare to 'complete'
    - Use SUM(quantity * price) for revenue
    """
    cleaned = orders_df.withColumn("status_norm", F.lower(F.col("status")))
    result = (
        cleaned
        .filter(F.col("status_norm") == F.lit("complete"))
        .withColumn("month", F.date_format(F.col("order_date"), "yyyy-MM"))
        .withColumn("line_revenue", F.col("quantity") * F.col("price"))
        .groupBy("month")
        .agg(F.sum("line_revenue").alias("revenue"))
        .orderBy("month")
    )
    return result
```

**Deliverable**: Fixed function + passing tests.

**Evaluation Criteria**:
- Correctly identified both bugs
- Implemented proper fix (not workaround)
- Tests pass
- Explained root cause

---

### Task C: Add New Gold Metric (15 minutes)

**Objective**: Implement `repeat_customer_rate` calculation.

**Definition**: Percentage of customers making repeat purchases (2+ orders) per month.

#### Steps

1. Open `notebooks/03_Gold_Aggregates.ipynb`
2. Navigate to "TASK C" section
3. Implement the calculation using window functions
4. Write results to Gold Delta table
5. Verify metric accuracy

#### Hints

- Use `Window.partitionBy("customer_id").orderBy("order_date")`
- Add `order_number` column with `row_number()`
- Flag `is_repeat_customer` when `order_number > 1`
- Group by month and calculate percentage

**Deliverable**: Gold table `repeat_customer_rate` with monthly metrics.

**Evaluation Criteria**:
- Correct use of window functions
- Accurate repeat customer identification
- Proper aggregation by month
- Code quality and comments

---

### Task D: Data Governance Documentation (10 minutes)

**Objective**: Explain PII scanning and classification strategy using Microsoft Purview.

1. Open `docs/GOVERNANCE.md`
2. Read the existing governance framework
3. In the "PII Classification with Purview" section, write **5 bullet points** explaining:
   - How to scan Lakehouse tables with Purview
   - What PII columns exist in this dataset
   - Classification labels to apply
   - Access controls to implement
   - Compliance considerations

**Deliverable**: 5 concise, actionable bullets in `GOVERNANCE.md`.

**Evaluation Criteria**:
- Understanding of Purview capabilities
- Identified correct PII fields (email, phone)
- Practical implementation steps
- Compliance awareness (GDPR, CCPA)

---

## 🧪 Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_aggregates.py -v
```

### Run with Coverage
```bash
pytest tests/ --cov=src --cov-report=html
```

### Expected Test Results

**Before fixes**:
```
tests/test_schema.py ............ PASSED
tests/test_quality.py ........... PASSED
tests/test_aggregates.py ........ FAILED  ← Expected (bugs not fixed)
```

**After Task B fixes**:
```
tests/test_schema.py ............ PASSED
tests/test_quality.py ........... PASSED
tests/test_aggregates.py ........ PASSED  ← All tests pass
```

---

## 📚 Additional Resources

- [Medallion Architecture Explanation](docs/ARCHITECTURE.md)
- [Data Governance Guidelines](docs/GOVERNANCE.md)
- [Azure Fabric Documentation](https://learn.microsoft.com/fabric/)
- [Delta Lake Documentation](https://docs.delta.io/)

---

## 🎯 Evaluation Rubric

| Criteria | Weight | Pass Threshold |
|----------|--------|----------------|
| **Setup** | 20 pts | Bronze tables created with metadata |
| **Debugging** | PASS | Both bugs identified and fixed correctly |
| **Data Modeling** | PASS | Repeat customer rate implemented accurately |
| **Feature Quality** | PASS | Clean code, proper window functions, tests pass |
| **Communication** | PASS | Clear governance documentation |
| **Overall** | PASS/FAIL | All sections must PASS for overall PASS |

### Observable Behaviors

**PASS (All 4 Sections)**:
- Identifies bugs within 10 minutes
- Implements repeat_customer_rate with optimized query
- Adds additional data quality checks
- Governance documentation includes automation strategies
- Clean code, clear communication

**FAIL (Any 1+ Sections)**:
- Missing either bug, or implementation incomplete
- Data modeling doesn't meet criteria
- Tests don't pass after fixes
- Governance documentation missing required elements
- Code quality significantly below expected
- Unable to fix bugs independently
- Repeat_customer_rate calculation incorrect
- Missing governance documentation
- Tests remain failing

---

## 🛠️ Troubleshooting

### Issue: PySpark Import Errors
**Solution**: Ensure `pyspark` is installed: `pip install -r requirements.txt`

### Issue: Delta Tables Not Found
**Solution**: Run `01_Bronze_Ingest.ipynb` first to create Bronze tables

### Issue: Tests Failing After Fix
**Solution**: Verify you modified `src/silver.py` correctly and restarted Python kernel

### Issue: Fabric Connection Errors (if using real Fabric)
**Solution**: Check workspace permissions and Azure CLI authentication

---

## 📄 License

This is provided for interview assessment purposes. Modify as needed for your organization.

---

## 🤝 Contributing

For production use of this assessment:
1. Replace mock scripts with real Azure Fabric API calls
2. Add authentication configuration
3. Implement CI/CD pipelines
4. Add monitoring and alerting

---

## 📧 Questions?

Contact your interviewer or hiring manager for clarification during the assessment.

**Good luck! 🚀**
