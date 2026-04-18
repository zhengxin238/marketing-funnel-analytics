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

- raw_events.csv → user-level behavior
- funnel_overview.csv → global funnel KPIs
- funnel_by_device.csv → device performance
- funnel_by_source.csv → channel performance

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
