from google.cloud import bigquery

client = bigquery.Client.from_service_account_json(
    "marketing-funnel-project-1b31b1d8b837.json"
)

query = """
SELECT
  COUNT(DISTINCT CASE WHEN event_name = 'page_view' THEN user_pseudo_id END) AS page_view,
  COUNT(DISTINCT CASE WHEN event_name = 'view_item' THEN user_pseudo_id END) AS view_item,
  COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN user_pseudo_id END) AS add_to_cart,
  COUNT(DISTINCT CASE WHEN event_name = 'begin_checkout' THEN user_pseudo_id END) AS checkout,
  COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_pseudo_id END) AS purchase
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
"""

df = client.query(query).to_dataframe()
print(df)