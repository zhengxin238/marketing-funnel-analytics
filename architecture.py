import os


def get_architecture_markdown():
    """
    Returns a production-grade architecture document (GitHub + portfolio ready)
    """

    md = """
# 📊 Marketing Funnel Analytics Pipeline — Architecture Overview

## 🧱 1. System Overview

This project implements an end-to-end data analytics pipeline that transforms raw GA4 ecommerce event data into BI-ready datasets for funnel, segmentation, and cohort analysis.

The system is designed to support marketing and product decision-making through scalable and modular data processing.

---

## 🔄 2. Data Pipeline Flow

**BigQuery (GA4 Dataset) → Python ETL → Transformation Layer → Aggregated Metrics → CSV Outputs → Tableau Dashboards**

---

## 🗄️ 3. Data Source Layer

- Google BigQuery public GA4 ecommerce dataset
- Event-level user interaction data
- Includes behavioral events such as:
  - page_view
  - view_item
  - add_to_cart
  - begin_checkout
  - purchase

---

## ⚙️ 4. Extraction Layer (Python + BigQuery)

- Uses Google Cloud BigQuery client
- Extracts raw event data into pandas DataFrames
- Handles authentication via environment variables (ADC)

---

## 🔄 5. Transformation Layer (Python ETL)

Transforms raw event data into analytical structures:

### Funnel Modeling
- Converts event-level data → user-level funnel states
- Tracks user progression through conversion steps

### Funnel Stages
- Page View
- Product View
- Add to Cart
- Checkout
- Purchase

---

## 📊 6. Segmentation Layer

Enables multi-dimensional analysis:

### Device Segmentation
- Desktop
- Mobile
- Tablet

### Traffic Source Segmentation
- Organic search
- Direct traffic
- Referral / campaigns

---

## 📦 7. Output Layer (BI-Ready Data)

All outputs are stored in `outputs/csv/` and optimized for Tableau:

- raw_events.csv → enriched user-level dataset
- funnel_overview.csv → overall funnel KPIs
- funnel_over_time.csv → time-based funnel trends
- funnel_by_device.csv → device performance comparison
- funnel_by_source.csv → channel attribution analysis
- conversion_rate.csv → global conversion metric
- cohort_retention.csv → user retention over time

---

## 📈 8. Visualization Layer (Tableau)

The exported datasets power interactive dashboards:

- Funnel drop-off visualization
- Conversion rate analysis
- Device vs performance comparison
- Channel attribution breakdown
- Cohort retention heatmaps

---

## 🎯 9. Business Objective

This pipeline is designed to answer key business questions:

- Where do users drop off in the funnel?
- Which acquisition channels drive the highest conversion?
- How does device type impact conversion rates?
- How does user retention evolve over time?

---

## 📌 10. Key Insights Enabled

- Significant drop-off between product view and checkout stages
- Mobile users show lower conversion rates than desktop users
- Traffic sources vary significantly in conversion efficiency
- Retention declines sharply after first interaction

---

## 🧠 11. Skills Demonstrated

This project demonstrates:

- Advanced SQL funnel modeling
- Python ETL pipeline design
- BigQuery data extraction
- Behavioral segmentation analysis
- Cohort retention analysis
- BI dashboard readiness (Tableau)
- Data storytelling for business impact

---

## 🚀 12. Design Principles

- Modular architecture
- Separation of concerns (SQL / ETL / analysis / visualization)
- Reusable query structure
- Scalable analytics pipeline
- Production-style data workflow
"""

    return md


def save_markdown(md_content, output_path="outputs/docs"):
    os.makedirs(output_path, exist_ok=True)

    file_path = os.path.join(output_path, "architecture_overview.md")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"✔ Architecture saved to: {file_path}")


def main():
    print("=== ARCHITECTURE DOC GENERATOR ===")

    md = get_architecture_markdown()

    save_markdown(md)

    print("✔ Done — portfolio-grade architecture file generated")


if __name__ == "__main__":
    main()