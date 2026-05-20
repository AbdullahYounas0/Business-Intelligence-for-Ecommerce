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


app = FastAPI(title="E-Commerce Intelligence Hub")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
