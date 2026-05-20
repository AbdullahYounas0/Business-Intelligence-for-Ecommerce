import logging
from fastapi import APIRouter, Request, UploadFile, File, HTTPException

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/webhook/{source}")
async def receive_webhook(source: str, request: Request):
    payload = await request.json()
    logger.info(f"Webhook received from {source}: {list(payload.keys())}")

    import os
    if not os.environ.get("GOOGLE_CLOUD_PROJECT"):
        return {"received": True, "source": source, "note": "mock mode — not persisted"}

    from src.shared.bigquery_client import BigQueryClient
    bq = BigQueryClient()
    bq.insert_rows(bq.raw, "orders", [payload])
    return {"received": True, "source": source}


@router.post("/upload")
async def upload_csv(table: str, file: UploadFile = File(...)):
    allowed = {"orders", "products", "reviews"}
    if table not in allowed:
        raise HTTPException(400, f"table must be one of {allowed}")

    from src.ingestion.csv_loader import load_csv_to_rows
    _required = {
        "orders": ["order_id", "customer_id", "total_price", "status", "created_at"],
        "products": ["product_id", "title", "sku", "units_available"],
        "reviews": ["review_id", "product_id", "rating", "body", "created_at"],
    }
    rows = await load_csv_to_rows(file, _required[table])

    import os
    if not os.environ.get("GOOGLE_CLOUD_PROJECT"):
        return {"uploaded": len(rows), "note": "mock mode — not persisted to BigQuery"}

    from src.shared.bigquery_client import BigQueryClient
    bq = BigQueryClient()
    bq.insert_rows(bq.raw, table, rows)
    return {"uploaded": len(rows)}
