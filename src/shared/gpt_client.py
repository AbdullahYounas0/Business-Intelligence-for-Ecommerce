import os
import time
from datetime import datetime, timezone
from openai import AsyncOpenAI


_COST_PER_1K = {"gpt-4o": {"prompt": 0.0025, "completion": 0.01}}

client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))


async def chat(
    module: str,
    messages: list[dict],
    model: str = "gpt-4o",
    max_tokens: int = 1024,
    bq_client=None,
) -> str:
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.7,
    )
    content = response.choices[0].message.content or ""
    usage = response.usage

    if bq_client and usage:
        rates = _COST_PER_1K.get(model, {"prompt": 0.0025, "completion": 0.01})
        cost = (usage.prompt_tokens / 1000 * rates["prompt"]) + \
               (usage.completion_tokens / 1000 * rates["completion"])
        try:
            bq_client.insert_rows(bq_client.audit, "gpt_calls", [{
                "module": module,
                "model": model,
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "cost_usd": round(cost, 6),
                "created_at": datetime.now(timezone.utc).isoformat(),
            }])
        except Exception:
            pass

    return content
