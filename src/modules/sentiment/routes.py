from fastapi import APIRouter
from src.ingestion.mock_data import mock_sentiment_summary

router = APIRouter()


@router.get("/summary")
async def summary():
    import os
    if not os.environ.get("GOOGLE_CLOUD_PROJECT"):
        return mock_sentiment_summary()

    from src.shared.bigquery_client import BigQueryClient
    bq = BigQueryClient()

    try:
        topic_rows = bq.query(f"""
            SELECT sentiment, topic, COUNT(*) as count
            FROM `{bq.table(bq.features, 'review_analysis')}`,
            UNNEST(topics) AS topic
            WHERE DATE(created_at) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
            GROUP BY sentiment, topic
            ORDER BY topic, sentiment
        """)

        totals = bq.query(f"""
            SELECT sentiment, COUNT(*) as count
            FROM `{bq.table(bq.features, 'review_analysis')}`
            WHERE DATE(created_at) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
            GROUP BY sentiment
        """)
        total_map = {r["sentiment"]: r["count"] for r in totals}
        total_reviews = sum(total_map.values())

        topic_map: dict = {}
        for r in topic_rows:
            t = r["topic"]
            if t not in topic_map:
                topic_map[t] = {"topic": t, "positive": 0, "neutral": 0, "negative": 0}
            s = r["sentiment"]
            if s in topic_map[t]:
                topic_map[t][s] = r["count"]

        return {
            "period": "last_7_days",
            "total_reviews": total_reviews,
            "breakdown": {
                "positive": total_map.get("positive", 0),
                "neutral":  total_map.get("neutral",  0),
                "negative": total_map.get("negative", 0),
            },
            "by_topic":  list(topic_map.values()),
            "narrative": "",
        }
    except Exception:
        return mock_sentiment_summary()


@router.get("/reviews")
async def reviews(page: int = 1, page_size: int = 20, sentiment: str = None):
    import os
    if not os.environ.get("GOOGLE_CLOUD_PROJECT"):
        from src.ingestion.mock_data import mock_reviews
        return {"reviews": mock_reviews()[:page_size]}
    from src.shared.bigquery_client import BigQueryClient
    bq = BigQueryClient()
    where = f"WHERE sentiment = '{sentiment}'" if sentiment else ""
    return {"reviews": bq.query(
        f"SELECT * FROM `{bq.table(bq.features, 'review_analysis')}` {where} "
        f"ORDER BY created_at DESC LIMIT {page_size} OFFSET {(page-1)*page_size}"
    )}


@router.post("/trigger")
async def trigger_sentiment():
    from src.modules.sentiment.classifier import run_sentiment_job
    await run_sentiment_job()
    return {"triggered": True}


@router.post("/report/generate")
async def generate_report():
    from src.modules.sentiment.reporter import run_weekly_narrative
    narrative = await run_weekly_narrative()
    return {"narrative": narrative}


@router.get("/report")
async def report():
    from src.modules.sentiment.reporter import run_weekly_narrative
    narrative = await run_weekly_narrative()
    return {"narrative": narrative}
