import os
from queries import (
    get_funnel_overview_query,
    get_funnel_over_time_query,
    get_funnel_by_device_query,
    get_funnel_by_source_query,
    get_conversion_rate_query,
    get_cohort_retention_rate_query
)
from data_loader import load_bigquery_data


OUTPUT_PATH = "outputs/csv"


def save_df(df, filename):
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    path = os.path.join(OUTPUT_PATH, filename)
    df.to_csv(path, index=False)
    print(f"Saved: {path}")


def main():
    print("=== RUNNING FULL FUNNEL ANALYTICS PIPELINE ===")

    try:
        # 1. Funnel overview
        df_overview = load_bigquery_data(get_funnel_overview_query())
        save_df(df_overview, "funnel_overview.csv")

        # 2. Funnel over time
        df_time = load_bigquery_data(get_funnel_over_time_query())
        save_df(df_time, "funnel_over_time.csv")

        # 3. Device segmentation
        df_device = load_bigquery_data(get_funnel_by_device_query())
        save_df(df_device, "funnel_by_device.csv")

        # 4. Source segmentation
        df_source = load_bigquery_data(get_funnel_by_source_query())
        save_df(df_source, "funnel_by_source.csv")

        # 5. Conversion rate
        df_conversion = load_bigquery_data(get_conversion_rate_query())
        save_df(df_conversion, "conversion_rate.csv")

        # 6. Cohort retention
        df_cohort = load_bigquery_data(get_cohort_retention_rate_query())
        save_df(df_cohort, "cohort_retention.csv")

        print("=== PIPELINE COMPLETED SUCCESSFULLY ===")

    except Exception as e:
        print("❌ ERROR OCCURRED:")
        print(e)


if __name__ == "__main__":
    main()