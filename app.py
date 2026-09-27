import streamlit as st
from utils.data_loader import (
    load_healed_data,
    load_anomaly_data,
    load_prediction_data,
    check_pipeline_status,
)
from utils.styles import load_css
from page_modules.dashboard_page     import show_dashboard
from page_modules.analytics_page     import show_analytics
from page_modules.monitoring_page    import show_monitoring
from page_modules.ai_insights_page   import show_ai_page
from page_modules.data_explorer_page import show_data_explorer
from page_modules.reports_page       import show_reports_page

# ══════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════
st.set_page_config(
    page_title = "AI Self-Healing Pipeline",
    page_icon  = "🚀",
    layout     = "wide",
)

st.markdown(load_css(), unsafe_allow_html=True)

# ══════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════
df              = load_healed_data()
anomaly_df      = load_anomaly_data()
prediction      = load_prediction_data()
pipeline_status = check_pipeline_status()

all_done   = all(pipeline_status.values())
completed  = sum(pipeline_status.values())
total_steps= len(pipeline_status)
risk       = prediction.get("FailureRisk", "N/A")
health     = prediction.get("HealthScore",  0.0)
det_rate   = prediction.get("DetectionRate", 0.0)
heal_rate  = prediction.get("HealingRate",   0.0)

risk_color = {
    "LOW"   : "#1DB954",
    "MEDIUM": "#F59E0B",
    "HIGH"  : "#EF4444",
}.get(risk, "#6B7280")

# ══════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════
with st.sidebar:

    # ── Brand ──
    st.markdown(
        """
        <div style="padding:1rem 0.5rem 0.5rem 0.5rem; text-align:center;">
            <div style="font-size:2rem;">🚀</div>
            <div style="font-weight:700; font-size:1rem; color:#111827;
                        line-height:1.3; margin-top:4px;">
                AI Self-Healing<br>Pipeline
            </div>
            <div style="font-size:0.75rem; color:#6B7280; margin-top:2px;">
                Enterprise Edition
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<hr style='border-color:#E8EDE8; margin:0.5rem 0'>", unsafe_allow_html=True)

    # ── Pipeline status pill ──
    if all_done:
        st.markdown(
            """
            <div style="background:#DCFCE7; border:1px solid #86EFAC;
                        border-radius:20px; padding:5px 12px; text-align:center;
                        font-size:0.82rem; font-weight:600; color:#166534;
                        margin:0.5rem 0;">
                🟢 Pipeline Complete
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="background:#FFFBEB; border:1px solid #FCD34D;
                        border-radius:20px; padding:5px 12px; text-align:center;
                        font-size:0.82rem; font-weight:600; color:#92400E;
                        margin:0.5rem 0;">
                🟡 {completed}/{total_steps} Steps Done
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Live KPI tiles ──
    kpis = [
        ("💚 Health Score",   f"{health:.2f}%",    risk_color if health < 95 else "#1DB954"),
        ("⚠️ Risk Level",     risk,                 risk_color),
        ("🎯 Detection Rate", f"{det_rate:.2f}%",  "#3B82F6"),
        ("🛠️ Healing Rate",  f"{heal_rate:.2f}%", "#8B5CF6"),
    ]

    for label, value, color in kpis:
        st.markdown(
            f"""
            <div style="background:#F9FAFB; border:1px solid #E8EDE8;
                        border-left:3px solid {color};
                        border-radius:8px; padding:8px 12px;
                        margin-bottom:6px;">
                <div style="font-size:0.72rem; font-weight:600; color:#6B7280;
                            text-transform:uppercase; letter-spacing:0.04em;">
                    {label}
                </div>
                <div style="font-size:1.1rem; font-weight:700; color:#111827;
                            margin-top:2px;">
                    {value}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#E8EDE8; margin:0'>", unsafe_allow_html=True)

    # ── Pipeline step checklist ──
    st.markdown(
        "<div style='font-size:0.78rem; font-weight:700; color:#6B7280; "
        "text-transform:uppercase; letter-spacing:0.05em; "
        "padding:0.6rem 0 0.3rem 0;'>Pipeline Steps</div>",
        unsafe_allow_html=True
    )

    step_icons = {
        "ETL"               : "⚙️",
        "Anomaly Detection" : "🔍",
        "Self Healing"      : "🛠️",
        "Database"          : "🗄️",
        "Failure Prediction": "📊",
    }

    for step, status in pipeline_status.items():
        icon   = step_icons.get(step, "▸")
        color  = "#1DB954" if status else "#EF4444"
        badge  = "✅" if status else "❌"
        st.markdown(
            f"""
            <div style="display:flex; justify-content:space-between;
                        align-items:center; padding:5px 4px;
                        border-bottom:1px solid #F3F4F6;">
                <span style="font-size:0.82rem; color:#374151;">
                    {icon} {step}
                </span>
                <span style="font-size:0.78rem;">{badge}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#E8EDE8; margin:0'>", unsafe_allow_html=True)

    # ── Navigation ──
    st.markdown(
        "<div style='font-size:0.78rem; font-weight:700; color:#6B7280; "
        "text-transform:uppercase; letter-spacing:0.05em; "
        "padding:0.6rem 0 0.3rem 0;'>Navigation</div>",
        unsafe_allow_html=True
    )

    page = st.radio(
        "nav",
        [
            "🏠  Dashboard",
            "📊  Analytics",
            "📡  Monitoring",
            "🤖  AI Insights",
            "🗄️  Data Explorer",
            "📄  Reports",
        ],
        label_visibility = "collapsed",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#E8EDE8; margin:0'>", unsafe_allow_html=True)

    # ── Footer info ──
    st.markdown(
        """
        <div style="padding:0.8rem 0.2rem; font-size:0.75rem; color:#9CA3AF;
                    line-height:1.8;">
            <div style="font-weight:600; color:#6B7280; margin-bottom:4px;">
                Built With
            </div>
            Streamlit · Pandas<br>
            Isolation Forest · SQLite<br>
            Scikit-learn · Plotly
        </div>
        """,
        unsafe_allow_html=True
    )

# ══════════════════════════════════════════
# REMOVE DEFAULT STREAMLIT TITLE
# (each page renders its own header banner)
# ══════════════════════════════════════════

# ══════════════════════════════════════════
# PAGE ROUTING
# ══════════════════════════════════════════
if "Dashboard" in page:
    show_dashboard(prediction)

elif "Analytics" in page:
    show_analytics(df, anomaly_df)

elif "Monitoring" in page:
    show_monitoring()

elif "AI Insights" in page:
    show_ai_page(
        prediction.get("TotalRecords",  0),
        prediction.get("Anomalies",     0),
        prediction.get("HealthScore",   0),
        prediction.get("FailureRisk", "LOW"),
    )

elif "Data Explorer" in page:
    show_data_explorer(df)

elif "Reports" in page:
    show_reports_page(df)

# ══════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="border-top:1px solid #E8EDE8; padding:1rem 0;
                text-align:center; color:#9CA3AF; font-size:0.78rem;">
        🚀 AI-Powered Autonomous Self-Healing Data Pipeline &nbsp;·&nbsp;
        Streamlit &nbsp;·&nbsp; Pandas &nbsp;·&nbsp;
        Isolation Forest &nbsp;·&nbsp; SQLite &nbsp;·&nbsp;
        Scikit-learn &nbsp;·&nbsp; Plotly
    </div>
    """,
    unsafe_allow_html=True
)