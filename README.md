# 📊 Marketing Funnel Analytics Pipeline (GA4 + BigQuery + Python)

---

## 🚀 Executive Summary

This project analyzes **270K+ GA4 ecommerce sessions** to identify user drop-off points, optimize marketing performance, and improve conversion efficiency.

Using BigQuery and Python, I built an end-to-end analytics pipeline that transforms raw event data into actionable business insights.

---

## 🎯 Business Problem

The ecommerce platform is losing users at critical funnel stages:

- Product View → Add to Cart
- Add to Cart → Checkout
- Checkout → Purchase

This project answers:

- Where do users drop off?
- Which channels bring high-quality traffic?
- How do devices affect conversion?
- What drives revenue loss in the funnel?

---

## 📊 Key Insights

### 🔻 Funnel Drop-off
- Largest drop-off occurs at **View Item → Add to Cart**
- Only a small fraction of users reach checkout

### 💰 Conversion Performance
- Overall conversion rate: ~1.6%
- Strong leakage before checkout stage

### 📱 Device Behavior
- Desktop users convert significantly better than mobile users
- Mobile funnel shows higher friction

### 🌐 Traffic Sources
- Google is the highest-quality traffic source
- Some sources drive volume but low conversion

---

## 📉 Funnel Summary

- Page Views: 269,792  
- Product Views: 61,252  
- Add to Cart: 12,545  
- Checkout: 9,715  
- Purchases: 4,419  

---

## 💡 Business Recommendations

- Improve product page engagement (images, UX, pricing clarity)
- Reduce friction in add-to-cart flow
- Optimize mobile checkout experience
- Reallocate marketing budget toward high-converting sources
- Improve retargeting for cart abandoners

---

## 🏗️ Methodology

### 1. Data Source
- Google Analytics 4 BigQuery public dataset

### 2. Pipeline Design
BigQuery → Python ETL → Funnel Modeling → Segmentation → BI Outputs

### 3. Analysis Layers
- Funnel analysis (conversion + drop-off)
- Device segmentation
- Traffic source analysis
- Cohort retention behavior

---

## 📊 Outputs Generated

All outputs are exported as BI-ready datasets:

- raw_events.csv → user-level funnel data  
- funnel_overview.csv → funnel performance summary  
- funnel_over_time.csv → trend analysis  
- funnel_by_device.csv → device segmentation  
- funnel_by_source.csv → marketing channel analysis  
- cohort_retention.csv → user retention behavior  
- kpis.csv → executive dashboard metrics  
- insights.csv → business interpretation layer  

---

## 🧠 Skills Demonstrated

- End-to-end GA4 funnel analytics pipeline
- BigQuery SQL for behavioral data extraction
- Python-based ETL and transformation logic
- Marketing funnel and conversion analysis
- Cohort retention modeling
- Business insight generation from raw data
- BI-ready dataset engineering

---

## 🚀 How to Run

```bash
python main.py