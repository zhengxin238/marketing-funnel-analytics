from google.cloud import bigquery


def get_bigquery_client():
    # Uses environment variable (best practice)
    return bigquery.Client()


def main():
    client = get_bigquery_client()
    print("BigQuery authentication SUCCESS")
    print(client)


if __name__ == "__main__":
    main()