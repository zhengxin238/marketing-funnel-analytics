# 📊 Marketing Funnel Analytics Pipeline (GA4 + BigQuery + Python + Tableau)



## 🚀 Overview

This project analyzes user behavior across a full ecommerce funnel using GA4 event data.

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

Uses **Google Application Default Credentials (ADC)** via environment variable:

```bash
setx GOOGLE_APPLICATION_CREDENTIALS "path_to_your_json"

---

## 🧠 Skills Demonstrated

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
