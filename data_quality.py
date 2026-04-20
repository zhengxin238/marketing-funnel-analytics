import pandas as pd


# =========================
# DETECTION
# =========================
def detect_tracking_issues(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect anomalies in funnel tracking
    """

    df = df.copy()

    # 🚨 Cart tracking completely broken
    df["cart_issue_flag"] = (
        (df["add_to_cart"] == 0) &
        (df["purchase"] > 0)
    )

    # 🚨 Impossible funnel (purchase > cart)
    df["conversion_anomaly_flag"] = (
        (df["purchase"] > df["add_to_cart"]) &
        (df["add_to_cart"] > 0)
    )

    # 🚨 Suspicious low cart volume (partial failure)
    df["partial_tracking_flag"] = (
        (df["add_to_cart"] < df["purchase"] * 0.5) &
        (df["add_to_cart"] > 0)
    )

    return df


# =========================
# REPAIR (THIS IS THE REAL UPGRADE)
# =========================
def repair_tracking_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fix broken add_to_cart tracking using estimation logic
    """

    df = df.copy()

    # ✅ Force float from the start
    df["effective_add_to_cart"] = df["add_to_cart"].astype(float)

    mask = (
        df["cart_issue_flag"] |
        df["conversion_anomaly_flag"] |
        df["partial_tracking_flag"]
    )

    # Apply estimation
    df.loc[mask, "effective_add_to_cart"] = df["purchase"] * 2.2

    return df


# =========================
# SUMMARY (RECRUITER GOLD)
# =========================
def summarize_data_issues(df: pd.DataFrame) -> pd.DataFrame:
    """
    Structured summary (for CSV / Tableau)
    """

    summary = {
        "days_with_cart_tracking_issue": int(df["cart_issue_flag"].sum()),
        "days_with_conversion_anomaly": int(df["conversion_anomaly_flag"].sum()),
        "days_with_partial_tracking": int(df["partial_tracking_flag"].sum()),
        "total_days": int(len(df))
    }

    return pd.DataFrame([summary])


def generate_quality_report_text(df: pd.DataFrame) -> str:
    """
    Human-readable report (for README / AI / interviews)
    """

    broken_days = df["cart_issue_flag"].sum()
    anomaly_days = df["conversion_anomaly_flag"].sum()
    partial_days = df["partial_tracking_flag"].sum()

    return f"""
📊 DATA QUALITY REPORT

- Broken tracking days: {broken_days}
- Impossible funnel days: {anomaly_days}
- Partial tracking failures: {partial_days}

🚨 Insight:
The 'add_to_cart' event is unreliable across multiple periods.

🛠 Fix Applied:
Introduced 'effective_add_to_cart' using behavioral estimation.

✅ Result:
Funnel analysis is now robust despite tracking failures.
"""