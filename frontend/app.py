import sys
from pathlib import Path

sys.path.append(
    str(
        Path(__file__).resolve().parent.parent
    )
)

import streamlit as st
import altair as alt
import pandas as pd

from streamlit_autorefresh import (
    st_autorefresh
)

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
    "Intelligent Multihop Routing"
)

st.caption(
    "Dynamic network conditions enabled"
)

st.write(
    "AI Routing Optimizer"
)

auto_mode = st.toggle(
    "Live Mode"
)

if auto_mode:

    st_autorefresh(
        interval=5000,
        key="refresh"
    )


if "normal_rewards" not in st.session_state:
    st.session_state.normal_rewards = []

if "failed_rewards" not in st.session_state:
    st.session_state.failed_rewards = []


run = st.button(
    "Train & Compare"
)

if (
    run
    or
    auto_mode
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

        st.session_state.normal_rewards = (
            normal_rewards
        )

        st.session_state.failed_rewards = (
            failed_rewards
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


if (
    len(
        st.session_state.normal_rewards
    )
    >
    0
):

    st.divider()

    st.subheader(
        "Learning Curve"
    )

    st.info(
        """
X-axis → Training Episodes

Y-axis → Total Reward

Higher reward means better routing decisions.
Stable curves indicate convergence.
"""
    )

    chart_left, chart_right = (
        st.columns(2)
    )

    with chart_left:

        normal_df = pd.DataFrame({

            "Episode":
            range(
                len(
                    st.session_state.normal_rewards
                )
            ),

            "Reward":
            st.session_state.normal_rewards

        })

        chart = (
            alt.Chart(
                normal_df
            )
            .mark_line()
            .encode(

                x=alt.X(
                    "Episode",
                    title="Training Episodes"
                ),

                y=alt.Y(
                    "Reward",
                    title="Total Reward"
                )
            )
        )

        st.altair_chart(
            chart,
            use_container_width=True
        )

    with chart_right:

        failed_df = pd.DataFrame({

            "Episode":
            range(
                len(
                    st.session_state.failed_rewards
                )
            ),

            "Reward":
            st.session_state.failed_rewards

        })

        chart = (
            alt.Chart(
                failed_df
            )
            .mark_line()
            .encode(

                x=alt.X(
                    "Episode",
                    title="Training Episodes"
                ),

                y=alt.Y(
                    "Reward",
                    title="Total Reward"
                )
            )
        )

        st.altair_chart(
            chart,
            use_container_width=True
        )
