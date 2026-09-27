import streamlit as st
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_PATH = BASE_DIR / "logs" / "pipeline.log"


def _parse_level(line: str) -> str:

    u = line.upper()

    if "ERROR" in u:
        return "ERROR"

    if "WARNING" in u:
        return "WARNING"

    if "SUCCESS" in u or "COMPLETED" in u:
        return "SUCCESS"

    return "INFO"


def _level_style(level: str):

    styles = {
        "ERROR": (
            "#FFF1F2",
            "#EF4444",
            "🔴"
        ),

        "WARNING": (
            "#FFFBEB",
            "#F59E0B",
            "🟡"
        ),

        "SUCCESS": (
            "#F0FDF4",
            "#1DB954",
            "🟢"
        ),

        "INFO": (
            "#F9FAFB",
            "#6B7280",
            "⚪"
        ),
    }

    return styles.get(
        level,
        ("#F9FAFB", "#6B7280", "⚪")
    )


def _safe_read_log():

    if not LOG_PATH.exists():
        return None

    try:

        with open(
            LOG_PATH,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            return f.read()

    except Exception as e:

        st.error(
            f"Unable to read log file: {str(e)}"
        )

        return None


def show_logs():

    # ══════════════════════════════════════════
    # Header
    # ══════════════════════════════════════════
    st.markdown(
        '<p class="section-header">📜 Pipeline Logs</p>',
        unsafe_allow_html=True
    )

    # ══════════════════════════════════════════
    # Toolbar
    # ══════════════════════════════════════════
    t1, t2, t3 = st.columns([1, 1, 4])

    with t1:

        if st.button(
            "🔄 Refresh",
            width="stretch"
        ):
            st.rerun()

    with t3:

        search = st.text_input(
            "Search",
            placeholder="Filter logs...",
            label_visibility="collapsed"
        )

    # ══════════════════════════════════════════
    # Read Logs
    # ══════════════════════════════════════════
    raw = _safe_read_log()

    if raw is None:

        st.markdown(
            f"""
            <div class="alert-medium">
                ⚠️ <b>Log file not found</b><br>
                <span style="font-size:0.85rem;">
                    Expected at:
                    <code>{LOG_PATH}</code>
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        return

    if not raw.strip():

        st.info(
            "Log file is empty. Run the pipeline first."
        )

        return

    # ══════════════════════════════════════════
    # Clean Lines
    # ══════════════════════════════════════════
    lines = [
        l.strip()
        for l in raw.splitlines()
        if l.strip()
    ]

    # ══════════════════════════════════════════
    # Stats
    # ══════════════════════════════════════════
    total = len(lines)

    errors = sum(
        _parse_level(l) == "ERROR"
        for l in lines
    )

    warnings = sum(
        _parse_level(l) == "WARNING"
        for l in lines
    )

    success = sum(
        _parse_level(l) == "SUCCESS"
        for l in lines
    )

    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "📋 Total Lines",
        f"{total:,}"
    )

    m2.metric(
        "🟢 Success",
        f"{success:,}"
    )

    m3.metric(
        "🟡 Warnings",
        f"{warnings:,}"
    )

    m4.metric(
        "🔴 Errors",
        f"{errors:,}"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # Status Banner
    # ══════════════════════════════════════════
    if errors > 0:

        st.markdown(
            f"""
            <div class="alert-high">
                🔴 <b>{errors} error(s)</b>
                detected in pipeline logs.
            </div>
            """,
            unsafe_allow_html=True
        )

    elif warnings > 0:

        st.markdown(
            f"""
            <div class="alert-medium">
                🟡 <b>{warnings} warning(s)</b>
                found in logs.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="alert-low">
                🟢 All pipeline steps completed successfully.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # Tabs
    # ══════════════════════════════════════════
    tab1, tab2, tab3, tab4 = st.tabs([
        f"📋 All ({total})",
        f"🟢 Success ({success})",
        f"🟡 Warnings ({warnings})",
        f"🔴 Errors ({errors})",
    ])

    def render_logs(filtered, empty_msg):

        if not filtered:
            st.info(empty_msg)
            return

        # Search Filter
        if search:

            filtered = [
                l for l in filtered
                if search.lower() in l.lower()
            ]

            if not filtered:

                st.info(
                    f"No results found for '{search}'."
                )

                return

        rows_html = ""

        # Last 100 lines only
        for line in filtered[-100:]:

            level = _parse_level(line)

            bg, border, emoji = _level_style(level)

            safe = (
                line.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
            )

            rows_html += f"""
            <div style="
                background:{bg};
                border-left:3px solid {border};
                border-radius:6px;
                padding:6px 10px;
                margin-bottom:4px;
                font-family:'JetBrains Mono','Fira Code',monospace;
                font-size:0.78rem;
                color:#374151;
                line-height:1.5;
            ">
                {emoji} {safe}
            </div>
            """

        st.markdown(
            f"""
            <div style="
                max-height:450px;
                overflow-y:auto;
                padding-right:4px;
            ">
                {rows_html}
            </div>
            """,
            unsafe_allow_html=True
        )

        if len(filtered) > 100:

            st.caption(
                f"Showing last 100 of {len(filtered):,} lines."
            )

    # ══════════════════════════════════════════
    # Tab Content
    # ══════════════════════════════════════════
    with tab1:

        render_logs(
            lines,
            "No logs found."
        )

    with tab2:

        render_logs(
            [
                l for l in lines
                if _parse_level(l) == "SUCCESS"
            ],
            "No success logs."
        )

    with tab3:

        render_logs(
            [
                l for l in lines
                if _parse_level(l) == "WARNING"
            ],
            "No warning logs."
        )

    with tab4:

        render_logs(
            [
                l for l in lines
                if _parse_level(l) == "ERROR"
            ],
            "No error logs."
        )

    # ══════════════════════════════════════════
    # Download
    # ══════════════════════════════════════════
    st.markdown("<br>", unsafe_allow_html=True)

    st.download_button(
        label="⬇️ Download Full Log",
        data=raw,
        file_name=(
            f"pipeline_logs_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        ),
        mime="text/plain",
        width="stretch"
    )