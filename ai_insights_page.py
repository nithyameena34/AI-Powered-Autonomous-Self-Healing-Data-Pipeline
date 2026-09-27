import streamlit as st
import pandas as pd
from components.ai_insights import show_ai_insights
from utils.data_loader import (
    load_anomaly_data,
    load_healed_data,
    load_prediction_data,
)


def show_ai_page(
    total_records  : int   = 0,
    total_anomalies: int   = 0,
    health_score   : float = 0.0,
    failure_risk   : str   = "LOW",
):
    # ── Header ──
    st.markdown(
        """
        <div class="pipeline-header">
            <h1>🤖 AI Insights</h1>
            <p>Intelligent risk interpretation, fraud pattern analysis,
               detection funnel, and action guidance — all derived from
               live pipeline output.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ── Load all data fresh ──
    prediction  = load_prediction_data()
    anomaly_df  = load_anomaly_data()
    df          = load_healed_data()

    # Override args with fresher prediction dict if available
    if prediction:
        total_records   = prediction.get("TotalRecords",   total_records)
        total_anomalies = prediction.get("Anomalies",      total_anomalies)
        health_score    = prediction.get("HealthScore",    health_score)
        failure_risk    = prediction.get("FailureRisk",    failure_risk)

    # ── Empty state ──
    if df.empty and anomaly_df.empty and not prediction:
        st.markdown(
            """
            <div class="alert-medium">
                🟡 <b>No pipeline data found.</b>
                Run <code>python main.py</code> to generate output,
                then refresh this page.
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    # ── Risk banner ──
    risk_banners = {
        "LOW" : (
            "alert-low",
            "🟢 <b>Pipeline risk is LOW.</b> "
            "All systems operating within safe thresholds. "
            "Fraud detection and self-healing are active."
        ),
        "MEDIUM" : (
            "alert-medium",
            "🟡 <b>Pipeline risk is MEDIUM.</b> "
            "Anomaly rate is elevated. Self-healing has been applied. "
            "Review recommendations below."
        ),
        "HIGH" : (
            "alert-high",
            "🔴 <b>Pipeline risk is HIGH.</b> "
            "Immediate action required. "
            "Quarantined records need manual review before downstream use."
        ),
    }

    css_class, message = risk_banners.get(failure_risk, risk_banners["LOW"])
    st.markdown(
        f'<div class="{css_class}">{message}</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs ──
    tab1, tab2 = st.tabs([
        "🧠 Insights & Recommendations",
        "📊 Fraud Deep Dive",
    ])

    with tab1:
        show_ai_insights(
            total_records   = total_records,
            total_anomalies = total_anomalies,
            health_score    = health_score,
            failure_risk    = failure_risk,
            df              = df,
            anomaly_df      = anomaly_df,
            prediction      = prediction,
        )

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        _show_fraud_deep_dive(anomaly_df, df, prediction)


def _show_fraud_deep_dive(
    anomaly_df : pd.DataFrame,
    df         : pd.DataFrame,
    prediction : dict,
):
    import plotly.express as px
    import plotly.graph_objects as go

    CHART_LAYOUT = dict(
        paper_bgcolor = "rgba(0,0,0,0)",
        plot_bgcolor  = "rgba(0,0,0,0)",
        font          = {"family": "Inter, Segoe UI, sans-serif", "color": "#374151"},
        margin        = dict(t=30, b=30, l=10, r=10),
        xaxis         = dict(showgrid=False, linecolor="#E5E7EB"),
        yaxis         = dict(gridcolor="#F3F4F6", linecolor="#E5E7EB"),
    )

    if anomaly_df.empty:
        st.info("No anomaly data available for deep dive.")
        return

    # ── Summary row ──
    confirmed  = prediction.get("ConfirmedFraud",    0)
    total      = prediction.get("TotalRecords",       0)
    det_rate   = prediction.get("DetectionRate",      0)
    fp         = prediction.get("FalsePositives",     0)
    fp_rate    = prediction.get("FalsePositiveRate",  0)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔒 Confirmed Fraud",    f"{confirmed:,}")
    c2.metric("🎯 Detection Rate",     f"{det_rate:.2f}%")
    c3.metric("❌ False Positives",    f"{fp:,}")
    c4.metric("📉 FP Rate",            f"{fp_rate:.4f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # ── Fraud amount scatter ──
    with col1:
        st.markdown(
            '<p class="section-header">💰 Fraud Transaction Amounts</p>',
            unsafe_allow_html=True
        )
        if "Amount" in anomaly_df.columns and "Class" in anomaly_df.columns:
            fraud_only = anomaly_df[anomaly_df["Class"] == 1].copy()
            fraud_only = fraud_only.reset_index(drop=True)
            fraud_only["Index"] = fraud_only.index

            fig = px.scatter(
                fraud_only,
                x      = "Index",
                y      = "Amount",
                color  = "Amount",
                color_continuous_scale = ["#DCFCE7", "#1DB954", "#EF4444"],
                labels = {"Index": "Transaction", "Amount": "Amount (USD)"},
                hover_data = ["Time", "Amount"] if "Time" in fraud_only.columns else ["Amount"],
            )
            fig.update_traces(marker=dict(size=6, opacity=0.7))
            fig.update_layout(
                **CHART_LAYOUT,
                height              = 300,
                coloraxis_showscale = False,
                xaxis_title         = "Transaction Index",
                yaxis_title         = "Amount (USD)",
            )
            st.plotly_chart(
                fig,
                use_container_width = True,
                config={"displayModeBar": False}
            )
        else:
            st.info("Amount or Class column not found.")

    # ── Missed vs caught fraud ──
    with col2:
        st.markdown(
            '<p class="section-header">🎯 Caught vs Missed Fraud</p>',
            unsafe_allow_html=True
        )
        if "Class" in anomaly_df.columns and "Anomaly" in anomaly_df.columns:
            real_fraud  = anomaly_df[anomaly_df["Class"] == 1]
            caught      = len(real_fraud[real_fraud["Anomaly"] == "Anomaly"])
            missed      = len(real_fraud[real_fraud["Anomaly"] == "Normal"])

            fig = go.Figure(go.Pie(
                labels    = ["Caught", "Missed"],
                values    = [caught, missed],
                hole      = 0.55,
                marker    = dict(
                    colors = ["#1DB954", "#EF4444"],
                    line   = dict(color="white", width=2)
                ),
                textinfo  = "percent+label",
                textfont  = dict(size=13),
            ))
            fig.update_layout(
                **CHART_LAYOUT,
                height      = 300,
                showlegend  = True,
                legend      = dict(orientation="h", y=-0.1),
                annotations = [{
                    "text"      : f"{caught}<br>caught",
                    "x": 0.5, "y": 0.5,
                    "font_size" : 14,
                    "font_color": "#111827",
                    "showarrow" : False,
                }]
            )
            st.plotly_chart(
                fig,
                use_container_width = True,
                config={"displayModeBar": False}
            )
        else:
            st.info("Class or Anomaly column not found.")

    # ── Quarantined records table ──
    st.markdown(
        '<p class="section-header">🔒 Quarantined Records Preview</p>',
        unsafe_allow_html=True
    )

    if not df.empty and "HealingStatus" in df.columns:
        quarantined = df[df["HealingStatus"] == "Quarantined"].copy()

        if not quarantined.empty:
            display_cols = (
                ["Time", "Amount", "Class", "Anomaly", "HealingStatus"]
                if all(c in quarantined.columns for c in ["Time", "Amount", "Class", "Anomaly"])
                else quarantined.columns[:6].tolist()
            )
            st.dataframe(
                quarantined[display_cols].reset_index(drop=True),
                use_container_width = True,
                hide_index          = True,
            )
            st.caption(
                f"{len(quarantined):,} quarantined records shown. "
                "Download full export from the Reports page."
            )
        else:
            st.markdown(
                '<div class="alert-low">✅ No quarantined records. '
                'All fraud records were healed or no fraud was detected.</div>',
                unsafe_allow_html=True
            )
    else:
        st.info("Healed dataset not available.")