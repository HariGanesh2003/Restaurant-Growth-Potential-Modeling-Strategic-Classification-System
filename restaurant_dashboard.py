"""
╔══════════════════════════════════════════════════════════════════════╗
║   Restaurant Growth Potential Modeling & Strategic Classification    ║
║   Streamlit Dashboard  |  SkyCity Auckland Restaurants & Bars        ║
╚══════════════════════════════════════════════════════════════════════╝
Run:  streamlit run restaurant_dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Restaurant Growth Intelligence",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS  — White background · Blue theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ---------- Base ---------- */
html, body, [class*="css"] {
    background-color: #FFFFFF !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.stApp { background-color: #FFFFFF !important; }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A1F5C 0%, #1A3A8F 50%, #1565C0 100%) !important;
    border-right: 3px solid #1E88E5;
}
[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {
    color: #B3D4FF !important;
    font-weight: 600;
    font-size: 13px;
    letter-spacing: 0.5px;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #1E3A6E !important;
    border: 1px solid #4A90D9 !important;
    color: #FFFFFF !important;
}

/* ---------- Main Title Banner ---------- */
.main-title-banner {
    background: linear-gradient(135deg, #0A1F5C 0%, #1565C0 50%, #1E88E5 100%);
    border-radius: 16px;
    padding: 32px 40px;
    margin-bottom: 28px;
    box-shadow: 0 8px 32px rgba(21, 101, 192, 0.35);
    text-align: center;
}
.main-title-banner h1 {
    color: #FFFFFF !important;
    font-size: 2.8rem !important;
    font-weight: 900 !important;
    letter-spacing: 1.5px;
    margin: 0 0 8px 0;
    text-shadow: 0 2px 8px rgba(0,0,0,0.3);
}
.main-title-banner p {
    color: #B3D4FF !important;
    font-size: 1.05rem;
    margin: 0;
    letter-spacing: 0.5px;
}

/* ---------- Tab Styling ---------- */
.stTabs [data-baseweb="tab-list"] {
    background-color: #F0F4FF;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #C5D8F5;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    border-radius: 10px;
    color: #1A3A8F !important;
    font-weight: 700;
    font-size: 14px;
    padding: 10px 20px;
    border: none;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1565C0, #1E88E5) !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 12px rgba(21, 101, 192, 0.4);
}

/* ---------- KPI Cards ---------- */
.kpi-card {
    background: linear-gradient(135deg, #FFFFFF 0%, #F0F6FF 100%);
    border: 1.5px solid #C5D8F5;
    border-top: 4px solid #1565C0;
    border-radius: 14px;
    padding: 20px 18px;
    text-align: center;
    box-shadow: 0 4px 16px rgba(21, 101, 192, 0.12);
    transition: transform 0.2s;
    height: 140px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.kpi-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(21,101,192,0.2); }
.kpi-icon { font-size: 1.6rem; margin-bottom: 6px; }
.kpi-label { color: #5A7DBF; font-size: 11px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 6px; }
.kpi-value { color: #0A1F5C; font-size: 1.8rem; font-weight: 900; line-height: 1.1; }
.kpi-sub { color: #7A9FCC; font-size: 11px; margin-top: 4px; }

/* ---------- Section Headers ---------- */
.section-header {
    background: linear-gradient(90deg, #EBF2FF, #FFFFFF);
    border-left: 5px solid #1565C0;
    border-radius: 0 10px 10px 0;
    padding: 14px 20px;
    margin: 24px 0 16px 0;
}
.section-header h2 {
    color: #0A1F5C !important;
    font-size: 1.35rem !important;
    font-weight: 800 !important;
    margin: 0;
}
.section-header p {
    color: #5A7DBF;
    font-size: 13px;
    margin: 4px 0 0 0;
}

/* ---------- Insight / Observation Cards ---------- */
.obs-card {
    background: #F8FBFF;
    border: 1px solid #D4E6FF;
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 10px;
    border-left: 4px solid #1E88E5;
}
.obs-card-number {
    background: linear-gradient(135deg, #1565C0, #1E88E5);
    color: white;
    border-radius: 50%;
    width: 26px; height: 26px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 800;
    margin-right: 10px;
}
.obs-card p { color: #1A2F5A; font-size: 14px; margin: 0; line-height: 1.6; }

/* ---------- Recommendation Cards ---------- */
.rec-card {
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 12px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.08);
}
.rec-card h4 { font-size: 15px; font-weight: 800; margin: 0 0 8px 0; }
.rec-card p { font-size: 13.5px; line-height: 1.65; margin: 0; }
.rec-high   { background: #FFF0F0; border-left: 5px solid #E53935; }
.rec-stable { background: #F0FFF4; border-left: 5px solid #1B8A3A; }
.rec-dep    { background: #FFFBF0; border-left: 5px solid #F59E0B; }
.rec-general{ background: #F0F6FF; border-left: 5px solid #1565C0; }
.rec-card h4.high-title   { color: #B71C1C; }
.rec-card h4.stable-title { color: #1B5E20; }
.rec-card h4.dep-title    { color: #7C4F00; }
.rec-card h4.gen-title    { color: #0A1F5C; }

/* ---------- Strategy Cluster Badge ---------- */
.badge-high    { background:#FFEBEE; color:#C62828; border:1.5px solid #EF9A9A; border-radius:20px; padding:4px 14px; font-size:12px; font-weight:700; }
.badge-stable  { background:#E8F5E9; color:#2E7D32; border:1.5px solid #A5D6A7; border-radius:20px; padding:4px 14px; font-size:12px; font-weight:700; }
.badge-dep     { background:#FFF8E1; color:#F57F17; border:1.5px solid #FFE082; border-radius:20px; padding:4px 14px; font-size:12px; font-weight:700; }

/* ---------- Sidebar Brand ---------- */
.sidebar-brand {
    text-align: center;
    padding: 10px 0 20px 0;
    border-bottom: 1px solid rgba(255,255,255,0.2);
    margin-bottom: 20px;
}
.sidebar-brand h2 { color: #FFFFFF !important; font-size: 1.1rem !important; font-weight: 800; margin: 8px 0 4px 0; }
.sidebar-brand p  { color: #B3D4FF !important; font-size: 11px; margin: 0; }

/* ---------- DataFrame styling ---------- */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }
.stDataFrame th { background-color: #1565C0 !important; color: white !important; }

/* ---------- Footer ---------- */
.dashboard-footer {
    text-align: center; color: #9BB8D9; font-size: 12px;
    margin-top: 40px; padding: 20px;
    border-top: 1px solid #D4E6FF;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  COLOUR PALETTES
# ─────────────────────────────────────────────
BLUE_GRADIENT  = ["#0A1F5C","#1A3A8F","#1565C0","#1E88E5","#42A5F5","#90CAF9","#BBDEFB","#E3F2FD"]
BLUE_5         = ["#0A1F5C","#1565C0","#1E88E5","#42A5F5","#90CAF9"]
CLUSTER_COLORS = {
    "High-Growth":          "#E53935",
    "Stable Performers":    "#1B8A3A",
    "Dependent Low Margin": "#F59E0B",
}
CHANNEL_COLORS = ["#0A1F5C","#1565C0","#1E88E5","#42A5F5"]


# ─────────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(r"D:\MyFiles\Downloads\Unified Mentor Intership Project\Resturant_Analysis.csv")
    df["TotalNetProfit"]    = (df["InStoreNetProfit"] + df["UberEatsNetProfit"] +
                               df["DoorDashNetProfit"] + df["SelfDeliveryNetProfit"])
    df["TotalRevenue"]      = (df["InStoreRevenue"] + df["UberEatsRevenue"] +
                               df["DoorDashRevenue"] + df["SelfDeliveryRevenue"])
    df["Scale"]             = df["MonthlyOrders"] * df["GrowthFactor"]
    df["CostDiscipline"]    = df["COGSRate"] + df["OPEXRate"]
    df["AggregatorDep"]     = df["UE_share"] + df["DD_share"]
    df["ExpansionHeadroom"] = df["DeliveryRadiusKM"] / (df["MonthlyOrders"] / 100)
    df["RevenueQuality"]    = df["AOV"] * (1 - df["CostDiscipline"])
    return df

df_full = load_data()


# ─────────────────────────────────────────────
#  SIDEBAR — FILTER PANEL
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div style="font-size:2.2rem">🍽️</div>
        <h2>Restaurant Intelligence</h2>
        <p>SkyCity Auckland · Growth Analytics</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("### 🎛️ Filter Panel")
    st.markdown("---")

    subregion_opts = ["All"] + sorted(df_full["Subregion"].unique().tolist())
    sel_subregion  = st.selectbox("📍 Subregion", subregion_opts)

    cuisine_opts   = ["All"] + sorted(df_full["CuisineType"].unique().tolist())
    sel_cuisine    = st.selectbox("🍜 Cuisine Type", cuisine_opts)

    segment_opts   = ["All"] + sorted(df_full["Segment"].unique().tolist())
    sel_segment    = st.selectbox("🏪 Segment", segment_opts)

    cluster_opts   = ["All"] + sorted(df_full["Cluster_Label"].unique().tolist())
    sel_cluster    = st.selectbox("📊 Cluster", cluster_opts)

    st.markdown("---")

    gpi_min = float(df_full["GPI"].min())
    gpi_max = float(df_full["GPI"].max())
    gpi_range = st.slider("📈 GPI Range", gpi_min, gpi_max, (gpi_min, gpi_max), step=0.01)

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; padding:10px 0">
        <p style="color:#B3D4FF; font-size:11px; margin:0">
            📋 1,696 Restaurants<br>
            🗺️ 4 Subregions · 8 Cuisines<br>
            🔬 3 Strategic Clusters
        </p>
    </div>""", unsafe_allow_html=True)

# ── Apply filters ──
df = df_full.copy()
if sel_subregion != "All": df = df[df["Subregion"] == sel_subregion]
if sel_cuisine   != "All": df = df[df["CuisineType"] == sel_cuisine]
if sel_segment   != "All": df = df[df["Segment"] == sel_segment]
if sel_cluster   != "All": df = df[df["Cluster_Label"] == sel_cluster]
df = df[(df["GPI"] >= gpi_range[0]) & (df["GPI"] <= gpi_range[1])]


# ─────────────────────────────────────────────
#  MAIN TITLE BANNER
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-title-banner">
    <h1>🍽️ Restaurant Growth Potential Modeling &amp; Strategic Classification System</h1>
    <p>SkyCity Auckland Restaurants &amp; Bars · Data-Driven Growth Intelligence Dashboard · 1,696 Restaurants Analyzed</p>
</div>
""", unsafe_allow_html=True)

# Active filter badge
active_filters = []
if sel_subregion != "All": active_filters.append(f"📍 {sel_subregion}")
if sel_cuisine   != "All": active_filters.append(f"🍜 {sel_cuisine}")
if sel_segment   != "All": active_filters.append(f"🏪 {sel_segment}")
if sel_cluster   != "All": active_filters.append(f"📊 {sel_cluster}")
if active_filters:
    st.info(f"🎛️ **Active Filters:** {' · '.join(active_filters)}  |  Showing **{len(df):,}** restaurants")
else:
    st.success(f"✅ Showing all **{len(df):,}** restaurants · No filters applied")


# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Executive Overview",
    "🔬 Cluster Intelligence",
    "📈 Growth Levers & EDA",
    "🍽️ Restaurant Explorer",
    "🎯 Strategy & Recommendations",
])


# ═══════════════════════════════════════════════════════════════
#  TAB 1 — EXECUTIVE OVERVIEW
# ═══════════════════════════════════════════════════════════════
with tab1:

    # ── KPI Cards ──
    st.markdown("""<div class="section-header"><h2>📌 Key Performance Indicators</h2>
    <p>Strategic KPIs derived from operational, financial and channel data</p></div>""",
    unsafe_allow_html=True)

    k1, k2, k3, k4, k5 = st.columns(5)

    scale_val    = df["Scale"].mean()
    cost_val     = df["CostDiscipline"].mean()
    agg_val      = df["AggregatorDep"].mean()
    head_val     = df["DeliveryRadiusKM"].mean()
    rev_val      = df["RevenueQuality"].mean()

    with k1:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-icon">⚡</div>
            <div class="kpi-label">Scale</div>
            <div class="kpi-value">{scale_val:,.0f}</div>
            <div class="kpi-sub">Orders × GrowthFactor</div>
        </div>""", unsafe_allow_html=True)

    with k2:
        cost_pct = cost_val * 100
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-icon">💰</div>
            <div class="kpi-label">Cost Discipline</div>
            <div class="kpi-value">{cost_pct:.1f}%</div>
            <div class="kpi-sub">COGS + OPEX Avg Rate</div>
        </div>""", unsafe_allow_html=True)

    with k3:
        agg_pct = agg_val * 100
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-icon">📦</div>
            <div class="kpi-label">Aggregator Dep.</div>
            <div class="kpi-value">{agg_pct:.1f}%</div>
            <div class="kpi-sub">UberEats + DoorDash Share</div>
        </div>""", unsafe_allow_html=True)

    with k4:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-icon">📡</div>
            <div class="kpi-label">Expansion Headroom</div>
            <div class="kpi-value">{head_val:.1f} km</div>
            <div class="kpi-sub">Avg Delivery Radius</div>
        </div>""", unsafe_allow_html=True)

    with k5:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-icon">💎</div>
            <div class="kpi-label">Revenue Quality</div>
            <div class="kpi-value">${rev_val:.2f}</div>
            <div class="kpi-sub">AOV × Margin Proxy</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 2 KPIs ──
    k6, k7, k8, k9, k10 = st.columns(5)
    total_rest  = len(df)
    avg_gpi     = df["GPI"].mean()
    avg_aov     = df["AOV"].mean()
    avg_orders  = df["MonthlyOrders"].mean()
    avg_profit  = df["TotalNetProfit"].mean()

    with k6:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-icon">🏢</div>
            <div class="kpi-label">Restaurants</div>
            <div class="kpi-value">{total_rest:,}</div>
            <div class="kpi-sub">In Current Filter</div>
        </div>""", unsafe_allow_html=True)

    with k7:
        gpi_sign = "+" if avg_gpi >= 0 else ""
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-icon">📊</div>
            <div class="kpi-label">Avg GPI Score</div>
            <div class="kpi-value">{gpi_sign}{avg_gpi:.3f}</div>
            <div class="kpi-sub">Growth Potential Index</div>
        </div>""", unsafe_allow_html=True)

    with k8:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-icon">🛒</div>
            <div class="kpi-label">Avg Order Value</div>
            <div class="kpi-value">${avg_aov:.2f}</div>
            <div class="kpi-sub">Average Order Value (AOV)</div>
        </div>""", unsafe_allow_html=True)

    with k9:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-icon">📋</div>
            <div class="kpi-label">Avg Monthly Orders</div>
            <div class="kpi-value">{avg_orders:,.0f}</div>
            <div class="kpi-sub">Per Restaurant</div>
        </div>""", unsafe_allow_html=True)

    with k10:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-icon">💵</div>
            <div class="kpi-label">Avg Net Profit</div>
            <div class="kpi-value">${avg_profit:,.0f}</div>
            <div class="kpi-sub">All Channels Combined</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Overview Charts ──
    st.markdown("""<div class="section-header"><h2>📊 Portfolio Overview</h2>
    <p>High-level view of restaurant distribution and growth performance</p></div>""",
    unsafe_allow_html=True)

    ov_col1, ov_col2 = st.columns(2)

    with ov_col1:
        clust_counts = df["Cluster_Label"].value_counts().reset_index()
        clust_counts.columns = ["Cluster", "Count"]
        fig_pie = px.pie(
            clust_counts, names="Cluster", values="Count",
            title="<b>Cluster Distribution</b>",
            color="Cluster",
            color_discrete_map=CLUSTER_COLORS,
            hole=0.42,
        )
        fig_pie.update_traces(textfont_size=13, textfont_color="white",
                              marker=dict(line=dict(color="#FFFFFF", width=2)))
        fig_pie.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(color="#000000", size=13),
            legend=dict(font=dict(color="#000000"), title_font=dict(color="#000000")),
            title_font=dict(size=16, color="#0A1F5C"),
            margin=dict(t=50, b=20),
        )
        fig_pie.update_xaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        fig_pie.update_yaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with ov_col2:
        seg_counts = df["Segment"].value_counts().reset_index()
        seg_counts.columns = ["Segment", "Count"]
        fig_seg = px.bar(
            seg_counts.sort_values("Count"),
            x="Count", y="Segment", orientation="h",
            title="<b>Restaurant Count by Segment</b>",
            color="Count",
            color_continuous_scale=["#BBDEFB","#1565C0","#0A1F5C"],
            text="Count",
        )
        fig_seg.update_traces(textfont_color="#000000", textposition="outside")
        fig_seg.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(color="#000000", size=13),
            xaxis=dict(color="#000000", showgrid=True, gridcolor="#E8F0FE", title_font=dict(color="#000000")),
            yaxis=dict(color="#000000", title_font=dict(color="#000000")),
            coloraxis_showscale=False,
            title_font=dict(size=16, color="#0A1F5C"),
            margin=dict(t=50, b=20),
        )
        fig_seg.update_xaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        fig_seg.update_yaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        st.plotly_chart(fig_seg, use_container_width=True)

    ov_col3, ov_col4 = st.columns(2)

    with ov_col3:
        gpi_sub = df.groupby("Subregion")["GPI"].mean().reset_index().sort_values("GPI")
        colors_sub = [BLUE_GRADIENT[i] for i in range(len(gpi_sub))]
        fig_gpi_sub = px.bar(
            gpi_sub, x="GPI", y="Subregion", orientation="h",
            title="<b>Avg GPI by Subregion</b>",
            color="GPI",
            color_continuous_scale=["#BBDEFB","#1565C0","#0A1F5C"],
            text=gpi_sub["GPI"].round(3),
        )
        fig_gpi_sub.update_traces(textfont_color="#000000", textposition="outside")
        fig_gpi_sub.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(color="#000000", size=13),
            xaxis=dict(color="#000000", showgrid=True, gridcolor="#E8F0FE", title_font=dict(color="#000000")),
            yaxis=dict(color="#000000", title_font=dict(color="#000000")),
            coloraxis_showscale=False,
            title_font=dict(size=16, color="#0A1F5C"),
            margin=dict(t=50, b=20),
        )
        fig_gpi_sub.update_xaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        fig_gpi_sub.update_yaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        st.plotly_chart(fig_gpi_sub, use_container_width=True)

    with ov_col4:
        gpi_seg = df.groupby("Segment")["GPI"].mean().reset_index().sort_values("GPI")
        fig_gpi_seg = px.bar(
            gpi_seg, x="GPI", y="Segment", orientation="h",
            title="<b>Avg GPI by Segment</b>",
            color="GPI",
            color_continuous_scale=["#BBDEFB","#1565C0","#0A1F5C"],
            text=gpi_seg["GPI"].round(3),
        )
        fig_gpi_seg.update_traces(textfont_color="#000000", textposition="outside")
        fig_gpi_seg.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(color="#000000", size=13),
            xaxis=dict(color="#000000", showgrid=True, gridcolor="#E8F0FE", title_font=dict(color="#000000")),
            yaxis=dict(color="#000000", title_font=dict(color="#000000")),
            coloraxis_showscale=False,
            title_font=dict(size=16, color="#0A1F5C"),
            margin=dict(t=50, b=20),
        )
        fig_gpi_seg.update_xaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        fig_gpi_seg.update_yaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        st.plotly_chart(fig_gpi_seg, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
#  TAB 2 — CLUSTER INTELLIGENCE
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""<div class="section-header"><h2>🔬 Cluster Intelligence & Profiling</h2>
    <p>Deep-dive into the 3 strategic restaurant archetypes identified via K-Means + PCA</p></div>""",
    unsafe_allow_html=True)

    # ── Cluster KPI comparison ──
    cl_col1, cl_col2, cl_col3 = st.columns(3)
    cluster_summary = df.groupby("Cluster_Label").agg(
        Count=("RestaurantID","count"),
        Avg_GPI=("GPI","mean"),
        Avg_Orders=("MonthlyOrders","mean"),
        Avg_AOV=("AOV","mean"),
        Avg_COGS=("COGSRate","mean"),
        Avg_OPEX=("OPEXRate","mean"),
        Avg_Radius=("DeliveryRadiusKM","mean"),
    ).round(3)

    for i, (cluster, row) in enumerate(cluster_summary.iterrows()):
        col = [cl_col1, cl_col2, cl_col3][i % 3]
        badge_class = ("badge-high" if "High" in cluster
                       else "badge-stable" if "Stable" in cluster else "badge-dep")
        icon = "🔴" if "High" in cluster else ("🟢" if "Stable" in cluster else "🟡")
        gpi_sign = "+" if row["Avg_GPI"] >= 0 else ""
        with col:
            st.markdown(f"""
            <div style="background:#F8FBFF; border:1.5px solid #C5D8F5; border-radius:14px;
                        padding:18px; border-top:4px solid {'#E53935' if 'High' in cluster else '#1B8A3A' if 'Stable' in cluster else '#F59E0B'}">
                <div style="font-size:1.6rem">{icon}</div>
                <h3 style="color:#0A1F5C; font-size:1rem; font-weight:800; margin:8px 0">{cluster}</h3>
                <table style="width:100%; font-size:13px; color:#1A2F5A">
                    <tr><td>🏢 Count</td><td><b>{row['Count']:,}</b></td></tr>
                    <tr><td>📊 Avg GPI</td><td><b>{gpi_sign}{row['Avg_GPI']:.3f}</b></td></tr>
                    <tr><td>📋 Avg Orders</td><td><b>{row['Avg_Orders']:,.0f}</b></td></tr>
                    <tr><td>💰 COGS Rate</td><td><b>{row['Avg_COGS']*100:.1f}%</b></td></tr>
                    <tr><td>🏗️ OPEX Rate</td><td><b>{row['Avg_OPEX']*100:.1f}%</b></td></tr>
                    <tr><td>📡 Delivery KM</td><td><b>{row['Avg_Radius']:.1f} km</b></td></tr>
                </table>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chart 1: GPI Distribution Box ──
    cl_r1c1, cl_r1c2 = st.columns(2)

    with cl_r1c1:
        fig_box = px.box(
            df, x="Cluster_Label", y="GPI",
            color="Cluster_Label",
            color_discrete_map=CLUSTER_COLORS,
            title="<b>Chart 1 · GPI Distribution by Cluster</b>",
            points="outliers",
        )
        fig_box.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(color="#000000", size=13),
            xaxis=dict(color="#000000", title="Cluster", showgrid=False, title_font=dict(color="#000000")),
            yaxis=dict(color="#000000", title="GPI Score", showgrid=True, gridcolor="#E8F0FE", title_font=dict(color="#000000")),
            showlegend=False,
            title_font=dict(size=15, color="#0A1F5C"),
            margin=dict(t=50, b=20),
        )
        fig_box.update_xaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        fig_box.update_yaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        st.plotly_chart(fig_box, use_container_width=True)

    with cl_r1c2:
        gpi_hist = df.copy()
        fig_hist = px.histogram(
            gpi_hist, x="GPI", color="Cluster_Label",
            nbins=40,
            color_discrete_map=CLUSTER_COLORS,
            title="<b>Chart 2 · GPI Score Distribution (Histogram)</b>",
            barmode="overlay", opacity=0.75,
        )
        fig_hist.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(color="#000000", size=13),
            xaxis=dict(color="#000000", title="GPI Score", showgrid=True, gridcolor="#E8F0FE", title_font=dict(color="#000000")),
            yaxis=dict(color="#000000", title="Count", title_font=dict(color="#000000")),
            legend=dict(font=dict(color="#000000"), title="Cluster"),
            title_font=dict(size=15, color="#0A1F5C"),
            margin=dict(t=50, b=20),
        )
        fig_hist.update_xaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        fig_hist.update_yaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    # ── Chart: Radar Chart — Cluster Feature Profile ──
    st.markdown("""<div class="section-header"><h2>📡 Cluster Feature Radar Profile</h2>
    <p>Normalized feature comparison across the 3 strategic clusters</p></div>""",
    unsafe_allow_html=True)

    radar_features = ["GrowthFactor","MonthlyOrders","AOV","COGSRate","OPEXRate","CommissionRate","DeliveryRadiusKM"]
    radar_labels   = ["Growth Factor","Monthly Orders","AOV","COGS Rate","OPEX Rate","Commission Rate","Delivery Radius"]

    radar_data = df.groupby("Cluster_Label")[radar_features].mean()
    # Normalize 0-1
    radar_norm = (radar_data - radar_data.min()) / (radar_data.max() - radar_data.min() + 1e-9)

    fig_radar = go.Figure()
    cluster_color_map = {
        "High-Growth":          "#E53935",
        "Stable Performers":    "#1B8A3A",
        "Dependent Low Margin": "#F59E0B",
    }
    cluster_fill_map = {
        "High-Growth":          "rgba(229,57,53,0.18)",
        "Stable Performers":    "rgba(27,138,58,0.18)",
        "Dependent Low Margin": "rgba(245,158,11,0.18)",
    }

    for cluster in radar_norm.index:
        vals = radar_norm.loc[cluster].tolist()
        vals += [vals[0]]  # close radar loop
        fig_radar.add_trace(go.Scatterpolar(
            r=vals,
            theta=radar_labels + [radar_labels[0]],
            fill="toself",
            name=cluster,
            line=dict(color=cluster_color_map.get(cluster, "#1565C0"), width=2),
            fillcolor=cluster_fill_map.get(cluster, "rgba(21,101,192,0.18)"),
            opacity=0.90,
        ))

    fig_radar.update_layout(
        polar=dict(
            bgcolor="white",
            radialaxis=dict(
                visible=True,
                range=[0,1],
                color="#000000",
                tickfont=dict(color="#000000", size=11)
            ),
            angularaxis=dict(
                color="#000000",
                tickfont=dict(color="#000000", size=12)
            ),
        ),
        showlegend=True,
        legend=dict(
            font=dict(color="#000000"),
            title_font=dict(color="#000000")
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#000000"),
        title=dict(
            text="<b>Chart 3 · Cluster Feature Radar — Normalized Comparison</b>",
            font=dict(size=15, color="#0A1F5C")
        ),
        height=480,
        margin=dict(t=60, b=40),
    )

    st.plotly_chart(fig_radar, use_container_width=True)

    # ── Cluster Profile Heatmap ──
    st.markdown("""<div class="section-header"><h2>🌡️ Cluster Profile Heatmap</h2>
    <p>Mean values of key metrics per cluster — darker = higher value</p></div>""",
    unsafe_allow_html=True)

    hm_features = ["GrowthFactor","MonthlyOrders","AOV","COGSRate","OPEXRate","CommissionRate","DeliveryRadiusKM"]
    hm_data = df.groupby("Cluster_Label")[hm_features].mean().round(3)
    hm_norm = ((hm_data - hm_data.min()) / (hm_data.max() - hm_data.min() + 1e-9)).round(3)

    fig_hm = go.Figure(data=go.Heatmap(
        z=hm_norm.values,
        x=["Growth\nFactor","Monthly\nOrders","AOV","COGS\nRate","OPEX\nRate","Commission\nRate","Delivery\nRadius"],
        y=hm_norm.index.tolist(),
        colorscale=[[0,"#E3F2FD"],[0.5,"#1565C0"],[1,"#0A1F5C"]],
        text=hm_data.values.round(3),
        texttemplate="%{text}",
        textfont=dict(color="#000000", size=12),
        showscale=True,
    ))
    fig_hm.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(color="#000000", size=13),
        xaxis=dict(color="#000000", title_font=dict(color="#000000")),
        yaxis=dict(color="#000000", title_font=dict(color="#000000")),
        title=dict(text="<b>Chart 4 · Cluster Feature Heatmap</b>",
                   font=dict(size=15, color="#0A1F5C")),
        height=280,
        margin=dict(t=50, b=20),
    )
    fig_hm.update_xaxes(
        title_font=dict(color="#000000", size=13),
        tickfont=dict(color="#000000", size=12),
        linecolor="#000000", ticks="outside",
    )
    fig_hm.update_yaxes(
        title_font=dict(color="#000000", size=13),
        tickfont=dict(color="#000000", size=12),
        linecolor="#000000", ticks="outside",
    )
    st.plotly_chart(fig_hm, use_container_width=True)

    # ── Observations ──
    st.markdown("""<div class="section-header"><h2>💡 Cluster Analysis Observations</h2></div>""",
    unsafe_allow_html=True)
    cluster_obs = [
        ("1", "Stable Performers dominate the portfolio (44.4%), but generate only ~52% of High-Growth monthly orders — indicating volume concentration risk in fewer outlets."),
        ("2", "High-Growth restaurants (19.0%) contribute the highest avg monthly orders (~1,531) yet show negative avg GPI (−0.08) — growth is driven by cost-heavy expansion strategies."),
        ("3", "Dependent Low-Margin cluster (36.6%) has the highest avg GPI (+0.31), proving that aggregator dependence can still deliver growth efficiency if costs are controlled."),
        ("4", "South Auckland leads geographically with the highest avg GPI (+0.34), while CBD shows the lowest (−0.58) despite comparable order volumes — a clear cost pressure hotspot."),
        ("5", "QSRs form the largest segment (32%), but Ghost Kitchens (11.6%) deliver the highest avg GPI (+0.12), highlighting scalability over size in low-overhead models."),
        ("6", "Top-10 restaurants generate ~1,550–1,770 monthly orders each, confirming growth is highly skewed toward a small elite set of outlets with outsized contribution."),
    ]
    for num, text in cluster_obs:
        st.markdown(f"""<div class="obs-card">
            <span class="obs-card-number">{num}</span>
            <span style="color:#1A2F5A; font-size:14px">{text}</span>
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  TAB 3 — GROWTH LEVERS & EDA (8 Charts)
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""<div class="section-header"><h2>📈 EDA Analysis · Growth Levers & Channel Intelligence</h2>
    <p>8 comprehensive EDA charts mapping the levers that drive or constrain restaurant expansion readiness</p></div>""",
    unsafe_allow_html=True)

    # ── EDA Chart 1 & 2: Orders by Channel + Revenue by Channel ──
    eda_r1c1, eda_r1c2 = st.columns(2)

    with eda_r1c1:
        order_ch = pd.DataFrame({
            "Channel": ["In-Store","Uber Eats","DoorDash","Self-Delivery"],
            "Total Orders": [
                df["InStoreOrders"].sum(),
                df["UberEatsOrders"].sum(),
                df["DoorDashOrders"].sum(),
                df["SelfDeliveryOrders"].sum(),
            ]
        }).sort_values("Total Orders")
        fig_ord = px.bar(
            order_ch, x="Total Orders", y="Channel", orientation="h",
            title="<b>EDA Chart 1 · Total Orders by Channel</b>",
            color="Total Orders",
            color_continuous_scale=["#BBDEFB","#1565C0","#0A1F5C"],
            text=order_ch["Total Orders"].apply(lambda x: f"{x:,.0f}"),
        )
        fig_ord.update_traces(textfont_color="#000000", textposition="outside")
        fig_ord.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(color="#000000", size=13),
            xaxis=dict(color="#000000", showgrid=True, gridcolor="#E8F0FE", title_font=dict(color="#000000")),
            yaxis=dict(color="#000000", title_font=dict(color="#000000")),
            coloraxis_showscale=False,
            title_font=dict(size=14, color="#0A1F5C"),
            margin=dict(t=50, b=20, r=80),
        )
        fig_ord.update_xaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        fig_ord.update_yaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        st.plotly_chart(fig_ord, use_container_width=True)

    with eda_r1c2:
        rev_ch = pd.DataFrame({
            "Channel": ["In-Store","Uber Eats","DoorDash","Self-Delivery"],
            "Avg Revenue ($)": [
                df["InStoreRevenue"].mean(),
                df["UberEatsRevenue"].mean(),
                df["DoorDashRevenue"].mean(),
                df["SelfDeliveryRevenue"].mean(),
            ]
        }).sort_values("Avg Revenue ($)")
        fig_rev = px.bar(
            rev_ch, x="Avg Revenue ($)", y="Channel", orientation="h",
            title="<b>EDA Chart 2 · Avg Revenue by Channel</b>",
            color="Avg Revenue ($)",
            color_continuous_scale=["#E3F2FD","#1E88E5","#0A1F5C"],
            text=rev_ch["Avg Revenue ($)"].apply(lambda x: f"${x:,.0f}"),
        )
        fig_rev.update_traces(textfont_color="#000000", textposition="outside")
        fig_rev.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(color="#000000", size=13),
            xaxis=dict(color="#000000", showgrid=True, gridcolor="#E8F0FE", title_font=dict(color="#000000")),
            yaxis=dict(color="#000000", title_font=dict(color="#000000")),
            coloraxis_showscale=False,
            title_font=dict(size=14, color="#0A1F5C"),
            margin=dict(t=50, b=20, r=80),
        )
        fig_rev.update_xaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        fig_rev.update_yaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        st.plotly_chart(fig_rev, use_container_width=True)

    # ── EDA Chart 3 & 4: Cuisine Orders + Cuisine GPI ──
    eda_r2c1, eda_r2c2 = st.columns(2)

    with eda_r2c1:
        cui_ord = df.groupby("CuisineType")["MonthlyOrders"].mean().reset_index().sort_values("MonthlyOrders")
        fig_cui_ord = px.bar(
            cui_ord, x="MonthlyOrders", y="CuisineType", orientation="h",
            title="<b>EDA Chart 3 · Avg Monthly Orders by Cuisine</b>",
            color="MonthlyOrders",
            color_continuous_scale=["#BBDEFB","#1565C0","#0A1F5C"],
            text=cui_ord["MonthlyOrders"].round(0).astype(int),
        )
        fig_cui_ord.update_traces(textfont_color="#000000", textposition="outside")
        fig_cui_ord.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(color="#000000", size=13),
            xaxis=dict(color="#000000", showgrid=True, gridcolor="#E8F0FE", title_font=dict(color="#000000")),
            yaxis=dict(color="#000000", title_font=dict(color="#000000")),
            coloraxis_showscale=False,
            title_font=dict(size=14, color="#0A1F5C"),
            margin=dict(t=50, b=20, r=60),
        )
        fig_cui_ord.update_xaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        fig_cui_ord.update_yaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        st.plotly_chart(fig_cui_ord, use_container_width=True)

    with eda_r2c2:
        cui_gpi = df.groupby("CuisineType")["GPI"].mean().reset_index().sort_values("GPI")
        cui_gpi["Color"] = cui_gpi["GPI"].apply(
            lambda x: "#E53935" if x < -0.1 else ("#F59E0B" if x < 0.1 else "#1B8A3A")
        )
        fig_cui_gpi = px.bar(
            cui_gpi, x="GPI", y="CuisineType", orientation="h",
            title="<b>EDA Chart 4 · Cuisine-Wise GPI Score</b>",
            color="GPI",
            color_continuous_scale=["#E53935","#FFFFFF","#1565C0"],
            text=cui_gpi["GPI"].round(3),
        )
        fig_cui_gpi.update_traces(textfont_color="#000000", textposition="outside")
        fig_cui_gpi.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(color="#000000", size=13),
            xaxis=dict(color="#000000", showgrid=True, gridcolor="#E8F0FE", title_font=dict(color="#000000")),
            yaxis=dict(color="#000000", title_font=dict(color="#000000")),
            coloraxis_showscale=False,
            title_font=dict(size=14, color="#0A1F5C"),
            margin=dict(t=50, b=20, r=70),
        )
        fig_cui_gpi.update_xaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        fig_cui_gpi.update_yaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        st.plotly_chart(fig_cui_gpi, use_container_width=True)

    # ── EDA Chart 5 & 6: Aggregator Dep + Cost Pressure ──
    eda_r3c1, eda_r3c2 = st.columns(2)

    with eda_r3c1:
        agg_dep = df.copy()
        agg_dep["Aggregator_Ratio"] = (agg_dep["UberEatsOrders"] + agg_dep["DoorDashOrders"]) / agg_dep["MonthlyOrders"]
        agg_cluster = agg_dep.groupby("Cluster_Label")["Aggregator_Ratio"].mean().reset_index()
        agg_cluster.columns = ["Cluster", "Aggregator Ratio"]
        fig_agg = px.bar(
            agg_cluster, x="Cluster", y="Aggregator Ratio",
            title="<b>EDA Chart 5 · Aggregator Dependency by Cluster</b>",
            color="Cluster",
            color_discrete_map=CLUSTER_COLORS,
            text=agg_cluster["Aggregator Ratio"].apply(lambda x: f"{x:.2f}"),
        )
        fig_agg.update_traces(textfont_color="#000000", textposition="outside")
        fig_agg.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(color="#000000", size=13),
            xaxis=dict(color="#000000", showgrid=False, title_font=dict(color="#000000")),
            yaxis=dict(color="#000000", showgrid=True, gridcolor="#E8F0FE", title_font=dict(color="#000000")),
            showlegend=False,
            title_font=dict(size=14, color="#0A1F5C"),
            margin=dict(t=50, b=20),
        )
        fig_agg.update_xaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        fig_agg.update_yaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        st.plotly_chart(fig_agg, use_container_width=True)

    with eda_r3c2:
        cost_data = df.groupby("Cluster_Label")[["COGSRate","OPEXRate"]].mean().reset_index()
        fig_cost = go.Figure()
        fig_cost.add_trace(go.Bar(
            x=cost_data["Cluster_Label"], y=cost_data["COGSRate"],
            name="COGS Rate", marker_color="#1565C0",
            text=cost_data["COGSRate"].round(3),
            textfont=dict(color="#000000"), textposition="inside",
        ))
        fig_cost.add_trace(go.Bar(
            x=cost_data["Cluster_Label"], y=cost_data["OPEXRate"],
            name="OPEX Rate", marker_color="#42A5F5",
            text=cost_data["OPEXRate"].round(3),
            textfont=dict(color="#000000"), textposition="inside",
        ))
        fig_cost.update_layout(
            barmode="stack",
            title=dict(text="<b>EDA Chart 6 · Cost Pressure by Cluster (COGS + OPEX)</b>",
                       font=dict(size=14, color="#0A1F5C")),
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(color="#000000", size=13),
            xaxis=dict(color="#000000", title_font=dict(color="#000000")),
            yaxis=dict(color="#000000", showgrid=True, gridcolor="#E8F0FE", title_font=dict(color="#000000")),
            legend=dict(font=dict(color="#000000"), title_font=dict(color="#000000")),
            margin=dict(t=50, b=20),
        )
        fig_cost.update_xaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        fig_cost.update_yaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        st.plotly_chart(fig_cost, use_container_width=True)

    # ── EDA Chart 7 & 8: Top-10 by Orders + Orders by Subregion ──
    eda_r4c1, eda_r4c2 = st.columns(2)

    with eda_r4c1:
        top10 = df.groupby("RestaurantName")["MonthlyOrders"].mean().round(0).sort_values(ascending=False).head(10).reset_index()
        top10.columns = ["Restaurant", "Avg Monthly Orders"]
        fig_top = px.bar(
            top10.sort_values("Avg Monthly Orders"), x="Avg Monthly Orders", y="Restaurant",
            orientation="h",
            title="<b>EDA Chart 7 · Top 10 Restaurants by Monthly Orders</b>",
            color="Avg Monthly Orders",
            color_continuous_scale=["#BBDEFB","#1565C0","#0A1F5C"],
            text=top10.sort_values("Avg Monthly Orders")["Avg Monthly Orders"].astype(int),
        )
        fig_top.update_traces(textfont_color="#000000", textposition="outside")
        fig_top.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(color="#000000", size=12),
            xaxis=dict(color="#000000", showgrid=True, gridcolor="#E8F0FE", title_font=dict(color="#000000")),
            yaxis=dict(color="#000000", title_font=dict(color="#000000")),
            coloraxis_showscale=False,
            title_font=dict(size=14, color="#0A1F5C"),
            margin=dict(t=50, b=20, r=60),
            height=400,
        )
        fig_top.update_xaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        fig_top.update_yaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        st.plotly_chart(fig_top, use_container_width=True)

    with eda_r4c2:
        sub_ord = df.groupby("Subregion")["MonthlyOrders"].mean().reset_index().sort_values("MonthlyOrders")
        fig_sub = px.bar(
            sub_ord, x="MonthlyOrders", y="Subregion", orientation="h",
            title="<b>EDA Chart 8 · Avg Monthly Orders by Subregion</b>",
            color="MonthlyOrders",
            color_continuous_scale=["#E3F2FD","#1E88E5","#0A1F5C"],
            text=sub_ord["MonthlyOrders"].round(0).astype(int),
        )
        fig_sub.update_traces(textfont_color="#000000", textposition="outside")
        fig_sub.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(color="#000000", size=13),
            xaxis=dict(color="#000000", showgrid=True, gridcolor="#E8F0FE", title_font=dict(color="#000000")),
            yaxis=dict(color="#000000", title_font=dict(color="#000000")),
            coloraxis_showscale=False,
            title_font=dict(size=14, color="#0A1F5C"),
            margin=dict(t=50, b=20, r=60),
            height=400,
        )
        fig_sub.update_xaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        fig_sub.update_yaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        st.plotly_chart(fig_sub, use_container_width=True)

    # ── EDA Observations ──
    st.markdown("""<div class="section-header"><h2>💡 EDA Observations</h2>
    <p>Key insights extracted from the data-driven restaurant classification analysis</p></div>""",
    unsafe_allow_html=True)

    obs_col1, obs_col2 = st.columns(2)

    eda_obs_a = [
        ("1","Aggregator dominance is structurally high — Uber Eats contributes the largest share of total orders (~800K) and highest avg revenue (~$18K), confirming strong demand but also heavy platform dependency risk."),
        ("2","Revenue does not scale proportionally with orders across channels — Self-Delivery and DoorDash generate comparable revenue with significantly fewer orders, indicating better unit economics per order."),
        ("3","High-volume cuisines are not always high-growth cuisines — Pizza and Burgers lead in monthly orders, but only Pizza shows positive GPI, proving demand alone does not imply growth readiness."),
        ("4","Cuisine-level monetization differs sharply from demand — Burgers and Indian generate high average order volumes, yet their GPI is weak or negative, suggesting cost pressure or channel imbalance."),
    ]
    eda_obs_b = [
        ("5","Only a few cuisines are truly growth-ready — Pizza and Burgers are the only cuisines with positive GPI, signaling scalable expansion potential; Thai, Kebabs/Mediterranean, and Indian show negative GPI."),
        ("6","High-Growth restaurants handle only ~55% of orders via aggregators — the lowest dependency ratio — showing better channel control and self-delivery balance for expansion."),
        ("7","Cost pressure peaks in High-Growth restaurants (COGS+OPEX ≈ 88%), making cost efficiency the primary expansion risk despite high demand volumes — a classic growth trap pattern."),
        ("8","Average Order Value is flat ($38–$39) across all clusters, contributing less than 3% variation — AOV is not a meaningful lever for differentiating growth strategy across clusters."),
    ]
    with obs_col1:
        for num, text in eda_obs_a:
            st.markdown(f"""<div class="obs-card">
                <span class="obs-card-number">{num}</span>
                <span style="color:#1A2F5A; font-size:14px">{text}</span>
            </div>""", unsafe_allow_html=True)
    with obs_col2:
        for num, text in eda_obs_b:
            st.markdown(f"""<div class="obs-card">
                <span class="obs-card-number">{num}</span>
                <span style="color:#1A2F5A; font-size:14px">{text}</span>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  TAB 4 — RESTAURANT EXPLORER
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.markdown("""<div class="section-header"><h2>🍽️ Restaurant Explorer</h2>
    <p>Compare, drill-down and filter restaurants across all dimensions</p></div>""",
    unsafe_allow_html=True)

    # ── Top 10 GPI Scorecards ──
    st.markdown("#### 🏆 Top 10 Restaurants by Growth Potential Index (GPI)")
    top10_gpi = df.nlargest(10, "GPI")[
        ["RestaurantName","CuisineType","Segment","Subregion",
         "Cluster_Label","GPI","MonthlyOrders","AOV","TotalNetProfit"]
    ].reset_index(drop=True)
    top10_gpi.index += 1
    top10_gpi.columns = ["Restaurant","Cuisine","Segment","Subregion",
                          "Cluster","GPI Score","Monthly Orders","AOV ($)","Net Profit ($)"]
    top10_gpi["GPI Score"] = top10_gpi["GPI Score"].round(3)
    top10_gpi["AOV ($)"]   = top10_gpi["AOV ($)"].round(2)
    top10_gpi["Net Profit ($)"] = top10_gpi["Net Profit ($)"].round(0).astype(int)
    st.dataframe(top10_gpi, use_container_width=True, height=380)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── GPI Scatter: Orders vs Net Profit ──
    exp_col1, exp_col2 = st.columns(2)

    with exp_col1:
        # GPI has negative values — shift to positive range for marker size only
        df_scatter = df.copy()
        gpi_shift = df_scatter["GPI"].min()
        df_scatter["GPI_Size"] = (df_scatter["GPI"] - gpi_shift + 0.5).abs() + 0.1
        fig_scatter = px.scatter(
            df_scatter, x="MonthlyOrders", y="TotalNetProfit",
            color="Cluster_Label",
            color_discrete_map=CLUSTER_COLORS,
            hover_data=["RestaurantName","CuisineType","Subregion","GPI"],
            title="<b>Orders vs Net Profit · Colored by Cluster</b>",
            size="GPI_Size",
            size_max=16,
            opacity=0.75,
        )
        fig_scatter.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(color="#000000", size=13),
            xaxis=dict(
                color="#000000",
                title="Monthly Orders",
                tickfont=dict(color="#000000"),
                showgrid=True,
                gridcolor="#E8F0FE",
            ),
            yaxis=dict(
    color="#000000",
    title="Total Net Profit ($)",
    title_font=dict(color="#000000"),
    tickfont=dict(color="#000000"),
    showgrid=True,
    gridcolor="#E8F0FE",
),
legend=dict(
    font=dict(color="#000000"),
    title="Cluster",
    title_font=dict(color="#000000")
),
title_font=dict(size=15, color="#0A1F5C"),
margin=dict(t=50, b=20),
        )
        fig_scatter.update_xaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        fig_scatter.update_yaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with exp_col2:
        fig_scatter2 = px.scatter(
            df, x="AOV", y="GPI",
            color="CuisineType",
            hover_data=["RestaurantName","Cluster_Label","MonthlyOrders"],
            title="<b>AOV vs GPI Score · Colored by Cuisine</b>",
            color_discrete_sequence=BLUE_GRADIENT + ["#E53935","#F59E0B"],
            opacity=0.75,
        )
        fig_scatter2.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
font=dict(color="#000000", size=13),
xaxis=dict(
    color="#000000",
    title="Average Order Value ($)",
    title_font=dict(color="#000000"),
    tickfont=dict(color="#000000"),
    showgrid=True,
    gridcolor="#E8F0FE",
),
            yaxis=dict(
                color="#000000",
                title="GPI Score",
                tickfont=dict(color="#000000"),
                showgrid=True,
                gridcolor="#E8F0FE",
            ),
            legend=dict(font=dict(color="#000000"), title="Cuisine",
                        title_font=dict(color="#000000")),
            title_font=dict(size=15, color="#0A1F5C"),
            margin=dict(t=50, b=20),
        )
        fig_scatter2.update_xaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        fig_scatter2.update_yaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        st.plotly_chart(fig_scatter2, use_container_width=True)

    # ── Full Data Table ──
    st.markdown("""<div class="section-header"><h2>📋 Full Restaurant Data Table</h2>
    <p>Searchable and sortable — all restaurants matching your filter criteria</p></div>""",
    unsafe_allow_html=True)

    display_cols = ["RestaurantName","CuisineType","Segment","Subregion","Cluster_Label",
                    "GPI","GPI_Rank","MonthlyOrders","AOV","TotalNetProfit",
                    "DeliveryRadiusKM","COGSRate","OPEXRate"]
    show_df = df[display_cols].copy()
    show_df["GPI"] = show_df["GPI"].round(3)
    show_df["TotalNetProfit"] = show_df["TotalNetProfit"].round(0).astype(int)
    show_df["COGSRate"] = (show_df["COGSRate"]*100).round(1)
    show_df["OPEXRate"] = (show_df["OPEXRate"]*100).round(1)
    show_df.columns = ["Restaurant","Cuisine","Segment","Subregion","Cluster",
                       "GPI","Rank","Orders/Month","AOV($)","Net Profit($)",
                       "Del. Radius(km)","COGS%","OPEX%"]
    st.dataframe(show_df.reset_index(drop=True), use_container_width=True, height=420)

    st.caption(f"📊 Showing **{len(show_df):,}** restaurants")


# ═══════════════════════════════════════════════════════════════
#  TAB 5 — STRATEGY & RECOMMENDATIONS
# ═══════════════════════════════════════════════════════════════
with tab5:
    st.markdown("""<div class="section-header"><h2>🎯 Strategic Recommendations & Action Plan</h2>
    <p>Data-driven strategic guidance for SkyCity Auckland Restaurants & Bars — derived from EDA, clustering, and GPI modeling</p></div>""",
    unsafe_allow_html=True)

    # ── Cluster Summary Badges ──
    b1, b2, b3 = st.columns(3)
    with b1:
        hg_count = len(df[df["Cluster_Label"]=="High-Growth"])
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#FFEBEE,#FFCDD2); border:2px solid #EF9A9A;
             border-radius:16px; padding:20px; text-align:center; box-shadow:0 4px 12px rgba(229,57,53,0.15)">
            <div style="font-size:2.5rem">🔴</div>
            <h3 style="color:#B71C1C; margin:8px 0 4px">High-Growth</h3>
            <div style="font-size:1.8rem; font-weight:900; color:#C62828">{hg_count:,}</div>
            <div style="color:#B71C1C; font-size:12px">Restaurants · 19.0% Share</div>
        </div>""", unsafe_allow_html=True)
    with b2:
        sp_count = len(df[df["Cluster_Label"]=="Stable Performers"])
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#E8F5E9,#C8E6C9); border:2px solid #A5D6A7;
             border-radius:16px; padding:20px; text-align:center; box-shadow:0 4px 12px rgba(27,138,58,0.15)">
            <div style="font-size:2.5rem">🟢</div>
            <h3 style="color:#1B5E20; margin:8px 0 4px">Stable Performers</h3>
            <div style="font-size:1.8rem; font-weight:900; color:#2E7D32">{sp_count:,}</div>
            <div style="color:#1B5E20; font-size:12px">Restaurants · 44.4% Share</div>
        </div>""", unsafe_allow_html=True)
    with b3:
        dl_count = len(df[df["Cluster_Label"]=="Dependent Low Margin"])
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#FFF8E1,#FFECB3); border:2px solid #FFE082;
             border-radius:16px; padding:20px; text-align:center; box-shadow:0 4px 12px rgba(245,158,11,0.15)">
            <div style="font-size:2.5rem">🟡</div>
            <h3 style="color:#7C4F00; margin:8px 0 4px">Dependent Low Margin</h3>
            <div style="font-size:1.8rem; font-weight:900; color:#B45309">{dl_count:,}</div>
            <div style="color:#7C4F00; font-size:12px">Restaurants · 36.6% Share</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 10 Recommendations ──
    st.markdown("""<div class="section-header"><h2>📌 10 Strategic Recommendations</h2>
    <p>Actionable, evidence-based recommendations for stakeholders and decision-makers</p></div>""",
    unsafe_allow_html=True)

    recs = [
        {
            "num": "01",
            "type": "high",
            "badge": "🔴 High-Growth Cluster",
            "title": "Implement Urgent Cost Control Programs for High-Growth Restaurants",
            "body": (
                "High-Growth restaurants average a combined COGS+OPEX rate of ~88%, which is critically high and "
                "directly explains their negative avg GPI (−0.08) despite leading in monthly orders (~1,531). "
                "<b>Action:</b> Introduce cluster-specific cost-efficiency audits, renegotiate supplier contracts, "
                "and set hard cost ceilings at 75% combined rate. Without this intervention, expansion will accelerate "
                "losses rather than profits."
            ),
        },
        {
            "num": "02",
            "type": "dep",
            "badge": "🟡 Dependent Low Margin",
            "title": "Reduce Aggregator Dependency — Build Self-Delivery Infrastructure",
            "body": (
                "The Dependent Low-Margin cluster contributes the highest avg GPI (+0.31) in the portfolio, yet "
                "70%+ of their orders flow through Uber Eats and DoorDash, exposing them to commission erosion "
                "(avg 28–33% per order). <b>Action:</b> Pilot in-house delivery fleets in high-density subregions "
                "(South Auckland first — highest GPI region). Even a 10% shift from aggregator to self-delivery "
                "can improve margin by 3–5 percentage points per restaurant."
            ),
        },
        {
            "num": "03",
            "type": "stable",
            "badge": "🟢 Stable Performers",
            "title": "Scale Top-Performing Stable Restaurants via Incremental Expansion",
            "body": (
                "Stable Performers (44.4% of portfolio) show consistent, predictable revenue but only moderate "
                "monthly order volumes (~804 avg). Their controlled cost structures make them ideal for safe, "
                "incremental expansion. <b>Action:</b> Identify the top quartile of Stable Performers by GPI and "
                "revenue quality, then invest in delivery radius expansion (+5 km) and targeted digital marketing "
                "to unlock demand without operational overhaul."
            ),
        },
        {
            "num": "04",
            "type": "general",
            "badge": "🌏 Geographic Strategy",
            "title": "Prioritize South Auckland for New Outlet Investments",
            "body": (
                "South Auckland leads all subregions with the highest avg GPI (+0.34) and strong order volumes, "
                "indicating a favourable demand-cost equilibrium. CBD, despite comparable volumes, has the lowest "
                "GPI (−0.58), driven by extreme cost pressure. <b>Action:</b> New outlet openings, ghost kitchen "
                "launches, and channel investment should prioritize South Auckland and West Auckland, while CBD "
                "strategy should focus on margin repair before any expansion."
            ),
        },
        {
            "num": "05",
            "type": "general",
            "badge": "🍕 Cuisine Strategy",
            "title": "Accelerate Pizza & Burger Expansion — Restructure Indian & Thai",
            "body": (
                "Pizza and Burgers are the only cuisine types with positive GPI, confirming both high demand and "
                "viable cost structures. Indian and Thai cuisine show high order volumes but negative or near-zero "
                "GPI — a clear sign of cost-channel mismatch. <b>Action:</b> Approve multi-outlet expansion budgets "
                "for Pizza and Burger brands. For Indian and Thai, conduct a channel mix reset — reduce aggregator "
                "share below 60% and evaluate COGS through menu re-engineering before any new investment."
            ),
        },
        {
            "num": "06",
            "type": "general",
            "badge": "👻 Ghost Kitchen Model",
            "title": "Invest in Ghost Kitchen Model for Low-Cost High-GPI Scaling",
            "body": (
                "Ghost Kitchens represent only 11.6% of the portfolio but deliver the highest avg GPI (+0.12) "
                "among all segment types, outperforming QSR, Cafe, and Full-Service formats. Their low overhead "
                "and delivery-first model aligns perfectly with aggregator-heavy demand patterns. "
                "<b>Action:</b> Increase Ghost Kitchen allocation to 20–25% of portfolio by converting "
                "underperforming Full-Service locations in high-cost subregions (CBD) into ghost format operations."
            ),
        },
        {
            "num": "07",
            "type": "high",
            "badge": "🔴 High-Growth Cluster",
            "title": "Optimize Channel Mix for High-Growth Restaurants Before Further Scaling",
            "body": (
                "High-Growth restaurants have the lowest aggregator dependency (~55%) — a positive structural "
                "signal — but their self-delivery cost per order is disproportionately high due to wide delivery "
                "radii. <b>Action:</b> Cap delivery radius at 12 km for High-Growth outlets, renegotiate "
                "self-delivery logistics contracts, and implement dynamic delivery pricing. This alone is projected "
                "to reduce SD_DeliveryTotalCost by 15–20%, directly improving net GPI."
            ),
        },
        {
            "num": "08",
            "type": "stable",
            "badge": "🟢 Stable Performers",
            "title": "Leverage Revenue Quality — Introduce Premium AOV Products for Stable Performers",
            "body": (
                "AOV is essentially flat across all clusters ($38–$39), representing a missed revenue lever. "
                "Stable Performers have the cost discipline and operational consistency to absorb premium SKU "
                "introductions without disruption. <b>Action:</b> Launch combo upgrades, premium meal bundles, "
                "and upsell prompts on digital ordering for Stable Performer restaurants. A 10% AOV increase "
                "across this cluster equates to an estimated +$2.8M incremental revenue annually."
            ),
        },
        {
            "num": "09",
            "type": "dep",
            "badge": "🟡 Dependent Low Margin",
            "title": "Commission Rate Negotiation Strategy for Aggregator-Heavy Restaurants",
            "body": (
                "The avg commission rate across the Dependent Low-Margin cluster is 28–33%, which directly "
                "suppresses UberEats and DoorDash net profits. Several restaurants in this cluster show "
                "negative UberEats/DoorDash net profit despite meaningful order volumes. "
                "<b>Action:</b> Consolidate volume-based negotiation with Uber Eats and DoorDash at the "
                "portfolio level to achieve a target commission rate of ≤25%. For restaurants below the "
                "break-even commission threshold, consider exclusive self-delivery conversion."
            ),
        },
        {
            "num": "10",
            "type": "general",
            "badge": "📊 Portfolio-Wide",
            "title": "Implement Real-Time GPI Monitoring Dashboard for Ongoing Decision Support",
            "body": (
                "The Growth Potential Index (GPI) — weighted across GrowthFactor (30%), MonthlyOrders (25%), "
                "AOV (15%), cost factors (−25%), and delivery reach (5%) — is the single most actionable score "
                "for investment decisions. Currently, GPI analysis requires manual computation. "
                "<b>Action:</b> Embed this Streamlit dashboard into the operational workflow with monthly "
                "data refresh cycles. Set GPI threshold alerts: restaurants falling below −0.3 trigger "
                "a strategic review; those above +0.5 qualify for fast-track expansion funding."
            ),
        },
    ]

    rec_type_class = {"high": "rec-high", "stable": "rec-stable", "dep": "rec-dep", "general": "rec-general"}
    title_class    = {"high": "high-title","stable":"stable-title","dep":"dep-title","general":"gen-title"}

    for rec in recs:
        css_class   = rec_type_class[rec["type"]]
        title_css   = title_class[rec["type"]]
        badge_class = ("badge-high" if rec["type"]=="high"
                       else "badge-stable" if rec["type"]=="stable"
                       else "badge-dep" if rec["type"]=="dep"
                       else "badge-dep")
        st.markdown(f"""
        <div class="rec-card {css_class}">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px">
                <div style="background:#0A1F5C; color:white; font-size:13px; font-weight:800;
                            border-radius:8px; padding:4px 10px; min-width:36px; text-align:center">
                    #{rec['num']}
                </div>
                <span class="{badge_class}">{rec['badge']}</span>
            </div>
            <h4 class="{title_css}">{rec['title']}</h4>
            <p>{rec['body']}</p>
        </div>
        """, unsafe_allow_html=True)

    # ── GPI Avg by Cluster Chart ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div class="section-header"><h2>📊 Strategic Cluster GPI Summary</h2></div>""",
    unsafe_allow_html=True)

    strat_col1, strat_col2 = st.columns(2)

    with strat_col1:
        gpi_cluster = df.groupby("Cluster_Label")["GPI"].mean().reset_index()
        gpi_cluster.columns = ["Cluster","Avg GPI"]
        fig_gpi_bar = px.bar(
            gpi_cluster, x="Cluster", y="Avg GPI",
            color="Cluster",
            color_discrete_map=CLUSTER_COLORS,
            title="<b>Avg GPI by Strategic Cluster</b>",
            text=gpi_cluster["Avg GPI"].round(3),
        )
        fig_gpi_bar.add_hline(y=0, line_dash="dash", line_color="#0A1F5C", line_width=1.5)
        fig_gpi_bar.update_traces(textfont_color="#000000", textposition="outside")
        fig_gpi_bar.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(color="#000000", size=13),
            xaxis=dict(color="#000000", title_font=dict(color="#000000")),
            yaxis=dict(color="#000000", showgrid=True, gridcolor="#E8F0FE", title_font=dict(color="#000000")),
            showlegend=False,
            title_font=dict(size=15, color="#0A1F5C"),
            margin=dict(t=50, b=20),
        )
        fig_gpi_bar.update_xaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        fig_gpi_bar.update_yaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        st.plotly_chart(fig_gpi_bar, use_container_width=True)

    with strat_col2:
        channel_profit = pd.DataFrame({
            "Channel": ["In-Store","Uber Eats","DoorDash","Self-Delivery"],
            "Avg Net Profit ($)": [
                df["InStoreNetProfit"].mean(),
                df["UberEatsNetProfit"].mean(),
                df["DoorDashNetProfit"].mean(),
                df["SelfDeliveryNetProfit"].mean(),
            ]
        })
        fig_cp = px.bar(
            channel_profit, x="Channel", y="Avg Net Profit ($)",
            color="Avg Net Profit ($)",
            color_continuous_scale=["#E53935","#FFFFFF","#0A1F5C"],
            title="<b>Avg Net Profit by Channel</b>",
            text=channel_profit["Avg Net Profit ($)"].round(0).astype(int),
        )
        fig_cp.update_traces(textfont_color="#000000", textposition="outside")
        fig_cp.add_hline(y=0, line_dash="dash", line_color="#E53935", line_width=1.5)
        fig_cp.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(color="#000000", size=13),
            xaxis=dict(color="#000000", title_font=dict(color="#000000")),
            yaxis=dict(color="#000000", showgrid=True, gridcolor="#E8F0FE", title_font=dict(color="#000000")),
            coloraxis_showscale=False,
            title_font=dict(size=15, color="#0A1F5C"),
            margin=dict(t=50, b=20),
        )
        fig_cp.update_xaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        fig_cp.update_yaxes(
            title_font=dict(color="#000000", size=13),
            tickfont=dict(color="#000000", size=12),
            linecolor="#000000", ticks="outside",
        )
        st.plotly_chart(fig_cp, use_container_width=True)


# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="dashboard-footer">
    🍽️ <b>Restaurant Growth Potential Modeling & Strategic Classification System</b><br>
    SkyCity Auckland Restaurants & Bars · 1,696 Restaurants · 4 Subregions · 8 Cuisine Types · 3 Strategic Clusters<br>
    Built with Streamlit · Plotly · Scikit-Learn · Pandas
</div>
""", unsafe_allow_html=True)