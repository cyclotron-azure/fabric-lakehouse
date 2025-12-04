# 📋 Medallion Architecture Assessment - Interviewer Guide

**Duration**: 40 minutes  
**Focus**: Medallion Architecture (Bronze/Silver/Gold)  
**Difficulty**: Intermediate-Advanced  

---

## 🎯 Assessment Timeline (40 min)

```
Introduction & Setup        2 min
├─ Welcome, explain 4 tasks, share screen
├─ Candidate clones repo and sets up environment
└─ Verify tests run (expect 10 pass, 4 fail)

Task A: Bronze Ingestion  10 min
├─ Candidate reads CSVs, adds metadata, writes Delta
├─ Observe: speed, understanding of schema
└─ Score: Did they complete end-to-end?

Task B: Debug Bugs        12 min
├─ Candidate identifies 2 bugs in silver.py
├─ Candidate fixes both issues
├─ Candidate verifies tests pass
└─ Observe: debugging methodology, attention to detail

Task C: Feature           12 min
├─ Candidate implements repeat_customer_rate metric
├─ Uses window functions correctly
├─ Writes to Delta table
└─ Observe: SQL/PySpark proficiency, design thinking

Task D: Governance         6 min
├─ Candidate writes 5 bullets on Purview PII classification
├─ Connects to medallion architecture
└─ Observe: Governance understanding, completeness

Wrap-up & Discussion       2 min
├─ Code review (optional)
├─ Discuss approach and tradeoffs
└─ Next steps / feedback
```

---

## 📊 Pass/Fail Evaluation Framework

### Task A: Bronze Layer Ingestion (10 min)

**PASS Criteria**:
- ✅ Reads both CSV files (customers.csv, orders.csv) correctly
- ✅ Adds all 3 metadata columns (ingestion_timestamp, source_file, bronze_layer_id)
- ✅ Writes clean Delta tables with correct schema
- ✅ Shows understanding of Bronze layer purpose (raw data with lineage)
- ✅ Code runs without errors

**FAIL Criteria**:
- ❌ Missing one or more CSV files
- ❌ Missing metadata columns
- ❌ Delta tables not created or have schema errors
- ❌ Fundamental misunderstanding of Bronze layer
- ❌ Code doesn't run

---

### Task B: Silver Layer - Debug Bugs (12 min)

**PASS Criteria**:
- ✅ Identifies BOTH bugs correctly:
  1. Case-sensitive status filter (misses "Complete", "COMPLETE")
  2. Revenue calculation ignores quantity
- ✅ Implements correct fixes in `src/silver.py`
- ✅ ALL 4 aggregate tests pass after fixes
- ✅ Explains root cause of each bug
- ✅ Shows systematic debugging approach (doesn't guess randomly)

**FAIL Criteria**:
- ❌ Only finds one bug or both found but not fixed correctly
- ❌ Tests still fail after "fix"
- ❌ Modifies test files instead of source code
- ❌ Cannot explain why each bug existed
- ❌ Uses random trial-and-error without understanding

---

### Task C: Gold Layer - Add Feature (12 min)

**PASS Criteria**:
- ✅ Implements repeat_customer_rate metric correctly
- ✅ Uses window functions properly (Window.partitionBy, row_number/rank)
- ✅ Correctly groups by month
- ✅ Writes results to Delta table
- ✅ Code is clean, readable, with comments
- ✅ All pytest tests pass

**FAIL Criteria**:
- ❌ Feature incomplete or doesn't run
- ❌ Window functions not used or incorrect syntax
- ❌ Calculation logic is wrong (off-by-one, wrong grouping, etc.)
- ❌ Tests fail
- ❌ Code is messy/hard to understand

---

### Task D: Governance - PII & Purview (6 min)

**PASS Criteria**:
- ✅ Writes 5 complete, substantive bullets
- ✅ Demonstrates Purview PII classification understanding
  - Email/phone identified as "Restricted" PII
  - Specific Purview features mentioned
- ✅ Explains lineage tracking (Bronze → Silver → Gold)
- ✅ Addresses access controls and audit trails
- ✅ Professional language, specific to enterprise governance

**FAIL Criteria**:
- ❌ Fewer than 5 bullets or incomplete response
- ❌ Generic governance concepts (not Purview-specific)
- ❌ No connection to medallion architecture
- ❌ Vague, incorrect, or off-topic information
- ❌ Shows no governance knowledge

---

### Overall Assessment

| Result | Criteria |
|--------|----------|
| **PASS** | All 4 tasks (A, B, C, D) achieve PASS |
| **FAIL** | 1 or more tasks achieve FAIL |

---

## 🎓 What You're Assessing

### Technical Competencies
1. **PySpark Proficiency**: Can they manipulate DataFrames efficiently?
2. **Debugging Skills**: How systematic is their approach to finding/fixing bugs?
3. **SQL/Window Functions**: Do they understand advanced analytics?
4. **Delta Lake Knowledge**: Can they work with ACID tables?
5. **Data Quality**: How do they think about validation?

### Professional Competencies
1. **Problem-Solving**: Do they ask clarifying questions?
2. **Communication**: Can they explain their approach?
3. **Attention to Detail**: Did they notice the case-sensitivity issue?
4. **Governance Mindset**: Do they think about PII, lineage, compliance?
5. **Time Management**: Did they pace themselves in 40 min?

---

## 🔍 What to Watch For

### Green Flags ✅
- **Systematic debugging**: Candidate reads error messages, checks data
- **Asks questions**: "Should I handle null values here?"
- **Tests incrementally**: Runs tests after each change
- **Explains approach**: "I'm normalizing status because..."
- **Handles edge cases**: Mentions nulls, duplicates, case sensitivity
- **Clean code**: Variable names, comments, no magic numbers
- **Time awareness**: "I have 5 min left, let me focus on governance"

### Red Flags 🚩
- **Guessing without testing**: Just changes code randomly
- **Silent for 5+ min**: No verbal communication
- **Modifies test files**: Tries to "fix" tests instead of code
- **Ignores error messages**: Just reruns same code
- **Copy-paste from docs**: No understanding of what they're doing
- **Complains about dataset**: "This data is bad" vs "How should I clean this?"
- **Doesn't review their work**: Ships with obvious bugs

---

## 💬 Interview Questions & Answer Guide

### Task A: Bronze Ingestion

**Q1: Why add metadata columns like ingestion_timestamp?**

✅ **Expected Answer**:
- Lineage tracking (when was this ingested?)
- Data quality auditing (replay from specific timestamp)
- SLA monitoring (did we ingest on time?)
- Compliance (audit trail for governance)

⚠️ **Acceptable**:
- "It's good practice to track when data came in"

❌ **Poor**:
- "The task asked me to"
- "I don't know, just added it"

**Q2: Why Delta tables instead of Parquet?**

✅ **Expected Answer**:
- ACID transactions (no partial writes)
- Schema enforcement (catch errors early)
- Time travel (recover old versions)
- Easier updates/deletes

⚠️ **Acceptable**:
- "Delta Lake is better for data lakes"

❌ **Poor**:
- "Both are the same"

---

### Task B: Debugging

**Q1: How did you identify the case-sensitivity bug?**

✅ **Expected Answer**:
- Looked at actual vs expected data
- Noticed some months missing revenue
- Checked status values in CSV (saw "Complete" vs "complete")
- Tested filter logic with different cases

⚠️ **Acceptable**:
- "I looked at the test failure and realized it needed case-insensitive matching"

❌ **Poor**:
- "I just tried different things until tests passed"

**Q2: Why is the aggregation `SUM(quantity * price)` instead of `SUM(price)`?**

✅ **Expected Answer**:
- Revenue = units sold × price per unit
- Just summing price ignores quantities
- E.g., 2 units at $10 = $20 revenue, not $10
- Misses the business logic

⚠️ **Acceptable**:
- "The test expected that calculation"

❌ **Poor**:
- "I don't know why"

---

### Task C: Feature Implementation

**Q1: Why use window functions for repeat_customer_rate?**

✅ **Expected Answer**:
- Need to compare customers across months (window partitions)
- Want to rank/count within each month group
- Window functions allow "row_number() OVER (PARTITION BY month)"
- More efficient than self-joins

⚠️ **Acceptable**:
- "Window functions are good for this kind of metric"

❌ **Poor**:
- "I wasn't sure, just tried it"
- "Don't know what window functions do"

**Q2: How do you define "repeat customer"?**

✅ **Expected Answer**:
- Customer appears in 2+ different months
- Or: `rank() OVER (ORDER BY month DESC) > 1` per customer
- Must be same customer_id across months

⚠️ **Acceptable**:
- "Someone who ordered more than once"

❌ **Poor**:
- Vague definition or incorrect logic

---

### Task D: Governance

**Q1: What PII is in the customers table?**

✅ **Expected Answer**:
- email (contact info)
- phone (contact info)
- name (can be PII in some regulations)
- signup_date (potentially de-anonymizing)

⚠️ **Acceptable**:
- email and phone

❌ **Poor**:
- "I'm not sure" or listing non-PII

**Q2: How would Purview help with data access control?**

✅ **Expected Answer**:
- Classify data (standard vs restricted)
- Tag columns with sensitivity level
- Integrate with Azure AD for access control
- Audit who accesses restricted data
- Block access based on classification

⚠️ **Acceptable**:
- "Purview tracks who accesses what"

❌ **Poor**:
- "I don't know what Purview does"

---

## 🐛 Expected Bug Fixes

### Bug #1: Case-Sensitive Status
**Location**: `src/silver.py`, line ~22
```python
# ❌ BUGGY:
.filter(F.col("status") == "complete")

# ✅ FIXED:
.filter(F.lower(F.col("status")) == "complete")
```

### Bug #2: Wrong Aggregation
**Location**: `src/silver.py`, line ~25
```python
# ❌ BUGGY:
.agg(F.sum("price").alias("revenue"))

# ✅ FIXED:
.withColumn("line_revenue", F.col("quantity") * F.col("price"))
.agg(F.sum("line_revenue").alias("revenue"))
```

---

## ✨ Task C Implementation Guide

### Expected Approach
```python
# 1. Add month column
df = orders_df.withColumn("month", F.trunc(F.col("order_date"), "month"))

# 2. Get distinct customers per month
customers_per_month = df.select("month", "customer_id").distinct()

# 3. Count repeat customers (2+ months)
window = Window.partitionBy("customer_id").orderBy("month")
repeat_customers = customers_per_month.withColumn(
    "month_rank", F.row_number().over(window)
).filter(F.col("month_rank") > 1)

# 4. Calculate repeat rate
repeat_count = repeat_customers.select("month", "customer_id").distinct().count()
total_count = customers_per_month.select("month", "customer_id").distinct().count()

repeat_rate = repeat_count / total_count
```

### Common Mistakes (Red Flags)
- ❌ No window function, just manual grouping
- ❌ Counting total rows, not distinct customers
- ❌ Not grouping by month (gives overall repeat rate)
- ❌ Including same month twice (customers in month 1+1 aren't repeat customers)

---

## 🎬 Interview Execution

### Before Interview (24h)
- [ ] Review candidate resume/background
- [ ] Test all notebooks locally (ensure they work)
- [ ] Verify tests run: `pytest tests/ -v`
- [ ] Prepare scoring sheet (print or digital)
- [ ] Test screen sharing setup
- [ ] Prepare 2-3 backup questions

### During Interview (40 min)

**First 2 min (Welcome)**:
- Introduce yourself and role
- Explain 4 tasks and 40-min timeline
- Share screen with candidate
- Confirm they can see and are ready

**Task A (10 min)**:
- Say: "Start with Bronze ingestion notebook"
- Watch: Do they understand CSV → Delta flow?
- Note: Speed, questions asked, understanding of schema
- Don't interrupt unless stuck for 2+ min

**Task B (12 min)**:
- Say: "Next, debug the silver.py module"
- Watch: Do they methodically find both bugs?
- Note: Debugging approach, test-driven mindset
- Ask: "Can you explain why that's a bug?"

**Task C (12 min)**:
- Say: "Implement repeat_customer_rate in Gold layer"
- Watch: Do they know window functions?
- Note: SQL/PySpark proficiency, design thinking
- Ask: "Why use window functions?"

**Task D (6 min)**:
- Say: "Write 5 bullets on Purview PII classification"
- Watch: Do they understand governance?
- Note: Completeness, Purview knowledge
- Don't rush (they need time to think)

**Wrap-up (2 min)**:
- Ask: "Any questions for me?"
- Say: "Thank you, we'll be in touch"
- Mention next steps

### After Interview (ASAP)
- [ ] Complete scoring (PASS/FAIL per section)
- [ ] Mark final result (PASS = all sections PASS; FAIL = any section FAIL)
- [ ] Write brief notes on strengths/gaps
- [ ] Flag any red flags or concerns
- [ ] Review decision with hiring team

---

## 📈 Performance Benchmarks

### Typical Time Breakdown
- **Task A**: 8-12 min (most candidates fast here)
- **Task B**: 12-18 min (debugging takes time)
- **Task C**: 10-15 min (window functions tricky)
- **Task D**: 4-8 min (quick bullets)

### Expected Results Distribution

Most assessments fall into one of these outcomes:
- **PASS (all 4 sections)**: ~20% (strong candidates with solid Medallion Architecture understanding)
- **FAIL (1+ sections)**: ~80% (gaps in one or more Medallion tiers or governance)

**Key**: It's harder to score PASS than expected - all 4 sections must meet the criteria.

---

## 🛑 Common Issues & Fixes

### Issue: Candidate Can't Find Bugs
**Action**:
1. Ask: "What does the test expect vs what you're getting?"
2. Hint: "Look at the status values in the data"
3. Last resort: "One is about status filtering, one is about calculation"

### Issue: Candidate Uses Wrong Window Syntax
**Action**:
1. Ask: "What does PARTITION BY do?"
2. Hint: "Try comparing customers across months"
3. Don't give exact code, guide to solution

### Issue: Candidate Finishes Early
**Action**:
1. Ask: "Can you add comments to explain the logic?"
2. Ask: "What edge cases could break this?"
3. Ask: "How would you optimize this for 1B rows?"

### Issue: Candidate Runs Out of Time
**Action**:
1. For Task C: "Do your best in remaining time"
2. For Task D: "Just outline the 5 bullets"
3. Assess PASS/FAIL for each section based on what they completed

---

## 📝 Scoring Sheet

```
CANDIDATE: ___________________
DATE: ___________________
INTERVIEWER: ___________________

Task A: Bronze Ingestion        ☐ PASS  ☐ FAIL
Task B: Silver - Debug Bugs     ☐ PASS  ☐ FAIL
Task C: Gold - Feature          ☐ PASS  ☐ FAIL
Task D: Governance              ☐ PASS  ☐ FAIL
─────────────────────────────────────────────
OVERALL RESULT:                 ☐ PASS  ☐ FAIL

(PASS = all 4 sections PASS; FAIL = any section FAIL)

STRENGTHS:
_________________________________
_________________________________

GAPS/AREAS FOR IMPROVEMENT:
_________________________________
_________________________________

OVERALL ASSESSMENT:
_________________________________
_________________________________

RECOMMENDATION:  ☐ HIRE (PASS)  ☐ PASS (with reservations)  ☐ REJECT (FAIL)
```

---

## 🎓 Post-Interview Discussion

### For PASS Candidates
### For PASS Candidates
- "Congratulations, you passed all 4 sections!"
- "Your strong areas: [mention specific tasks]"
- "Area to potentially develop: [mention if any section was close]"
- "Next step: Technical interview with the team"

### For FAIL Candidates
- "Thank you for your time"
- "While you completed [tasks], we were looking for PASS on all 4 sections"
- "Consider practice on: [mention failed section]"
- "Feel free to reapply after additional practice"

---

**This is a comprehensive assessment designed to fairly evaluate Azure Fabric and data engineering fundamentals in 40 minutes. Good luck with your interviews!**
