# 📚 Azure Fabric Lakehouse Medallion Architecture

**Hands-on project demonstrating Bronze → Silver → Gold data pipeline patterns**

---

## 🎯 Quick Navigation

### Getting Started 👈

**[CANDIDATE_README.md](CANDIDATE_README.md)**

- ✅ 3-minute setup instructions
- ✅ 4 hands-on tasks
- ✅ Exercise guidelines
- ✅ Common mistakes to avoid

### Architecture Deep Dive

**[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**

- Bronze → Silver → Gold medallion pattern
- Delta Lake and PySpark integration
- Data flow diagrams and best practices

### Governance Framework

**[docs/GOVERNANCE.md](docs/GOVERNANCE.md)**

- Data classification matrix
- PII inventory and compliance
- Purview integration (Task D placeholder)

---

## 📋 Project Overview

| Skill | Task | Estimated Time |
|-------|------|----------------|
| **Ingestion** | Bronze CSV → Delta | 10 min |
| **Debugging** | Find & fix 2 bugs | 12 min |
| **Analytics** | Window functions | 12 min |
| **Governance** | PII + Purview | 6 min |
| **Overall** | All sections | **40 min** |

---

## 🚀 Quick Start

```bash
# 1. Clone repository
git clone https://github.com/cyclotron-azure/fabric-lakehouse.git
cd fabric-lakehouse

# 2. Setup environment (3 min)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Verify installation
pytest tests/ -v  # Expect: 10 pass, 4 fail

# 4. Read instructions
cat CANDIDATE_README.md

# 5. Open Jupyter
jupyter lab
```

---

## 📂 Repository Structure

```
inteview/
├── README.md                          # Overview (you are here)
├── CANDIDATE_README.md                # Task instructions
├── requirements.txt                   # Python dependencies
├── pytest.ini                         # Test configuration
├── .gitignore                         # Python/Spark exclusions
│
├── data/                              # Sample CSVs
│   ├── customers.csv                  # 30 rows with quality issues
│   └── orders.csv                     # 36 rows (mixed-case status)
│
├── notebooks/                         # Jupyter notebooks
│   ├── 01_Bronze_Ingest.ipynb         # Task A - CSV ingestion
│   ├── 02_Silver_Transform.ipynb      # Task B - Bug fixing
│   └── 03_Gold_Aggregates.ipynb       # Task C - Feature implementation
│
├── src/                               # Python modules
│   ├── __init__.py
│   ├── schema_utils.py                # Schema validation
│   ├── quality_checks.py              # Data quality framework
│   ├── logging_utils.py               # Logging helpers
│   ├── silver.py                      # 🐛 BUGGY - for Task B
│   └── agent_helper.py                # Mock Semantic Kernel agent
│
├── tests/                             # Pytest test suite
│   ├── conftest.py
│   ├── __init__.py
│   ├── test_schema.py                 # 4 tests (all pass)
│   ├── test_quality.py                # 7 tests (all pass)
│   └── test_aggregates.py             # 4 tests (FAIL until Task B fixed)
│
├── docs/                              # Documentation
│   ├── ARCHITECTURE.md                # Medallion pattern guide
│   └── GOVERNANCE.md                  # Data governance framework
│
└── .devcontainer/                     # VS Code dev container
    └── devcontainer.json
```

---

## ⏱️ Suggested Timeline (40 minutes)

```
┌─────────────────────────────────────────────────────────┐
│                   PROJECT TIMELINE                       │
├─────────────────────────────────────────────────────────┤
│ Task A: Bronze Ingestion 10 min                         │
│   → Read CSV, add metadata, write Delta                 │
├─────────────────────────────────────────────────────────┤
│ Task B: Debug Bugs       12 min                         │
│   → Find 2 bugs in silver.py, fix them                  │
├─────────────────────────────────────────────────────────┤
│ Task C: Feature          12 min                         │
│   → Implement repeat_customer_rate metric               │
├─────────────────────────────────────────────────────────┤
│ Task D: Governance        6 min                         │
│   → Write 5 bullets on Purview PII classification       │
├─────────────────────────────────────────────────────────┤
│ TOTAL: 40 minutes                                       │
└─────────────────────────────────────────────────────────┘
```

---

## 🎓 Technical Stack

- **PySpark 3.5.0** - Distributed data processing
- **Delta Lake** - ACID transactions, schema enforcement
- **Pandas 2.1.4** - Data manipulation
- **Pytest 7.4.3** - Testing framework
- **Semantic Kernel 0.9.0** - Mock mode (no API keys)
- **Jupyter Lab** - Interactive notebooks
- **Python 3.11+** - Runtime

---

## 🧪 Data Overview

### customers.csv (30 rows)

- Quality issues: 1 duplicate, 5 missing values
- PII: email, phone, name

### orders.csv (36 rows)

- Quality issues: mixed-case status ("complete", "Complete", "COMPLETE")
- Negative quantities/prices
- Invalid dates

**Note**: These issues are intentional for Task B debugging

---

## ✨ Task C Challenge

Implement `repeat_customer_rate` metric:

- Identify customers who ordered in 2+ different months
- Calculate: repeat_customers / total_customers per month
- Use window functions (Window.partitionBy, row_number)
- Write results to Delta table

---



## 🎬 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Before Task B: Expect 10 pass, 4 fail
# After Task B: Expect 14 pass, 0 fail

# Run specific test file
pytest tests/test_aggregates.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

---



## 📖 Documentation

1. **CANDIDATE_README.md** - Start here! Tasks, setup, FAQ
2. **ARCHITECTURE.md** - Understand Bronze/Silver/Gold
3. **GOVERNANCE.md** - Learn PII classification

---

## 🚀 Setup Options

### Option 1: Local Environment (Recommended)

```bash
git clone https://github.com/cyclotron-azure/fabric-lakehouse.git
cd inteview
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v  # Verify
jupyter lab       # Start
```

### Option 2: VS Code Dev Container

1. Install Docker + Dev Containers extension
2. Open repo in VS Code
3. Ctrl+Shift+P → "Reopen in Container"
4. Auto-setup (2 min)

### Option 3: GitHub Codespaces

1. Open repo on GitHub
2. Click **Code** → **Codespaces** → Create
3. Auto-setup (2 min)

---

## 🤔 FAQ

**Q: Can candidates use documentation?**  
A: Yes! Real developers use docs. We assess problem-solving, not memory.

**Q: What if they get stuck?**  
A: Interviewers can provide hints (see INTERVIEWER_GUIDE.md).

**Q: How long does this take to set up?**  
A: 3 minutes (pip install -r requirements.txt).

**Q: Can I customize the tasks?**  
A: Absolutely! Modify notebooks, data, or requirements as needed.

**Q: Is this tested on Windows/Mac?**  
A: Yes. All notebooks and code are cross-platform.

---

## 📧 Next Steps

1. Clone repository
2. Read CANDIDATE_README.md
3. Set up environment
4. Review ARCHITECTURE.md
5. Run `pytest tests/ -v` to verify
6. Complete the 4 tasks

---

## ✅ Quality Assurance

- ✅ 15 pytest test cases
- ✅ 2 intentional bugs for Task B
- ✅ 3 Jupyter notebooks (Bronze → Silver → Gold)
- ✅ 6 Python modules with full documentation
- ✅ Cross-platform compatible (Windows/Mac/Linux)
- ✅ No external API keys required
- ✅ Runs completely offline

---

## 🎉 Ready to Start?

Read **CANDIDATE_README.md** for detailed task instructions.

Good luck! 🚀

---

**Estimated Duration**: 40 minutes  
**Project**: Azure Fabric Lakehouse Medallion Architecture (Bronze → Silver → Gold)
