from fastapi import APIRouter
from src.modules.inventory.monitor import get_active_alerts
from src.modules.inventory.alerter import enrich_alerts

router = APIRouter()


@router.get("/alerts")
async def alerts():
    raw = await get_active_alerts()
    enriched = await enrich_alerts(raw)
    return {"alerts": enriched}


@router.get("/forecast")
async def forecast():
    import os
    if not os.environ.get("GOOGLE_CLOUD_PROJECT"):
        return {"forecasts": [
            {"product_id": "prod-003", "sku": "SKU-003", "title": "Product 3",
             "units_available": 3, "daily_velocity": 4.2, "days_until_stockout": 0.7},
            {"product_id": "prod-008", "sku": "SKU-008", "title": "Product 8",
             "units_available": 12, "daily_velocity": 1.5, "days_until_stockout": 8.0},
        ]}
    from src.shared.bigquery_client import BigQueryClient
    bq = BigQueryClient()
    return {"forecasts": bq.query(
        f"SELECT * FROM `{bq.table(bq.features, 'inventory_alerts')}` LIMIT 50"
    )}


@router.post("/trigger")
async def trigger_inventory():
    from src.modules.inventory.monitor import run_inventory_job
    await run_inventory_job()
    raw = await get_active_alerts()
    enriched = await enrich_alerts(raw)
    return {"triggered": True, "alert_count": len(enriched)}


@router.get("/history")
async def history():
    import os
    if not os.environ.get("GOOGLE_CLOUD_PROJECT"):
        return {"records": []}
    from src.shared.bigquery_client import BigQueryClient
    bq = BigQueryClient()
    return {"records": bq.query(
        f"SELECT * FROM `{bq.table(bq.features, 'inventory_alerts')}` ORDER BY created_at DESC LIMIT 100"
    )}
