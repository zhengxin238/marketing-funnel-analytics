import os
import pandas as pd

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


# =========================
# SAVE FUNCTION
# =========================
def save_df(df, filename):
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    path = os.path.join(OUTPUT_PATH, filename)
    df.to_csv(path, index=False)
    print(f"✔ Saved: {path}")


# =========================
# MAIN PIPELINE
# =========================
def main():
    print("\n🚀 RUNNING FULL GA4 FUNNEL ANALYTICS PIPELINE\n")

    try:
        # =========================
        # 1. FUNNEL OVERVIEW
        # =========================
        print("📊 Loading funnel overview...")
        df_overview = load_bigquery_data(get_funnel_overview_query())
        save_df(df_overview, "funnel_overview.csv")

        # =========================
        # 2. FUNNEL OVER TIME
        # =========================
        print("📈 Loading funnel over time...")
        df_time = load_bigquery_data(get_funnel_over_time_query())
        save_df(df_time, "funnel_over_time.csv")

        # =========================
        # 3. DEVICE ANALYSIS
        # =========================
        print("📱 Loading device segmentation...")
        df_device = load_bigquery_data(get_funnel_by_device_query())
        save_df(df_device, "funnel_by_device.csv")

        # =========================
        # 4. SOURCE ANALYSIS
        # =========================
        print("🌐 Loading source segmentation...")
        df_source = load_bigquery_data(get_funnel_by_source_query())
        save_df(df_source, "funnel_by_source.csv")

        # =========================
        # 5. CONVERSION RATE
        # =========================
        print("💰 Loading conversion rate...")
        df_conversion = load_bigquery_data(get_conversion_rate_query())
        save_df(df_conversion, "conversion_rate.csv")

        # =========================
        # 6. COHORT RETENTION
        # =========================
        print("👥 Loading cohort retention...")
        df_cohort = load_bigquery_data(get_cohort_retention_query())
        save_df(df_cohort, "cohort_retention.csv")


        # =========================
        # 7. USER LEVEL FUNNEL
        # =========================
        print("👥 Loading user level funnel...")
        df_userlevelfunnel = load_bigquery_data(get_user_level_funnel_query())
        save_df(df_userlevelfunnel, "user_funnel.csv")



        # =========================
        # FINAL STATUS
        # =========================
        print("\n==============================")
        print("✔ PIPELINE COMPLETED SUCCESSFULLY")
        print("==============================\n")

        print("Generated outputs:")
        print("- funnel_overview.csv")
        print("- funnel_over_time.csv")
        print("- funnel_by_device.csv")
        print("- funnel_by_source.csv")
        print("- conversion_rate.csv")
        print("- cohort_retention.csv")
        print("- user_funnel.csv")

    except Exception as e:
        print("\n❌ PIPELINE FAILED")
        print("===================")
        print(str(e))


# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()