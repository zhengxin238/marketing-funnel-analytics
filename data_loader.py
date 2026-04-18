import pandas as pd
from bigquery_client import get_bigquery_client
from queries import get_user_level_funnel_query


def load_bigquery_data(query: str) -> pd.DataFrame:
    client = get_bigquery_client()
    return client.query(query).to_dataframe()


def main():
    print("Running data load test...")

    query = get_user_level_funnel_query()
    df = load_bigquery_data(query)

    print("\nData preview:")
    print(df.head())


if __name__ == "__main__":
    main()