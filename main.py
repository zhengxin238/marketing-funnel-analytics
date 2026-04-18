from queries import get_funnel_query
from data_loader import load_bigquery_data
from analysis import (
    compute_overall_funnel,
    compute_segmented_funnel,
    save_outputs
)
from visualization import plot_overall_funnel


def main():
    print("=== SENIOR FUNNEL ANALYTICS PIPELINE ===")

    query = get_funnel_query()
    df = load_bigquery_data(query)

    print(f"Loaded dataset: {df.shape}")

    # overall funnel
    funnel_df = compute_overall_funnel(df)

    # segmentation (this is what recruiters LOVE)
    device_df = compute_segmented_funnel(df, "device")
    source_df = compute_segmented_funnel(df, "source")

    save_outputs(df, funnel_df, device_df, source_df)

    print("\n=== FUNNEL OVERVIEW ===")
    print(funnel_df)

    plot_overall_funnel(funnel_df)


if __name__ == "__main__":
    main()