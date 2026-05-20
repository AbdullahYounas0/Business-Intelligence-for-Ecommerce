import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

_scheduler = AsyncIOScheduler()
logger = logging.getLogger(__name__)
