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
