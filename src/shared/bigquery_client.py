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


class BigQueryClient:
    def __init__(self):
        self.project  = os.environ["GOOGLE_CLOUD_PROJECT"]
        self.raw      = os.environ.get("BIGQUERY_DATASET_RAW",      "ecom_raw")
        self.features = os.environ.get("BIGQUERY_DATASET_FEATURES",  "ecom_features")
        self.audit    = os.environ.get("BIGQUERY_DATASET_AUDIT",     "ecom_audit")
        self.client   = bigquery.Client(project=self.project)

    def _ds(self, key: str) -> str:
        return {"raw": self.raw, "features": self.features, "audit": self.audit}[key]

    def table(self, dataset: str, name: str) -> str:
        return f"{self.project}.{dataset}.{name}"

    def query(self, sql: str) -> list[dict]:
        return [dict(row) for row in self.client.query(sql).result()]

    def insert_rows(self, dataset: str, table_name: str, rows: list[dict]) -> None:
        if not rows:
            return
        table_ref = f"{self.project}.{dataset}.{table_name}"
        schema    = _SCHEMAS.get(table_name)
        cfg = bigquery.LoadJobConfig(
            schema=schema,
            write_disposition="WRITE_APPEND",
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        )
        job = self.client.load_table_from_json(rows, table_ref, job_config=cfg)
        job.result()
        if job.errors:
            raise RuntimeError(f"BigQuery load errors: {job.errors}")
