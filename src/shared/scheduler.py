import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

_scheduler = AsyncIOScheduler()
logger = logging.getLogger(__name__)


def start_scheduler(ws_manager):
    from src.modules.churn.scorer import run_churn_job
    from src.modules.inventory.monitor import run_inventory_job
    from src.modules.sentiment.classifier import run_sentiment_job

    _scheduler.add_job(run_churn_job, "cron", hour=2, minute=0, args=[ws_manager])
    _scheduler.add_job(run_inventory_job, "interval", minutes=15, args=[ws_manager])
    _scheduler.add_job(run_sentiment_job, "cron", hour=3, minute=0, args=[ws_manager])

    # Weekly narrative: Monday 7am
    from src.modules.sentiment.reporter import run_weekly_narrative
    _scheduler.add_job(run_weekly_narrative, "cron", day_of_week="mon", hour=7)

    _scheduler.start()
    logger.info("Scheduler started")


def shutdown_scheduler():
    if _scheduler.running:
        _scheduler.shutdown(wait=False)
