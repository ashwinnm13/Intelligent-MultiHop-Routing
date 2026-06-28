from fastapi import (
    FastAPI,
    WebSocket
)

import asyncio

from backend.telemetry import (
    generate_metrics
)

app = FastAPI()


@app.websocket(
    "/telemetry"
)
async def telemetry(
    websocket: WebSocket
):

    await websocket.accept()

    while True:

        data = (
            generate_metrics()
        )

        await websocket.send_json(
            data
        )

        await asyncio.sleep(
            2
        )
