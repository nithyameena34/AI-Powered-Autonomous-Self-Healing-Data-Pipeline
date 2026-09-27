import streamlit as st
from utils.data_loader import check_pipeline_status


def show_pipeline_status():

    st.markdown(
        '<p class="section-header">🔧 Pipeline Status</p>',
        unsafe_allow_html=True
    )

    status = check_pipeline_status()

    # Pipeline steps with icons and descriptions
    steps = [
        {
            "key"   : "ETL",
            "icon"  : "⚙️",
            "label" : "ETL Processing",
            "desc"  : "Data cleaning and normalization",
            "file"  : "clean_transactions.csv"
        },
        {
            "key"   : "Anomaly Detection",
            "icon"  : "🔍",
            "label" : "Anomaly Detection",
            "desc"  : "Isolation Forest ML model",
            "file"  : "anomaly_results.csv"
        },
        {
            "key"   : "Self Healing",
            "icon"  : "🛠️",
            "label" : "Self Healing",
            "desc"  : "Autonomous record repair",
            "file"  : "healed_transactions.csv"
        },
        {
            "key"   : "Database",
            "icon"  : "🗄️",
            "label" : "Database Storage",
            "desc"  : "SQLite persistence",
            "file"  : "pipeline.db"
        },
        {
            "key"   : "Failure Prediction",
            "icon"  : "📊",
            "label" : "Failure Prediction",
            "desc"  : "Risk classification",
            "file"  : "failure_prediction.csv"
        },
    ]

    # Overall summary row
    total     = len(steps)
    completed = sum(1 for s in steps if status.get(s["key"], False))

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Steps", total)

    with col2:
        st.metric("Completed", completed)

    with col3:
        st.metric("Failed", total - completed)

    st.markdown("<br>", unsafe_allow_html=True)

    # Step cards
    for step in steps:
        done        = status.get(step["key"], False)
        card_class  = "pipeline-step-done" if done else "pipeline-step-fail"
        badge_class = "badge-success"      if done else "badge-danger"
        badge_text  = "✅ Completed"        if done else "❌ Not Run"

        st.markdown(
            f"""
            <div class="pipeline-step {card_class}">
                <div style="display:flex; align-items:center; gap:12px;">
                    <span style="font-size:1.4rem">{step["icon"]}</span>
                    <div>
                        <div style="font-weight:600; color:#111827; font-size:0.95rem;">
                            {step["label"]}
                        </div>
                        <div style="font-size:0.8rem; color:#6B7280; margin-top:2px;">
                            {step["desc"]}  ·  <code style="font-size:0.75rem;">{step["file"]}</code>
                        </div>
                    </div>
                </div>
                <span class="{badge_class}">{badge_text}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Overall pipeline health bar
    progress = completed / total if total > 0 else 0
    color    = "#1DB954" if progress == 1.0 else "#F59E0B" if progress >= 0.6 else "#EF4444"

    st.markdown(
        f"""
        <div class="dashboard-card">
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span style="font-weight:600; color:#111827;">Pipeline Completion</span>
                <span style="font-weight:700; color:{color};">{int(progress * 100)}%</span>
            </div>
            <div style="background:#F3F4F6; border-radius:999px; height:10px; overflow:hidden;">
                <div style="
                    width:{int(progress * 100)}%;
                    height:100%;
                    background:{color};
                    border-radius:999px;
                    transition: width 0.5s ease;
                "></div>
            </div>
            <div style="margin-top:8px; font-size:0.8rem; color:#6B7280;">
                {completed} of {total} steps completed
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )