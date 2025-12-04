# Data Governance Framework

## Overview

This document outlines data governance practices for the Retail Lakehouse project, including data quality, privacy, security, and compliance considerations.

---

## Data Quality Standards

### Quality Dimensions

1. **Completeness**: All required fields populated
2. **Accuracy**: Data reflects real-world values
3. **Consistency**: Data format uniform across sources
4. **Timeliness**: Data available when needed
5. **Validity**: Data conforms to business rules
6. **Uniqueness**: No unintended duplicates

### Quality Metrics (This Project)

| Table | Quality Score Target | Critical Fields |
|-------|---------------------|-----------------|
| Bronze/Customers | 70%+ | customer_id, name, email |
| Bronze/Orders | 65%+ | order_id, customer_id, order_date |
| Silver/Customers | 95%+ | customer_id, name, email |
| Silver/Orders | 90%+ | order_id, customer_id, status |

### Implementation

Quality checks are implemented in `src/quality_checks.py`:

```python
from src.quality_checks import check_data_quality

report = check_data_quality(
    df, 
    table_name="customers",
    required_columns=["customer_id", "name", "email"]
)

print(f"Quality Score: {report.quality_score}%")
for issue in report.issues:
    print(f"- {issue['type']}: {issue['column']} ({issue['count']} rows)")
```

---

## Data Classification

### Classification Levels

| Level | Description | Examples | Access Control |
|-------|-------------|----------|----------------|
| **Public** | Non-sensitive business data | Product SKUs, categories | All users |
| **Internal** | Business-sensitive data | Revenue, customer counts | Employees only |
| **Confidential** | Sensitive business data | Customer names, locations | Need-to-know basis |
| **Restricted** | PII and regulated data | Email, phone, payment info | Strict access controls |

### Data Inventory (This Project)

#### Customers Table

| Column | Classification | Data Type | PII |
|--------|---------------|-----------|-----|
| customer_id | Internal | string | No |
| name | Confidential | string | Yes |
| email | **Restricted** | string | **Yes (PII)** |
| phone | **Restricted** | string | **Yes (PII)** |
| signup_date | Internal | date | No |

#### Orders Table

| Column | Classification | Data Type | PII |
|--------|---------------|-----------|-----|
| order_id | Internal | string | No |
| customer_id | Confidential | string | No (indirect) |
| order_date | Internal | date | No |
| status | Internal | string | No |
| quantity | Internal | int | No |
| price | Internal | double | No |

---

## PII Classification with Microsoft Purview

### 🎯 TASK D: Complete This Section

**Instructions**: Write 5 bullet points explaining how you would use Microsoft Purview to scan and classify PII in this Lakehouse.

#### Your Response (5 bullets):

1. ___TODO: Your answer here___

2. ___TODO: Your answer here___

3. ___TODO: Your answer here___

4. ___TODO: Your answer here___

5. ___TODO: Your answer here___

---

### Example Purview Classification Strategy

For reference, a complete Purview strategy includes:

#### 1. Scan Configuration
- Register Fabric Lakehouse as a data source in Purview
- Create scan rule set to identify Delta tables
- Schedule regular scans (daily for Bronze, weekly for Silver/Gold)

#### 2. Classification Rules
- Apply built-in classifiers:
  - **Email Address**: `email` column → Automatic detection via regex
  - **Phone Number**: `phone` column → Pattern matching
  - **Person Name**: `name` column → NLP-based detection
- Create custom classifiers for domain-specific PII (customer_id patterns)

#### 3. Sensitivity Labels
- Apply Microsoft Information Protection labels:
  - `General`: order_date, status, quantity
  - `Confidential`: customer_id, name
  - `Highly Confidential`: email, phone
- Labels propagate to downstream Power BI reports

#### 4. Access Controls
- Implement Azure RBAC based on sensitivity:
  - **Data Reader**: View General and Confidential
  - **PII Viewer**: View Highly Confidential (requires approval)
  - **Data Steward**: Manage classifications
- Enable row-level security (RLS) for multi-tenant scenarios

#### 5. Compliance Monitoring
- Track data lineage: Source CSV → Bronze → Silver → Gold → Power BI
- Generate compliance reports for audits (GDPR, CCPA)
- Set up alerts for PII access anomalies

---

## Data Retention Policy

### Retention Schedule

| Layer | Retention Period | Rationale |
|-------|------------------|-----------|
| **Bronze** | 7 years | Legal compliance, audit trail |
| **Silver** | 3 years | Analytics, ML training data |
| **Gold** | 1 year active, 2 years archive | Reporting, historical analysis |

### Implementation

```python
# Vacuum old data (Delta Lake time travel)
spark.sql(f"""
    VACUUM delta.`Tables/bronze/orders`
    RETAIN 168 HOURS  -- 7 days
""")
```

**Note**: Consult legal/compliance before implementing deletion.

---

## Data Access Controls

### Role-Based Access Control (RBAC)

| Role | Bronze | Silver | Gold | Notebooks |
|------|--------|--------|------|-----------|
| **Data Engineer** | Read/Write | Read/Write | Read/Write | Execute |
| **Data Analyst** | Read | Read | Read | Execute |
| **Data Scientist** | Read | Read/Write | Read | Execute |
| **Business User** | - | - | Read | - |

### Implementation in Fabric

```python
# Grant permissions (example - requires Fabric admin)
# fabric.workspace.grant_permission(
#     workspace_id="<workspace-id>",
#     principal="data-analysts@company.com",
#     role="Reader"
# )
```

---

## Privacy Considerations

### GDPR Compliance

**Right to Erasure (Article 17)**:
- Implement customer data deletion workflow
- Use Delta Lake `DELETE` for hard removal
- Maintain deletion audit log

```python
# Delete customer data
spark.sql(f"""
    DELETE FROM delta.`Tables/silver/customers`
    WHERE customer_id = 'C001'
""")

# Propagate to downstream tables
spark.sql(f"""
    DELETE FROM delta.`Tables/silver/orders`
    WHERE customer_id = 'C001'
""")
```

**Right to Access (Article 15)**:
- Provide customer data export functionality
- Generate PDF report of all stored customer data

### CCPA Compliance (California Consumer Privacy Act)

- **Opt-out mechanism**: Track and honor "Do Not Sell" preferences
- **Data inventory**: Maintain catalog of all PII collected
- **Disclosure**: Provide transparency on data usage

---

## Data Lineage

### Tracking Lineage

**Tools**:
- Microsoft Purview for automated lineage capture
- Delta Lake transaction log for change tracking
- Metadata tables for manual lineage documentation

**Example Lineage**:
```
customers.csv 
  → Bronze/customers (ingestion_timestamp: 2025-12-04 10:00)
  → Silver/customers (cleaned, deduplicated)
  → Gold/customer_metrics (aggregated)
  → Power BI Dashboard (visualized)
```

### Implementation

```python
# Add lineage metadata
enriched_df = enriched_df \
    .withColumn("source_layer", F.lit("silver")) \
    .withColumn("transformation_date", F.current_timestamp()) \
    .withColumn("pipeline_version", F.lit("v1.2.0"))
```

---

## Data Security

### Encryption

**At Rest**:
- Azure Storage encryption enabled by default
- Customer-managed keys (CMK) for sensitive data (optional)

**In Transit**:
- TLS 1.2+ for all data transfers
- HTTPS endpoints for API access

### Network Security

- Private endpoints for Fabric workspace
- Firewall rules to restrict access by IP
- Virtual Network (VNet) integration for enterprise

---

## Incident Response

### Data Breach Protocol

1. **Detect**: Monitor Purview alerts for unusual access patterns
2. **Contain**: Revoke compromised credentials immediately
3. **Assess**: Determine scope of PII exposure
4. **Notify**: Inform affected customers within 72 hours (GDPR requirement)
5. **Remediate**: Patch vulnerabilities, rotate keys
6. **Document**: Maintain incident log for audit

### Contact

- **Data Protection Officer**: dpo@company.com
- **Security Operations Center (SOC)**: soc@company.com

---

## Metadata Management

### Business Glossary

| Term | Definition | Owner |
|------|------------|-------|
| **Customer** | Individual or organization making purchases | Product Team |
| **Order** | Transaction record of purchased items | Sales Team |
| **Repeat Customer** | Customer with 2+ orders | Analytics Team |
| **Churn** | Customer inactive for 90+ days | Marketing Team |

### Data Catalog

Maintain catalog in Purview with:
- Table descriptions
- Column-level documentation
- Sample queries
- Owner and steward assignments

---

## Compliance Checklist

### Pre-Production

- [ ] Data classification completed for all tables
- [ ] PII identified and labeled
- [ ] Access controls configured
- [ ] Encryption enabled (at rest and in transit)
- [ ] Retention policy documented
- [ ] Data lineage mapped
- [ ] Privacy policy updated

### Ongoing

- [ ] Quarterly Purview scans
- [ ] Annual data access audits
- [ ] Retention policy enforcement
- [ ] Security patch management
- [ ] Incident response drills

---

## Monitoring and Auditing

### Audit Logging

Track all data access and modifications:

```python
# Example: Log data access
logger.info(f"User {user_id} accessed table {table_name} at {timestamp}")
```

**Required Audit Fields**:
- User ID
- Action (read, write, delete)
- Table/column accessed
- Timestamp
- IP address

### Compliance Dashboards

**Metrics to Track**:
- PII access frequency by user
- Data quality scores over time
- Retention policy violations
- Failed access attempts
- Data deletion requests (GDPR)

---

## References

- [Microsoft Purview Documentation](https://learn.microsoft.com/purview/)
- [GDPR Compliance Guide](https://gdpr.eu/)
- [CCPA Overview](https://oag.ca.gov/privacy/ccpa)
- [Delta Lake Security](https://docs.delta.io/latest/delta-security.html)
- [Azure Fabric Governance](https://learn.microsoft.com/fabric/governance/)

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-04 | Medallion Architecture | Initial version |

---

**Note**: This is for interview assessment purposes. Adapt to your organization's specific compliance and governance requirements.
