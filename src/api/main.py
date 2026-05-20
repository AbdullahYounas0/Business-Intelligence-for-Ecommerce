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


@app.get("/analytics/costs")
async def costs():
    if not os.environ.get("GOOGLE_CLOUD_PROJECT"):
        from src.shared.bigquery_client import _mock_cost_audit
        return _mock_cost_audit()
    from src.shared.bigquery_client import BigQueryClient
    bq = BigQueryClient()
    return await bq.get_cost_audit()


@app.get("/bigquery/debug")
async def bq_debug():
    """Shows exactly what datasets/tables/rows exist in BigQuery."""
    if not os.environ.get("GOOGLE_CLOUD_PROJECT"):
        return {"mode": "mock", "project": None}
    try:
        from src.shared.bigquery_client import BigQueryClient
        bq = BigQueryClient()
        project = bq.project
        datasets = [ds.dataset_id for ds in bq.client.list_datasets()]
        tables: dict = {}
        for ds in [bq.raw, bq.features, bq.audit]:
            try:
                tbls = list(bq.client.list_tables(f"{project}.{ds}"))
                tables[ds] = {}
                for t in tbls:
                    try:
                        count = bq.query(f"SELECT COUNT(*) as n FROM `{project}.{ds}.{t.table_id}`")
                        tables[ds][t.table_id] = count[0]["n"] if count else 0
                    except Exception as e:
                        tables[ds][t.table_id] = f"error: {e}"
            except Exception as e:
                tables[ds] = f"error listing: {e}"
        return {
            "project": project,
            "datasets_in_project": datasets,
            "configured_datasets": {
                "raw": bq.raw, "features": bq.features, "audit": bq.audit
            },
            "tables_and_rows": tables,
        }
    except Exception as e:
        import traceback
        return {"error": str(e), "detail": traceback.format_exc()}


@app.post("/demo")
async def seed_demo():
    from src.ingestion.mock_data import seed_all
    try:
        return await seed_all()
    except Exception as e:
        import traceback
        return {"error": str(e), "detail": traceback.format_exc()}


# ── Static frontend — must be last ───────────────────────────────────────────
_dist = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist")
if os.path.exists(_dist):
    from fastapi.staticfiles import StaticFiles
    app.mount("/", StaticFiles(directory=_dist, html=True), name="frontend")
