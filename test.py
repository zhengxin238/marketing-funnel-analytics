import os
import pandas as pd


# =========================
# CONFIG
# =========================
CSV_FOLDER = "outputs/csv"


# =========================
# CHECK FUNCTION
# =========================
def analyze_csv(file_path):
    print("\n" + "=" * 60)
    print(f"📄 FILE: {file_path}")
    print("=" * 60)

    try:
        df = pd.read_csv(file_path)

        print(f"Rows: {len(df)} | Columns: {len(df.columns)}\n")

        for col in df.columns:
            print(f"🔎 Column: {col}")
            print(f"   dtype: {df[col].dtype}")

            # Try numeric conversion test
            converted = pd.to_numeric(df[col], errors="coerce")

            total_null_after = converted.isna().sum()
            total_original_null = df[col].isna().sum()

            # Detect if column is mostly numeric or broken
            numeric_ratio = (len(df) - total_null_after) / len(df)

            if numeric_ratio == 1:
                status = "✅ CLEAN NUMERIC"
            elif numeric_ratio > 0.7:
                status = "⚠️ MOSTLY NUMERIC (some bad values)"
            else:
                status = "❌ NON-NUMERIC / BROKEN"

            print(f"   status: {status}")
            print(f"   invalid values: {total_null_after}")

            # Show sample bad values
            bad_values = df[col][converted.isna()].dropna().unique()

            if len(bad_values) > 0:
                print(f"   sample bad values: {bad_values[:5]}")

            print("-" * 40)

    except Exception as e:
        print(f"❌ ERROR reading file: {e}")


# =========================
# SCAN ALL CSV FILES
# =========================
def main():
    print("\n🚀 STARTING CSV DATA QUALITY AUDIT\n")

    if not os.path.exists(CSV_FOLDER):
        print(f"❌ Folder not found: {CSV_FOLDER}")
        return

    files = [f for f in os.listdir(CSV_FOLDER) if f.endswith(".csv")]

    if not files:
        print("❌ No CSV files found")
        return

    for file in files:
        file_path = os.path.join(CSV_FOLDER, file)
        analyze_csv(file_path)

    print("\n✔ AUDIT COMPLETE")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()











# import os
# from dotenv import load_dotenv
# from google import genai
#
# load_dotenv()
#
#
# def test_ai_connection():
#     api_key = os.getenv("GEMINI_API_KEY")
#     client = genai.Client(api_key=api_key)
#
#     try:
#         print("🧠 Test mit dem stabilen 'Latest' Alias...")
#
#         # Wir nutzen den Alias aus deiner Liste:
#         response = client.models.generate_content(
#             model="gemini-flash-latest",
#             contents="Say 'Everything is working now!'"
#         )
#
#         print(f"✅ SUCCESS: {response.text}")
#
#     except Exception as e:
#         print(f"❌ Error: {e}")
#
#
# if __name__ == "__main__":
#     test_ai_connection()
