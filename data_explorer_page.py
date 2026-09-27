import streamlit as st
import pandas as pd
from utils.data_loader import (
    load_healed_data,
    load_anomaly_data,
    load_anomaly_db,
    load_healing_summary,
)


def show_data_explorer(df: pd.DataFrame):

    # ── Header ──
    st.markdown(
        """
        <div class="pipeline-header">
            <h1>🗄️ Data Explorer</h1>
            <p>Browse, filter, and inspect every record produced by the pipeline —
               healed transactions, anomalies, quarantined fraud, and database tables.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ── Load fresh data ──
    healed_df    = df if not df.empty else load_healed_data()
    anomaly_df   = load_anomaly_data()
    healing_sum  = load_healing_summary()

    if healed_df.empty:
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
    # ROW 1 — Dataset quick stats
    # ══════════════════════════════════════════
    total       = len(healed_df)
    original    = len(healed_df[healed_df["HealingStatus"] == "Original"])    \
                  if "HealingStatus" in healed_df.columns else 0
    healed      = len(healed_df[healed_df["HealingStatus"] == "Healed"])      \
                  if "HealingStatus" in healed_df.columns else 0
    quarantined = len(healed_df[healed_df["HealingStatus"] == "Quarantined"]) \
                  if "HealingStatus" in healed_df.columns else 0
    cols_count  = len(healed_df.columns)

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("📦 Total Records",    f"{total:,}")
    m2.metric("✅ Original",          f"{original:,}")
    m3.metric("🛠️ Healed",           f"{healed:,}")
    m4.metric("🔒 Quarantined",       f"{quarantined:,}")
    m5.metric("📋 Columns",           f"{cols_count}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # TABS
    # ══════════════════════════════════════════
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 All Transactions",
        "🚨 Anomalies Only",
        "🔒 Quarantined Fraud",
        "🛠️ Healed Records",
        "📊 DB Tables",
    ])

    # ──────────────────────────────────────────
    # TAB 1 — All Transactions
    # ──────────────────────────────────────────
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        _render_table(
            healed_df,
            title        = "All Transactions",
            filter_col   = "HealingStatus",
            search_label = "Search / filter records",
        )

    # ──────────────────────────────────────────
    # TAB 2 — Anomalies Only
    # ──────────────────────────────────────────
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)

        if anomaly_df.empty:
            st.info("No anomaly data available.")
        else:
            anomalies_only = anomaly_df[
                anomaly_df["Anomaly"] == "Anomaly"
            ].reset_index(drop=True)

            st.markdown(
                f"""
                <div class="alert-medium" style="margin-bottom:1rem;">
                    🚨 <b>{len(anomalies_only):,}</b> anomalous records detected
                    by Isolation Forest.
                </div>
                """,
                unsafe_allow_html=True
            )
            _render_table(
                anomalies_only,
                title        = "Anomaly Records",
                filter_col   = "Class",
                search_label = "Filter anomaly records",
            )

    # ──────────────────────────────────────────
    # TAB 3 — Quarantined Fraud
    # ──────────────────────────────────────────
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)

        if "HealingStatus" not in healed_df.columns:
            st.info("HealingStatus column not found.")
        else:
            fraud_df = healed_df[
                healed_df["HealingStatus"] == "Quarantined"
            ].reset_index(drop=True)

            if fraud_df.empty:
                st.markdown(
                    """
                    <div class="alert-low">
                        ✅ <b>No quarantined records.</b>
                        The pipeline did not isolate any confirmed fraud.
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div class="alert-high" style="margin-bottom:1rem;">
                        🔒 <b>{len(fraud_df):,}</b> confirmed fraud records
                        quarantined and isolated from the clean dataset.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Amount summary for fraud records
                if "Amount" in fraud_df.columns:
                    fa1, fa2, fa3 = st.columns(3)
                    fa1.metric("💰 Total Fraud Amount",
                               f"${fraud_df['Amount'].sum():,.2f}")
                    fa2.metric("📊 Avg Fraud Amount",
                               f"${fraud_df['Amount'].mean():,.2f}")
                    fa3.metric("🔺 Max Fraud Amount",
                               f"${fraud_df['Amount'].max():,.2f}")
                    st.markdown("<br>", unsafe_allow_html=True)

                _render_table(
                    fraud_df,
                    title        = "Quarantined Fraud Records",
                    filter_col   = None,
                    search_label = "Filter fraud records",
                )

    # ──────────────────────────────────────────
    # TAB 4 — Healed Records
    # ──────────────────────────────────────────
    with tab4:
        st.markdown("<br>", unsafe_allow_html=True)

        if "HealingStatus" not in healed_df.columns:
            st.info("HealingStatus column not found.")
        else:
            healed_only = healed_df[
                healed_df["HealingStatus"] == "Healed"
            ].reset_index(drop=True)

            if healed_only.empty:
                st.info("No healed records found.")
            else:
                st.markdown(
                    f"""
                    <div class="alert-low" style="margin-bottom:1rem;">
                        🛠️ <b>{len(healed_only):,}</b> anomalous records were
                        automatically repaired by the self-healing engine.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if "Amount" in healed_only.columns:
                    ha1, ha2, ha3 = st.columns(3)
                    ha1.metric("💰 Total Healed Amount",
                               f"${healed_only['Amount'].sum():,.2f}")
                    ha2.metric("📊 Avg Healed Amount",
                               f"${healed_only['Amount'].mean():,.2f}")
                    ha3.metric("🔺 Max Healed Amount",
                               f"${healed_only['Amount'].max():,.2f}")
                    st.markdown("<br>", unsafe_allow_html=True)

                _render_table(
                    healed_only,
                    title        = "Healed Records",
                    filter_col   = None,
                    search_label = "Filter healed records",
                )

    # ──────────────────────────────────────────
    # TAB 5 — DB Tables
    # ──────────────────────────────────────────
    with tab5:
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            '<p class="section-header">🗄️ Database Tables (pipeline.db)</p>',
            unsafe_allow_html=True
        )

        db_tab1, db_tab2 = st.tabs([
            "📊 Healing Summary",
            "🔍 Anomaly Results (DB)",
        ])

        with db_tab1:
            if not healing_sum.empty:
                st.markdown("<br>", unsafe_allow_html=True)

                for _, row in healing_sum.iterrows():
                    status = row.get("HealingStatus", "Unknown")
                    count  = int(row.get("Count", 0))
                    color_map = {
                        "Original"    : "#1DB954",
                        "Healed"      : "#3B82F6",
                        "Quarantined" : "#EF4444",
                    }
                    color = color_map.get(status, "#6B7280")
                    st.markdown(
                        f"""
                        <div class="dashboard-card"
                             style="border-left:4px solid {color};
                                    display:flex;
                                    justify-content:space-between;
                                    align-items:center;
                                    padding:0.8rem 1.2rem;
                                    margin-bottom:8px;">
                            <span style="font-weight:600; color:#111827;">
                                {status}
                            </span>
                            <span style="font-size:1.3rem; font-weight:700;
                                         color:{color};">
                                {count:,}
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info("Healing summary table not found in database.")

        with db_tab2:
            anomaly_db_df = load_anomaly_db()
            if not anomaly_db_df.empty:
                st.markdown("<br>", unsafe_allow_html=True)
                _render_table(
                    anomaly_db_df,
                    title        = "Anomaly Results (from DB)",
                    filter_col   = "Anomaly",
                    search_label = "Filter DB anomaly records",
                    page_size    = 50,
                )
            else:
                st.info("Anomaly results table not found in database.")


# ══════════════════════════════════════════════
# Helper — reusable filtered + paginated table
# ══════════════════════════════════════════════

def _render_table(
    data         : pd.DataFrame,
    title        : str,
    filter_col   : str | None,
    search_label : str  = "Filter records",
    page_size    : int  = 100,
):
    if data.empty:
        st.info("No records to display.")
        return

    filtered = data.copy()

    # ── Filter controls ──
    fc1, fc2, fc3 = st.columns([2, 2, 1])

    with fc1:
        search = st.text_input(
            search_label,
            key              = f"search_{title}",
            placeholder      = "Type to filter any column...",
            label_visibility = "collapsed"
        )

    with fc2:
        if filter_col and filter_col in data.columns:
            options  = ["All"] + sorted(data[filter_col].astype(str).unique().tolist())
            selected = st.selectbox(
                f"Filter by {filter_col}",
                options,
                key              = f"filter_{title}",
                label_visibility = "collapsed"
            )
            if selected != "All":
                filtered = filtered[
                    filtered[filter_col].astype(str) == selected
                ]

    with fc3:
        st.markdown(
            f"""
            <div style="
                background:#F0FDF4;
                border:1px solid #86EFAC;
                border-radius:8px;
                padding:6px 12px;
                text-align:center;
                font-size:0.85rem;
                font-weight:600;
                color:#166534;
            ">
                {len(filtered):,} rows
            </div>
            """,
            unsafe_allow_html=True
        )

    # ── Text search across all columns ──
    if search:
        mask     = filtered.astype(str).apply(
            lambda col: col.str.contains(search, case=False, na=False)
        ).any(axis=1)
        filtered = filtered[mask]

    if filtered.empty:
        st.info("No records match the current filter.")
        return

    # ── Pagination ──
    total_pages = max(1, (len(filtered) - 1) // page_size + 1)

    if total_pages > 1:
        page = st.number_input(
            f"Page (1–{total_pages})",
            min_value        = 1,
            max_value        = total_pages,
            value            = 1,
            key              = f"page_{title}",
            label_visibility = "collapsed"
        )
    else:
        page = 1

    start = (page - 1) * page_size
    end   = start + page_size

    st.dataframe(
        filtered.iloc[start:end].reset_index(drop=True),
        use_container_width = True,
        hide_index          = True,
    )

    if total_pages > 1:
        st.caption(
            f"Page {page} of {total_pages} · "
            f"Showing rows {start+1:,}–{min(end, len(filtered)):,} "
            f"of {len(filtered):,}"
        )