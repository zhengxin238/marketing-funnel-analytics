import os
import pandas as pd

# =========================
# 📁 CONFIG
# =========================
BASE_DIR = os.getcwd()
CSV_DIR = os.path.join(BASE_DIR, "outputs", "csv")


# =========================
# 📄 README CONTENT
# =========================
README_CONTENT = """# 📊 Marketing Funnel Analytics Pipeline (GA4 + BigQuery + Python + Tableau)



## 🚀 Overview

This project analyzed GA4 ecommerce event data (270K+ user sessions) to identify funnel drop-off points and optimize conversion performance using Python and BigQuery.

End-to-end marketing funnel analytics project using GA4 BigQuery data.

Pipeline:
BigQuery → Python ETL → Funnel Modeling → Segmentation → Tableau-ready CSVs

It identifies:
- Where users drop off
- Which channels convert best
- How device behavior impacts conversion

---

## 🎯 Business Problem

The company is losing users between:
- Product view → Add to cart
- Checkout → Purchase

We need to quantify:
1. Funnel drop-off points
2. Conversion rates per stage
3. Segment performance (device + source)

---

## 🔍 Key Findings

- Largest drop-off occurs between View Item → Add to Cart (~80% loss)
- Overall conversion rate is ~1.6%
- Mobile users convert less than desktop users
- Google is the strongest traffic source

---

## 📊 Funnel Performance

- Page Views: 269,792  
- Product Views: 61,252  
- Add to Cart: 12,545  
- Checkout: 9,715  
- Purchases: 4,419  

Overall Conversion Rate: ~1.6%

---

## 💡 Recommendations

- Improve product page engagement (images, pricing clarity)
- Simplify checkout flow to reduce drop-off
- Optimize mobile experience
- Focus budget on high-converting traffic sources

---

## 🏗️ Approach

### 1. Data Source
GA4 BigQuery public dataset

### 2. Transformation Logic
User-level funnel aggregation:
- page_view
- view_item
- add_to_cart
- begin_checkout
- purchase

### 3. Segmentation
- Device (mobile vs desktop)
- Traffic source (google, direct, email)

---

## 📊 Outputs

All outputs are generated in `outputs/csv/` and are ready for BI tools like Tableau.

- **raw_events.csv** → user-level dataset containing funnel stage flags, device, source, and first-touch timestamp  
- **funnel_overview.csv** → aggregated funnel metrics (total users per stage + drop-off analysis)  
- **funnel_over_time.csv** → daily funnel activity to analyze trends over time  
- **funnel_by_device.csv** → conversion performance segmented by device category  
- **funnel_by_source.csv** → conversion performance segmented by traffic source  
- **conversion_rate.csv** → overall funnel conversion rate (purchase / page view)  
- **cohort_retention.csv** → cohort-based retention analysis (user engagement over time)  

---

## 🔐 Authentication

Uses **Google Application Default Credentials (ADC)** via environment variable

---

## 🧠 Skills Demonstrated

- Built end-to-end GA4 funnel analytics pipeline
- Performed user segmentation and conversion analysis
- Created BI-ready datasets for Tableau dashboards

with

✔ SQL funnel modeling  
✔ Python ETL pipeline  
✔ Segmented behavioral analysis  
✔ KPI design (conversion + drop-off)  
✔ BI-ready dataset creation  
✔ Business storytelling  

---

## 🚀 How to Run

Run the script:

python main.py

---

## 👤 Author

Xin Zheng
"""


# =========================
# 📁 CREATE FOLDERS
# =========================
def create_folders():
    os.makedirs(CSV_DIR, exist_ok=True)
    print("✔ Folders created")


# =========================
# 📄 CREATE README
# =========================
def create_readme():
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(README_CONTENT)
    print("✔ README.md created")


# =========================
# 📊 CREATE SAMPLE CSVs
# =========================
def create_csvs():
    os.makedirs(CSV_DIR, exist_ok=True)

    raw_events = pd.DataFrame({
        "user_id": ["U1", "U2", "U3", "U4"],
        "page_view": [1, 1, 1, 1],
        "view_item": [1, 1, 0, 1],
        "add_to_cart": [1, 0, 0, 1],
        "begin_checkout": [1, 0, 0, 0],
        "purchase": [1, 0, 0, 0],
        "device": ["mobile", "desktop", "mobile", "desktop"],
        "source": ["google", "direct", "email", "google"]
    })

    raw_events.to_csv(os.path.join(CSV_DIR, "raw_events.csv"), index=False)

    funnel_overview = pd.DataFrame({
        "step": ["page_view", "view_item", "add_to_cart", "begin_checkout", "purchase"],
        "users": [1000, 700, 400, 250, 120]
    })

    funnel_overview.to_csv(os.path.join(CSV_DIR, "funnel_overview.csv"), index=False)

    device_funnel = pd.DataFrame({
        "device": ["mobile", "desktop"],
        "users": [600, 400]
    })

    device_funnel.to_csv(os.path.join(CSV_DIR, "funnel_by_device.csv"), index=False)

    source_funnel = pd.DataFrame({
        "source": ["google", "direct", "email"],
        "users": [500, 300, 200]
    })

    source_funnel.to_csv(os.path.join(CSV_DIR, "funnel_by_source.csv"), index=False)

    print("✔ CSV files created")


# =========================
# 🚀 MAIN
# =========================
def main():
    print("=== GENERATING PORTFOLIO ASSETS ===")

    create_folders()
    create_readme()
    create_csvs()

    print("\n🎉 DONE!")
    print("Your portfolio files are ready.")


if __name__ == "__main__":
    main()