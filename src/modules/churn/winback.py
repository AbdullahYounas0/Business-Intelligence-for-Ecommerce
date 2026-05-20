from src.shared import gpt_client
from src.shared.bigquery_client import BigQueryClient


async def generate_winback_email(customer: dict) -> dict:
    prompt = f"""You are a retention email specialist for an e-commerce brand.

Customer profile:
- Name: {customer['name']}
- Last order: {customer['last_order_date']} ({customer['recency_days']} days ago)
- Total orders: {customer['frequency']}
- Lifetime value: ${customer['lifetime_value']:.2f}
- RFM score: {customer['rfm_score']}/100

Write a short, personalized win-back email. Be warm but not desperate.
Return JSON with keys: subject, body (plain text, 3 paragraphs max)."""

    bq = BigQueryClient() if _bq_available() else None
    raw = await gpt_client.chat(
        module="churn",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        bq_client=bq,
    )

    import json, re
    try:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        return json.loads(match.group()) if match else {"subject": "We miss you!", "body": raw}
    except Exception:
        return {"subject": "We miss you!", "body": raw}


def _bq_available() -> bool:
    import os
    return bool(os.environ.get("GOOGLE_CLOUD_PROJECT"))
