# =========================
# GA4 ANALYTICS QUERIES (FULL LIBRARY)
# =========================


# -------------------------
# USER-LEVEL FUNNEL (CORE)
# -------------------------
def get_user_level_funnel_query():
    return """
    WITH base AS (
      SELECT
        user_pseudo_id,
        event_name,
        device.category AS device,
        traffic_source.source AS source,
        TIMESTAMP_MICROS(event_timestamp) AS event_time
      FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
    ),

    user_level AS (
      SELECT
        user_pseudo_id,

        MAX(CASE WHEN event_name = 'page_view' THEN 1 ELSE 0 END) AS page_view,
        MAX(CASE WHEN event_name = 'view_item' THEN 1 ELSE 0 END) AS view_item,
        MAX(CASE WHEN event_name = 'add_to_cart' THEN 1 ELSE 0 END) AS add_to_cart,
        MAX(CASE WHEN event_name = 'begin_checkout' THEN 1 ELSE 0 END) AS begin_checkout,
        MAX(CASE WHEN event_name = 'purchase' THEN 1 ELSE 0 END) AS purchase,

        ANY_VALUE(device) AS device,
        ANY_VALUE(source) AS source

      FROM base
      GROUP BY user_pseudo_id
    )

    SELECT * FROM user_level
    """


# -------------------------
# FUNNEL OVERVIEW (KPI)
# -------------------------
def get_funnel_overview_query():
    return """
    WITH user_level AS (
      SELECT
        user_pseudo_id,
        MAX(CASE WHEN event_name = 'page_view' THEN 1 ELSE 0 END) AS page_view,
        MAX(CASE WHEN event_name = 'view_item' THEN 1 ELSE 0 END) AS view_item,
        MAX(CASE WHEN event_name = 'add_to_cart' THEN 1 ELSE 0 END) AS add_to_cart,
        MAX(CASE WHEN event_name = 'begin_checkout' THEN 1 ELSE 0 END) AS begin_checkout,
        MAX(CASE WHEN event_name = 'purchase' THEN 1 ELSE 0 END) AS purchase
      FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
      GROUP BY user_pseudo_id
    )

    SELECT
      SUM(page_view) AS page_view,
      SUM(view_item) AS view_item,
      SUM(add_to_cart) AS add_to_cart,
      SUM(begin_checkout) AS begin_checkout,
      SUM(purchase) AS purchase
    FROM user_level
    """


# -------------------------
# FUNNEL OVER TIME
# -------------------------
def get_funnel_over_time_query():
    return """
    WITH base AS (
      SELECT
        DATE(TIMESTAMP_MICROS(event_timestamp)) AS date,
        event_name,
        user_pseudo_id
      FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
    ),

    aggregated AS (
      SELECT
        date,
        COUNTIF(event_name = 'page_view') AS page_view,
        COUNTIF(event_name = 'view_item') AS view_item,
        COUNTIF(event_name = 'add_to_cart') AS add_to_cart,
        COUNTIF(event_name = 'purchase') AS purchase
      FROM base
      GROUP BY date
    ),

    corrected AS (
      SELECT
        *,

        -- 🚨 flag broken tracking
        CASE
          WHEN add_to_cart = 0 AND purchase > 0 THEN TRUE
          ELSE FALSE
        END AS cart_tracking_broken,

        -- 🧠 fallback estimation
        CASE
          WHEN add_to_cart = 0 AND purchase > 0
          THEN purchase * 2   -- simple heuristic (can explain in interview)
          ELSE add_to_cart
        END AS effective_add_to_cart

      FROM aggregated
    )

    SELECT * FROM corrected
    ORDER BY date
    """


# -------------------------
# DEVICE SEGMENTATION
# -------------------------
def get_funnel_by_device_query():
    return """
    SELECT
      device.category AS device,
      COUNTIF(event_name = 'page_view') AS page_view,
      COUNTIF(event_name = 'purchase') AS purchase,
      SAFE_DIVIDE(
        COUNTIF(event_name = 'purchase'),
        COUNTIF(event_name = 'page_view')
      ) AS conversion_rate
    FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
    GROUP BY device
    ORDER BY purchase DESC
    """


# -------------------------
# SOURCE SEGMENTATION
# -------------------------
def get_funnel_by_source_query():
    return """
    SELECT
      traffic_source.source AS source,
      COUNTIF(event_name = 'page_view') AS page_view,
      COUNTIF(event_name = 'purchase') AS purchase,
      SAFE_DIVIDE(
        COUNTIF(event_name = 'purchase'),
        COUNTIF(event_name = 'page_view')
      ) AS conversion_rate
    FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
    GROUP BY source
    ORDER BY purchase DESC
    """


# -------------------------
# GLOBAL CONVERSION RATE
# -------------------------
def get_conversion_rate_query():
    return """
    SELECT
      SAFE_DIVIDE(
        COUNT(DISTINCT IF(event_name = 'purchase', user_pseudo_id, NULL)),
        COUNT(DISTINCT IF(event_name = 'page_view', user_pseudo_id, NULL))
      ) AS conversion_rate
    FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
    """


# -------------------------
# COHORT RETENTION (ADVANCED)
# -------------------------
def get_cohort_retention_query():
    return """
    WITH user_first_touch AS (
      SELECT
        user_pseudo_id,
        DATE(MIN(TIMESTAMP_MICROS(event_timestamp))) AS cohort_date
      FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
      GROUP BY user_pseudo_id
    ),

    activity AS (
      SELECT
        e.user_pseudo_id,
        DATE(TIMESTAMP_MICROS(e.event_timestamp)) AS event_date,
        u.cohort_date
      FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` e
      JOIN user_first_touch u
        ON e.user_pseudo_id = u.user_pseudo_id
    )

    SELECT
      cohort_date,
      DATE_DIFF(event_date, cohort_date, DAY) AS day_offset,
      COUNT(DISTINCT user_pseudo_id) AS active_users
    FROM activity
    GROUP BY cohort_date, day_offset
    ORDER BY cohort_date, day_offset
    """