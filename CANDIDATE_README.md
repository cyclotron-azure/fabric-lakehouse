# 📚 Azure Fabric Lakehouse Medallion Architecture - Candidate Guide

**Duration**: 40 minutes  
**Tasks**: 4 hands-on Medallion challenges (Bronze → Silver → Gold)  
**Setup**: 3 minutes  

---

## 🚀 Quick Setup (3 min)

### Option 1: Local Environment (Recommended)
```bash
git clone <repo-url>
cd inteview
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pytest tests/ -v  # Verify installation (expect 10 pass, 4 fail)
jupyter lab       # Start notebooks
```

### Option 2: VS Code Dev Container
1. Install [Docker](https://docker.com) and [VS Code](https://code.visualstudio.com)
2. Install [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
3. Clone repo → Open in VS Code → Ctrl+Shift+P → "Reopen in Container"
4. Automatic setup (wait 2 min)

### Option 3: GitHub Codespaces
1. Open repo on GitHub
2. Click **Code** → **Codespaces** → **Create codespace on main**
3. Auto-setup (2 min) → Ready to code

---

## 📋 Medallion Architecture Tasks (40 min total)

### ✅ Task A: Bronze Layer Ingestion (10 min)
**File**: `notebooks/01_Bronze_Ingest.ipynb`

1. **Open notebook** in Jupyter
2. **Read CSV files** from `data/` folder
3. **Add metadata columns**:
   - `ingestion_timestamp` (current date/time)
   - `source_file` (filename)
   - `bronze_layer_id` (UUID or row index)
4. **Write to Delta tables** in `Tables/bronze/customers` and `Tables/bronze/orders`
5. **Verify**: Display row counts and schema

**Success Criteria**:
- ✅ Both CSV files loaded
- ✅ All metadata columns added
- ✅ Delta tables created with correct schema
- ✅ No errors in execution

---

### 🐛 Task B: Silver Layer - Debug Data Quality Bugs (12 min)
**File**: `notebooks/02_Silver_Transform.ipynb` + `src/silver.py`

**Problem**: Monthly revenue calculation is **broken**.

1. **Run notebook** to see incorrect results
2. **Identify bugs** (hint: check `src/silver.py` line ~16-30)
3. **Find both issues**:
   - **Bug #1**: Status filter is case-sensitive
   - **Bug #2**: Revenue calculation is wrong
4. **Fix code** in `src/silver.py`
5. **Verify fixes**: Run tests
   ```bash
   pytest tests/test_aggregates.py -v
   ```
   All 4 tests should **PASS**

**Hints**:
- Look at test failure messages carefully
- Check how the data looks (status values, revenue calculation)
- The bugs are in the `compute_monthly_revenue()` function

**Success Criteria**:
- ✅ Both bugs identified correctly
- ✅ Fixes implemented in `src/silver.py`
- ✅ All 4 aggregate tests pass
- ✅ Explanation of root cause

---

### ⭐ Task C: Gold Layer - Add Feature (12 min)
**File**: `notebooks/03_Gold_Aggregates.ipynb`

**Challenge**: Implement **repeat customer rate** metric.

1. **Locate Task C section** in notebook (search for "Task C")
2. **Add SQL/PySpark code** that:
   - Identifies repeat customers (purchased 2+ months)
   - Calculates repeat rate: `repeat_customers / total_customers` per month
   - Uses **window functions** correctly
   - Writes results to Delta table
3. **Test your implementation**:
   ```bash
   pytest tests/ -v  # Full suite should pass
   ```

**Hints**:
- Use `Window.partitionBy("month")` to compare customers across months
- Use `row_number()` or `rank()` to identify repeats
- Formula: `repeat_rate = count_distinct_repeat_customers / count_distinct_all_customers`

**Success Criteria**:
- ✅ Metric calculated correctly
- ✅ Window function used properly
- ✅ Results written to Delta
- ✅ Test suite passes
- ✅ Code is readable with comments

---

### 📝 Task D: Data Governance (6 min)
**File**: `docs/GOVERNANCE.md`

**Challenge**: Complete governance documentation.

1. **Open** `docs/GOVERNANCE.md`
2. **Locate Task D section** (search for "Task D")
3. **Write 5 bullets** explaining how Microsoft Purview would:
   - Classify PII in customer email/phone columns
   - Track data lineage through Bronze → Silver → Gold
   - Enable access controls for sensitive data
   - Audit data access for compliance
   - Implement retention policies

4. **Example format**:
   ```
   - **PII Classification**: Purview scans email/phone → Tags as "Restricted"
   - **Lineage Tracking**: Captures metadata → Shows data flow across layers
   - ... (3 more bullets)
   ```

**Success Criteria**:
- ✅ 5 bullets completed
- ✅ Shows understanding of Purview capabilities
- ✅ Connects to Bronze/Silver/Gold architecture
- ✅ Addresses compliance concerns
- ✅ Professional language

---

## 🎯 Evaluation Rubric

| Task | Duration | Result | Criteria |
|------|----------|--------|----------|
| **A: Bronze** | 10 min | PASS/FAIL | Both CSVs loaded → Metadata added → Delta tables created |
| **B: Silver** | 12 min | PASS/FAIL | Both bugs found → Fixes implemented → All tests pass |
| **C: Gold** | 12 min | PASS/FAIL | Metric implemented correctly → Window functions used → Tests pass |
| **D: Governance** | 6 min | PASS/FAIL | 5 bullets written → Purview understanding shown → Clear connections |

### Pass/Fail Criteria

#### Task A: PASS
- ✅ Reads both customers.csv and orders.csv
- ✅ Adds ingestion_timestamp, source_file, bronze_layer_id columns
- ✅ Writes to Delta tables (Tables/bronze/customers, Tables/bronze/orders)
- ✅ Schema is correct with proper data types

#### Task A: FAIL
- ❌ Missing one or more CSV files
- ❌ Missing metadata columns
- ❌ Delta tables not created or have errors
- ❌ Fundamental misunderstanding of Bronze layer

#### Task B: PASS
- ✅ Both bugs identified correctly (case-sensitive filter + wrong aggregation)
- ✅ Fixes implemented in src/silver.py
- ✅ ALL 4 aggregate tests pass
- ✅ Explains why each bug existed

#### Task B: FAIL
- ❌ Only one bug found or both bugs not fixed correctly
- ❌ Tests still fail after "fix"
- ❌ Modified test files instead of source code
- ❌ Cannot explain root cause

#### Task C: PASS
- ✅ Repeat customer rate metric implemented
- ✅ Window functions used correctly (Window.partitionBy, row_number/rank)
- ✅ Correctly groups by month
- ✅ Writes results to Delta table
- ✅ Code is clean with comments
- ✅ All tests pass

#### Task C: FAIL
- ❌ Feature incomplete or doesn't run
- ❌ Window functions not used or incorrect syntax
- ❌ Calculation logic is wrong
- ❌ Tests fail
- ❌ Hard to understand code

#### Task D: PASS
- ✅ Writes 5 complete bullets
- ✅ Shows understanding of Purview PII classification
- ✅ Explains lineage tracking (Bronze → Silver → Gold)
- ✅ Addresses access controls and audit trails
- ✅ Professional, specific language

#### Task D: FAIL
- ❌ Fewer than 5 bullets or incomplete
- ❌ Generic governance concepts (not Purview-specific)
- ❌ No connection to medallion architecture
- ❌ Vague or incorrect information

### Overall Result

| Outcome | Criteria |
|---------|----------|
| **PASS** | All 4 tasks (A, B, C, D) = PASS |
| **FAIL** | 1 or more tasks = FAIL |

---

## 🔍 Data You'll Work With

### customers.csv (30 rows)
| Column | Notes |
|--------|-------|
| `customer_id` | Some null values |
| `name` | Includes duplicates (C025 appears 2x) |
| `email` | Some missing |
| `phone` | Some missing |
| `signup_date` | Some missing |

**Quality Issues**: 5 duplicates/nulls/missing values (expected)

### orders.csv (36 rows)
| Column | Notes |
|--------|-------|
| `order_id` | Unique identifier |
| `customer_id` | Some foreign key mismatches |
| `order_date` | One future date |
| `status` | ⚠️ **MIXED-CASE**: complete, Complete, COMPLETE |
| `quantity` | Some zero/negative (invalid) |
| `price` | Some zero/negative (invalid) |

**Quality Issues**: 8+ data quality problems (for you to handle in Task B)

---

## 💡 Architecture Overview (Read before tasks)

### Medallion Architecture
```
Data Lake Layers:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  BRONZE          SILVER          GOLD
  ↓               ↓               ↓
Raw CSVs    →    Cleaned      →  Aggregated
              Normalized         Metrics
              Validated
```

### Layer Purposes
- **Bronze**: Raw data copy with lineage metadata
- **Silver**: Cleaned, deduplicated, quality-validated data
- **Gold**: Business metrics, dashboards, reports ready

### Technologies
- **PySpark**: Distributed data processing
- **Delta Lake**: ACID transactions, time travel, schema enforcement
- **Jupyter**: Interactive code development

---

## 🛠️ Useful Commands

```bash
# Run all tests
pytest tests/ -v

# Run only aggregate tests (Task B)
pytest tests/test_aggregates.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Check specific test details
pytest tests/test_aggregates.py::test_compute_monthly_revenue_uses_qty_times_price -v

# Start Jupyter
jupyter lab

# Install new package (if needed)
pip install <package-name>

# View Delta table schema
# (In Jupyter notebook)
spark.read.format("delta").load("Tables/bronze/customers").printSchema()
```

---

## ⚠️ Common Mistakes to Avoid

### Task B (Debugging)
- ❌ Only fix one bug (there are TWO)
- ❌ Modify test files (don't do this!)
- ❌ Forget to handle both uppercase/lowercase status values
- ❌ Calculate revenue without considering quantity

### Task C (Feature)
- ❌ Use window functions incorrectly (check partitionBy/orderBy)
- ❌ Forget to group by month
- ❌ Hardcode values instead of calculating dynamically
- ❌ Leave code without comments

### Task D (Governance)
- ❌ Write generic text (be specific to Purview)
- ❌ Only mention one feature
- ❌ Forget to connect to Medallion architecture
- ❌ Use non-technical language

---

## 🎓 Learning Objectives

After completing this interview, you'll have demonstrated:

### Technical Skills
✅ PySpark DataFrame operations (filter, groupBy, window functions)  
✅ Delta Lake table creation and management  
✅ Python debugging and root cause analysis  
✅ SQL-like aggregations in PySpark  
✅ Data quality validation patterns  

### Data Engineering Knowledge
✅ Medallion architecture (Bronze/Silver/Gold)  
✅ Data lineage and governance  
✅ PII identification and classification  
✅ Incremental data processing  
✅ Enterprise data platform design  

### Azure Fabric / Lakehouse
✅ Fabric workspace and Lakehouse concepts  
✅ Notebook-based development  
✅ Delta Lake in Azure Fabric  
✅ Metadata and lineage tracking  

---

## ❓ FAQ

**Q: Can I use Google/Documentation?**  
A: Yes! Real-world developers use docs. Focus on problem-solving.

**Q: What if I get stuck?**  
A: Ask your interviewer for clarification, not the answer.

**Q: Can I modify test files?**  
A: No. Fix only `src/silver.py` and implement Task C in the notebook.

**Q: How long should this take?**  
A: 40 minutes total. Tasks are sized accordingly.

**Q: What if I finish early?**  
A: Review your code for clarity, add comments, optimize if possible.

**Q: Can I use ChatGPT?**  
A: No. This is a take-home where we assess YOUR skills.

---

## 📞 Support

### During Interview
- Ask interviewer for clarification if tasks are unclear
- Show your thought process (debugging, design decisions)
- Discuss tradeoffs (performance vs readability, etc.)

### Before Interview
- Read this document thoroughly
- Set up environment locally first
- Review ARCHITECTURE.md for context
- Test commands: `pytest tests/ -v`

### Repository Structure
```
├── README.md                    # Overview (you are here)
├── CANDIDATE_README.md          # Task descriptions (you are reading this)
├── INTERVIEWER_GUIDE.md         # For interviewer only
├── data/                        # Sample CSVs
├── notebooks/                   # Your Jupyter files
├── src/                         # Python modules (Task B fixes go here)
├── tests/                       # Pytest suite
└── docs/                        # GOVERNANCE.md (Task D goes here)
```

---

## 🎯 Time Management

```
Setup:          3 min  (pip install, verify)
Task A:        10 min  (Bronze ingestion)
Task B:        12 min  (Debug + fix bugs)
Task C:        12 min  (Implement feature)
Task D:         6 min  (Governance bullets)
─────────────────────
TOTAL:         40 min
```

**Pro Tips**:
- Start with Task A immediately (warm up)
- Task B is trickiest (2 bugs to find)
- Task C needs window functions (practice first)
- Task D is quick (just 5 bullets)

---

## ✅ Before You Start

- [ ] Environment set up (venv activated)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Tests verified (`pytest tests/ -v` shows 10 pass, 4 fail)
- [ ] Jupyter running (`jupyter lab`)
- [ ] Read this document
- [ ] Reviewed ARCHITECTURE.md
- [ ] Timer ready (40 min)

**Ready? Let's go! 🚀**

---

**Questions? Ask your interviewer. Good luck!** 🎉
