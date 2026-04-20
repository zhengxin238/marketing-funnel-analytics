# ai/insight_engine.py

import os
from ai.ai_client import get_ai_client

OUTPUT_PATH = "outputs/reports"

# IMPORTANT: This is the model that worked in your test!
MODEL_NAME = "gemini-flash-latest"

def save_report(text: str, filename: str):
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    path = os.path.join(OUTPUT_PATH, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"🧠 AI Report saved: {path}")

# =========================
# FUNNEL INSIGHTS (UPGRADED)
# =========================
def generate_funnel_insights(funnel_df):
    client = get_ai_client()

    prompt = f"""
You are a senior data analyst.

Your goal is NOT to describe the data.
Your goal is to provide business-impact-driven insights.

Rules:
- Identify biggest drop-offs in the funnel
- Quantify impact (percentages, scale)
- Explain WHY users drop off
- Highlight risks for the business
- Provide actionable recommendations
- Be concise and professional

Funnel Data:
{funnel_df.to_string(index=False)}

Output structure:
1. Key Drop-Off Points
2. Insights (Why this happens)
3. Business Impact
4. Recommendations
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    result = response.text

    save_report(result, "funnel_insights.txt")
    print(result)

    return result


# =========================
# EXECUTIVE SUMMARY (UPGRADED)
# =========================
def generate_executive_summary(funnel_df, conversion_df):
    client = get_ai_client()

    prompt = f"""
You are preparing a report for business stakeholders.

Write a concise executive summary.

Rules:
- Focus on business impact (NOT technical details)
- Highlight key performance metrics
- Mention conversion rate clearly
- Identify biggest risk/opportunity
- Keep it short (5–8 sentences max)

Funnel Data:
{funnel_df.to_string(index=False)}

Conversion Data:
{conversion_df.to_string(index=False)}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    result = response.text

    save_report(result, "executive_summary.txt")
    print(result)

    return result


# =========================
# ANOMALY ANALYSIS (STRONG VERSION)
# =========================
def explain_anomalies(time_df):
    client = get_ai_client()

    prompt = f"""
You are a senior data analyst specializing in data quality and anomaly detection.

Your task:
Identify anomalies AND explain their business impact.

Rules:
- Classify anomalies:
  • Technical (tracking issues)
  • Behavioral (user trends)
- Flag impossible patterns (e.g. purchases > add_to_cart)
- Detect tracking failures (e.g. zero values)
- Quantify how much of the dataset is affected
- Warn if data is unreliable
- Suggest how to fix or handle the issue

Data Sample:
{time_df.head(30).to_string(index=False)}

Output structure:
1. Critical Issues (data reliability)
2. Secondary Anomalies
3. Valid Trends
4. Business Impact
5. Recommendations
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    result = response.text

    save_report(result, "anomaly_report.txt")
    print(result)

    return result
