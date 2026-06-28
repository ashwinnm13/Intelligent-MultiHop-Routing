import json

import websocket


def get_live_metrics():

    ws = websocket.create_connection(
        "ws://127.0.0.1:8000/telemetry"
    )

    data = ws.recv()

    ws.close()

    return json.loads(
        data
    )
