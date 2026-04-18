import pandas as pd
from google.cloud import bigquery
from bigquery_client import get_bigquery_client


# =========================
# BIGQUERY LOADER CORE
# =========================
def load_bigquery_data(query: str, max_gb_scanned: float = 10.0) -> pd.DataFrame:
    """
    Executes a BigQuery SQL query and returns a pandas DataFrame.
    Includes safety limits and error handling.
    """

    try:
        client = get_bigquery_client()

        job_config = bigquery.QueryJobConfig(
            maximum_bytes_billed=int(max_gb_scanned * 10**9)  # cost control
        )

        print("🚀 Executing query in BigQuery...")

        query_job = client.query(query, job_config=job_config)
        df = query_job.to_dataframe()

        print(f"✔ Query successful — rows: {len(df)}")
        return df

    except Exception as e:
        print("\n❌ BigQuery query failed")
        print("========================")
        print(str(e))
        return pd.DataFrame()


# =========================
# DEBUG / TEST FUNCTION
# =========================
def test_loader():
    from queries import get_user_level_funnel_query

    print("\n=== TESTING BIGQUERY LOADER ===\n")

    query = get_user_level_funnel_query()
    df = load_bigquery_data(query)

    if not df.empty:
        print("\n📊 Data preview:")
        print(df.head())
    else:
        print("⚠ No data returned")


# =========================
# MAIN (OPTIONAL DEBUG RUN)
# =========================
if __name__ == "__main__":
    test_loader()