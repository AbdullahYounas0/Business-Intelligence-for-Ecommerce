import os
import logging
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

logger = logging.getLogger(__name__)

# ── Schema definitions ────────────────────────────────────────────────────────

S = bigquery.SchemaField

_SCHEMAS: dict[str, list] = {
    "orders": [
        S("order_id", "STRING"), S("customer_id", "STRING"),
        S("customer_name", "STRING"), S("customer_email", "STRING"),
        S("product_id", "STRING"), S("product_title", "STRING"),
        S("total_price", "FLOAT"), S("status", "STRING"),
        S("created_at", "TIMESTAMP"),
    ],
    "products": [
        S("product_id", "STRING"), S("title", "STRING"), S("sku", "STRING"),
        S("category", "STRING"), S("units_available", "INTEGER"),
        S("reorder_threshold", "INTEGER"), S("pending_orders", "INTEGER"),
        S("price", "FLOAT"), S("updated_at", "TIMESTAMP"),
    ],
    "reviews": [
        S("review_id", "STRING"), S("product_id", "STRING"),
        S("customer_name", "STRING"), S("rating", "INTEGER"),
        S("body", "STRING"), S("created_at", "TIMESTAMP"),
    ],
    "rfm_scores": [
        S("customer_id", "STRING"), S("name", "STRING"), S("email", "STRING"),
        S("rfm_score", "INTEGER"), S("recency_days", "INTEGER"),
        S("frequency", "INTEGER"), S("monetary", "FLOAT"),
        S("lifetime_value", "FLOAT"), S("last_order_date", "STRING"),
        S("created_at", "TIMESTAMP"),
    ],
    "inventory_alerts": [
        S("alert_id", "STRING"), S("type", "STRING"), S("severity", "STRING"),
        S("product_id", "STRING"), S("product_title", "STRING"), S("sku", "STRING"),
        S("units_available", "INTEGER"), S("pending_orders", "INTEGER"),
        S("gpt_recommendation", "STRING"), S("created_at", "TIMESTAMP"),
    ],
    "review_analysis": [
        S("review_id", "STRING"), S("product_id", "STRING"),
        S("rating", "INTEGER"), S("body", "STRING"),
        S("sentiment", "STRING"),
        S("topics", "STRING", mode="REPEATED"),
        S("urgent", "BOOL"), S("created_at", "TIMESTAMP"),
    ],
    "gpt_calls": [
        S("module", "STRING"), S("model", "STRING"),
        S("prompt_tokens", "INTEGER"), S("completion_tokens", "INTEGER"),
        S("cost_usd", "FLOAT"), S("created_at", "TIMESTAMP"),
    ],
}

_DATASET_FOR_TABLE = {
    "orders": "raw", "products": "raw", "reviews": "raw",
    "rfm_scores": "features", "inventory_alerts": "features", "review_analysis": "features",
    "gpt_calls": "audit",
}
