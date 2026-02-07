# SkyGenI Task - Data Sciene and Applied AI Engineer

---

## How to Read This Submission

- Part 1 frames the business problem
- Part 2 explores the data and extracts validated insights
- Part 3 converts insights into a decision engine
- Part 4 shows how this could be productized
- Part 5 reflects on limitations and next steps

---

## Part 1 – Problem Framing

### 1. What is the real business problem?

The core business problem is not a lack of pipeline volume, but a decline in the conversion of pipeline into revenue. While a healthy number of deals are being created, a growing proportion of these deals are being lost, indicating potential issues with deal quality, sales execution, targeting, or process efficiency rather than top-of-funnel lead generation.

---

### 2. What key questions should an AI system answer for the CRO?

An AI-driven sales intelligence system should help the CRO understand where and why win rate is declining by answering questions such as:
- Which segments (industry, region, product type, sales representative, or lead source) are experiencing the largest drops in win rate?
- What deal characteristics are most strongly associated with losses?
- Which open deals are currently at the highest risk of being lost?
- What actions or interventions are most likely to improve revenue outcomes?

---

### 3. What metrics matter most for diagnosing win rate issues?

The most important metrics include win rate segmented by industry, region, product type, lead source, and sales representative, as well as average deal size, sales cycle length, stage-to-stage conversion rates, and loss concentration across reps or segments. These metrics help identify whether declining win rates are driven by deal quality, sales execution, or specific operational bottlenecks.

---

### 4. What assumptions are being made about the data or business?

This analysis assumes that deal outcomes, dates, and stages are accurately and consistently recorded in the CRM, and that historical performance patterns reasonably reflect current sales behavior. It also assumes there were no major external disruptions—such as pricing changes, product launches, or market shifts—during the period covered by the data.

---

## Part 2 – Data Exploration & Business Insights

### Overview

Exploratory data analysis (EDA) was conducted using Python to understand deal behavior, sales performance, and factors contributing to declining win rates.  
All analysis, visualizations, and detailed commentary are available in the Jupyter notebook:  
`analysis.ipynb`.

The focus of this analysis was not on surface-level metrics, but on identifying **patterns that explain why deals are being won or lost** and translating those patterns into **actionable business insights**.

---

### Key Business Insights

**1. Sales Cycle Length Is a Strong Early Warning Signal**  
Deals with longer sales cycles are significantly more likely to be lost, while shorter cycles correlate with higher win probability.  
**Action:** Flag and escalate deals that exceed a healthy sales cycle threshold.

**2. Funnel Losses Are Concentrated at Specific Sales Stages**  
Certain deal stages show consistently higher losses than wins, indicating funnel bottlenecks rather than random failures.  
**Action:** Improve qualification, messaging, and enablement at high-loss stages.

**3. Lost Deals Remain Open Longer Before Closure**  
Lost deals tend to stay in the pipeline much longer before closing compared to won deals, inflating pipeline size and reducing forecast accuracy.  
**Action:** Enforce pipeline hygiene rules to re-qualify or close stale deals.

**4. Win and Loss Volumes Change Over Time**  
Monthly trends reveal periods where losses increase faster than wins, validating concerns about declining win rates.  
**Action:** Investigate operational or strategic changes during decline periods and adjust sales strategy accordingly.

---

### Deliverables

- 📊 **Detailed EDA & Visualizations:** `analysis.ipynb`  
- 🧠 **Business Interpretations:** Embedded alongside each analysis in the notebook  
- 🎯 **Actionable Outcomes:** Used as inputs for the Decision Engine in Part 3

---

## Part 3 – Decision Engine: Deal Risk Scoring

The Decision Engine directly operationalizes the insights identified in Part 2, particularly sales cycle duration, deal aging, and funnel-stage risk.


### Overview

In this section, a **Deal Risk Scoring Decision Engine** is built to help sales leaders identify which deals are most likely to be lost and therefore require immediate attention.  

The goal of this engine is **not prediction accuracy**, but **decision support**.  
It uses simple, interpretable business rules derived from earlier insights to prioritize deals that show warning signs.

This directly addresses the CRO’s concern:

> “Pipeline volume looks healthy, but win rate is dropping. I don’t know where to focus.”

---

### Problem Definition

Sales leaders lack visibility into **which deals are at risk** and **why**.  
Without this visibility, attention is spread evenly across all deals, leading to missed intervention opportunities on high-risk, high-impact deals.

**Objective:**  
Create a system that scores each deal based on risk factors and produces a ranked list of deals that require action.

---

### Modeling Approach

A **rule-based scoring system** was chosen instead of a machine learning model because:

- Business users need **explainability**
- Data is limited to historical deal attributes
- The goal is **action**, not probabilistic accuracy

Each deal is scored using a weighted combination of intuitive risk signals.

---

### Risk Signals Used

| Risk Signal | Description | Why It Matters |
|------------|-------------|----------------|
| Sales Cycle Risk | Normalized deal duration | Longer deals are more likely to be lost |
| Deal Stagnation Risk | Deal duration above median | Stale deals indicate low buyer intent |
| Stage Risk | Historical loss rate at current stage | Some funnel stages leak more than others |

---

### Risk Score Formula

Deal Risk Score =  
0.4 × Sales Cycle Risk  
+ 0.3 × Deal Stagnation Risk  
+ 0.3 × Stage Risk


All components are normalized between **0 and 1**, making the score easy to interpret.

---

### Setup Instructions

#### Prerequisites

- Python 3.8+

#### Steps for Installation:

1) **Creating the virtual environment**:
```bash
python -m venv venv
```

2) **Activating the virtual environment**:
```bash
venv\Scripts\activate
```

3) **Installing dependencies**:
```bash
python -m pip install -r requirements.txt
```

4) **Run the script**:
```bash
python decision_engine.py
```

### Instructions to Run the script

1) **Default Usage (Daily Review)**:
```bash
deal_risk_engine(df)
```
Returns the top 10 highest-risk deals using default assumptions.

2) **Adjusting Risk Assumptions (Interactive Use)**:

- Example: Emphasize long-running deals
```bash
deal_risk_engine(
    df,
    cycle_weight=0.6,
    stagnation_weight=0.2,
    stage_weight=0.2
)
```

- Example: Aggressive pipeline hygiene
```bash
deal_risk_engine(
    df,
    stagnation_threshold=30,
    top_n=15
)
```

### Output Description

The engine returns a ranked table with the following fields:

| Column | Description |
|--------|-------------|
| deal_id |	Unique deal identifier |
| deal_stage | Current sales stage |
| sales_cycle_days | Duration of the deal |
| deal_amount |	Revenue at stake |
| deal_risk_score |	Composite risk score (0–1) |

Higher scores indicate higher priority for intervention.

---

### How a Sales Leader Would Use This

**Daily**:
Review the top-risk deals and assign managers or specialists to intervene.

- **Weekly pipeline reviews**:
Focus discussion on why deals are risky instead of pipeline size.

- **Strategic planning**:
Adjust sales process, stage definitions, or escalation rules based on recurring risk patterns.

---

### Business Value

- Improves win rate without increasing pipeline volume
- Focuses leadership attention where it matters most
- Fully explainable and easy to trust
- Suitable for productization as a sales intelligence feature

---

### Summary

This Deal Risk Scoring engine demonstrates how simple, interpretable decision systems can create immediate business value. By translating sales behavior into actionable signals, the system helps leaders move from reactive reporting to proactive revenue management.

---

## Part 4 – Mini System Design: Sales Insight & Alert System

### Overview

This section outlines a lightweight **Sales Insight & Alert System** designed to operationalize the insights and decision engine built earlier.  
The goal is to move from *analysis* to *action* by continuously monitoring sales data and proactively alerting sales leaders about risks, bottlenecks, and performance changes.

The system is intentionally simple, explainable, and suitable for early-stage productization at SkyGeni.

---

### High-Level Architecture

┌─────────────────────────────┐
│   CRM Systems               │
│   (Salesforce / HubSpot)    │
└───────────────┬─────────────┘
                │
                │  Daily Sync
                ▼
┌─────────────────────────────┐
│   Data Ingestion Layer      │
│   (ETL / Validation)        │
└───────────────┬─────────────┘
                │
                ▼
┌─────────────────────────────┐
│   Analytics &               │
│   Decision Engine           │
│   - Insights                │
│   - Risk Scoring            │
└───────────────┬─────────────┘
                │
                ▼
┌─────────────────────────────┐
│   Insights Store            │
│   (Metrics & Scores)        │
└───────────────┬─────────────┘
                │
                ▼
┌─────────────────────────────┐
│   Alerts & Dashboards       │
│   (Slack / Email / Web UI)  │
└─────────────────────────────┘

*System Explanation*:
Sales data is ingested daily from CRM systems, processed by an analytics and decision engine to generate insights and risk scores, and then stored and surfaced through dashboards and proactive alerts to support timely sales leadership decisions.

---

### Data Flow

1. **Data Ingestion**
   - Pull deal data from CRM systems (deal_id, dates, stage, amount, outcome, etc.).
   - Runs on a scheduled basis (e.g., nightly batch job).

2. **Data Processing**
   - Clean and normalize fields (dates, outcomes, stages).
   - Compute derived metrics such as sales cycle duration and deal aging.

3. **Insight Generation**
   - Apply analytical logic (e.g., sales cycle thresholds, stage-level loss rates).
   - Generate time-based trends (monthly wins vs losses).

4. **Decision Engine Execution**
   - Run the Deal Risk Scoring engine.
   - Rank deals based on composite risk signals.

5. **Insight & Alert Delivery**
   - Store results for dashboards.
   - Trigger alerts when predefined conditions are met.

---

### Example Alerts & Insights

**Deal-Level Alerts**
- “⚠️ Deal `D-1023` has exceeded the healthy sales cycle threshold and is at high risk.”
- “🚨 High-value deal stuck in a high-loss stage for 20+ days.”

**Pipeline & Funnel Insights**
- “📉 Losses have increased significantly at the ‘Proposal’ stage this week.”
- “🧹 18% of pipeline deals are stale and unlikely to close based on historical patterns.”

**Trend-Based Alerts**
- “📊 Monthly win rate dropped by 12% compared to last month.”
- “📈 Loss volume has exceeded wins for two consecutive weeks.”

---

### Execution Frequency

| Component | Frequency |
|---------|----------|
| Data ingestion | Daily |
| Risk scoring engine | Daily |
| Trend analysis | Weekly |
| Executive summaries | Monthly |
| Alerts | Near real-time or daily |

This balance ensures **timely action** without overwhelming users with noise.

---

### How Sales Leaders Use the System

- **Daily Standups**
  - Review top high-risk deals.
  - Assign intervention actions.

- **Weekly Pipeline Reviews**
  - Focus discussions on risk drivers and bottlenecks.
  - Identify stages or behaviors needing improvement.

- **Monthly Strategy Reviews**
  - Analyze performance trends.
  - Adjust sales strategy, quotas, or enablement efforts.

---

### Failure Cases & Limitations

**Data Quality Issues**
- Inconsistent stage definitions across reps.
- Missing or incorrect dates affecting sales cycle calculations.

**Limited Context**
- No visibility into call activity, emails, or meeting data.
- Does not account for pricing changes or competitive pressure.

**False Positives**
- Some long-running deals may still close successfully.
- Risk scores should guide attention, not replace judgment.

**Model Simplicity**
- Rule-based logic may not capture all edge cases.
- Requires periodic review and recalibration.

---

### Why This Design Works for SkyGeni

- Lightweight and easy to implement
- Fully explainable to business users
- Focused on decision-making, not raw prediction
- Naturally extensible to ML models and richer signals later

---

### Future Enhancements

- Incorporate activity data (calls, emails, meetings).
- Add industry- or rep-specific risk baselines.
- Introduce adaptive thresholds based on historical performance.
- Integrate feedback loops from sales leader actions.

---

### Summary

This Sales Insight & Alert System demonstrates how SkyGeni could productize data-driven decision intelligence. By combining simple analytics, explainable risk scoring, and proactive alerts, the system helps sales leaders focus on the right deals at the right time to improve revenue outcomes.

---

## Part 5 – Reflection

### What assumptions in your solution are weakest?

The weakest assumptions are related to data completeness and consistency. The solution assumes that deal stages are applied consistently across sales representatives and that deal dates accurately reflect real sales activity. In practice, CRM data often contains inconsistencies, delayed updates, or subjective stage definitions, which could impact the accuracy of risk signals derived from sales cycle length and stage-level loss rates.

---

### What would break in real-world production?

The system would be sensitive to poor data quality and changing sales behavior. If reps delay updating deal stages or outcomes, risk scores may become stale or misleading. Additionally, major changes such as new pricing models, product launches, or shifts in target markets could invalidate historical patterns, requiring recalibration of thresholds and risk weights.

---

### What would you build next if given one month?

With additional time, the next priority would be to incorporate **activity-level data**, such as emails, calls, meetings, and response times. These signals would significantly improve deal risk detection by capturing buyer engagement directly. I would also introduce feedback loops that learn from sales leader interventions to continuously improve alert relevance and reduce false positives.

---

### What part of your solution are you least confident about?

The stage-level risk component is the area of least confidence, as it depends heavily on how consistently stages are used across the organization. Without standardized stage definitions and enforcement, stage-based loss rates may reflect process variance rather than true deal risk. This component would require ongoing validation and close collaboration with sales operations teams.
