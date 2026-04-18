import pandas as pd
import os
from config import OUTPUT_CSV_PATH


FUNNEL_STEPS = [
    "page_view",
    "view_item",
    "add_to_cart",
    "begin_checkout",
    "purchase"
]


def compute_overall_funnel(df: pd.DataFrame) -> pd.DataFrame:
    totals = df[FUNNEL_STEPS].sum()

    funnel = pd.DataFrame({
        "step": FUNNEL_STEPS,
        "users": totals.values
    })

    funnel["conversion_rate"] = funnel["users"] / funnel["users"].iloc[0]
    funnel["drop_off"] = funnel["users"].shift(1) - funnel["users"]
    funnel["drop_off_rate"] = 1 - (funnel["users"] / funnel["users"].shift(1))

    return funnel


def compute_segmented_funnel(df: pd.DataFrame, segment: str) -> pd.DataFrame:
    results = []

    for value, group in df.groupby(segment):
        totals = group[FUNNEL_STEPS].sum()

        temp = pd.DataFrame({
            "segment": value,
            "step": FUNNEL_STEPS,
            "users": totals.values
        })

        results.append(temp)

    return pd.concat(results)


def save_outputs(df: pd.DataFrame, funnel_df: pd.DataFrame, device_df: pd.DataFrame, source_df: pd.DataFrame):
    os.makedirs(OUTPUT_CSV_PATH, exist_ok=True)

    df.to_csv(f"{OUTPUT_CSV_PATH}/raw_events.csv", index=False)
    funnel_df.to_csv(f"{OUTPUT_CSV_PATH}/funnel_overview.csv", index=False)
    device_df.to_csv(f"{OUTPUT_CSV_PATH}/funnel_by_device.csv", index=False)
    source_df.to_csv(f"{OUTPUT_CSV_PATH}/funnel_by_source.csv", index=False)

def main():
    print("=== ANALYSIS MODULE TEST RUN ===")

    # mock test data (so file is runnable independently)
    test_df = pd.DataFrame({
        "page_view": [1, 1, 1, 1],
        "view_item": [1, 1, 0, 1],
        "add_to_cart": [1, 0, 0, 1],
        "begin_checkout": [1, 0, 0, 0],
        "purchase": [1, 0, 0, 0],
        "device": ["mobile", "desktop", "mobile", "desktop"],
        "source": ["google", "direct", "google", "email"]
    })

    print("\n--- COMPUTING OVERALL FUNNEL ---")
    funnel_df = compute_overall_funnel(test_df)
    print(funnel_df)

    print("\n--- COMPUTING DEVICE SEGMENT ---")
    device_df = compute_segmented_funnel(test_df, "device")
    print(device_df)

    print("\n--- COMPUTING SOURCE SEGMENT ---")
    source_df = compute_segmented_funnel(test_df, "source")
    print(source_df)

    print("\n--- SAVING OUTPUTS ---")
    save_outputs(test_df, funnel_df, device_df, source_df)

    print("\n✔ Analysis pipeline completed successfully.")


if __name__ == "__main__":
    main()