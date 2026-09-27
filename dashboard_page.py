import streamlit as st
import pandas as pd
import plotly.express as px

from components.kpi_cards       import show_kpi_cards
from components.health_gauge    import show_health_gauge
from components.failure_gauge   import show_failure_gauge
from components.pipeline_status import show_pipeline_status
from components.alerts          import show_alerts
from utils.data_loader          import (
    load_anomaly_data,
    load_prediction_data,
)


def show_dashboard(prediction: dict):

    if not prediction:
        prediction = load_prediction_data()

    risk         = prediction.get("FailureRisk",      "LOW")
    anomalies    = prediction.get("Anomalies",         0)
    health       = prediction.get("HealthScore",       0)
    anomaly_rate = prediction.get("AnomalyRate",       0)
    confirmed    = prediction.get("ConfirmedFraud",    0)
    healed       = prediction.get("HealedRecords",     0)
    det_rate     = prediction.get("DetectionRate",     0)
    fp_rate      = prediction.get("FalsePositiveRate", 0)
    heal_rate    = prediction.get("HealingRate",       0)
    total        = prediction.get("TotalRecords",      0)
    risk_score   = prediction.get("RiskScore",         0)
    fraud_rate   = prediction.get("FraudRate",         0)

    risk_color = {
        "LOW"   : "#1DB954",
        "MEDIUM": "#F59E0B",
        "HIGH"  : "#EF4444",
    }.get(risk, "#6B7280")

    # ══════════════════════════════════════════
    # HEADER
    # ══════════════════════════════════════════
    st.markdown(
        """
        <div class="pipeline-header">
            <h1>🚀 Pipeline Dashboard</h1>
            <p>Real-time overview of pipeline health, anomaly detection,
               self-healing activity, and fraud risk.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ══════════════════════════════════════════
    # ROW 1 — Alert Banner
    # ══════════════════════════════════════════
    show_alerts(risk, anomalies)
    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # ROW 2 — KPI Cards
    # ══════════════════════════════════════════
    show_kpi_cards(prediction)
    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # ROW 3 — Gauges + Pipeline Status
    # ══════════════════════════════════════════
    gauge_col, status_col = st.columns([2, 1])

    with gauge_col:
        g1, g2 = st.columns(2)
        with g1:
            show_health_gauge(health)
        with g2:
            show_failure_gauge(anomaly_rate, risk)

    with status_col:
        show_pipeline_status()

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # ROW 4 — Run Summary
    # ══════════════════════════════════════════
    st.markdown(
        '<p class="section-header">📋 Run Summary</p>',
        unsafe_allow_html=True
    )

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.markdown(
            f"""
            <div class="dashboard-card" style="text-align:center;">
                <div style="font-size:0.75rem; font-weight:600;
                            color:#6B7280; text-transform:uppercase;
                            letter-spacing:0.05em;">
                    Total Processed
                </div>
                <div style="font-size:1.6rem; font-weight:700;
                            color:#111827; margin:6px 0;">
                    {total:,}
                </div>
                <div style="font-size:0.75rem; color:#9CA3AF;">
                    records in pipeline
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with s2:
        st.markdown(
            f"""
            <div class="dashboard-card" style="text-align:center;">
                <div style="font-size:0.75rem; font-weight:600;
                            color:#6B7280; text-transform:uppercase;
                            letter-spacing:0.05em;">
                    Fraud Caught
                </div>
                <div style="font-size:1.6rem; font-weight:700;
                            color:#EF4444; margin:6px 0;">
                    {confirmed:,}
                </div>
                <div style="font-size:0.75rem; color:#9CA3AF;">
                    {det_rate:.2f}% detection rate
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with s3:
        st.markdown(
            f"""
            <div class="dashboard-card" style="text-align:center;">
                <div style="font-size:0.75rem; font-weight:600;
                            color:#6B7280; text-transform:uppercase;
                            letter-spacing:0.05em;">
                    Self-Healed
                </div>
                <div style="font-size:1.6rem; font-weight:700;
                            color:#3B82F6; margin:6px 0;">
                    {healed:,}
                </div>
                <div style="font-size:0.75rem; color:#9CA3AF;">
                    {heal_rate:.2f}% healing rate
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with s4:
        st.markdown(
            f"""
            <div class="dashboard-card" style="text-align:center;">
                <div style="font-size:0.75rem; font-weight:600;
                            color:#6B7280; text-transform:uppercase;
                            letter-spacing:0.05em;">
                    Risk Level
                </div>
                <div style="font-size:1.6rem; font-weight:700;
                            color:{risk_color}; margin:6px 0;">
                    {risk}
                </div>
                <div style="font-size:0.75rem; color:#9CA3AF;">
                    score {risk_score:.2f} · FP {fp_rate:.4f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Fraud rate progress bar
    st.markdown(
        f"""
        <div class="dashboard-card" style="margin-top:0.5rem;">
            <div style="display:flex; justify-content:space-between;
                        margin-bottom:6px;">
                <span style="font-size:0.8rem; font-weight:600; color:#374151;">
                    Fraud Rate
                </span>
                <span style="font-size:0.8rem; font-weight:700; color:{risk_color};">
                    {fraud_rate:.4f}%
                </span>
            </div>
            <div style="background:#F3F4F6; border-radius:999px;
                        height:8px; overflow:hidden;">
                <div style="width:{min(fraud_rate * 100, 100):.2f}%;
                            height:100%; background:{risk_color};
                            border-radius:999px;">
                </div>
            </div>
            <div style="display:flex; justify-content:space-between; margin-top:6px;">
                <span style="font-size:0.72rem; color:#9CA3AF;">0%</span>
                <span style="font-size:0.72rem; color:#9CA3AF;">
                    Industry avg: ~0.17%
                </span>
                <span style="font-size:0.72rem; color:#9CA3AF;">1%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # ROW 5 — Anomaly Snapshot
    # ══════════════════════════════════════════
    st.markdown(
        '<p class="section-header">📊 Anomaly Snapshot</p>',
        unsafe_allow_html=True
    )

    anomaly_df = load_anomaly_data()

    if not anomaly_df.empty and "Anomaly" in anomaly_df.columns:

        col_chart, col_info = st.columns([2, 1])

        value_counts = anomaly_df["Anomaly"].value_counts()
        normal_count = int(value_counts.get("Normal",  0))
        anom_count   = int(value_counts.get("Anomaly", 0))

        counts = pd.DataFrame({
            "Type" : ["Normal", "Anomaly"],
            "Count": [normal_count, anom_count]
        })

        with col_chart:
            fig = px.pie(
                counts,
                names  = "Type",
                values = "Count",
                hole   = 0.6,
                color  = "Type",
                color_discrete_map={
                    "Normal" : "#1DB954",
                    "Anomaly": "#EF4444",
                },
            )
            fig.update_traces(
                textinfo      = "percent+label",
                textfont_size = 13,
                marker        = dict(line=dict(color="white", width=2))
            )
            fig.update_layout(
                height        = 280,
                margin        = dict(t=20, b=20, l=20, r=20),
                paper_bgcolor = "rgba(0,0,0,0)",
                showlegend    = False,
                annotations   = [{
                    "text"      : f"{anom_count:,}<br><span style='font-size:11px'>anomalies</span>",
                    "x"         : 0.5,
                    "y"         : 0.5,
                    "font_size" : 18,
                    "font_color": "#111827",
                    "showarrow" : False,
                }]
            )
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )

        # ── Each card as its own st.markdown call ──
        with col_info:
            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(
                f"""
                <div class="dashboard-card"
                     style="border-left:4px solid #1DB954;">
                    <div style="font-size:0.75rem; font-weight:600;
                                color:#6B7280; text-transform:uppercase;">
                        Normal
                    </div>
                    <div style="font-size:1.4rem; font-weight:700;
                                color:#1DB954; margin:4px 0;">
                        {normal_count:,}
                    </div>
                    <div style="font-size:0.75rem; color:#9CA3AF;">
                        {normal_count / max(total, 1) * 100:.2f}% of total
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="dashboard-card"
                     style="border-left:4px solid #EF4444;">
                    <div style="font-size:0.75rem; font-weight:600;
                                color:#6B7280; text-transform:uppercase;">
                        Anomalies
                    </div>
                    <div style="font-size:1.4rem; font-weight:700;
                                color:#EF4444; margin:4px 0;">
                        {anom_count:,}
                    </div>
                    <div style="font-size:0.75rem; color:#9CA3AF;">
                        {anom_count / max(total, 1) * 100:.4f}% of total
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="dashboard-card"
                     style="border-left:4px solid #F59E0B;">
                    <div style="font-size:0.75rem; font-weight:600;
                                color:#6B7280; text-transform:uppercase;">
                        Confirmed Fraud
                    </div>
                    <div style="font-size:1.4rem; font-weight:700;
                                color:#F59E0B; margin:4px 0;">
                        {confirmed:,}
                    </div>
                    <div style="font-size:0.75rem; color:#9CA3AF;">
                        {confirmed / max(total, 1) * 100:.4f}% of total
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        st.info("Run the pipeline to see anomaly distribution.")