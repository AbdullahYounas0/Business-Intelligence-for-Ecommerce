import os
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)
_REORDER    = int(os.environ.get("INVENTORY_REORDER_THRESHOLD", "10"))
_STALL_HOURS = int(os.environ.get("STALLED_ORDER_HOURS", "24"))


def detect_anomalies(products: list[dict], orders: list[dict]) -> list[dict]:
    alerts = []
    now = datetime.now(timezone.utc)

    for p in products:
        units   = int(p.get("units_available", 999))
        pending = int(p.get("pending_orders", 0))
        if units < _REORDER and pending > 0:
            alerts.append({
                "type":            "low_stock",
                "severity":        "high" if units < 5 else "medium",
                "product_id":      p["product_id"],
                "product_title":   p.get("title", ""),
                "sku":             p.get("sku", ""),
                "units_available": units,
                "pending_orders":  pending,
                "created_at":      now.isoformat(),
            })

    for o in orders:
        if o.get("status") != "unfulfilled":
            continue
        try:
            created = datetime.fromisoformat(str(o["created_at"]).replace("Z", "+00:00"))
            if created.tzinfo is None:
                created = created.replace(tzinfo=timezone.utc)
            age_hours = (now - created).total_seconds() / 3600
            if age_hours > _STALL_HOURS:
                alerts.append({
                    "type":            "stalled_order",
                    "severity":        "medium",
                    "product_id":      o.get("product_id", ""),
                    "product_title":   o.get("product_title", ""),
                    "sku":             o.get("sku", ""),
                    "order_id":        o.get("order_id"),
                    "age_hours":       round(age_hours, 1),
                    "units_available": None,
                    "pending_orders":  None,
                    "created_at":      now.isoformat(),
                })
        except Exception:
            continue

    return alerts


async def get_active_alerts() -> list[dict]:
    if not os.environ.get("GOOGLE_CLOUD_PROJECT"):
        from src.ingestion.mock_data import mock_inventory_alerts
        return mock_inventory_alerts()

    from src.shared.bigquery_client import BigQueryClient
    bq = BigQueryClient()
    products = bq.query(f"SELECT * FROM `{bq.table(bq.raw, 'products')}`")
    orders   = bq.query(
        f"SELECT * FROM `{bq.table(bq.raw, 'orders')}` WHERE status = 'unfulfilled'"
    )
    return detect_anomalies(products, orders)
