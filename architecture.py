import os


def get_architecture_markdown():
    """
    Returns architecture as a Markdown document (GitHub + portfolio friendly)
    """

    md = """
# 📊 Marketing Funnel Analytics Architecture

## 🧱 System Overview

This project implements an end-to-end analytics pipeline for ecommerce funnel analysis using GA4 BigQuery data.

---

## 🔄 Data Pipeline Flow

### 1. Data Source
- Google BigQuery (GA4 ecommerce dataset)
- Raw event-level user interactions

---

### 2. Extraction Layer
- Python (BigQuery Client)
- Loads raw event data into pandas DataFrame

---

### 3. Transformation Layer
- Pandas-based processing
- Converts event-level data → user-level funnel stages

Funnel stages:
- page_view
- view_item
- add_to_cart
- begin_checkout
- purchase

---

### 4. Segmentation Layer
- Device segmentation (mobile / desktop)
- Traffic source segmentation (google / direct / email)

---

### 5. Output Layer (BI Ready)
Generated CSV files:
- raw_events.csv
- funnel_overview.csv
- funnel_by_device.csv
- funnel_by_source.csv
- architecture_overview.md

---

### 6. Visualization Layer (Tableau)
Dashboards built on exported CSVs:
- Funnel conversion analysis
- Device performance comparison
- Channel attribution analysis

---

## 🎯 Business Objective

The goal of this pipeline is to:

- Identify funnel drop-off points
- Measure conversion efficiency
- Compare performance across segments
- Support data-driven marketing optimization

---

## 📈 Key Insight Areas

- Largest drop-off occurs before purchase
- Mobile users convert lower than desktop users
- Acquisition channel quality varies significantly

---

## 🧠 Skills Demonstrated

- SQL-based funnel modeling
- Python ETL pipeline design
- Segmented behavioral analytics
- BI-ready dataset engineering
- Business storytelling through data
"""
    return md


def save_markdown(md_content, output_path="outputs/docs"):
    os.makedirs(output_path, exist_ok=True)

    file_path = os.path.join(output_path, "architecture_overview.md")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"✔ Markdown saved to: {file_path}")


def main():
    print("=== ARCHITECTURE MARKDOWN GENERATOR ===")

    md = get_architecture_markdown()

    save_markdown(md)

    print("✔ Done — architecture markdown created for GitHub + portfolio")


if __name__ == "__main__":
    main()