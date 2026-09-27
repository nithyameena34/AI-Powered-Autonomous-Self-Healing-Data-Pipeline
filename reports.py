import streamlit as st
import pandas as pd
from datetime import datetime
from io import StringIO, BytesIO


def _section(title: str):
    st.markdown(
        f'<p class="section-header">{title}</p>',
        unsafe_allow_html=True
    )


def _summary_card(label: str, value: str, sub: str, color: str):
    st.markdown(
        f"""
        <div class="dashboard-card" style="border-left: 4px solid {color}; padding: 1rem;">
            <div style="font-size:0.78rem; font-weight:600; color:#6B7280;
                        text-transform:uppercase; letter-spacing:0.05em;">
                {label}
            </div>
            <div style="font-size:1.5rem; font-weight:700; color:#111827; margin: 4px 0;">
                {value}
            </div>
            <div style="font-size:0.78rem; color:#9CA3AF;">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_reports(
    df         : pd.DataFrame,
    anomaly_df : pd.DataFrame = None,
    prediction : dict         = None,
):
    prediction  = prediction  or {}
    anomaly_df  = anomaly_df  if anomaly_df  is not None else pd.DataFrame()

    st.markdown(
        '<p class="section-header">📄 Reports Center</p>',
        unsafe_allow_html=True
    )
    st.caption("Export pipeline outputs, review summaries, and download reports.")

    # ══════════════════════════════════════════
    # ROW 1 — Pipeline Summary Cards
    # ══════════════════════════════════════════
    _section("📊 Pipeline Run Summary")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        _summary_card(
            "Total Records",
            f"{prediction.get('TotalRecords', len(df)):,}",
            "processed in this run",
            "#3B82F6"
        )
    with c2:
        _summary_card(
            "Anomalies Detected",
            f"{prediction.get('Anomalies', 0):,}",
            f"{prediction.get('AnomalyRate', 0):.4f}% anomaly rate",
            "#F59E0B"
        )
    with c3:
        _summary_card(
            "Confirmed Fraud",
            f"{prediction.get('ConfirmedFraud', 0):,}",
            "quarantined automatically",
            "#EF4444"
        )
    with c4:
        _summary_card(
            "Health Score",
            f"{prediction.get('HealthScore', 0):.2f}%",
            f"Risk: {prediction.get('FailureRisk', 'N/A')}",
            "#1DB954"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # ROW 2 — Model Performance Summary
    # ══════════════════════════════════════════
    _section("🤖 Model Performance")

    p1, p2, p3, p4 = st.columns(4)

    with p1:
        _summary_card(
            "Detection Rate",
            f"{prediction.get('DetectionRate', 0):.2f}%",
            "of real fraud caught",
            "#1DB954"
        )
    with p2:
        _summary_card(
            "False Positives",
            f"{prediction.get('FalsePositives', 0):,}",
            f"{prediction.get('FalsePositiveRate', 0):.4f}% FP rate",
            "#F59E0B"
        )
    with p3:
        _summary_card(
            "Healed Records",
            f"{prediction.get('HealedRecords', 0):,}",
            f"{prediction.get('HealingRate', 0):.2f}% of anomalies",
            "#3B82F6"
        )
    with p4:
        _summary_card(
            "Fraud Rate",
            f"{prediction.get('FraudRate', 0):.4f}%",
            "of total transactions",
            "#8B5CF6"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # ROW 3 — Downloads
    # ══════════════════════════════════════════
    _section("⬇️ Download Reports")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    d1, d2, d3 = st.columns(3)

    # ── Healed Dataset ──
    with d1:
        st.markdown(
            """
            <div class="dashboard-card">
                <div style="font-weight:700; color:#111827; margin-bottom:4px;">
                    🛠️ Healed Transactions
                </div>
                <div style="font-size:0.82rem; color:#6B7280; margin-bottom:12px;">
                    Full cleaned and healed dataset with HealingStatus column.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if not df.empty:
            st.download_button(
                label             = "⬇️ Download CSV",
                data              = df.to_csv(index=False),
                file_name         = f"healed_transactions_{ts}.csv",
                mime              = "text/csv",
                use_container_width = True,
                key               = "dl_healed"
            )
        else:
            st.info("No healed data available.")

    # ── Anomaly Results ──
    with d2:
        st.markdown(
            """
            <div class="dashboard-card">
                <div style="font-weight:700; color:#111827; margin-bottom:4px;">
                    🔍 Anomaly Results
                </div>
                <div style="font-size:0.82rem; color:#6B7280; margin-bottom:12px;">
                    All records with Isolation Forest anomaly labels.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if not anomaly_df.empty:
            st.download_button(
                label             = "⬇️ Download CSV",
                data              = anomaly_df.to_csv(index=False),
                file_name         = f"anomaly_results_{ts}.csv",
                mime              = "text/csv",
                use_container_width = True,
                key               = "dl_anomaly"
            )
        else:
            st.info("No anomaly data available.")

    # ── Fraud-only Export ──
    with d3:
        st.markdown(
            """
            <div class="dashboard-card">
                <div style="font-weight:700; color:#111827; margin-bottom:4px;">
                    🔒 Quarantined Fraud Records
                </div>
                <div style="font-size:0.82rem; color:#6B7280; margin-bottom:12px;">
                    Only confirmed fraud records flagged for review.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        fraud_df = (
            df[df["HealingStatus"] == "Quarantined"]
            if not df.empty and "HealingStatus" in df.columns
            else pd.DataFrame()
        )
        if not fraud_df.empty:
            st.download_button(
                label             = "⬇️ Download CSV",
                data              = fraud_df.to_csv(index=False),
                file_name         = f"fraud_quarantined_{ts}.csv",
                mime              = "text/csv",
                use_container_width = True,
                key               = "dl_fraud"
            )
        else:
            st.info("No quarantined records found.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # ROW 4 — Text Report
    # ══════════════════════════════════════════
    _section("📝 Pipeline Report")

    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = f"""
AI SELF-HEALING PIPELINE — RUN REPORT
======================================
Generated     : {run_time}
Dataset       : Credit Card Fraud Detection (Kaggle)

PIPELINE SUMMARY
----------------
Total Records       : {prediction.get('TotalRecords', len(df)):,}
Normal Records      : {prediction.get('NormalRecords', 0):,}
Anomalies Detected  : {prediction.get('Anomalies', 0):,}
Confirmed Fraud     : {prediction.get('ConfirmedFraud', 0):,}
Healed Records      : {prediction.get('HealedRecords', 0):,}

RATES
-----
Anomaly Rate        : {prediction.get('AnomalyRate', 0):.4f}%
Fraud Rate          : {prediction.get('FraudRate', 0):.4f}%
Healing Rate        : {prediction.get('HealingRate', 0):.2f}%

RISK ASSESSMENT
---------------
Failure Risk        : {prediction.get('FailureRisk', 'N/A')}
Risk Score          : {prediction.get('RiskScore', 0):.2f}
Health Score        : {prediction.get('HealthScore', 0):.2f}%

MODEL PERFORMANCE
-----------------
Detection Rate      : {prediction.get('DetectionRate', 0):.2f}%
False Positives     : {prediction.get('FalsePositives', 0):,}
False Positive Rate : {prediction.get('FalsePositiveRate', 0):.4f}%

PIPELINE STEPS
--------------
1. ETL Processing       — Duplicates removed, data types normalized
2. Anomaly Detection    — Isolation Forest (n_estimators=100)
3. Self Healing         — Median replacement + quarantine
4. Database Storage     — SQLite (4 tables)
5. Failure Prediction   — Risk classification

END OF REPORT
""".strip()

    st.text_area(
        "Full Report",
        report,
        height            = 380,
        label_visibility  = "collapsed"
    )

    st.download_button(
        label             = "⬇️ Download Full Report (.txt)",
        data              = report,
        file_name         = f"pipeline_report_{ts}.txt",
        mime              = "text/plain",
        use_container_width = True,
        key               = "dl_report"
    )