import streamlit as st
from datetime import datetime
from components.logs_viewer import show_logs
from components.pipeline_status import show_pipeline_status
from utils.data_loader import check_pipeline_status, load_logs


def show_monitoring():

    # ── Header ──
    st.markdown(
        """
        <div class="pipeline-header">
            <h1>📡 Pipeline Monitoring</h1>
            <p>Track pipeline activity, step completion, errors, and runtime status in real time.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ══════════════════════════════════════════
    # ROW 1 — Live Status Metrics
    # ══════════════════════════════════════════
    pipeline_status = check_pipeline_status()
    all_done        = all(pipeline_status.values())
    completed       = sum(pipeline_status.values())
    total_steps     = len(pipeline_status)
    now             = datetime.now()

    m1, m2, m3, m4, m5 = st.columns(5)

    m1.metric(
        "🔄 Status",
        "✅ Complete" if all_done else "🟡 Partial"
    )
    m2.metric(
        "✅ Steps Done",
        f"{completed} / {total_steps}"
    )
    m3.metric(
        "🕐 Last Refresh",
        now.strftime("%I:%M %p")
    )
    m4.metric(
        "📅 Run Date",
        now.strftime("%d %b %Y")
    )
    m5.metric(
        "📂 Log Source",
        "pipeline.log"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # ROW 2 — Quick Health Banner
    # ══════════════════════════════════════════
    if all_done:
        st.markdown(
            """
            <div class="alert-low">
                🟢 <b>All pipeline steps completed successfully.</b>
                Output files are available for dashboard and export.
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        failed = [k for k, v in pipeline_status.items() if not v]
        st.markdown(
            f"""
            <div class="alert-medium">
                🟡 <b>Pipeline incomplete.</b>
                The following steps have not run yet:
                <b>{", ".join(failed)}</b>.
                Run <code>python main.py</code> to complete the pipeline.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # ROW 3 — Pipeline Status + Log Summary
    # ══════════════════════════════════════════
    left, right = st.columns([1, 1])

    with left:
        show_pipeline_status()

    with right:
        st.markdown(
            '<p class="section-header">📊 Log Summary</p>',
            unsafe_allow_html=True
        )

        logs      = load_logs()
        log_lines = [l.strip() for l in logs if l.strip()]

        total    = len(log_lines)
        errors   = sum("ERROR"   in l.upper() for l in log_lines)
        warnings = sum("WARNING" in l.upper() for l in log_lines)
        success  = sum(
            "COMPLETED" in l.upper() or "SUCCESS" in l.upper()
            for l in log_lines
        )

        lm1, lm2 = st.columns(2)
        lm1.metric("📋 Log Lines",   f"{total:,}")
        lm2.metric("🟢 Completions", f"{success:,}")

        lm3, lm4 = st.columns(2)
        lm3.metric("🟡 Warnings",    f"{warnings:,}")
        lm4.metric("🔴 Errors",      f"{errors:,}")

        st.markdown("<br>", unsafe_allow_html=True)

        # Recent activity — last 5 log lines
        st.markdown(
            '<p class="section-header">🕐 Recent Activity</p>',
            unsafe_allow_html=True
        )

        recent    = log_lines[-5:] if log_lines else []
        level_cfg = {
            "ERROR"   : ("#FFF1F2", "#EF4444", "🔴"),
            "WARNING" : ("#FFFBEB", "#F59E0B", "🟡"),
            "SUCCESS" : ("#F0FDF4", "#1DB954", "🟢"),
            "COMPLETED":("#F0FDF4", "#1DB954", "🟢"),
            "INFO"    : ("#F9FAFB", "#6B7280", "⚪"),
        }

        if recent:
            for line in reversed(recent):
                level = "INFO"
                for key in level_cfg:
                    if key in line.upper():
                        level = key
                        break

                bg, border, emoji = level_cfg[level]
                safe = (
                    line.replace("&", "&amp;")
                        .replace("<", "&lt;")
                        .replace(">", "&gt;")
                )
                st.markdown(
                    f"""
                    <div style="
                        background:{bg};
                        border-left: 3px solid {border};
                        border-radius:6px;
                        padding:5px 10px;
                        margin-bottom:4px;
                        font-family:'JetBrains Mono','Fira Code',monospace;
                        font-size:0.76rem;
                        color:#374151;
                        line-height:1.5;
                    ">{emoji} {safe}</div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("No recent log activity.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # ROW 4 — Full Log Viewer
    # ══════════════════════════════════════════
    with st.expander("📜 Full Log Viewer", expanded=False):
        show_logs()