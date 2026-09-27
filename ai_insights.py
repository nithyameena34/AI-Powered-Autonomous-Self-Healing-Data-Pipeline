import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


CHART_LAYOUT = dict(
    paper_bgcolor = "rgba(0,0,0,0)",
    plot_bgcolor  = "rgba(0,0,0,0)",
    font          = {"family": "Inter, Segoe UI, sans-serif", "color": "#374151"},
    margin        = dict(t=30, b=30, l=10, r=10),
)


def _insight_card(title: str, body: str, color: str, emoji: str):
    st.markdown(
        f"""
        <div class="dashboard-card" style="border-left: 4px solid {color};">
            <div style="font-weight:700; color:#111827; margin-bottom:6px;">
                {emoji} {title}
            </div>
            <div style="font-size:0.88rem; color:#374151; line-height:1.6;">
                {body}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_ai_insights(
    total_records  : int,
    total_anomalies: int,
    health_score   : float,
    failure_risk   : str,
    df             : pd.DataFrame = None,
    anomaly_df     : pd.DataFrame = None,
    prediction     : dict         = None,
):
    prediction = prediction or {}

    st.markdown(
        '<p class="section-header">🤖 AI Insight Panel</p>',
        unsafe_allow_html=True
    )
    st.caption("Intelligent summary, risk assessment, and recommended actions based on real pipeline data.")

    # ══════════════════════════════════════════
    # ROW 1 — KPI Summary
    # ══════════════════════════════════════════
    m1, m2, m3, m4, m5 = st.columns(5)

    m1.metric("💚 Health Score",    f"{health_score:.2f}%")
    m2.metric("🚨 Anomalies",       f"{total_anomalies:,}")
    m3.metric("⚠️ Risk Level",      failure_risk)
    m4.metric("🎯 Detection Rate",  f"{prediction.get('DetectionRate', 0):.2f}%")
    m5.metric("🛠️ Healing Rate",    f"{prediction.get('HealingRate', 0):.2f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # ROW 2 — AI Summary + Recommendations
    # ══════════════════════════════════════════
    left, right = st.columns([1, 1])

    with left:
        st.markdown(
            '<p class="section-header">🧠 AI Risk Assessment</p>',
            unsafe_allow_html=True
        )

        confirmed  = prediction.get("ConfirmedFraud", 0)
        healed     = prediction.get("HealedRecords", 0)
        fp         = prediction.get("FalsePositives", 0)
        det_rate   = prediction.get("DetectionRate", 0)
        fraud_rate = prediction.get("FraudRate", 0)

        if failure_risk == "LOW":
            _insight_card(
                "Pipeline Stable",
                f"Health score is <b>{health_score:.2f}%</b> — excellent. "
                f"<b>{confirmed}</b> confirmed fraud records were quarantined. "
                f"<b>{healed}</b> anomalous records were repaired automatically. "
                f"Isolation Forest detected <b>{det_rate:.2f}%</b> of real fraud cases.",
                "#1DB954", "🟢"
            )
        elif failure_risk == "MEDIUM":
            _insight_card(
                "Moderate Risk Detected",
                f"Anomaly rate is <b>{prediction.get('AnomalyRate', 0):.4f}%</b>. "
                f"<b>{confirmed}</b> real fraud cases caught — <b>{det_rate:.2f}%</b> detection rate. "
                f"<b>{fp}</b> false positives flagged non-fraudulent records as suspicious. "
                f"Self-healing resolved <b>{healed}</b> records automatically.",
                "#F59E0B", "🟡"
            )
        else:
            _insight_card(
                "High Risk — Immediate Action Required",
                f"Pipeline health has dropped below safe thresholds. "
                f"Fraud rate is <b>{fraud_rate:.4f}%</b>. "
                f"Only <b>{det_rate:.2f}%</b> of real fraud cases were detected — "
                f"consider retraining with adjusted contamination. "
                f"<b>{confirmed}</b> records quarantined for manual review.",
                "#EF4444", "🔴"
            )

    with right:
        st.markdown(
            '<p class="section-header">💡 AI Recommendations</p>',
            unsafe_allow_html=True
        )

        recs = {
            "LOW": [
                ("Schedule next pipeline run", "Maintain regular cadence to catch drift early.", "#1DB954"),
                ("Monitor false positive rate", f"Current FP rate: {prediction.get('FalsePositiveRate', 0):.4f}% — within safe range.", "#3B82F6"),
                ("Review quarantined records", f"{confirmed} fraud records need manual confirmation.", "#F59E0B"),
            ],
            "MEDIUM": [
                ("Investigate false positives", f"{fp} normal records flagged — review feature scaling.", "#F59E0B"),
                ("Tune contamination parameter", f"Current: {prediction.get('AnomalyRate', 0):.4f}% — adjust if fraud rate shifts.", "#F59E0B"),
                ("Validate healing logic", "Confirm median-based repair is appropriate for flagged amounts.", "#3B82F6"),
            ],
            "HIGH": [
                ("Pause downstream automation", "Do not use pipeline output until root cause is resolved.", "#EF4444"),
                ("Retrain Isolation Forest", "Add more recent fraud samples and lower contamination threshold.", "#EF4444"),
                ("Manual fraud review", f"{confirmed} quarantined records require urgent investigation.", "#EF4444"),
            ],
        }

        for title, body, color in recs.get(failure_risk, recs["LOW"]):
            _insight_card(title, body, color, "→")
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # ROW 3 — Anomaly Amount Scatter + Detection Funnel
    # ══════════════════════════════════════════
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<p class="section-header">💰 Fraud Amount Distribution</p>',
            unsafe_allow_html=True
        )
        if anomaly_df is not None and not anomaly_df.empty and "Amount" in anomaly_df.columns:
            cap     = anomaly_df["Amount"].quantile(0.99)
            plot_df = anomaly_df[anomaly_df["Amount"] <= cap].copy()

            fig = px.violin(
                plot_df,
                x      = "Anomaly",
                y      = "Amount",
                color  = "Anomaly",
                box    = True,
                points = False,
                color_discrete_map = {
                    "Normal"  : "#1DB954",
                    "Anomaly" : "#EF4444",
                },
            )
            fig.update_layout(
                **CHART_LAYOUT,
                height      = 280,
                showlegend  = False,
                xaxis_title = "",
                yaxis_title = "Amount (USD)",
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No amount data available.")

    with col2:
        st.markdown(
            '<p class="section-header">🔬 Detection Funnel</p>',
            unsafe_allow_html=True
        )

        funnel_data = {
            "Stage": [
                "Total Records",
                "After ETL Cleaning",
                "Anomalies Flagged",
                "Confirmed Fraud",
                "Successfully Healed",
            ],
            "Count": [
                prediction.get("TotalRecords",   total_records),
                prediction.get("TotalRecords",   total_records),
                prediction.get("Anomalies",      total_anomalies),
                prediction.get("ConfirmedFraud", 0),
                prediction.get("HealedRecords",  0),
            ]
        }

        fig = go.Figure(go.Funnel(
            y           = funnel_data["Stage"],
            x           = funnel_data["Count"],
            textinfo    = "value+percent initial",
            marker      = dict(
                color       = ["#3B82F6", "#1DB954", "#F59E0B", "#EF4444", "#8B5CF6"],
                line        = dict(width=1, color="white")
            ),
            connector   = dict(line=dict(color="#E5E7EB", width=1))
        ))

        fig.update_layout(
            **CHART_LAYOUT,
            height = 280,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # ROW 4 — Action Checklist
    # ══════════════════════════════════════════
    st.markdown(
        '<p class="section-header">✅ Action Checklist</p>',
        unsafe_allow_html=True
    )

    actions = [
        ("Review quarantined fraud records in Data Explorer",       failure_risk in ["MEDIUM", "HIGH"]),
        ("Verify healing logic applied to high-value transactions",  healed > 0),
        ("Check false positive rate — currently "
         f"{prediction.get('FalsePositiveRate', 0):.4f}%",          fp > 100),
        ("Validate Isolation Forest contamination parameter",        failure_risk == "HIGH"),
        ("Export pipeline report for stakeholder review",            True),
        ("Schedule next pipeline run after source data refresh",     failure_risk == "LOW"),
    ]

    cols = st.columns(2)
    for i, (label, default) in enumerate(actions):
        with cols[i % 2]:
            st.checkbox(label, value=default, key=f"action_{i}")

    # ══════════════════════════════════════════
    # ROW 5 — Expander: Why this matters
    # ══════════════════════════════════════════
    with st.expander("📖 About this AI Insight Panel"):
        st.markdown("""
        This panel uses real pipeline output to generate contextual insights:

        - **Risk Assessment** — derived from anomaly rate, health score, and detection rate
        - **Recommendations** — tailored to current `FailureRisk` level (LOW / MEDIUM / HIGH)
        - **Detection Funnel** — shows how records flow from raw input to confirmed fraud
        - **Fraud Amount Distribution** — violin chart comparing normal vs anomalous transaction amounts
        - **Action Checklist** — pre-ticked based on actual pipeline state, not hardcoded defaults

        All metrics sourced from `failure_prediction.csv` — no hardcoded values.
        """)