import pandas as pd

# =========================
# FUNNEL CONFIG (MUST MATCH QUERIES.PY)
# =========================
FUNNEL_STEPS = [
    "page_view",
    "view_item",
    "add_to_cart",
    "begin_checkout",
    "purchase"
]


# =========================================================
# 1. CORE FUNNEL ANALYSIS (MOST IMPORTANT BUSINESS OUTPUT)
# =========================================================
def compute_overall_funnel(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full funnel performance + drop-off + conversion rates
    """

    totals = df[FUNNEL_STEPS].sum()

    funnel = pd.DataFrame({
        "step": FUNNEL_STEPS,
        "users": totals.values
    })

    # Step conversion (relative to previous step)
    funnel["step_conversion_rate"] = funnel["users"] / funnel["users"].shift(1)

    # Overall conversion (relative to first step)
    funnel["overall_conversion_rate"] = funnel["users"] / funnel["users"].iloc[0]

    # Drop-off analysis
    funnel["drop_off_users"] = funnel["users"].shift(1) - funnel["users"]
    funnel["drop_off_rate"] = 1 - funnel["step_conversion_rate"]

    return funnel


# =========================================================
# 2. DEVICE PERFORMANCE ANALYSIS (USER BEHAVIOR DIFFERENCE)
# =========================================================
def compute_device_funnel(df: pd.DataFrame) -> pd.DataFrame:
    """
    How different devices convert through funnel
    """

    results = []

    for device, group in df.groupby("device"):
        totals = group[FUNNEL_STEPS].sum()

        temp = pd.DataFrame({
            "device": device,
            "step": FUNNEL_STEPS,
            "users": totals.values
        })

        temp["step_conversion_rate"] = temp["users"] / temp["users"].shift(1)
        temp["overall_conversion_rate"] = temp["users"] / temp["users"].iloc[0]

        # add key KPI per device
        temp["final_conversion_rate"] = temp["users"].iloc[-1] / temp["users"].iloc[0]

        results.append(temp)

    return pd.concat(results, ignore_index=True)


# =========================================================
# 3. TRAFFIC SOURCE ANALYSIS (MARKETING CHANNEL QUALITY)
# =========================================================
def compute_source_funnel(df: pd.DataFrame) -> pd.DataFrame:
    """
    Which traffic sources bring high-quality users
    """

    results = []

    for source, group in df.groupby("source"):
        totals = group[FUNNEL_STEPS].sum()

        temp = pd.DataFrame({
            "source": source,
            "step": FUNNEL_STEPS,
            "users": totals.values
        })

        temp["step_conversion_rate"] = temp["users"] / temp["users"].shift(1)
        temp["overall_conversion_rate"] = temp["users"] / temp["users"].iloc[0]
        temp["final_conversion_rate"] = temp["users"].iloc[-1] / temp["users"].iloc[0]

        results.append(temp)

    return pd.concat(results, ignore_index=True)


# =========================================================
# 4. TIME-BASED BEHAVIOR (TREND ANALYSIS)
# =========================================================
def compute_time_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect behavioral changes over time
    """

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    daily = df.groupby("date")[FUNNEL_STEPS].sum().reset_index()

    # add growth rates
    daily["purchase_growth_rate"] = daily["purchase"].pct_change()
    daily["add_to_cart_growth_rate"] = daily["add_to_cart"].pct_change()

    return daily


# =========================================================
# 5. KPI ENGINE (EXECUTIVE SUMMARY METRICS)
# =========================================================
def compute_kpis(df: pd.DataFrame) -> dict:
    """
    High-level business KPIs for dashboard cards
    """

    total_users = len(df)

    return {
        "total_users": total_users,
        "total_purchases": int(df["purchase"].sum()),
        "total_add_to_cart": int(df["add_to_cart"].sum()),
        "total_checkout": int(df["begin_checkout"].sum()),
        "overall_conversion_rate": df["purchase"].sum() / total_users if total_users else 0,
        "cart_to_purchase_rate": (
            df["purchase"].sum() / df["add_to_cart"].sum()
            if df["add_to_cart"].sum() > 0 else 0
        )
    }


# =========================================================
# 6. COHORT INSIGHTS (NOT RAW OUTPUT — INTERPRETABLE FORM)
# =========================================================
def compute_cohort_summary(cohort_df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts raw cohort table into retention summary
    """

    cohort_df = cohort_df.copy()

    # average retention per day offset
    summary = cohort_df.groupby("day_offset")["active_users"].mean().reset_index()

    summary["retention_decay"] = summary["active_users"].pct_change()

    return summary


# =========================================================
# 7. DATA VALIDATION (CRITICAL FOR REAL PROJECTS)
# =========================================================
def validate_data(df: pd.DataFrame):
    """
    Ensures dataset integrity before analysis
    """

    required_cols = FUNNEL_STEPS + ["device", "source"]

    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if df.empty:
        raise ValueError("Dataset is empty")

    print("✔ Data validation passed")


# =========================================================
# 8. INSIGHT GENERATOR (PORTFOLIO LEVEL UPGRADE)
# =========================================================
def generate_insights(funnel_df: pd.DataFrame, kpis: dict) -> list:
    """
    Converts numbers into business insights (VERY IMPORTANT FOR PORTFOLIO)
    """

    insights = []

    dropoff = funnel_df["drop_off_rate"].max()

    weakest_step = funnel_df.loc[funnel_df["drop_off_rate"].idxmax(), "step"]

    insights.append(f"Highest drop-off occurs at: {weakest_step}")

    insights.append(f"Overall conversion rate is {kpis['overall_conversion_rate']:.2%}")

    if kpis["cart_to_purchase_rate"] < 0.2:
        insights.append("Cart-to-purchase rate is low → checkout friction likely exists")

    if dropoff > 0.5:
        insights.append("Severe funnel leakage detected (>50% drop-off at one stage)")

    return insights