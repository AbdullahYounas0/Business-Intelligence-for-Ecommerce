# WebSocket manager is in src/api/main.py (ConnectionManager).
# This module re-exports a helper for broadcasting from background jobs.

async def broadcast_from_job(app_state, message: dict) -> None:
    manager = getattr(app_state, "ws_manager", None)
    if manager:
        await manager.broadcast(message)
