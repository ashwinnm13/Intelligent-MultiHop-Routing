import sys
from pathlib import Path

sys.path.append(
    str(
        Path(__file__).resolve().parent.parent
    )
)

import streamlit as st

from rl_engine.train import train
from rl_engine.inference import (
    get_best_route
)

from backend.metrics import (
    route_metrics
)


st.set_page_config(
    page_title="RouteFlux",
    layout="wide",
)

st.title(
    "🚀 RouteFlux"
)

st.write(
    "AI Multi-Hop Routing Optimizer"
)


if st.button(
    "Train & Find Route"
):

    with st.spinner(
        "Training..."
    ):

        agent = train()

        route = (
            get_best_route(
                agent
            )
        )

        metrics = (
            route_metrics(
                route
            )
        )

    st.success(
        "Route Generated"
    )

    st.subheader(
        "Best Route"
    )

    st.write(
        " → ".join(
            map(
                str,
                route
            )
        )
    )

    col1, col2, col3 = (
        st.columns(3)
    )

    col1.metric(
        "Latency",
        f"{metrics['latency']} ms"
    )

    col2.metric(
        "Packet Loss",
        f"{metrics['loss']} %"
    )

    col3.metric(
        "Hops",
        metrics["hops"]
    )