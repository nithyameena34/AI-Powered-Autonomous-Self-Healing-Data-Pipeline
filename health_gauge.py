import streamlit as st
import plotly.graph_objects as go


def show_health_gauge(score: float):

    # ── Color based on score ──
    if score >= 95:
        color      = "#1DB954"
        label      = "Excellent"
        badge      = "badge-success"
        bar_color  = "#1DB954"

    elif score >= 85:
        color      = "#F59E0B"
        label      = "Good"
        badge      = "badge-warning"
        bar_color  = "#F59E0B"

    else:
        color      = "#EF4444"
        label      = "Critical"
        badge      = "badge-danger"
        bar_color  = "#EF4444"

    # ── Plotly Gauge Chart ──
    fig = go.Figure(go.Indicator(
        mode  = "gauge+number",
        value = score,
        title = {
            "text"     : "Pipeline Health Score",
            "font"     : {"size": 14, "color": "#6B7280", "family": "Inter"}
        },
        number = {
            "suffix"   : "%",
            "font"     : {"size": 36, "color": "#111827", "family": "Inter"}
        },
        gauge = {
            "axis"     : {
                "range"     : [0, 100],
                "tickwidth" : 1,
                "tickcolor" : "#E5E7EB",
                "tickfont"  : {"size": 10, "color": "#9CA3AF"}
            },
            "bar"      : {"color": bar_color, "thickness": 0.25},
            "bgcolor"  : "white",
            "borderwidth": 0,
            "steps"    : [
                {"range": [0,  60],  "color": "#FEE2E2"},
                {"range": [60, 85],  "color": "#FEF9C3"},
                {"range": [85, 100], "color": "#DCFCE7"},
            ],
            "threshold": {
                "line" : {"color": color, "width": 3},
                "thickness": 0.8,
                "value": score
            }
        }
    ))

    fig.update_layout(
        height      = 240,
        margin      = dict(t=40, b=10, l=20, r=20),
        paper_bgcolor = "rgba(0,0,0,0)",
        font        = {"family": "Inter, Segoe UI, sans-serif"}
    )

    # ── Card Wrapper ──
    st.markdown(
        f"""
        <div class="dashboard-card" style="padding-bottom: 0.5rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
                <span style="font-weight:700; color:#111827; font-size:0.95rem;">
                    💚 Pipeline Health
                </span>
                <span class="{badge}" style="font-size:0.8rem;">
                    {label}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ── Score breakdown bar ──
    st.markdown(
        f"""
        <div style="
            background: #F9FAFB;
            border: 1px solid #E8EDE8;
            border-radius: 12px;
            padding: 0.8rem 1rem;
            margin-top: -0.5rem;
        ">
            <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                <span style="font-size:0.82rem; color:#6B7280; font-weight:500;">Health Score</span>
                <span style="font-size:0.82rem; font-weight:700; color:{color};">{score:.2f}%</span>
            </div>
            <div style="background:#E5E7EB; border-radius:999px; height:8px; overflow:hidden;">
                <div style="
                    width:{score}%;
                    height:100%;
                    background: linear-gradient(90deg, {color}99, {color});
                    border-radius:999px;
                "></div>
            </div>
            <div style="display:flex; justify-content:space-between; margin-top:6px;">
                <span style="font-size:0.75rem; color:#9CA3AF;">0%</span>
                <span style="font-size:0.75rem; color:#9CA3AF;">Critical &lt;85%</span>
                <span style="font-size:0.75rem; color:#9CA3AF;">100%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )