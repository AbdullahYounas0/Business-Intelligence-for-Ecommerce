from fastapi import APIRouter, HTTPException
from src.modules.churn.scorer import get_at_risk_customers
from src.modules.churn.winback import generate_winback_email

router = APIRouter()


@router.get("/at-risk")
async def at_risk(page: int = 1, page_size: int = 20):
    customers = await get_at_risk_customers()
    start = (page - 1) * page_size
    return {
        "total": len(customers),
        "page": page,
        "customers": customers[start: start + page_size],
    }


@router.post("/winback/{customer_id}")
async def winback(customer_id: str):
    customers = await get_at_risk_customers()
    customer = next((c for c in customers if c["customer_id"] == customer_id), None)
    if not customer:
        raise HTTPException(404, "Customer not found")
    email = await generate_winback_email(customer)
    return {"customer_id": customer_id, "email": email}


@router.post("/trigger")
async def trigger_churn():
    from src.modules.churn.scorer import run_churn_job
    await run_churn_job()
    customers = await get_at_risk_customers()
    return {"triggered": True, "at_risk_count": len(customers)}


@router.get("/history")
async def history():
    import os
    if not os.environ.get("GOOGLE_CLOUD_PROJECT"):
        return {"records": []}
    from src.shared.bigquery_client import BigQueryClient
    bq = BigQueryClient()
    return {"records": bq.query(
        f"SELECT * FROM `{bq.table(bq.features, 'rfm_scores')}` ORDER BY created_at DESC LIMIT 100"
    )}
