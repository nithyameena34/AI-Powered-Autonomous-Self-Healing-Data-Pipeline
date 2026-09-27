import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from components.charts import show_charts
from utils.data_loader import load_prediction_data


CHART_LAYOUT = dict(
    paper_bgcolor = "rgba(0,0,0,0)",
    plot_bgcolor  = "rgba(0,0,0,0)",
    font          = {"family": "Inter, Segoe UI, sans-serif", "color": "#374151"},
    margin        = dict(t=30, b=30, l=10, r=10),
    xaxis         = dict(showgrid=False, linecolor="#E5E7EB"),
    yaxis         = dict(gridcolor="#F3F4F6", linecolor="#E5E7EB"),
)


def show_analytics(df: pd.DataFrame, anomaly_df: pd.DataFrame):

    # ── Header ──
    st.markdown(
        """
        <div class="pipeline-header">
            <h1>📊 Analytics</h1>
            <p>Deep-dive into transaction patterns, anomaly distribution,
               and model performance across the full dataset.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    prediction = load_prediction_data()

    if df.empty and anomaly_df.empty:
        st.markdown(
            """
            <div class="alert-medium">
                🟡 <b>No data available.</b>
                Run <code>python main.py</code> to generate pipeline output.
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    # ══════════════════════════════════════════
    # ROW 1 — Quick Stats Bar
    # ══════════════════════════════════════════
    m1, m2, m3, m4, m5, m6 = st.columns(6)

    m1.metric("📦 Total",          f"{prediction.get('TotalRecords',   0):,}")
    m2.metric("✅ Normal",          f"{prediction.get('NormalRecords',  0):,}")
    m3.metric("🚨 Anomalies",       f"{prediction.get('Anomalies',      0):,}")
    m4.metric("🔒 Fraud",           f"{prediction.get('ConfirmedFraud', 0):,}")
    m5.metric("🎯 Detection Rate",  f"{prediction.get('DetectionRate',  0):.2f}%")
    m6.metric("💚 Health",          f"{prediction.get('HealthScore',    0):.2f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # TABS — organise analytics into sections
    # ══════════════════════════════════════════
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Anomaly Analysis",
        "💰 Transaction Patterns",
        "🤖 Model Performance",
        "📋 Data Profile",
    ])

    # ──────────────────────────────────────────
    # TAB 1 — Anomaly Analysis
    # ──────────────────────────────────────────
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        show_charts(df, anomaly_df)

    # ──────────────────────────────────────────
    # TAB 2 — Transaction Patterns
    # ──────────────────────────────────────────
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)

        if anomaly_df.empty:
            st.info("No transaction data available.")
        else:
            col1, col2 = st.columns(2)

            # Amount by Healing Status
            with col1:
                st.markdown(
                    '<p class="section-header">💳 Amount by Healing Status</p>',
                    unsafe_allow_html=True
                )
                if "Amount" in df.columns and "HealingStatus" in df.columns:
                    cap     = df["Amount"].quantile(0.99)
                    plot_df = df[df["Amount"] <= cap]

                    fig = px.box(
                        plot_df,
                        x      = "HealingStatus",
                        y      = "Amount",
                        color  = "HealingStatus",
                        points = False,
                        color_discrete_map = {
                            "Original"    : "#1DB954",
                            "Healed"      : "#3B82F6",
                            "Quarantined" : "#EF4444",
                        }
                    )
                    fig.update_layout(
                        **CHART_LAYOUT,
                        height      = 300,
                        showlegend  = False,
                        xaxis_title = "",
                        yaxis_title = "Amount (USD)",
                    )
                    st.plotly_chart(
                        fig,
                        use_container_width = True,
                        config={"displayModeBar": False}
                    )
                else:
                    st.info("Amount or HealingStatus column not found.")

            # High-value anomalies
            with col2:
                st.markdown(
                    '<p class="section-header">🔺 High-Value Anomalies (Top 20)</p>',
                    unsafe_allow_html=True
                )
                if "Amount" in anomaly_df.columns and "Anomaly" in anomaly_df.columns:
                    top_anomalies = (
                        anomaly_df[anomaly_df["Anomaly"] == "Anomaly"]
                        .nlargest(20, "Amount")[["Amount", "Time", "Class"]]
                        .reset_index(drop=True)
                    )
                    top_anomalies.index += 1

                    fig = px.bar(
                        top_anomalies.reset_index(),
                        x     = "index",
                        y     = "Amount",
                        color = "Amount",
                        color_continuous_scale = ["#DCFCE7", "#1DB954", "#166534"],
                        text  = "Amount",
                    )
                    fig.update_traces(
                        texttemplate      = "$%{text:,.2f}",
                        textposition      = "outside",
                        marker_line_width = 0,
                    )
                    fig.update_layout(
                        **CHART_LAYOUT,
                        height              = 300,
                        coloraxis_showscale = False,
                        xaxis_title         = "Rank",
                        yaxis_title         = "Amount (USD)",
                        showlegend          = False,
                    )
                    st.plotly_chart(
                        fig,
                        use_container_width = True,
                        config={"displayModeBar": False}
                    )
                else:
                    st.info("No amount data available.")

            # Time distribution
            st.markdown(
                '<p class="section-header">🕐 Transaction Volume over Time</p>',
                unsafe_allow_html=True
            )
            if "Time" in anomaly_df.columns and "Anomaly" in anomaly_df.columns:
                temp = anomaly_df.copy()
                temp["TimeBlock"] = pd.cut(
                    temp["Time"],
                    bins   = 48,
                    labels = [f"T{i+1}" for i in range(48)]
                )

                volume = (
                    temp.groupby(["TimeBlock", "Anomaly"], observed=True)
                    .size()
                    .reset_index(name="Count")
                )

                fig = px.bar(
                    volume,
                    x      = "TimeBlock",
                    y      = "Count",
                    color  = "Anomaly",
                    barmode= "stack",
                    color_discrete_map = {
                        "Normal"  : "#1DB954",
                        "Anomaly" : "#EF4444",
                    },
                )
                fig.update_layout(
                    **CHART_LAYOUT,
                    height      = 280,
                    xaxis_title = "Time Block",
                    yaxis_title = "Transactions",
                    legend      = dict(orientation="h", y=1.1),
                    bargap      = 0.05,
                )
                st.plotly_chart(
                    fig,
                    use_container_width = True,
                    config={"displayModeBar": False}
                )
            else:
                st.info("No time column found.")

    # ──────────────────────────────────────────
    # TAB 3 — Model Performance
    # ──────────────────────────────────────────
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                '<p class="section-header">🎯 Confusion Matrix</p>',
                unsafe_allow_html=True
            )

            if not anomaly_df.empty and "Class" in anomaly_df.columns and "Anomaly" in anomaly_df.columns:
                from sklearn.metrics import confusion_matrix

                y_true = anomaly_df["Class"].map({0: "Normal", 1: "Anomaly"})
                y_pred = anomaly_df["Anomaly"]

                cm     = confusion_matrix(
                    y_true, y_pred,
                    labels=["Normal", "Anomaly"]
                )

                fig = px.imshow(
                    cm,
                    labels = dict(x="Predicted", y="Actual", color="Count"),
                    x      = ["Normal", "Anomaly"],
                    y      = ["Normal", "Anomaly"],
                    text_auto = True,
                    color_continuous_scale = ["#F0FDF4", "#1DB954", "#166534"],
                )
                fig.update_layout(
                    **CHART_LAYOUT,
                    height = 300,
                )
                st.plotly_chart(
                    fig,
                    use_container_width = True,
                    config={"displayModeBar": False}
                )
            else:
                st.info("Class labels not available for confusion matrix.")

        with col2:
            st.markdown(
                '<p class="section-header">📈 Performance Metrics</p>',
                unsafe_allow_html=True
            )

            metrics = [
                ("Detection Rate",      prediction.get("DetectionRate",     0),  100, "#1DB954"),
                ("Health Score",        prediction.get("HealthScore",        0),  100, "#3B82F6"),
                ("Healing Rate",        prediction.get("HealingRate",        0),  100, "#8B5CF6"),
                ("False Positive Rate", prediction.get("FalsePositiveRate",  0),    1, "#F59E0B"),
            ]

            for label, value, scale, color in metrics:
                pct = min((value / scale) * 100, 100)
                st.markdown(
                    f"""
                    <div style="margin-bottom: 14px;">
                        <div style="display:flex; justify-content:space-between;
                                    margin-bottom:4px;">
                            <span style="font-size:0.85rem; font-weight:600;
                                         color:#374151;">{label}</span>
                            <span style="font-size:0.85rem; font-weight:700;
                                         color:{color};">{value:.4f}%</span>
                        </div>
                        <div style="background:#F3F4F6; border-radius:999px;
                                    height:8px; overflow:hidden;">
                            <div style="
                                width:{pct:.1f}%;
                                height:100%;
                                background:{color};
                                border-radius:999px;
                            "></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # ──────────────────────────────────────────
    # TAB 4 — Data Profile
    # ──────────────────────────────────────────
    with tab4:
        st.markdown("<br>", unsafe_allow_html=True)

        target_df = anomaly_df if not anomaly_df.empty else df

        if target_df.empty:
            st.info("No data available.")
        else:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(
                    '<p class="section-header">📋 Dataset Overview</p>',
                    unsafe_allow_html=True
                )
                overview = pd.DataFrame({
                    "Property" : ["Rows", "Columns", "Memory (MB)", "Missing Values"],
                    "Value"    : [
                        f"{len(target_df):,}",
                        f"{len(target_df.columns)}",
                        f"{target_df.memory_usage(deep=True).sum() / 1e6:.2f}",
                        f"{target_df.isnull().sum().sum():,}",
                    ]
                })
                st.dataframe(
                    overview,
                    use_container_width = True,
                    hide_index          = True
                )

            with col2:
                st.markdown(
                    '<p class="section-header">📊 Column Summary</p>',
                    unsafe_allow_html=True
                )
                num_cols  = target_df.select_dtypes(include="number").columns
                summary   = target_df[num_cols].describe().T[
                    ["mean", "std", "min", "max"]
                ].round(4)
                st.dataframe(
                    summary,
                    use_container_width = True
                )