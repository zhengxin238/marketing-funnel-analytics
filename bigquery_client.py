from google.cloud import bigquery
from config import PROJECT_ID, SERVICE_ACCOUNT_FILE


def get_bigquery_client():
    return bigquery.Client.from_service_account_json(
        SERVICE_ACCOUNT_FILE,
        project=PROJECT_ID
    )


def main():
    client = get_bigquery_client()
    print("BigQuery authentication SUCCESS")
    print(client)


if __name__ == "__main__":
    main()