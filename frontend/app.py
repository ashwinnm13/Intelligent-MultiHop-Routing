import sys
from datetime import datetime
from pathlib import Path

sys.path.append(
    str(
        Path(__file__).resolve().parent.parent
    )
)

import streamlit as st
from streamlit_autorefresh import (
    st_autorefresh,
)

from backend.explainer import (
    explain_route,
)
from backend.metrics import (
    route_metrics,
)
from backend.network_health import (
    evaluate_health,
)
from backend.report import (
    generate_report,
)
from backend.trigger import (
    should_retrain,
)
from frontend.live_telemetry import (
    get_live_metrics,
)
from frontend.visualizer import (
    draw_route,
)
from rl_engine.inference import (
    get_best_route,
)
from rl_engine.topology import (
    adjacency_matrix,
)
from rl_engine.train import (
    train,
)


MAX_HISTORY_POINTS = 30


def format_number(value):
    if isinstance(value, float):
        return f"{value:.2f}".rstrip("0").rstrip(".")

    return str(value)


st.set_page_config(
    page_title="RouteFlux",
    layout="wide",
)

st.title(
    "Intelligent Multihop Routing"
)

st.caption(
    "Live telemetry-driven adaptive routing"
)

telemetry = (
    get_live_metrics()
)

is_congested = (
    should_retrain(
        telemetry
    )
)

if "latency_history" not in st.session_state:
    st.session_state.latency_history = []

if "loss_history" not in st.session_state:
    st.session_state.loss_history = []

if "selected_route" not in st.session_state:
    st.session_state.selected_route = None

if "events" not in st.session_state:
    st.session_state.events = []

if "decision_count" not in st.session_state:
    st.session_state.decision_count = 0

st.session_state.latency_history.append(
    telemetry[
        "latency"
    ]
)
st.session_state.loss_history.append(
    telemetry[
        "loss"
    ]
)

st.session_state.latency_history = (
    st.session_state.latency_history[
        -MAX_HISTORY_POINTS:
    ]
)
st.session_state.loss_history = (
    st.session_state.loss_history[
        -MAX_HISTORY_POINTS:
    ]
)


st.subheader(
    "Live Telemetry Metrics"
)

metric_latency, metric_loss, metric_bandwidth = (
    st.columns(3)
)

metric_latency.metric(
    "Latency",
    f"{format_number(telemetry['latency'])} ms",
)
metric_loss.metric(
    "Packet Loss",
    f"{format_number(telemetry['loss'])} %",
)
metric_bandwidth.metric(
    "Bandwidth",
    f"{format_number(telemetry['bandwidth'])} Mbps",
)

st.subheader(
    "Network Status"
)

if is_congested:
    st.warning(
        "Congested"
    )
else:
    st.success(
        "Stable"
    )

st.divider()

controls_left, controls_right = (
    st.columns(
        [
            1,
            4,
        ]
    )
)

with controls_left:
    live_mode = st.toggle(
        "Live Mode",
        value=False,
    )

with controls_right:
    train_route = st.button(
        "Train Route",
        type="primary",
    )

if live_mode:
    st_autorefresh(
        interval=5000,
        key="refresh",
    )

if train_route:
    with st.spinner(
        "Training route from live telemetry..."
    ):
        agent, _ = train(
            telemetry=telemetry
        )
        st.session_state.selected_route = (
            get_best_route(
                agent,
                adjacency_matrix,
            )
        )

        metrics = route_metrics(
            st.session_state.selected_route,
            telemetry,
        )

        st.session_state.decision_count += 1

        st.session_state.events.append({
            "id": st.session_state.decision_count,
            "time": datetime.now().strftime(
                "%H:%M:%S"
            ),
            "route": " -> ".join(
                map(
                    str,
                    st.session_state.selected_route,
                )
            ),
            "reason": explain_route(
                metrics
            ),
            "latency": telemetry[
                "latency"
            ],
            "loss": telemetry[
                "loss"
            ],
            "reward": metrics[
                "reward"
            ],
        })

    st.success(
        "Route trained from current telemetry"
    )

st.divider()

st.subheader(
    "Current Selected Route"
)

if st.session_state.selected_route is None:
    st.info(
        "Press Train Route to generate a route from the current telemetry snapshot."
    )
else:
    route = st.session_state.selected_route
    metrics = route_metrics(
        route,
        telemetry,
    )
    status = evaluate_health(
        metrics[
            "latency"
        ],
        metrics[
            "loss"
        ],
    )
    reason = explain_route(
        metrics
    )

    route_fig = draw_route(
        route
    )

    graph_left, graph_center, graph_right = st.columns(
        [
            1,
            2,
            1,
        ]
    )

    with graph_center:
        st.pyplot(
            route_fig,
            use_container_width=False,
        )

    st.subheader(
        "Route Explanation"
    )

    detail_a, detail_b, detail_c, detail_d = (
        st.columns(4)
    )

    detail_a.metric(
        "Selected Path",
        " -> ".join(
            map(
                str,
                route,
            )
        ),
    )
    detail_b.metric(
        "Latency",
        f"{format_number(metrics['latency'])} ms",
    )
    detail_c.metric(
        "Packet Loss",
        f"{format_number(metrics['loss'])} %",
    )
    detail_d.metric(
        "Estimated Reward",
        format_number(
            metrics[
                "reward"
            ]
        ),
    )

    st.write(
        reason
    )
    st.success(
        status
    )

    report = generate_report(
        route,
        metrics,
        status,
        telemetry,
        st.session_state.latency_history,
        st.session_state.loss_history,
        route_fig,
    )

    with open(
        report,
        "rb",
    ) as file:
        st.download_button(
            "Download Report",
            file,
            file_name="RouteFlux_Report.pdf",
            mime="application/pdf",
        )

st.divider()

st.subheader(
    "Latency Trend"
)
st.line_chart(
    st.session_state.latency_history,
    color="#FF4B4B",
)

st.subheader(
    "Packet Loss Trend"
)
st.line_chart(
    st.session_state.loss_history,
    color="#0068C9",
)

if st.session_state.events:
    st.divider()
    st.subheader(
        "Route Decision Timeline"
    )
    st.caption(
        "A new decision is recorded each time Train Route is pressed."
    )

    for event in reversed(
        st.session_state.events[-10:]
    ):
        st.markdown(
            f"""
**Decision #{event['id']} · {event['time']}**

Route: {event['route']}

Telemetry: {format_number(event['latency'])} ms, {format_number(event['loss'])} % loss

Estimated Reward: {format_number(event['reward'])}

Reason: {event['reason']}
"""
        )
