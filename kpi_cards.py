import streamlit as st


def show_kpi_cards(prediction: dict):

    # ── Row 1: Core Metrics ──
    st.markdown("### 📊 Pipeline Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="📦 Total Records",
            value=f"{prediction.get('TotalRecords', 0):,}"
        )

    with col2:
        st.metric(
            label="✅ Normal Records",
            value=f"{prediction.get('NormalRecords', 0):,}"
        )

    with col3:
        st.metric(
            label="🚨 Anomalies Detected",
            value=f"{prediction.get('Anomalies', 0):,}",
            delta=f"{prediction.get('AnomalyRate', 0):.4f}% rate",
            delta_color="inverse"
        )

    with col4:
        st.metric(
            label="🔒 Confirmed Fraud",
            value=f"{prediction.get('ConfirmedFraud', 0):,}",
            delta=f"{prediction.get('FraudRate', 0):.4f}% rate",
            delta_color="inverse"
        )

    st.markdown("---")

    # ── Row 2: Health & Risk ──
    st.markdown("### 🏥 Health & Risk")

    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.metric(
            label="💚 Health Score",
            value=f"{prediction.get('HealthScore', 0):.2f}%"
        )

    with col6:
        risk = prediction.get("FailureRisk", "LOW")
        risk_emoji = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}.get(risk, "⚪")
        st.metric(
            label="⚠️ Failure Risk",
            value=f"{risk_emoji} {risk}"
        )

    with col7:
        st.metric(
            label="🎯 Risk Score",
            value=f"{prediction.get('RiskScore', 0):.2f}"
        )

    with col8:
        st.metric(
            label="🛠️ Healed Records",
            value=f"{prediction.get('HealedRecords', 0):,}",
            delta=f"{prediction.get('HealingRate', 0):.2f}% healed",
            delta_color="normal"
        )

    st.markdown("---")

    # ── Row 3: Model Performance ──
    st.markdown("### 🤖 Model Performance")

    col9, col10, col11, col12 = st.columns(4)

    with col9:
        st.metric(
            label="🎯 Detection Rate",
            value=f"{prediction.get('DetectionRate', 0):.2f}%"
        )

    with col10:
        st.metric(
            label="❌ False Positives",
            value=f"{prediction.get('FalsePositives', 0):,}",
            delta=f"{prediction.get('FalsePositiveRate', 0):.4f}% FP rate",
            delta_color="inverse"
        )

    with col11:
        st.metric(
            label="🔁 Healing Rate",
            value=f"{prediction.get('HealingRate', 0):.2f}%"
        )

    with col12:
        st.metric(
            label="🦠 Fraud Rate",
            value=f"{prediction.get('FraudRate', 0):.4f}%"
        )