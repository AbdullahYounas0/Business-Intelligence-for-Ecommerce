import os
import logging
import resend

logger = logging.getLogger(__name__)


async def send_digest(churn_customers: list[dict], inventory_alerts: list[dict], sentiment: dict) -> None:
    api_key = os.environ.get("RESEND_API_KEY")
    to_email = os.environ.get("DIGEST_EMAIL_TO")
    if not api_key or not to_email:
        logger.info("Digest email skipped — Resend not configured")
        return

    resend.api_key = api_key
    html = _build_html(churn_customers, inventory_alerts, sentiment)
    try:
        resend.Emails.send({
            "from": "info@flowerzone.ae",
            "to": to_email,
            "subject": "Weekly E-Commerce Intelligence Digest",
            "html": html,
        })
        logger.info("Digest email sent")
    except Exception as e:
        logger.error(f"Resend error: {e}")


def _build_html(churn: list[dict], inventory: list[dict], sentiment: dict) -> str:
    churn_rows = "".join(
        f"<tr><td>{c['name']}</td><td>{c['rfm_score']}</td><td>{c['last_order_date']}</td><td>${c['lifetime_value']:.2f}</td></tr>"
        for c in churn[:10]
    )
    inv_rows = "".join(
        f"<tr><td>{a.get('product_title')}</td><td>{a.get('type')}</td><td>{a.get('gpt_recommendation','')}</td></tr>"
        for a in inventory[:5]
    )
    narrative = sentiment.get("narrative", "No narrative available.")

    return f"""
<html><body style="font-family:sans-serif;max-width:700px;margin:auto">
<h1>Weekly E-Commerce Intelligence Digest</h1>
<h2>🔴 At-Risk Customers ({len(churn)})</h2>
<table border="1" cellpadding="6" width="100%">
<tr><th>Name</th><th>RFM</th><th>Last Order</th><th>LTV</th></tr>
{churn_rows}
</table>
<h2>⚠️ Inventory Alerts ({len(inventory)})</h2>
<table border="1" cellpadding="6" width="100%">
<tr><th>Product</th><th>Type</th><th>Recommendation</th></tr>
{inv_rows}
</table>
<h2>📊 Sentiment Summary</h2>
<p>{narrative}</p>
</body></html>"""
