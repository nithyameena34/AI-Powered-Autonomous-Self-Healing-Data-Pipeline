def load_css():
    return """
    <style>

        /* ── Base ── */
        .main {
            background-color: #F4F7F6;
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E8EDE8;
        }

        [data-testid="stSidebar"] .stRadio label {
            font-size: 0.9rem;
            color: #374151;
            padding: 6px 0;
        }

        [data-testid="stSidebar"] .stRadio label:hover {
            color: #1DB954;
        }

        /* ── Header ── */
        .pipeline-header {
            background: linear-gradient(135deg, #1DB954, #17A349);
            padding: 1.5rem 2rem;
            border-radius: 16px;
            margin-bottom: 1.5rem;
            color: white;
            box-shadow: 0 4px 20px rgba(29, 185, 84, 0.25);
        }

        .pipeline-header h1 {
            font-size: 1.6rem;
            font-weight: 700;
            margin: 0;
            color: white;
        }

        .pipeline-header p {
            font-size: 0.9rem;
            margin: 0.3rem 0 0 0;
            color: rgba(255,255,255,0.85);
        }

        /* ── KPI Cards ── */
        div[data-testid="metric-container"] {
            background: #FFFFFF;
            border: 1px solid #E8EDE8;
            border-radius: 16px;
            padding: 1.2rem 1rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: box-shadow 0.2s ease;
        }

        div[data-testid="metric-container"]:hover {
            box-shadow: 0 4px 16px rgba(29, 185, 84, 0.15);
            border-color: #1DB954;
        }

        div[data-testid="metric-container"] label {
            font-size: 0.8rem;
            font-weight: 600;
            color: #6B7280;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        div[data-testid="metric-container"] [data-testid="stMetricValue"] {
            font-size: 1.6rem;
            font-weight: 700;
            color: #111827;
        }

        div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
            font-size: 0.8rem;
        }

        /* ── Section Headers ── */
        .section-header {
            font-size: 1rem;
            font-weight: 700;
            color: #111827;
            margin: 1.5rem 0 0.8rem 0;
            padding-bottom: 0.4rem;
            border-bottom: 2px solid #1DB954;
            display: inline-block;
        }

        /* ── Cards ── */
        .dashboard-card {
            background: #FFFFFF;
            border: 1px solid #E8EDE8;
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
        }

        .dashboard-card h3 {
            font-size: 1rem;
            font-weight: 600;
            color: #111827;
            margin-bottom: 0.5rem;
        }

        .dashboard-card p {
            font-size: 0.88rem;
            color: #6B7280;
        }

        /* ── Alert Banners ── */
        .alert-low {
            background: #F0FDF4;
            border: 1px solid #86EFAC;
            border-left: 4px solid #1DB954;
            border-radius: 10px;
            padding: 0.8rem 1.2rem;
            color: #166534;
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: 1rem;
        }

        .alert-medium {
            background: #FFFBEB;
            border: 1px solid #FCD34D;
            border-left: 4px solid #F59E0B;
            border-radius: 10px;
            padding: 0.8rem 1.2rem;
            color: #92400E;
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: 1rem;
        }

        .alert-high {
            background: #FFF1F2;
            border: 1px solid #FDA4AF;
            border-left: 4px solid #EF4444;
            border-radius: 10px;
            padding: 0.8rem 1.2rem;
            color: #9F1239;
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: 1rem;
        }

        /* ── Status Badges ── */
        .badge-success {
            background: #DCFCE7;
            color: #166534;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 600;
        }

        .badge-warning {
            background: #FEF9C3;
            color: #854D0E;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 600;
        }

        .badge-danger {
            background: #FFE4E6;
            color: #9F1239;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 600;
        }

        .badge-info {
            background: #DBEAFE;
            color: #1E40AF;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 600;
        }

        /* ── Pipeline Status Steps ── */
        .pipeline-step {
            background: #FFFFFF;
            border: 1px solid #E8EDE8;
            border-radius: 12px;
            padding: 0.8rem 1.2rem;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        }

        .pipeline-step-done {
            border-left: 4px solid #1DB954;
        }

        .pipeline-step-fail {
            border-left: 4px solid #EF4444;
        }

        /* ── Tables ── */
        .dataframe {
            border: none !important;
            font-size: 0.85rem !important;
        }

        .dataframe thead th {
            background-color: #F9FAFB !important;
            color: #374151 !important;
            font-weight: 600 !important;
            border-bottom: 2px solid #E5E7EB !important;
        }

        .dataframe tbody tr:hover {
            background-color: #F0FDF4 !important;
        }

        /* ── Tabs ── */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #F9FAFB;
            border-radius: 10px;
            padding: 4px;
            gap: 4px;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            color: #6B7280;
            font-weight: 500;
            font-size: 0.88rem;
        }

        .stTabs [aria-selected="true"] {
            background-color: #1DB954 !important;
            color: white !important;
        }

        /* ── Plotly Charts ── */
        .js-plotly-plot {
            border-radius: 12px;
        }

        /* ── Scrollbar ── */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }

        ::-webkit-scrollbar-track {
            background: #F4F7F6;
        }

        ::-webkit-scrollbar-thumb {
            background: #1DB954;
            border-radius: 10px;
        }

        /* ── Headings ── */
        h1, h2, h3 {
            color: #111827;
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }

        /* ── Divider ── */
        hr {
            border: none;
            border-top: 1px solid #E8EDE8;
            margin: 1rem 0;
        }

    </style>
    """