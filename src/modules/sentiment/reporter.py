import logging
from src.shared import gpt_client

logger = logging.getLogger(__name__)


async def run_weekly_narrative():
    logger.info("Generating weekly sentiment narrative")
    try:
        summary = await _get_week_summary()
        narrative = await _generate_narrative(summary)
        logger.info("Weekly narrative generated")
        return narrative
    except Exception as e:
        logger.error(f"Narrative generation failed: {e}")
        return ""


async def _get_week_summary() -> dict:
    import os
    if not os.environ.get("SHOPIFY_API_KEY"):
        from src.ingestion.mock_data import mock_sentiment_summary
        return mock_sentiment_summary()
    from src.shared.bigquery_client import BigQueryClient
    bq = BigQueryClient()
    rows = bq.query(f"""
        SELECT sentiment, topics, COUNT(*) as count
        FROM `{bq.table(bq.features, 'review_analysis')}`
        WHERE DATE(created_at) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
        GROUP BY sentiment, topics
    """)
    return {"rows": rows}


async def _generate_narrative(summary: dict) -> str:
    prompt = f"""You are an e-commerce analyst. Summarize this week's customer review data for an executive report.

Data: {summary}

Write 2-3 paragraphs: overall trend, key topics of praise, key topics of complaint, and one recommended action.
Be specific and data-driven."""

    return await gpt_client.chat(
        module="sentiment",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
    )
