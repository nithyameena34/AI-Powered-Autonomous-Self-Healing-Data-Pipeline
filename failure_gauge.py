import plotly.graph_objects as go
import streamlit as st


def show_failure_gauge(anomaly_rate: float, risk: str):

    # ── Colors based on risk ──
    risk_config = {
        "LOW"    : {"color": "#1DB954", "bg": "#DCFCE7", "text": "#166534", "badge": "badge-success", "emoji": "🟢"},
        "MEDIUM" : {"color": "#F59E0B", "bg": "#FEF9C3", "text": "#92400E", "badge": "badge-warning", "emoji": "🟡"},
        "HIGH"   : {"color": "#EF4444", "bg": "#FFE4E6", "text": "#9F1239", "badge": "badge-danger",  "emoji": "🔴"},
    }

    cfg   = risk_config.get(risk, risk_config["LOW"])
    color = cfg["color"]

    # ── Clamp display range ──
    # Real anomaly rates are tiny (0.17%), so use 0–1% range for visual clarity
    display_max = max(1.0, anomaly_rate * 3)

    fig = go.Figure(go.Indicator(
        mode  = "gauge+number+delta",
        value = anomaly_rate,
        title = {
            "text" : "Anomaly Rate",
            "font" : {"size": 14, "color": "#6B7280", "family": "Inter"}
        },
        number = {
            "suffix"    : "%",
            "font"      : {"size": 36, "color": "#111827", "family": "Inter"},
            "valueformat": ".4f"
        },
        delta  = {
            "reference"  : 0.1,
            "increasing" : {"color": "#EF4444"},
            "decreasing" : {"color": "#1DB954"},
            "valueformat": ".4f"
        },
        gauge = {
            "axis" : {
                "range"    : [0, display_max],
                "tickwidth": 1,
                "tickcolor": "#E5E7EB",
                "tickfont" : {"size": 10, "color": "#9CA3AF"},
                "tickformat": ".2f"
            },
            "bar"        : {"color": color, "thickness": 0.25},
            "bgcolor"    : "white",
            "borderwidth": 0,
            "steps"      : [
                {"range": [0,              display_max * 0.3], "color": "#DCFCE7"},
                {"range": [display_max * 0.3, display_max * 0.6], "color": "#FEF9C3"},
                {"range": [display_max * 0.6, display_max],       "color": "#FFE4E6"},
            ],
            "threshold"  : {
                "line"     : {"color": color, "width": 3},
                "thickness": 0.8,
                "value"    : anomaly_rate
            }
        }
    ))

    fig.update_layout(
        height        = 240,
        margin        = dict(t=40, b=10, l=20, r=20),
        paper_bgcolor = "rgba(0,0,0,0)",
        font          = {"family": "Inter, Segoe UI, sans-serif"}
    )

    # ── Card wrapper ──
    st.markdown(
        f"""
        <div class="dashboard-card" style="padding-bottom: 0.5rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
                <span style="font-weight:700; color:#111827; font-size:0.95rem;">
                    ⚠️ Failure Risk Gauge
                </span>
                <span class="{cfg['badge']}">
                    {cfg['emoji']} {risk}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ── Risk breakdown ──
    thresholds = [
        ("🟢 Low",    "< 0.10%",  "#1DB954"),
        ("🟡 Medium", "0.10–0.50%", "#F59E0B"),
        ("🔴 High",   "> 0.50%",  "#EF4444"),
    ]

    cols = st.columns(3)

    for i, (label, range_text, t_color) in enumerate(thresholds):
        active = (
            (risk == "LOW"    and i == 0) or
            (risk == "MEDIUM" and i == 1) or
            (risk == "HIGH"   and i == 2)
        )
        border = f"2px solid {t_color}" if active else "1px solid #E8EDE8"
        bg     = cfg["bg"] if active else "#F9FAFB"

        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    background:{bg};
                    border:{border};
                    border-radius:10px;
                    padding:0.6rem 0.8rem;
                    text-align:center;
                ">
                    <div style="font-size:0.82rem; font-weight:700; color:{t_color};">
                        {label}
                    </div>
                    <div style="font-size:0.75rem; color:#6B7280; margin-top:2px;">
                        {range_text}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )