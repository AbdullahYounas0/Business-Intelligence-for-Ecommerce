import pytest
from src.ingestion.mock_data import mock_reviews, mock_sentiment_summary
from src.shared.pii_masker import mask


def test_mock_reviews_have_required_fields():
    reviews = mock_reviews()
    required = {"review_id", "product_id", "rating", "body", "created_at"}
    for r in reviews:
        assert required.issubset(r.keys())


def test_mock_reviews_ratings_in_range():
    reviews = mock_reviews()
    for r in reviews:
        assert 1 <= r["rating"] <= 5


def test_sentiment_summary_has_breakdown():
    summary = mock_sentiment_summary()
    assert "breakdown" in summary
    assert {"positive", "neutral", "negative"} == set(summary["breakdown"].keys())


def test_sentiment_by_topic_is_list():
    summary = mock_sentiment_summary()
    assert isinstance(summary["by_topic"], list)
    assert len(summary["by_topic"]) > 0


def test_pii_masker_passthrough_when_presidio_unavailable():
    text = "Hello World"
    result = mask(text)
    assert isinstance(result, str)
    assert len(result) > 0
