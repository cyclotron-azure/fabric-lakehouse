"""
Agentic helper module using Semantic Kernel (Mock Mode).

This module provides AI-powered data quality summarization using
Semantic Kernel stubs. No external API keys required - all responses
are mocked for interview demonstration purposes.
"""

import logging
from typing import List, Dict, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class DataQualitySummary:
    """Summary of data quality analysis."""
    overall_score: float
    critical_issues: List[str]
    warnings: List[str]
    recommendations: List[str]
    ai_summary: str


class MockSemanticKernelAgent:
    """
    Mock Semantic Kernel agent for data quality summarization.
    
    In a production environment, this would connect to Azure OpenAI
    or other LLM services via Semantic Kernel. For this assessment,
    all responses are mocked.
    """
    
    def __init__(self, model: str = "gpt-4", mock_mode: bool = True):
        """
        Initialize the agent.
        
        Args:
            model: Model identifier (mocked)
            mock_mode: Always True for this assessment
        """
        self.model = model
        self.mock_mode = mock_mode
        logger.info(f"Initialized MockSemanticKernelAgent (mock_mode={mock_mode})")
    
    def summarize_quality_report(self, quality_data: Dict) -> DataQualitySummary:
        """
        Generate AI-powered summary of data quality report.
        
        Args:
            quality_data: Dictionary containing quality metrics and issues
            
        Returns:
            DataQualitySummary with AI-generated insights
        """
        logger.info("Generating data quality summary (mocked)...")
        
        # Extract metrics
        table_name = quality_data.get('table_name', 'unknown')
        quality_score = quality_data.get('quality_score', 0.0)
        issues = quality_data.get('issues', [])
        warnings = quality_data.get('warnings', [])
        
        # Mock AI analysis
        critical_issues = []
        warning_list = []
        recommendations = []
        
        # Analyze issues
        for issue in issues:
            issue_type = issue.get('type', '')
            column = issue.get('column', '')
            count = issue.get('count', 0)
            
            if issue_type == 'NULL_VALUES':
                critical_issues.append(f"Missing values in {column} ({count} rows)")
                recommendations.append(f"Implement validation to prevent null {column} values")
            elif issue_type == 'DUPLICATES':
                critical_issues.append(f"Duplicate records found in {column} ({count} instances)")
                recommendations.append(f"Add unique constraint or deduplication logic for {column}")
            elif issue_type == 'INVALID_VALUE':
                warning_list.append(f"Invalid values detected in {column} ({count} rows)")
                recommendations.append(f"Add data validation rules for {column}")
            elif issue_type == 'OUTLIER':
                warning_list.append(f"Statistical outliers in {column} ({count} values)")
                recommendations.append(f"Review and potentially cap extreme values in {column}")
        
        # Generate AI summary (mocked)
        if quality_score >= 90:
            summary = f"✅ The {table_name} dataset demonstrates excellent data quality with a score of {quality_score:.1f}%. "
            summary += "Minor issues detected are typical of production data and can be addressed through standard cleaning procedures."
        elif quality_score >= 70:
            summary = f"⚠️ The {table_name} dataset has acceptable data quality ({quality_score:.1f}%) but requires attention. "
            summary += f"Identified {len(critical_issues)} critical issues and {len(warning_list)} warnings that should be addressed "
            summary += "before using this data for analytics or machine learning."
        else:
            summary = f"❌ The {table_name} dataset has significant quality issues (score: {quality_score:.1f}%). "
            summary += "Immediate data cleansing and validation procedures are recommended before downstream use."
        
        # Add specific issue context
        if critical_issues:
            summary += f" Critical concerns include: {', '.join(critical_issues[:2])}."
        
        # Add recommendations context
        if recommendations:
            summary += f" Priority actions: {recommendations[0]}"
        
        return DataQualitySummary(
            overall_score=quality_score,
            critical_issues=critical_issues,
            warnings=warning_list,
            recommendations=recommendations,
            ai_summary=summary
        )
    
    def suggest_cleaning_strategy(self, issues: List[Dict]) -> str:
        """
        Suggest data cleaning strategy based on identified issues.
        
        Args:
            issues: List of data quality issues
            
        Returns:
            AI-generated cleaning strategy (mocked)
        """
        logger.info("Generating cleaning strategy (mocked)...")
        
        strategy = "🤖 AI-Recommended Data Cleaning Strategy:\\n\\n"
        
        # Group issues by type
        issue_types = {}
        for issue in issues:
            itype = issue.get('type', 'UNKNOWN')
            if itype not in issue_types:
                issue_types[itype] = []
            issue_types[itype].append(issue)
        
        # Generate strategies
        step = 1
        
        if 'NULL_VALUES' in issue_types:
            strategy += f"{step}. Handle Missing Values:\\n"
            for issue in issue_types['NULL_VALUES']:
                col = issue.get('column', 'unknown')
                strategy += f"   - Filter out rows with missing {col} if it's a critical field\\n"
                strategy += f"   - Or impute using domain-appropriate defaults\\n"
            step += 1
        
        if 'DUPLICATES' in issue_types:
            strategy += f"{step}. Deduplicate Records:\\n"
            strategy += "   - Use dropDuplicates() to keep first occurrence\\n"
            strategy += "   - Consider business rules for selecting 'best' duplicate\\n"
            step += 1
        
        if 'INVALID_VALUE' in issue_types:
            strategy += f"{step}. Remove Invalid Values:\\n"
            for issue in issue_types['INVALID_VALUE']:
                col = issue.get('column', 'unknown')
                strategy += f"   - Filter {col} to exclude negative, zero, or out-of-range values\\n"
            step += 1
        
        if 'OUTLIER' in issue_types:
            strategy += f"{step}. Handle Outliers:\\n"
            strategy += "   - Review outliers manually to determine if they're errors or valid\\n"
            strategy += "   - Consider capping at percentile thresholds (95th/99th)\\n"
            step += 1
        
        strategy += f"{step}. Validate and Test:\\n"
        strategy += "   - Re-run quality checks after cleaning\\n"
        strategy += "   - Compare before/after metrics\\n"
        strategy += "   - Document any data transformations applied\\n"
        
        return strategy
    
    def explain_medallion_architecture(self, layer: str) -> str:
        """
        Provide AI explanation of medallion architecture layer.
        
        Args:
            layer: Layer name (bronze, silver, gold)
            
        Returns:
            AI-generated explanation (mocked)
        """
        explanations = {
            'bronze': """
🥉 Bronze Layer (Raw/Landing Zone):
The Bronze layer serves as the initial landing zone for raw data ingested from source systems.
Key characteristics:
- Preserves data in its original format with minimal transformation
- Adds metadata columns for lineage tracking (ingestion timestamp, source file)
- Provides historical record of all data received
- Enables data recovery and replay capabilities
- Schema-on-read approach for flexibility
            """,
            'silver': """
🥈 Silver Layer (Cleaned/Curated):
The Silver layer contains validated, cleaned, and conformed data ready for analysis.
Key characteristics:
- Data quality rules applied (null handling, deduplication)
- Schema standardization and type conversions
- Business logic implementation (calculations, derived fields)
- Data enrichment through joins
- Serves as the foundation for downstream analytics
            """,
            'gold': """
🥇 Gold Layer (Analytics/Aggregated):
The Gold layer provides business-ready, aggregated datasets optimized for analytics.
Key characteristics:
- Pre-calculated KPIs and metrics
- Denormalized for query performance
- Optimized for specific use cases (reporting, ML, dashboards)
- May include feature engineering for ML models
- Designed for end-user consumption in BI tools
            """
        }
        
        return explanations.get(layer.lower(), "Unknown layer")


# Convenience function
def create_quality_agent() -> MockSemanticKernelAgent:
    """Create a data quality agent instance."""
    return MockSemanticKernelAgent(mock_mode=True)
