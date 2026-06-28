import json

import websocket

from backend.network_collector import (
    collect_network
)


def get_live_metrics():

    try:

        ws = websocket.create_connection(
            "ws://127.0.0.1:8000/telemetry",
            timeout=2
        )

        data = ws.recv()

        ws.close()

        return json.loads(
            data
        )

    except Exception:

        return collect_network()
