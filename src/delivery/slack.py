import os
import httpx
import logging

logger = logging.getLogger(__name__)


async def send(webhook_env_var: str, text: str, blocks: list[dict] | None = None) -> None:
    url = os.environ.get(webhook_env_var)
    if not url:
        logger.info(f"Slack skipped — {webhook_env_var} not set")
        return
    payload: dict = {"text": text}
    if blocks:
        payload["blocks"] = blocks
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, timeout=10)
            if resp.status_code != 200:
                logger.error(f"Slack error {resp.status_code}: {resp.text}")
            else:
                logger.info(f"Slack sent to {webhook_env_var}")
    except Exception as e:
        logger.error(f"Slack send failed: {e}")


def churn_blocks(customers: list[dict]) -> tuple[str, list[dict]]:
    if not customers:
        return "No at-risk customers today.", []

    lines = "\n".join(
        f"• *{c['name']}* — score {c['rfm_score']}, last order {c['last_order_date']}, LTV ${c.get('lifetime_value', 0):.2f}"
        for c in customers[:10]
    )
    header = f"At-Risk Customers — {len(customers)} flagged today"
    text   = f"*At-Risk Customers* — {len(customers)} flagged\n{lines}"
    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": header, "emoji": False},
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": lines[:2900]},
        },
    ]
    return text, blocks


def inventory_alert_blocks(alert: dict) -> tuple[str, list[dict]]:
    severity   = alert.get("severity", "low")
    alert_type = alert.get("type", "").replace("_", " ").title()
    product    = alert.get("product_title", "Unknown product")
    rec        = alert.get("gpt_recommendation", "No recommendation available.") or "No recommendation available."
    header     = f"Inventory Alert: {alert_type} — {product}"[:150]
    text       = f"*{header}*\n{rec}"
    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": header, "emoji": False},
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": rec[:2900]},
        },
        {
            "type": "context",
            "elements": [
                {"type": "mrkdwn", "text": f"Severity: *{severity}* | SKU: {alert.get('sku', 'N/A')}"}
            ],
        },
    ]
    return text, blocks
