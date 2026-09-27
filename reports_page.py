import streamlit as st
import pandas as pd
from components.reports import show_reports
from utils.data_loader import (
    load_healed_data,
    load_anomaly_data,
    load_prediction_data,
    check_pipeline_status,
)


def show_reports_page(df: pd.DataFrame):

    # ── Header ──
    st.markdown(
        """
        <div class="pipeline-header">
            <h1>📄 Reports</h1>
            <p>Export pipeline outputs, download fraud records, review run summaries,
               and generate shareable reports for stakeholders.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ── Load fresh data ──
    healed_df  = df if not df.empty else load_healed_data()
    anomaly_df = load_anomaly_data()
    prediction = load_prediction_data()
    pipeline_status = check_pipeline_status()

    # ── Empty state ──
    if healed_df.empty and not prediction:
        st.markdown(
            """
            <div class="alert-medium">
                🟡 <b>No pipeline output found.</b>
                Run <code>python main.py</code> to generate data,
                then refresh this page.
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    # ══════════════════════════════════════════
    # ROW 1 — Run Status Banner
    # ══════════════════════════════════════════
    completed   = sum(pipeline_status.values())
    total_steps = len(pipeline_status)
    all_done    = completed == total_steps
    risk        = prediction.get("FailureRisk", "N/A")

    risk_color = {
        "LOW"    : ("#F0FDF4", "#1DB954", "#166534"),
        "MEDIUM" : ("#FFFBEB", "#F59E0B", "#92400E"),
        "HIGH"   : ("#FFF1F2", "#EF4444", "#9F1239"),
    }.get(risk, ("#F9FAFB", "#6B7280", "#374151"))

    st.markdown(
        f"""
        <div style="
            background:{risk_color[0]};
            border:1px solid {risk_color[1]};
            border-left:4px solid {risk_color[1]};
            border-radius:10px;
            padding:0.9rem 1.2rem;
            margin-bottom:1rem;
            display:flex;
            justify-content:space-between;
            align-items:center;
        ">
            <div>
                <span style="font-weight:700; color:{risk_color[2]}; font-size:0.95rem;">
                    Pipeline Run Summary
                </span>
                <span style="font-size:0.85rem; color:{risk_color[2]}; margin-left:12px;">
                    {completed}/{total_steps} steps completed ·
                    Risk: <b>{risk}</b> ·
                    Health: <b>{prediction.get('HealthScore', 0):.2f}%</b>
                </span>
            </div>
            <span style="
                background:{risk_color[1]};
                color:white;
                padding:3px 12px;
                border-radius:20px;
                font-size:0.82rem;
                font-weight:600;
            ">
                {'✅ Complete' if all_done else '🟡 Partial'}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # TABS
    # ══════════════════════════════════════════
    tab1, tab2, tab3 = st.tabs([
        "📊 Summary & Exports",
        "🔍 Pipeline Step Report",
        "📋 Raw Data Preview",
    ])

    # ──────────────────────────────────────────
    # TAB 1 — Summary & Exports
    # ──────────────────────────────────────────
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        show_reports(
            df         = healed_df,
            anomaly_df = anomaly_df,
            prediction = prediction,
        )

    # ──────────────────────────────────────────
    # TAB 2 — Pipeline Step Report
    # ──────────────────────────────────────────
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            '<p class="section-header">🔧 Step-by-Step Pipeline Report</p>',
            unsafe_allow_html=True
        )

        steps = [
            {
                "key"     : "ETL",
                "icon"    : "⚙️",
                "label"   : "ETL Processing",
                "detail"  : (
                    f"Loaded raw transactions · "
                    f"Removed {prediction.get('TotalRecords', 0) - prediction.get('NormalRecords', 0):,} "
                    f"duplicates/invalids · "
                    f"Final records: {prediction.get('TotalRecords', 0):,}"
                ),
            },
            {
                "key"     : "Anomaly Detection",
                "icon"    : "🔍",
                "label"   : "Anomaly Detection",
                "detail"  : (
                    f"Isolation Forest (n_estimators=100) · "
                    f"Contamination: {prediction.get('AnomalyRate', 0):.4f}% · "
                    f"Anomalies flagged: {prediction.get('Anomalies', 0):,} · "
                    f"Detection rate: {prediction.get('DetectionRate', 0):.2f}%"
                ),
            },
            {
                "key"     : "Self Healing",
                "icon"    : "🛠️",
                "label"   : "Self Healing",
                "detail"  : (
                    f"Median replacement on V1–V28 + Amount · "
                    f"Healed: {prediction.get('HealedRecords', 0):,} records · "
                    f"Quarantined: {prediction.get('ConfirmedFraud', 0):,} fraud records · "
                    f"Healing rate: {prediction.get('HealingRate', 0):.2f}%"
                ),
            },
            {
                "key"     : "Database",
                "icon"    : "🗄️",
                "label"   : "Database Storage",
                "detail"  : (
                    f"SQLite · 4 tables created · "
                    f"transactions, anomaly_results, healing_summary, fraud_summary · "
                    f"{prediction.get('TotalRecords', 0):,} records stored"
                ),
            },
            {
                "key"     : "Failure Prediction",
                "icon"    : "📊",
                "label"   : "Failure Prediction",
                "detail"  : (
                    f"Risk: {prediction.get('FailureRisk', 'N/A')} · "
                    f"Risk Score: {prediction.get('RiskScore', 0):.2f} · "
                    f"Health Score: {prediction.get('HealthScore', 0):.2f}% · "
                    f"FP Rate: {prediction.get('FalsePositiveRate', 0):.4f}%"
                ),
            },
        ]

        for step in steps:
            done        = pipeline_status.get(step["key"], False)
            card_class  = "pipeline-step-done" if done else "pipeline-step-fail"
            badge_class = "badge-success"      if done else "badge-danger"
            badge_text  = "✅ Completed"        if done else "❌ Not Run"

            st.markdown(
                f"""
                <div class="pipeline-step {card_class}"
                     style="flex-direction:column; align-items:flex-start;
                            padding:1rem 1.2rem; margin-bottom:8px;">
                    <div style="display:flex; justify-content:space-between;
                                width:100%; align-items:center;">
                        <div style="display:flex; align-items:center; gap:10px;">
                            <span style="font-size:1.3rem;">{step["icon"]}</span>
                            <span style="font-weight:700; color:#111827;
                                         font-size:0.95rem;">{step["label"]}</span>
                        </div>
                        <span class="{badge_class}">{badge_text}</span>
                    </div>
                    <div style="font-size:0.82rem; color:#6B7280;
                                margin-top:6px; padding-left:2px;">
                        {step["detail"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # ──────────────────────────────────────────
    # TAB 3 — Raw Data Preview
    # ──────────────────────────────────────────
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)

        ds1, ds2 = st.tabs(["🛠️ Healed Dataset", "🔍 Anomaly Results"])

        with ds1:
            if not healed_df.empty:
                r1, r2, r3 = st.columns(3)
                r1.metric("Rows",    f"{len(healed_df):,}")
                r2.metric("Columns", f"{len(healed_df.columns)}")
                r3.metric("Memory",
                          f"{healed_df.memory_usage(deep=True).sum()/1e6:.1f} MB")
                st.markdown("<br>", unsafe_allow_html=True)
                st.dataframe(
                    healed_df.head(200),
                    use_container_width = True,
                    hide_index          = True,
                )
                st.caption("Showing first 200 rows. Download full dataset from the Summary & Exports tab.")
            else:
                st.info("No healed data available.")

        with ds2:
            if not anomaly_df.empty:
                r1, r2, r3 = st.columns(3)
                r1.metric("Rows",    f"{len(anomaly_df):,}")
                r2.metric("Columns", f"{len(anomaly_df.columns)}")
                r3.metric("Anomalies",
                          f"{len(anomaly_df[anomaly_df['Anomaly']=='Anomaly']):,}"
                          if "Anomaly" in anomaly_df.columns else "N/A")
                st.markdown("<br>", unsafe_allow_html=True)
                st.dataframe(
                    anomaly_df.head(200),
                    use_container_width = True,
                    hide_index          = True,
                )
                st.caption("Showing first 200 rows. Download full dataset from the Summary & Exports tab.")
            else:
                st.info("No anomaly data available.")