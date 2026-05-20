from src.shared import gpt_client


async def enrich_alerts(alerts: list[dict]) -> list[dict]:
    enriched = []
    for alert in alerts:
        if alert.get("gpt_recommendation"):
            enriched.append(alert)
            continue
        try:
            rec = await _generate_recommendation(alert)
            enriched.append({**alert, "gpt_recommendation": rec})
        except Exception:
            enriched.append({**alert, "gpt_recommendation": "Unable to generate recommendation."})
    return enriched


async def _generate_recommendation(alert: dict) -> str:
    context = {
        "low_stock": f"Product '{alert.get('product_title')}' (SKU: {alert.get('sku')}) has {alert.get('units_available')} units with {alert.get('pending_orders')} pending orders.",
        "stalled_order": f"Order {alert.get('order_id')} for '{alert.get('product_title')}' has been unfulfilled for {alert.get('age_hours')} hours.",
        "demand_spike": f"Demand spike detected for '{alert.get('product_title')}'. Current stock: {alert.get('units_available')} units.",
    }.get(alert["type"], f"Alert type: {alert['type']}")

    prompt = f"{context}\n\nWrite a one-sentence plain-English action recommendation for the operations team."
    return await gpt_client.chat(
        module="inventory",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
    )
