from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect
)
from fastapi.middleware.cors import (
    CORSMiddleware,
)

import asyncio

from backend.telemetry import (
    generate_metrics
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_methods=[
        "*"
    ],
    allow_headers=[
        "*"
    ],
)


@app.get(
    "/"
)
def health():
    return {
        "status": "running"
    }


@app.websocket(
    "/telemetry"
)
async def telemetry(
    websocket: WebSocket
):

    await websocket.accept()

    try:

        while True:

            data = (
                generate_metrics()
            )

            await websocket.send_json(
                data
            )

            await asyncio.sleep(
                5
            )

    except WebSocketDisconnect:
        pass

    except Exception:
        pass
