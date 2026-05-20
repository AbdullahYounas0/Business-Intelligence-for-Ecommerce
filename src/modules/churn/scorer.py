import os
import logging
from collections import defaultdict
from datetime import datetime, timezone

logger = logging.getLogger(__name__)
_THRESHOLD = int(os.environ.get("CHURN_RFM_THRESHOLD", "30"))


def compute_rfm(orders: list[dict]) -> list[dict]:
    now = datetime.now(timezone.utc)
    customer_orders: dict = defaultdict(list)
    for o in orders:
        customer_orders[o["customer_id"]].append(o)

    results = []
    for cid, corders in customer_orders.items():
        latest = max(corders, key=lambda x: x["created_at"])
        try:
            last_dt = datetime.fromisoformat(str(latest["created_at"]).replace("Z", "+00:00"))
            if last_dt.tzinfo is None:
                last_dt = last_dt.replace(tzinfo=timezone.utc)
            recency = (now - last_dt).days
        except Exception:
            recency = 999

        frequency = len(corders)
        monetary  = sum(float(o.get("total_price", 0)) for o in corders)
        r_score   = max(0, 100 - recency)
        f_score   = min(100, frequency * 10)
        m_score   = min(100, int(monetary / 20))
        rfm       = int((r_score + f_score + m_score) / 3)

        results.append({
            "customer_id":    cid,
            "name":           latest.get("customer_name", ""),
            "email":          latest.get("customer_email", ""),
            "rfm_score":      rfm,
            "recency_days":   recency,
            "frequency":      frequency,
            "monetary":       round(monetary, 2),
            "lifetime_value": round(monetary, 2),
            "last_order_date": str(latest["created_at"])[:10],
        })
    return results
