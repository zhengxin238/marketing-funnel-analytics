import pandas as pd
import matplotlib.pyplot as plt
import os
from config import OUTPUT_PLOT_PATH


def plot_overall_funnel(funnel_df):
    os.makedirs(OUTPUT_PLOT_PATH, exist_ok=True)

    plt.figure(figsize=(8, 5))

    plt.barh(funnel_df["step"], funnel_df["users"])

    plt.title("Marketing Funnel (Overall)")
    plt.xlabel("Users")

    for i, v in enumerate(funnel_df["users"]):
        plt.text(v, i, str(int(v)))

    plt.gca().invert_yaxis()

    plt.tight_layout()

    plt.savefig(f"{OUTPUT_PLOT_PATH}/funnel_overall.png")

    plt.show()


def main():
    print("=== VISUALIZATION TEST ===")

    test_df = pd.DataFrame([{
        "page": 100,
        "view": 80,
        "cart": 40,
        "checkout": 30,
        "purchase": 20,
    }])

    plot_overall_funnel(test_df)


if __name__ == "__main__":
    main()