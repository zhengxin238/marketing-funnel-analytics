PROJECT_ID = "marketing-funnel-project"

# Path to your service account JSON
SERVICE_ACCOUNT_FILE = "marketing-funnel-project-1b31b1d8b837.json"

DATASET = "bigquery-public-data.ga4_obfuscated_sample_ecommerce"
TABLE = "events_*"

# Output directories (added for pipeline completeness)
OUTPUT_CSV_PATH = "outputs/csv/"
OUTPUT_PLOT_PATH = "outputs/plots/"

def main():
    print("=== CONFIGURATION CHECK ===")
    print("Project:", PROJECT_ID)
    print("Service Account File:", SERVICE_ACCOUNT_FILE)
    print("Dataset:", DATASET)
    print("Table:", TABLE)
    print("CSV Output Path:", OUTPUT_CSV_PATH)
    print("Plot Output Path:", OUTPUT_PLOT_PATH)


if __name__ == "__main__":
    main()