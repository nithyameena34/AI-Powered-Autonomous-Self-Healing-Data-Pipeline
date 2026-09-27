import streamlit as st
import plotly.express as px
import pandas as pd


def _card(title: str):
    st.markdown(
        f'<p class="section-header">{title}</p>',
        unsafe_allow_html=True
    )


COLORS = {
    "green": "#1DB954",
    "yellow": "#F59E0B",
    "red": "#EF4444",
    "blue": "#3B82F6",
    "gray": "#E5E7EB",
    "palette": [
        "#1DB954",
        "#3B82F6",
        "#F59E0B",
        "#EF4444",
        "#8B5CF6",
        "#06B6D4",
    ],
}


CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font={
        "family": "Inter, Segoe UI, sans-serif",
        "color": "#374151",
    },
    margin=dict(t=30, b=30, l=10, r=10),
    xaxis=dict(
        showgrid=False,
        linecolor="#E5E7EB"
    ),
    yaxis=dict(
        gridcolor="#F3F4F6",
        linecolor="#E5E7EB"
    ),
)


def show_charts(df: pd.DataFrame, anomaly_df: pd.DataFrame):

    # ──────────────────────────────────────────
    # Empty check
    # ──────────────────────────────────────────
    if df.empty:
        st.info("No data available. Run the pipeline first.")
        return

    # ──────────────────────────────────────────
    # Safe numeric conversion
    # ──────────────────────────────────────────
    if "Amount" in df.columns:
        df["Amount"] = pd.to_numeric(
            df["Amount"],
            errors="coerce"
        )

    if "Amount" in anomaly_df.columns:
        anomaly_df["Amount"] = pd.to_numeric(
            anomaly_df["Amount"],
            errors="coerce"
        )

    if "Time" in df.columns:
        df["Time"] = pd.to_numeric(
            df["Time"],
            errors="coerce"
        )

    if "Time" in anomaly_df.columns:
        anomaly_df["Time"] = pd.to_numeric(
            anomaly_df["Time"],
            errors="coerce"
        )

    # ══════════════════════════════════════════
    # ROW 1
    # ══════════════════════════════════════════
    col1, col2 = st.columns(2)

    # ──────────────────────────────────────────
    # Anomaly Distribution
    # ──────────────────────────────────────────
    with col1:

        _card("🔵 Anomaly Distribution")

        if (
            not anomaly_df.empty
            and "Anomaly" in anomaly_df.columns
        ):

            counts = (
                anomaly_df["Anomaly"]
                .value_counts()
                .reset_index()
            )

            counts.columns = ["Type", "Count"]

            fig = px.pie(
                counts,
                names="Type",
                values="Count",
                hole=0.55,
                color="Type",
                color_discrete_map={
                    "Normal": COLORS["green"],
                    "Anomaly": COLORS["red"],
                }
            )

            fig.update_traces(
                textinfo="percent+label",
                textfont_size=13,
                marker=dict(
                    line=dict(
                        color="white",
                        width=2
                    )
                )
            )

            fig.update_layout(
                **CHART_LAYOUT,
                height=280,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    y=-0.1
                ),
                annotations=[{
                    "text": f"{len(anomaly_df):,}<br>records",
                    "x": 0.5,
                    "y": 0.5,
                    "font_size": 13,
                    "font_color": "#111827",
                    "showarrow": False
                }]
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={"displayModeBar": False}
            )

        else:
            st.info("No anomaly data available.")

    # ──────────────────────────────────────────
    # Healing Status
    # ──────────────────────────────────────────
    with col2:

        _card("🛡️ Healing Status Breakdown")

        if "HealingStatus" in df.columns:

            heal_counts = (
                df["HealingStatus"]
                .value_counts()
                .reset_index()
            )

            heal_counts.columns = ["Status", "Count"]

            fig = px.bar(
                heal_counts,
                x="Status",
                y="Count",
                color="Status",
                text="Count",
                color_discrete_map={
                    "Original": COLORS["green"],
                    "Healed": COLORS["blue"],
                    "Quarantined": COLORS["red"],
                }
            )

            fig.update_traces(
                texttemplate="%{text:,}",
                textposition="outside",
                marker_line_width=0,
                width=0.5
            )

            fig.update_layout(
                **CHART_LAYOUT,
                height=280,
                showlegend=False,
                yaxis_title="Records",
                xaxis_title=""
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={"displayModeBar": False}
            )

        else:
            st.info("No healing status data available.")

    # ══════════════════════════════════════════
    # ROW 2
    # ══════════════════════════════════════════
    col3, col4 = st.columns(2)

    # ──────────────────────────────────────────
    # Amount Distribution
    # ──────────────────────────────────────────
    with col3:

        _card("💰 Transaction Amount Distribution")

        if "Amount" in df.columns:

            temp_df = df.dropna(subset=["Amount"])

            if not temp_df.empty:

                cap = temp_df["Amount"].quantile(0.99)

                capped = temp_df[
                    temp_df["Amount"] <= cap
                ]["Amount"]

                fig = px.histogram(
                    capped,
                    nbins=60,
                    color_discrete_sequence=[COLORS["green"]],
                    labels={
                        "value": "Amount (USD)",
                        "count": "Transactions"
                    }
                )

                fig.update_traces(
                    marker_line_width=0
                )

                fig.update_layout(
                    **CHART_LAYOUT,
                    height=280,
                    bargap=0.05,
                    xaxis_title="Amount (USD)",
                    yaxis_title="Transactions",
                    showlegend=False
                )

                st.plotly_chart(
                    fig,
                    width="stretch",
                    config={"displayModeBar": False}
                )

            else:
                st.info("No valid amount data available.")

        else:
            st.info("No Amount column found.")

    # ──────────────────────────────────────────
    # Time Analysis
    # ──────────────────────────────────────────
    with col4:

        _card("🕐 Anomalies over Time")

        if (
            not anomaly_df.empty
            and "Time" in anomaly_df.columns
            and "Anomaly" in anomaly_df.columns
        ):

            temp = anomaly_df.copy()

            temp = temp.dropna(subset=["Time"])

            temp["TimeBlock"] = pd.cut(
                temp["Time"],
                bins=24,
                labels=[f"T{i+1}" for i in range(24)]
            )

            trend = (
                temp[temp["Anomaly"] == "Anomaly"]
                .groupby("TimeBlock", observed=True)
                .size()
                .reset_index(name="Anomalies")
            )

            fig = px.area(
                trend,
                x="TimeBlock",
                y="Anomalies",
                color_discrete_sequence=[COLORS["red"]],
            )

            fig.update_traces(
                line_color=COLORS["red"],
                fillcolor="rgba(239,68,68,0.15)"
            )

            fig.update_layout(
                **CHART_LAYOUT,
                height=280,
                xaxis_title="Time Block",
                yaxis_title="Anomaly Count",
                showlegend=False
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={"displayModeBar": False}
            )

        else:
            st.info("No time-series data available.")

    # ══════════════════════════════════════════
    # ROW 3
    # ══════════════════════════════════════════
    col5, col6 = st.columns(2)

    # ──────────────────────────────────────────
    # Box Plot
    # ──────────────────────────────────────────
    with col5:

        _card("📦 Amount: Normal vs Fraud")

        if (
            not anomaly_df.empty
            and "Amount" in anomaly_df.columns
            and "Anomaly" in anomaly_df.columns
        ):

            temp_df = anomaly_df.dropna(
                subset=["Amount"]
            )

            if not temp_df.empty:

                cap = temp_df["Amount"].quantile(0.99)

                plot_df = temp_df[
                    temp_df["Amount"] <= cap
                ]

                fig = px.box(
                    plot_df,
                    x="Anomaly",
                    y="Amount",
                    color="Anomaly",
                    points=False,
                    color_discrete_map={
                        "Normal": COLORS["green"],
                        "Anomaly": COLORS["red"],
                    }
                )

                fig.update_layout(
                    **CHART_LAYOUT,
                    height=280,
                    showlegend=False,
                    xaxis_title="",
                    yaxis_title="Amount (USD)"
                )

                st.plotly_chart(
                    fig,
                    width="stretch",
                    config={"displayModeBar": False}
                )

            else:
                st.info("No valid amount data.")

        else:
            st.info("No data available.")

    # ──────────────────────────────────────────
    # Correlation Chart
    # ──────────────────────────────────────────
    with col6:

        _card("🔬 Top Feature Correlations")

        if (
            not anomaly_df.empty
            and "Anomaly" in anomaly_df.columns
        ):

            feature_cols = [
                f"V{i}"
                for i in range(1, 29)
                if f"V{i}" in anomaly_df.columns
            ]

            if feature_cols:

                temp = anomaly_df.copy()

                temp["AnomalyBinary"] = (
                    temp["Anomaly"] == "Anomaly"
                ).astype(int)

                corrs = (
                    temp[
                        feature_cols + ["AnomalyBinary"]
                    ]
                    .corr(numeric_only=True)["AnomalyBinary"]
                    .drop("AnomalyBinary")
                    .abs()
                    .sort_values(ascending=False)
                    .head(10)
                    .reset_index()
                )

                corrs.columns = [
                    "Feature",
                    "Correlation"
                ]

                fig = px.bar(
                    corrs,
                    x="Correlation",
                    y="Feature",
                    orientation="h",
                    color="Correlation",
                    text="Correlation",
                    color_continuous_scale=[
                        "#DCFCE7",
                        "#1DB954",
                        "#166534"
                    ]
                )

                fig.update_traces(
                    texttemplate="%{text:.3f}",
                    textposition="outside",
                    marker_line_width=0
                )

                fig.update_layout(
                    **CHART_LAYOUT,
                    height=280,
                    showlegend=False,
                    coloraxis_showscale=False,
                    xaxis_title="Absolute Correlation",
                    yaxis_title=""
                )

                fig.update_yaxes(
                    autorange="reversed",
                    gridcolor="#F3F4F6"
                )

                st.plotly_chart(
                    fig,
                    width="stretch",
                    config={"displayModeBar": False}
                )

            else:
                st.info("No V-feature columns found.")

        else:
            st.info("No anomaly data available.")