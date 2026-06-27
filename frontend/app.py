import sys
from pathlib import Path

sys.path.append(
    str(
        Path(__file__).resolve().parent.parent
    )
)

import streamlit as st

from frontend.visualizer import (
    draw_route
)

from rl_engine.train import (
    train
)

from rl_engine.inference import (
    get_best_route
)

from rl_engine.topology import (
    adjacency_matrix
)

from backend.metrics import (
    route_metrics
)

from backend.chaos_router import (
    break_link
)


st.set_page_config(
    page_title="RouteFlux",
    layout="wide",
)

st.title(
    "🚀 Intelligent Multihop Routing"
)

st.write(
    "AI Routing Optimizer"
)


if st.button(
    "Train & Compare"
):

    with st.spinner(
        "Training..."
    ):

        normal_agent, normal_rewards = train()

        normal_route = (
            get_best_route(
                normal_agent
            )
        )

        normal_metrics = (
            route_metrics(
                normal_route
            )
        )

        failed_topology = (
            break_link(
                adjacency_matrix,
                2,
                4
            )
        )

        failed_agent, failed_rewards = (
            train(
                failed_topology
            )
        )

        failed_route = (
            get_best_route(
                failed_agent
            )
        )

        failed_metrics = (
            route_metrics(
                failed_route
            )
        )

    st.success(
        "Comparison Ready"
    )

    st.divider()

    left, right = (
        st.columns(2)
    )

    with left:

        st.subheader(
            "Normal Network"
        )

        fig = draw_route(
            normal_route
        )

        st.pyplot(
            fig,
            use_container_width=False
        )

        st.write(
            " → ".join(
                map(
                    str,
                    normal_route
                )
            )
        )

        c1, c2, c3 = (
            st.columns(3)
        )

        c1.metric(
            "Latency",
            f"{normal_metrics['latency']} ms"
        )

        c2.metric(
            "Loss",
            f"{normal_metrics['loss']} %"
        )

        c3.metric(
            "Hops",
            normal_metrics[
                "hops"
            ]
        )

    with right:

        st.subheader(
            "Broken 2 ↔ 4"
        )

        fig = draw_route(
            failed_route
        )

        st.pyplot(
            fig,
            use_container_width=False
        )

        st.write(
            " → ".join(
                map(
                    str,
                    failed_route
                )
            )
        )

        c1, c2, c3 = (
            st.columns(3)
        )

        c1.metric(
            "Latency",
            f"{failed_metrics['latency']} ms"
        )

        c2.metric(
            "Loss",
            f"{failed_metrics['loss']} %"
        )

        c3.metric(
            "Hops",
            failed_metrics[
                "hops"
            ]
        )


        st.subheader(
        "Learning Curve"
    )

    chart_left, chart_right = (
        st.columns(2)
    )

    with chart_left:

        st.write(
            "Normal Network Rewards"
        )

        st.line_chart(
            normal_rewards
        )

    with chart_right:

        st.write(
            "Broken Network Rewards"
        )

        st.line_chart(
            failed_rewards
        )