# ⚡ Quick Commands Reference

**40-minute Medallion Architecture Assessment**

---

## 🎯 Assessment Scoring

```
Bronze Layer (Task A):     PASS or FAIL
Silver Layer (Task B):     PASS or FAIL
Gold Layer (Task C):       PASS or FAIL
Governance (Task D):       PASS or FAIL
─────────────────────────────────────
Overall Result:            PASS (all 4) or FAIL (any 1+)
```

---

```bash
# Clone repository
git clone <repo-url>
cd inteview

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies (takes ~2 min)
pip install -r requirements.txt

# Verify installation (should show 10 pass, 4 fail)
pytest tests/ -v

# Start Jupyter
jupyter lab

# Open in browser: http://localhost:8888
```

---

## 📋 During Assessment Commands

### Task A: Bronze Ingestion (10 min)
```bash
# In Jupyter, open: notebooks/01_Bronze_Ingest.ipynb
# Tasks:
# 1. Load data/customers.csv and data/orders.csv
# 2. Add columns: ingestion_timestamp, source_file, bronze_layer_id
# 3. Write to Delta tables: Tables/bronze/customers, Tables/bronze/orders
# 4. Display results with df.show()

# After finishing, run:
pytest tests/test_schema.py -v  # All should pass
```

### Task B: Debug Bugs (12 min)
```bash
# 1. Run current tests - some will fail
pytest tests/test_aggregates.py -v
# Expected: 10 passed, 4 failed

# 2. Open and run: notebooks/02_Silver_Transform.ipynb
# 3. Inspect output - notice wrong revenue numbers

# 4. Check src/silver.py line ~20-30
# Find bugs in: compute_monthly_revenue()

# 5. Fix both bugs:
#    Bug 1: Status filter is case-sensitive
#    Bug 2: Revenue calculation missing quantity

# 6. Verify fixes
pytest tests/test_aggregates.py -v
# Expected after fix: 4 passed ✅

# Run full suite
pytest tests/ -v
# Expected: 14 passed ✅
```

### Task C: Feature Implementation (12 min)
```bash
# 1. Open: notebooks/03_Gold_Aggregates.ipynb
# 2. Find Task C section (search for "Task C")
# 3. Implement repeat_customer_rate metric using window functions
# 4. Write results to Delta table

# 5. Verify implementation
pytest tests/ -v  # All should still pass

# Test specific feature (if created)
# pytest tests/test_aggregates.py::test_repeat_customer_rate -v
```

### Task D: Governance Documentation (6 min)
```bash
# 1. Open: docs/GOVERNANCE.md
# 2. Find section: "## Task D: PII Classification with Purview"
# 3. Write 5 bullets explaining:
#    - How Purview classifies PII (email, phone)
#    - Lineage tracking (Bronze → Silver → Gold)
#    - Access controls
#    - Audit trail
#    - Retention policy

# No code to run - just documentation
```

---

## 🧪 Test Commands

```bash
# Run everything
pytest tests/ -v

# Run specific test file
pytest tests/test_schema.py -v      # 4 tests
pytest tests/test_quality.py -v     # 7 tests
pytest tests/test_aggregates.py -v  # 4 tests

# Run specific test
pytest tests/test_aggregates.py::test_compute_monthly_revenue_uses_qty_times_price -v

# Run with output capturing
pytest tests/ -v -s

# Run with coverage report
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html

# Run only failing tests (after Bug fix)
pytest tests/ -v --lf  # "last failed"

# Run tests quietly
pytest tests/ -q
```

---

## 🐛 Debugging Commands

```bash
# Check what tests expect
pytest tests/test_aggregates.py -v

# Look at actual data in CSV
head -5 data/customers.csv
head -5 data/orders.csv

# Check status values (mixed case!)
grep "status" data/orders.csv | sort | uniq

# Look at src/silver.py for bugs
cat src/silver.py | grep -A 10 "compute_monthly_revenue"

# Check current errors
pytest tests/test_aggregates.py::test_monthly_revenue_case_insensitive_status -v
```

---

## 📊 Data Inspection

```bash
# In Jupyter notebook, run:

# Load and inspect customers
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("inspect").getOrCreate()
customers = spark.read.option("header", True).csv("data/customers.csv")
customers.show()
customers.printSchema()

# Load and inspect orders
orders = spark.read.option("header", True).csv("data/orders.csv")
orders.show()

# Check unique status values
orders.select("status").distinct().show()
```

---

## 🔧 Troubleshooting

### "Module not found" errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Verify installation
pip list | grep -E "pyspark|delta-spark|pandas|pytest"
```

### "Jupyter not found"
```bash
# Install Jupyter
pip install jupyter jupyterlab

# Start again
jupyter lab
```

### "Tests still fail after fix"
```bash
# Make sure you changed src/silver.py, not test files
cat src/silver.py | grep "def compute_monthly_revenue" -A 15

# Run just that test with verbose output
pytest tests/test_aggregates.py -v -s
```

### "Can't find data files"
```bash
# Make sure you're in right directory
pwd  # Should show: .../inteview

# Check files exist
ls -la data/
```

---

## ⏱️ Medallion Timeline (40 min)

```
Setup:           3 min    (pip install, verify environment)
Bronze:         10 min    (CSV ingestion with metadata)
Silver:         12 min    (Debug + fix data quality bugs)
Gold:           12 min    (Feature: repeat_customer_rate)
Governance:      6 min    (Write Purview PII bullets)
─────────────────────────
TOTAL:          40 min
Wrap-up:         2 min    (feedback)
```

**Pro Tips**:
- Start Task A immediately (warm up)
- Don't spend >15 min on Task B (move to next task)
- Task C needs window functions (if stuck, use simpler approach)
- Task D is quick (don't over-think)

---

## 📚 Helpful Resources

```bash
# View test expectations
cat tests/test_aggregates.py

# View bug location
grep -n "compute_monthly_revenue" src/silver.py

# Check data quality
pytest tests/test_quality.py -v

# See schema
grep -n "schema" src/schema_utils.py
```

---

## ✅ Checklist Before Starting

```bash
# 1. Verify environment activated
echo $VIRTUAL_ENV  # Should show path to venv

# 2. Verify dependencies installed
pip list | head -10

# 3. Verify tests set up correctly
pytest --collect-only tests/ | head -20

# 4. Verify Jupyter works
jupyter --version

# 5. Verify data files present
ls -lh data/

# 6. Verify source code present
ls -la src/*.py
```

---

## 🎉 After Interview

```bash
# Clean up (optional)
deactivate              # Exit venv
rm -rf htmlcov/         # Remove coverage reports
rm -rf .pytest_cache/   # Remove cache

# Archive results
# Create zip of completed notebooks:
zip -r interview_results.zip notebooks/ src/

# View final result
echo "RESULT: PASS or FAIL (depends on PASS/FAIL per section)"
```

---

## 📞 Quick Help

| Issue | Command |
|-------|---------|
| Unsure what to do | `cat CANDIDATE_README.md` |
| Tests not passing | `pytest tests/test_aggregates.py -v` |
| Data looks wrong | `head -20 data/*.csv` |
| Need to restart | `deactivate && source venv/bin/activate` |
| Forgot PySpark syntax | `grep -n "DataFrame" src/*.py` |

---

**Duration**: 40 minutes | **Result**: PASS/FAIL per section | **Pass Criteria**: All 4 sections must PASS
