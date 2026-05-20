import os
import json
import logging
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)


# ── WebSocket manager ────────────────────────────────────────────────────────

class ConnectionManager:
    def __init__(self):
        self._active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self._active.append(ws)
        logger.info("WS connected — %d client(s)", len(self._active))

    def disconnect(self, ws: WebSocket):
        try:
            self._active.remove(ws)
        except ValueError:
            pass
        logger.info("WS disconnected — %d client(s) remaining", len(self._active))

    async def broadcast(self, message: dict):
        payload = json.dumps(message)
        clients = list(self._active)
        dead: list[WebSocket] = []
        for ws in clients:
            try:
                await ws.send_text(payload)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)


manager = ConnectionManager()


from contextlib import asynccontextmanager

from src.modules.churn.routes import router as churn_router
from src.modules.inventory.routes import router as inventory_router
from src.modules.sentiment.routes import router as sentiment_router
from src.ingestion.webhook_handler import router as ingest_router
from src.shared.scheduler import start_scheduler, shutdown_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ws_manager = manager
    try:
        start_scheduler(manager)
    except Exception as e:
        logger.error("Scheduler failed to start: %s", e)
    yield
    shutdown_scheduler()


app = FastAPI(title="E-Commerce Intelligence Hub", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(churn_router,    prefix="/churn",     tags=["Churn"])
app.include_router(inventory_router, prefix="/inventory", tags=["Inventory"])
app.include_router(sentiment_router, prefix="/sentiment", tags=["Sentiment"])
app.include_router(ingest_router,   prefix="/ingest",    tags=["Ingestion"])


@app.get("/health")
async def health():
    return {"status": "ok", "clients": len(manager._active)}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            msg = await websocket.receive()
            if msg.get("type") == "websocket.disconnect":
                break
    except Exception as e:
        logger.debug("WS exception (normal on browser close): %s", type(e).__name__)
    finally:
        manager.disconnect(websocket)
