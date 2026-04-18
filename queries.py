# =========================
# FUNNEL BASE (USER LEVEL)
# =========================
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

    enriched AS (
      SELECT
        *,
        MIN(event_time) OVER (PARTITION BY user_pseudo_id) AS first_touch
      FROM base
    ),

    user_level AS (
      SELECT
        user_pseudo_id,

        MAX(CASE WHEN event_name = 'page_view' THEN 1 ELSE 0 END) AS page,
        MAX(CASE WHEN event_name = 'view_item' THEN 1 ELSE 0 END) AS view,
        MAX(CASE WHEN event_name = 'add_to_cart' THEN 1 ELSE 0 END) AS cart,
        MAX(CASE WHEN event_name = 'begin_checkout' THEN 1 ELSE 0 END) AS checkout,
        MAX(CASE WHEN event_name = 'purchase' THEN 1 ELSE 0 END) AS purchase,

        ANY_VALUE(device) AS device,
        ANY_VALUE(source) AS source,
        ANY_VALUE(first_touch) AS first_touch

      FROM enriched
      GROUP BY user_pseudo_id
    )

    SELECT * FROM user_level
    """


# =========================
# FUNNEL OVERVIEW
# =========================
def get_funnel_overview_query():
    return """
    WITH user_level AS (
      SELECT
        user_pseudo_id,
        MAX(CASE WHEN event_name = 'page_view' THEN 1 ELSE 0 END) AS page,
        MAX(CASE WHEN event_name = 'view_item' THEN 1 ELSE 0 END) AS view,
        MAX(CASE WHEN event_name = 'add_to_cart' THEN 1 ELSE 0 END) AS cart,
        MAX(CASE WHEN event_name = 'begin_checkout' THEN 1 ELSE 0 END) AS checkout,
        MAX(CASE WHEN event_name = 'purchase' THEN 1 ELSE 0 END) AS purchase
      FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
      GROUP BY user_pseudo_id
    )

    SELECT
      SUM(page) AS page_users,
      SUM(view) AS view_users,
      SUM(cart) AS cart_users,
      SUM(checkout) AS checkout_users,
      SUM(purchase) AS purchase_users
    FROM user_level
    """


# =========================
# FUNNEL OVER TIME
# =========================
def get_funnel_over_time_query():
    return """
    SELECT
      DATE(TIMESTAMP_MICROS(event_timestamp)) AS date,
      COUNTIF(event_name = 'page_view') AS page,
      COUNTIF(event_name = 'view_item') AS view,
      COUNTIF(event_name = 'add_to_cart') AS cart,
      COUNTIF(event_name = 'purchase') AS purchase
    FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
    GROUP BY date
    ORDER BY date
    """


# =========================
# FUNNEL BY DEVICE
# =========================
def get_funnel_by_device_query():
    return """
    SELECT
      device.category AS device,
      COUNTIF(event_name = 'page_view') AS page,
      COUNTIF(event_name = 'purchase') AS purchase,
      SAFE_DIVIDE(
        COUNTIF(event_name = 'purchase'),
        COUNTIF(event_name = 'page_view')
      ) AS conversion_rate
    FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
    GROUP BY device
    ORDER BY purchase DESC
    """


# =========================
# FUNNEL BY SOURCE
# =========================
def get_funnel_by_source_query():
    return """
    SELECT
      traffic_source.source AS source,
      COUNTIF(event_name = 'page_view') AS page,
      COUNTIF(event_name = 'purchase') AS purchase,
      SAFE_DIVIDE(
        COUNTIF(event_name = 'purchase'),
        COUNTIF(event_name = 'page_view')
      ) AS conversion_rate
    FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
    GROUP BY source
    ORDER BY purchase DESC
    """


# =========================
# GLOBAL CONVERSION RATE
# =========================
def get_conversion_rate_query():
    return """
    SELECT
      SAFE_DIVIDE(
        COUNT(DISTINCT IF(event_name = 'purchase', user_pseudo_id, NULL)),
        COUNT(DISTINCT IF(event_name = 'page_view', user_pseudo_id, NULL))
      ) AS conversion_rate
    FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
    """

# =========================
# COHORT RETENTION RATE
# =========================
def get_cohort_retention_rate_query():
    return """
    WITH user_first_touch AS (
      SELECT
        user_pseudo_id,
        DATE(MIN(TIMESTAMP_MICROS(event_timestamp))) AS cohort_date
      FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
      GROUP BY user_pseudo_id
    ),

    user_activity AS (
      SELECT
        e.user_pseudo_id,
        DATE(TIMESTAMP_MICROS(e.event_timestamp)) AS activity_date,
        u.cohort_date
      FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` e
      JOIN user_first_touch u
        ON e.user_pseudo_id = u.user_pseudo_id
    ),

    cohort_size AS (
      SELECT
        cohort_date,
        COUNT(DISTINCT user_pseudo_id) AS cohort_users
      FROM user_first_touch
      GROUP BY cohort_date
    ),

    cohort_activity AS (
      SELECT
        cohort_date,
        DATE_DIFF(activity_date, cohort_date, DAY) AS days_since_signup,
        COUNT(DISTINCT user_pseudo_id) AS active_users
      FROM user_activity
      GROUP BY cohort_date, days_since_signup
    )

    SELECT
      a.cohort_date,
      a.days_since_signup,
      a.active_users,
      c.cohort_users,
      SAFE_DIVIDE(a.active_users, c.cohort_users) AS retention_rate
    FROM cohort_activity a
    JOIN cohort_size c
      ON a.cohort_date = c.cohort_date
    ORDER BY a.cohort_date, a.days_since_signup
    """

# =========================
# MAIN (FOR DEBUG / TEST)
# =========================
def main():
    print("=== QUERY PREVIEW ===\n")

    print("User Level Funnel Query:\n")
    print(get_user_level_funnel_query())

    print("\n---\nFunnel Overview Query:\n")
    print(get_funnel_overview_query())

    print("\n---\nFunnel Over Time Query:\n")
    print(get_funnel_over_time_query())

    print("\n---\nFunnel By Device Query:\n")
    print(get_funnel_by_device_query())

    print("\n---\nFunnel By Source Query:\n")
    print(get_funnel_by_source_query())

    print("\n---\nConversion Rate Query:\n")
    print(get_conversion_rate_query())

    print("\n---\nCohort Retention Rate Query:\n")
    print(get_cohort_retention_rate_query())




if __name__ == "__main__":
    main()