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
