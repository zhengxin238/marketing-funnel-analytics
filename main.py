import os

from data_quality import (
    detect_tracking_issues,
    repair_tracking_data,
    summarize_data_issues,
    generate_quality_report_text
)

from ai.insight_engine import (
    generate_funnel_insights,
    generate_executive_summary,
    explain_anomalies
)

from queries import (
    get_funnel_overview_query,
    get_funnel_over_time_query,
    get_funnel_by_device_query,
    get_funnel_by_source_query,
    get_conversion_rate_query,
    get_cohort_retention_query,
    get_user_level_funnel_query
)

from data_loader import load_bigquery_data


# =========================
# CONFIG
# =========================
OUTPUT_PATH = "outputs/csv"
DOCS_PATH = "outputs/docs"


# =========================
# HELPERS
# =========================
def save_df(df, filename):
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    path = os.path.join(OUTPUT_PATH, filename)
    df.to_csv(path, index=False)
    print(f"✔ Saved: {path}")


def save_text(content: str, filename: str):
    os.makedirs(DOCS_PATH, exist_ok=True)
    path = os.path.join(DOCS_PATH, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✔ Saved report: {path}")


# =========================
# MAIN PIPELINE
# =========================
def main():
    print("\n🚀 RUNNING FULL GA4 FUNNEL ANALYTICS PIPELINE\n")

    try:
        # =========================
        # 1. LOAD DATA
        # =========================
        print("📊 Loading datasets from BigQuery...")

        df_overview = load_bigquery_data(get_funnel_overview_query())
        df_time_raw = load_bigquery_data(get_funnel_over_time_query())
        df_device = load_bigquery_data(get_funnel_by_device_query())
        df_source = load_bigquery_data(get_funnel_by_source_query())
        df_conversion = load_bigquery_data(get_conversion_rate_query())
        df_cohort = load_bigquery_data(get_cohort_retention_query())
        df_user = load_bigquery_data(get_user_level_funnel_query())

        # =========================
        # 2. DATA QUALITY + REPAIR
        # =========================
        print("🧪 Running data quality checks...")

        df_time_checked = detect_tracking_issues(df_time_raw)

        print("🛠 Repairing tracking issues...")
        df_time_clean = repair_tracking_data(df_time_checked)

        # Summary outputs
        df_quality = summarize_data_issues(df_time_clean)
        quality_text = generate_quality_report_text(df_time_clean)

        # Save quality outputs
        save_df(df_quality, "data_quality_report.csv")
        save_text(quality_text, "data_quality_report.md")

        # =========================
        # 3. SAVE CORE OUTPUTS
        # =========================
        print("💾 Saving processed datasets...")

        # Save BOTH raw and cleaned (important for credibility)
        save_df(df_time_raw, "funnel_over_time_raw.csv")
        save_df(df_time_clean, "funnel_over_time_clean.csv")

        save_df(df_overview, "funnel_overview.csv")
        save_df(df_device, "funnel_by_device.csv")
        save_df(df_source, "funnel_by_source.csv")
        save_df(df_conversion, "conversion_rate.csv")
        save_df(df_cohort, "cohort_retention.csv")
        save_df(df_user, "user_funnel.csv")

        # =========================
        # 4. AI INSIGHTS (USE CLEAN DATA)
        # =========================
        print("🧠 Generating AI insights...")

        funnel_insights = generate_funnel_insights(df_overview)
        exec_summary = generate_executive_summary(df_overview, df_conversion)

        # IMPORTANT: use CLEAN data here
        anomaly_report = explain_anomalies(df_time_clean)

        save_text(funnel_insights, "funnel_insights.md")
        save_text(exec_summary, "executive_summary.md")
        save_text(anomaly_report, "anomaly_report.md")

        # =========================
        # FINAL STATUS
        # =========================
        print("\n==============================")
        print("✔ PIPELINE COMPLETED SUCCESSFULLY")
        print("==============================\n")

        print("📁 CSV Outputs:")
        print("- funnel_overview.csv")
        print("- funnel_over_time_raw.csv")
        print("- funnel_over_time_clean.csv")
        print("- funnel_by_device.csv")
        print("- funnel_by_source.csv")
        print("- conversion_rate.csv")
        print("- cohort_retention.csv")
        print("- user_funnel.csv")
        print("- data_quality_report.csv")

        print("\n📄 Reports:")
        print("- funnel_insights.md")
        print("- executive_summary.md")
        print("- anomaly_report.md")
        print("- data_quality_report.md")

    except Exception as e:
        print("\n❌ PIPELINE FAILED")
        print("===================")
        print(str(e))


# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()