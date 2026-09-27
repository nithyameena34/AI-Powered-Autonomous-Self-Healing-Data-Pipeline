import streamlit as st


def show_alerts(failure_risk: str, total_anomalies: int):

    st.markdown(
        '<p class="section-header">🚨 System Alerts</p>',
        unsafe_allow_html=True
    )

    if failure_risk == "HIGH":

        st.markdown(
            f"""
            <div class="alert-high">
                <div style="font-size:1rem; font-weight:700; margin-bottom:4px;">
                    🔴 Critical Alert — High Failure Risk
                </div>
                <div style="font-size:0.88rem;">
                    <b>{total_anomalies:,}</b> anomalies detected in the pipeline.
                    Immediate investigation recommended.
                    Confirmed fraud records have been <b>quarantined</b> automatically.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Additional critical warnings
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                """
                <div class="alert-high" style="margin-bottom:0;">
                    <div style="font-weight:600; font-size:0.85rem;">
                        ⚠️ Action Required
                    </div>
                    <div style="font-size:0.82rem; margin-top:4px;">
                        Review quarantined records in Data Explorer
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                """
                <div class="alert-high" style="margin-bottom:0;">
                    <div style="font-weight:600; font-size:0.85rem;">
                        🛑 Pipeline Health: Critical
                    </div>
                    <div style="font-size:0.82rem; margin-top:4px;">
                        Re-run pipeline after resolving anomalies
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    elif failure_risk == "MEDIUM":

        st.markdown(
            f"""
            <div class="alert-medium">
                <div style="font-size:1rem; font-weight:700; margin-bottom:4px;">
                    🟡 Warning — Medium Failure Risk
                </div>
                <div style="font-size:0.88rem;">
                    <b>{total_anomalies:,}</b> anomalies detected.
                    Self-healing has been applied automatically.
                    Monitor pipeline for further degradation.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                """
                <div class="alert-medium" style="margin-bottom:0;">
                    <div style="font-weight:600; font-size:0.85rem;">
                        🔍 Recommended
                    </div>
                    <div style="font-size:0.82rem; margin-top:4px;">
                        Review Analytics page for anomaly trends
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                """
                <div class="alert-medium" style="margin-bottom:0;">
                    <div style="font-weight:600; font-size:0.85rem;">
                        🛠️ Self-Healing Active
                    </div>
                    <div style="font-size:0.82rem; margin-top:4px;">
                        Anomalous records repaired automatically
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.markdown(
            f"""
            <div class="alert-low">
                <div style="font-size:1rem; font-weight:700; margin-bottom:4px;">
                    🟢 System Operating Normally — Low Risk
                </div>
                <div style="font-size:0.88rem;">
                    <b>{total_anomalies:,}</b> anomalies detected and handled.
                    Pipeline health is excellent.
                    All systems are functioning within normal parameters.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                """
                <div class="alert-low" style="margin-bottom:0;">
                    <div style="font-weight:600; font-size:0.85rem;">
                        ✅ Pipeline Healthy
                    </div>
                    <div style="font-size:0.82rem; margin-top:4px;">
                        All 5 pipeline steps completed successfully
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                """
                <div class="alert-low" style="margin-bottom:0;">
                    <div style="font-weight:600; font-size:0.85rem;">
                        🛡️ Fraud Protection Active
                    </div>
                    <div style="font-size:0.82rem; margin-top:4px;">
                        Isolation Forest monitoring all transactions
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )