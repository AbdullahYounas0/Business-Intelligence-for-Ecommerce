import os
import json
import logging
from src.shared import gpt_client
from src.shared.pii_masker import mask

logger = logging.getLogger(__name__)


async def classify_review(review: dict) -> dict:
    text = mask(review.get("body", ""))
    rating = review.get("rating", 3)

    prompt = f"""Classify this e-commerce product review.
Rating: {rating}/5
Review: "{text}"

Return JSON with:
- sentiment: "positive" | "neutral" | "negative"
- topics: array of tags from [shipping, quality, sizing, returns, packaging, other]
- urgent: true if rating <= 2 AND contains words like broken/never arrived/refund/dangerous/fraud"""

    raw = await gpt_client.chat(
        module="sentiment",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
    )

    try:
        import re
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        result = json.loads(match.group()) if match else {}
    except Exception:
        result = {}

    return {
        **review,
        "sentiment": result.get("sentiment", "neutral"),
        "topics": result.get("topics", []),
        "urgent": result.get("urgent", False),
    }


async def run_sentiment_job(ws_manager=None):
    logger.info("Sentiment job started")
    try:
        reviews = await _get_unclassified_reviews()
        for review in reviews:
            await classify_review(review)
    except Exception as e:
        logger.error(f"Sentiment job failed: {e}")


async def _get_unclassified_reviews() -> list[dict]:
    if not os.environ.get("GOOGLE_CLOUD_PROJECT"):
        from src.ingestion.mock_data import mock_reviews
        return mock_reviews()[:10]
    from src.shared.bigquery_client import BigQueryClient
    bq = BigQueryClient()
    return bq.query(
        f"SELECT r.* FROM `{bq.table(bq.raw, 'reviews')}` r "
        f"LEFT JOIN `{bq.table(bq.features, 'review_analysis')}` a USING (review_id) "
        f"WHERE a.review_id IS NULL LIMIT 100"
    )
