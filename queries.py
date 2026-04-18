
def get_funnel_query():
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

        MAX(CASE WHEN event_name = 'page_view' THEN 1 ELSE 0 END) AS page_view,
        MAX(CASE WHEN event_name = 'view_item' THEN 1 ELSE 0 END) AS view_item,
        MAX(CASE WHEN event_name = 'add_to_cart' THEN 1 ELSE 0 END) AS add_to_cart,
        MAX(CASE WHEN event_name = 'begin_checkout' THEN 1 ELSE 0 END) AS begin_checkout,
        MAX(CASE WHEN event_name = 'purchase' THEN 1 ELSE 0 END) AS purchase,

        ANY_VALUE(device) AS device,
        ANY_VALUE(source) AS source,
        ANY_VALUE(first_touch) AS first_touch

      FROM enriched
      GROUP BY user_pseudo_id
    )

    SELECT * FROM user_level
    """


def main():
    print("Previewing funnel query:\n")
    print(get_funnel_query())


if __name__ == "__main__":
    main()