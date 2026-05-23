"""
Term Agent Inc — Analytics Dashboard (Redesigned)
===================================================
Run with:
    pip install streamlit anthropic pandas openpyxl plotly
    streamlit run agent_analytics_app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import anthropic
import json

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AgentIQ · Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Design System & CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

/* ════════════════════════════════════════════
   ANIMATION KEYFRAMES
   ════════════════════════════════════════════ */

/* Fade + lift — main page entry */
@keyframes fadeUp {
    0%   { opacity: 0; transform: translateY(22px); }
    100% { opacity: 1; transform: translateY(0); }
}

/* Fade + slide from left — sidebar items */
@keyframes fadeLeft {
    0%   { opacity: 0; transform: translateX(-16px); }
    100% { opacity: 1; transform: translateX(0); }
}

/* Gentle fade — overlays, charts */
@keyframes fadeIn {
    0%   { opacity: 0; }
    100% { opacity: 1; }
}

/* Scale pop — KPI cards */
@keyframes scalePop {
    0%   { opacity: 0; transform: scale(0.92) translateY(12px); }
    60%  { transform: scale(1.02) translateY(-2px); }
    100% { opacity: 1; transform: scale(1) translateY(0); }
}

/* Shimmer sweep — loading bar accent */
@keyframes shimmer {
    0%   { background-position: -600px 0; }
    100% { background-position: 600px 0; }
}

/* Pulse glow — active nav item */
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 0 0 rgba(59,130,246,0); }
    50%       { box-shadow: 0 0 12px 2px rgba(59,130,246,0.25); }
}

/* Counter tick — numeric values */
@keyframes countUp {
    0%   { opacity: 0; transform: translateY(8px); }
    100% { opacity: 1; transform: translateY(0); }
}

/* Slide in from top — page title */
@keyframes slideDown {
    0%   { opacity: 0; transform: translateY(-18px); }
    100% { opacity: 1; transform: translateY(0); }
}

/* Horizontal bar grow — progress indicators */
@keyframes growRight {
    0%   { width: 0 !important; }
    100% { width: var(--target-width) !important; }
}

/* Border trace — section dividers */
@keyframes traceRight {
    0%   { width: 0; opacity: 0; }
    100% { width: 100%; opacity: 1; }
}

/* Float — decorative accents */
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-6px); }
}

/* ════════════════════════════════════════════
   PAGE TRANSITION WRAPPER
   ════════════════════════════════════════════ */

/* Every top-level block animates in on render */
.main .block-container > div > div {
    animation: fadeUp 0.45s cubic-bezier(0.16, 1, 0.3, 1) both;
}

/* Stagger children of the main container */
.main .block-container > div > div:nth-child(1)  { animation-delay: 0.00s; }
.main .block-container > div > div:nth-child(2)  { animation-delay: 0.04s; }
.main .block-container > div > div:nth-child(3)  { animation-delay: 0.08s; }
.main .block-container > div > div:nth-child(4)  { animation-delay: 0.12s; }
.main .block-container > div > div:nth-child(5)  { animation-delay: 0.16s; }
.main .block-container > div > div:nth-child(6)  { animation-delay: 0.20s; }
.main .block-container > div > div:nth-child(7)  { animation-delay: 0.24s; }
.main .block-container > div > div:nth-child(8)  { animation-delay: 0.28s; }
.main .block-container > div > div:nth-child(9)  { animation-delay: 0.32s; }
.main .block-container > div > div:nth-child(10) { animation-delay: 0.36s; }
.main .block-container > div > div:nth-child(11) { animation-delay: 0.40s; }
.main .block-container > div > div:nth-child(12) { animation-delay: 0.44s; }

/* ════════════════════════════════════════════
   METRIC CARDS — staggered scale pop
   ════════════════════════════════════════════ */
[data-testid="metric-container"] {
    animation: scalePop 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}
/* Each column staggered */
[data-testid="column"]:nth-child(1) [data-testid="metric-container"] { animation-delay: 0.05s; }
[data-testid="column"]:nth-child(2) [data-testid="metric-container"] { animation-delay: 0.12s; }
[data-testid="column"]:nth-child(3) [data-testid="metric-container"] { animation-delay: 0.19s; }
[data-testid="column"]:nth-child(4) [data-testid="metric-container"] { animation-delay: 0.26s; }

/* Hover lift on metric cards */
[data-testid="metric-container"]:hover {
    transform: translateY(-3px) scale(1.01) !important;
    border-color: #2a3f5f !important;
    box-shadow: 0 12px 40px rgba(0,0,0,0.4), 0 0 0 1px rgba(59,130,246,0.12) !important;
    transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease !important;
}

/* ════════════════════════════════════════════
   PLOTLY CHARTS — fade in
   ════════════════════════════════════════════ */
[data-testid="stPlotlyChart"] {
    animation: fadeIn 0.6s ease both;
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid #1e2d45;
}
[data-testid="column"]:nth-child(1) [data-testid="stPlotlyChart"] { animation-delay: 0.10s; }
[data-testid="column"]:nth-child(2) [data-testid="stPlotlyChart"] { animation-delay: 0.22s; }
[data-testid="column"]:nth-child(3) [data-testid="stPlotlyChart"] { animation-delay: 0.34s; }

/* ════════════════════════════════════════════
   DATAFRAME — slide up
   ════════════════════════════════════════════ */
[data-testid="stDataFrame"] {
    animation: fadeUp 0.55s cubic-bezier(0.16, 1, 0.3, 1) 0.2s both;
}

/* ════════════════════════════════════════════
   SIDEBAR NAV ITEMS — fade from left
   ════════════════════════════════════════════ */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:nth-child(1) { animation: fadeLeft 0.3s ease 0.05s both; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:nth-child(2) { animation: fadeLeft 0.3s ease 0.10s both; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:nth-child(3) { animation: fadeLeft 0.3s ease 0.15s both; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:nth-child(4) { animation: fadeLeft 0.3s ease 0.20s both; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:nth-child(5) { animation: fadeLeft 0.3s ease 0.25s both; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:nth-child(6) { animation: fadeLeft 0.3s ease 0.30s both; }

/* ════════════════════════════════════════════
   PAGE TITLE — slide from top
   ════════════════════════════════════════════ */
.page-title {
    animation: slideDown 0.4s cubic-bezier(0.16, 1, 0.3, 1) both;
}
.page-subtitle {
    animation: fadeIn 0.5s ease 0.1s both;
}
.section-label {
    animation: fadeIn 0.4s ease 0.15s both;
}

/* ════════════════════════════════════════════
   PODIUM CARDS — staggered scale pop
   ════════════════════════════════════════════ */
[data-testid="column"]:nth-child(1) .podium-card,
[data-testid="column"]:nth-child(1) > div > div { animation-delay: 0.05s; }
[data-testid="column"]:nth-child(2) .podium-card,
[data-testid="column"]:nth-child(2) > div > div { animation-delay: 0.15s; }
[data-testid="column"]:nth-child(3) .podium-card,
[data-testid="column"]:nth-child(3) > div > div { animation-delay: 0.25s; }

/* ════════════════════════════════════════════
   BUTTONS — fade in staggered
   ════════════════════════════════════════════ */
.stButton {
    animation: fadeUp 0.35s ease both;
}
.stButton:nth-child(1) { animation-delay: 0.05s; }
.stButton:nth-child(2) { animation-delay: 0.10s; }
.stButton:nth-child(3) { animation-delay: 0.15s; }

/* ════════════════════════════════════════════
   CHAT MESSAGES — slide up per message
   ════════════════════════════════════════════ */
[data-testid="stChatMessage"] {
    animation: fadeUp 0.35s cubic-bezier(0.16, 1, 0.3, 1) both;
}

/* ════════════════════════════════════════════
   SHIMMER LOADING BAR at top of page
   ════════════════════════════════════════════ */
.main::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg,
        transparent 0%,
        #3b82f6 20%,
        #06b6d4 50%,
        #8b5cf6 80%,
        transparent 100%
    );
    background-size: 600px 2px;
    animation: shimmer 1.2s ease-out 1;
    z-index: 9999;
    pointer-events: none;
}

/* ════════════════════════════════════════════
   SECTION LABEL line trace animation
   ════════════════════════════════════════════ */
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
    animation: traceRight 0.6s ease 0.3s both;
    transform-origin: left;
}


/* ── Root variables — Premium Light Theme ── */
:root {
    --bg-base:        #f0f4fa;
    --bg-page:        #eef2f9;
    --bg-card:        #ffffff;
    --bg-card2:       #f8fafd;
    --bg-card-hover:  #f1f6ff;
    --bg-sidebar:     #1a2340;
    --bg-sidebar2:    #141c33;
    --border:         #dde3ef;
    --border-bright:  #c3cedf;
    --border-hover:   #93a8d0;
    --text-primary:   #0f1c2e;
    --text-secondary: #4a5e7a;
    --text-muted:     #8fa0b8;
    --accent-blue:    #2563eb;
    --accent-blue-lt: #dbeafe;
    --accent-cyan:    #0891b2;
    --accent-cyan-lt: #cffafe;
    --accent-green:   #059669;
    --accent-green-lt:#d1fae5;
    --accent-amber:   #d97706;
    --accent-amber-lt:#fef3c7;
    --accent-rose:    #e11d48;
    --accent-rose-lt: #ffe4e6;
    --accent-violet:  #7c3aed;
    --accent-violet-lt:#ede9fe;
    --shadow-sm:      0 1px 4px rgba(15,28,46,0.07), 0 0 0 1px rgba(15,28,46,0.04);
    --shadow-md:      0 4px 16px rgba(15,28,46,0.10), 0 1px 4px rgba(15,28,46,0.06);
    --shadow-hover:   0 12px 36px rgba(37,99,235,0.14), 0 2px 8px rgba(15,28,46,0.08);
    --shadow-chart:   0 6px 24px rgba(15,28,46,0.09), 0 1px 4px rgba(15,28,46,0.05);
}

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg-page) !important;
    color: var(--text-primary) !important;
}

.main {
    background: linear-gradient(160deg, #eef2f9 0%, #e8eef8 40%, #edf1f8 100%) !important;
    min-height: 100vh;
}
.block-container { padding: 1.5rem 2rem 2rem !important; }

/* ── Sidebar — deep navy, executive feel ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a2340 0%, #141c33 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.18) !important;
}
[data-testid="stSidebar"] > div { padding-top: 0 !important; }
[data-testid="stSidebar"] * { color: #a8b8d8 !important; }
[data-testid="stSidebar"] .stRadio > label { display: none; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap: 2px; display: flex; flex-direction: column; }
[data-testid="stSidebar"] .stRadio label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #7a90b8 !important;
    padding: 9px 14px !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
    border: 1px solid transparent !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.07) !important;
    color: #e2eaf8 !important;
    border-color: rgba(255,255,255,0.08) !important;
}
[data-testid="stSidebar"] .stRadio [aria-checked="true"] ~ div,
[data-testid="stSidebar"] .stRadio [data-checked="true"] ~ div {
    color: #fff !important;
}

/* ── Metric cards — premium white glass cards ── */
[data-testid="metric-container"] {
    background: linear-gradient(145deg, #ffffff 0%, #f8fbff 100%) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 22px 24px !important;
    position: relative !important;
    overflow: hidden !important;
    box-shadow: var(--shadow-sm) !important;
    transition:
        transform 0.32s cubic-bezier(0.34, 1.56, 0.64, 1),
        box-shadow 0.32s ease,
        border-color 0.25s ease,
        background 0.25s ease !important;
    cursor: default;
}

/* Coloured top-edge accent stripe per card position */
[data-testid="column"]:nth-child(1) [data-testid="metric-container"] { border-top: 3px solid #2563eb !important; }
[data-testid="column"]:nth-child(2) [data-testid="metric-container"] { border-top: 3px solid #059669 !important; }
[data-testid="column"]:nth-child(3) [data-testid="metric-container"] { border-top: 3px solid #d97706 !important; }
[data-testid="column"]:nth-child(4) [data-testid="metric-container"] { border-top: 3px solid #7c3aed !important; }

/* Subtle corner glow blob */
[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: -20px; right: -20px;
    width: 90px; height: 90px;
    border-radius: 50%;
    opacity: 0.06;
    transition: opacity 0.3s ease, transform 0.35s ease;
    pointer-events: none;
}
[data-testid="column"]:nth-child(1) [data-testid="metric-container"]::before { background: #2563eb; }
[data-testid="column"]:nth-child(2) [data-testid="metric-container"]::before { background: #059669; }
[data-testid="column"]:nth-child(3) [data-testid="metric-container"]::before { background: #d97706; }
[data-testid="column"]:nth-child(4) [data-testid="metric-container"]::before { background: #7c3aed; }

/* ✨ HOVER STATE — lift + glow + blob expand ✨ */
[data-testid="metric-container"]:hover {
    transform: translateY(-5px) scale(1.025) !important;
    box-shadow: var(--shadow-hover) !important;
    border-color: var(--border-hover) !important;
    background: linear-gradient(145deg, #ffffff 0%, #eef5ff 100%) !important;
}
[data-testid="metric-container"]:hover::before {
    opacity: 0.13 !important;
    transform: scale(1.4) !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.85rem !important;
    font-weight: 800 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.03em !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    color: var(--text-secondary) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}
[data-testid="stMetricDelta"] {
    font-size: 0.75rem !important;
    font-weight: 600 !important;
}

/* ── Plotly charts — white card with lift-on-hover ── */
[data-testid="stPlotlyChart"] {
    animation: fadeIn 0.6s ease both;
    border-radius: 16px !important;
    overflow: hidden !important;
    border: 1px solid var(--border) !important;
    background: #ffffff !important;
    box-shadow: var(--shadow-chart) !important;
    transition:
        transform 0.30s cubic-bezier(0.34, 1.56, 0.64, 1),
        box-shadow 0.30s ease,
        border-color 0.25s ease !important;
}
[data-testid="stPlotlyChart"]:hover {
    transform: translateY(-4px) scale(1.008) !important;
    box-shadow: 0 18px 48px rgba(37,99,235,0.13), 0 4px 12px rgba(15,28,46,0.08) !important;
    border-color: #93a8d0 !important;
}

/* ── Dataframe — clean white card ── */
[data-testid="stDataFrame"] {
    animation: fadeUp 0.55s cubic-bezier(0.16, 1, 0.3, 1) 0.2s both;
    border-radius: 16px !important;
    overflow: hidden !important;
    border: 1px solid var(--border) !important;
    background: #ffffff !important;
    box-shadow: var(--shadow-sm) !important;
    transition: box-shadow 0.25s ease, transform 0.25s ease !important;
}
[data-testid="stDataFrame"]:hover {
    box-shadow: var(--shadow-md) !important;
    transform: translateY(-2px) !important;
}
[data-testid="stDataFrame"] iframe { background: #ffffff !important; }

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    margin-bottom: 10px !important;
    box-shadow: var(--shadow-sm) !important;
}

/* ── Inputs ── */
.stTextInput input, .stChatInput textarea {
    background: #ffffff !important;
    border: 1.5px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    box-shadow: var(--shadow-sm) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
.stTextInput input:focus, .stChatInput textarea:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #f8fafd !important;
    border: 1.5px dashed var(--border-bright) !important;
    border-radius: 12px !important;
    padding: 12px !important;
    transition: border-color 0.2s ease, background 0.2s ease !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent-blue) !important;
    background: #eff6ff !important;
}

/* ── Buttons ── */
.stButton button {
    background: #ffffff !important;
    border: 1.5px solid var(--border) !important;
    color: var(--text-secondary) !important;
    border-radius: 9px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 12.5px !important;
    box-shadow: var(--shadow-sm) !important;
    transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
}
.stButton button:hover {
    border-color: var(--accent-blue) !important;
    color: var(--accent-blue) !important;
    background: #eff6ff !important;
    transform: translateY(-2px) scale(1.03) !important;
    box-shadow: 0 6px 18px rgba(37,99,235,0.15) !important;
}

/* ── Dividers ── */
hr { border-color: var(--border) !important; margin: 16px 0 !important; }

/* ── Success/info alerts ── */
.stSuccess {
    background: linear-gradient(135deg, #f0fdf4, #ecfdf5) !important;
    border: 1px solid #6ee7b7 !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}
.stInfo {
    background: linear-gradient(135deg, #eff6ff, #dbeafe) !important;
    border: 1px solid #93c5fd !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

/* ── Hide branding ── */
#MainMenu { visibility: hidden; }
footer { visibility: visible; }
header { visibility: visible; }

/* ── Page header banner ── */
.page-header-wrap {
    margin: -8px -8px 28px -8px;
    padding: 26px 28px 22px;
    border-radius: 18px;
    position: relative;
    overflow: hidden;
    animation: headerSlideIn 0.45s cubic-bezier(0.16,1,0.3,1) both;
}
@keyframes headerSlideIn {
    0%   { opacity:0; transform:translateY(-14px) scale(0.98); }
    100% { opacity:1; transform:translateY(0)     scale(1); }
}

/* Noise texture overlay */
.page-header-wrap::before {
    content:'';
    position:absolute; inset:0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
    background-size: 160px;
    pointer-events:none; border-radius:inherit;
}
/* Sheen sweep on load */
.page-header-wrap::after {
    content:'';
    position:absolute; top:0; left:-60%;
    width:40%; height:100%;
    background:linear-gradient(105deg,transparent 20%,rgba(255,255,255,0.18) 50%,transparent 80%);
    animation: headerSheen 1.1s ease 0.3s both;
    pointer-events:none;
}
@keyframes headerSheen {
    0%   { left:-60%; }
    100% { left:130%; }
}

.page-header-inner {
    position:relative; z-index:1;
    display:flex; align-items:center; justify-content:space-between; gap:16px;
}
.page-header-left { flex:1; }

.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 26px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.025em;
    margin: 0 0 5px;
    line-height: 1.15;
    text-shadow: 0 1px 3px rgba(0,0,0,0.15);
}
.page-subtitle {
    font-size: 13px;
    color: rgba(255,255,255,0.72);
    font-weight: 400;
    margin: 0;
    line-height: 1.5;
}
.page-header-badge {
    display:flex; align-items:center; gap:6px;
    background:rgba(255,255,255,0.15);
    border:1px solid rgba(255,255,255,0.22);
    border-radius:99px;
    padding:7px 14px;
    font-size:11.5px; font-weight:600;
    color:rgba(255,255,255,0.9);
    white-space:nowrap;
    backdrop-filter:blur(4px);
    flex-shrink:0;
}
.page-header-icon {
    font-size:36px; line-height:1;
    filter: drop-shadow(0 2px 6px rgba(0,0,0,0.18));
    flex-shrink:0;
}
.section-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 10.5px;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin: 28px 0 14px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.kpi-accent {
    position: absolute;
    top: 0; right: 0;
    width: 80px; height: 80px;
    border-radius: 50%;
    opacity: 0.06;
    transform: translate(20px, -20px);
}
.stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 11px 0;
    border-bottom: 1px solid var(--border);
    font-size: 13px;
}
.stat-row:last-child { border-bottom: none; }
.stat-label { color: var(--text-secondary); }
.stat-value { font-family: 'JetBrains Mono', monospace; font-size: 12.5px; color: var(--text-primary); font-weight: 600; }
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    font-family: 'DM Sans', sans-serif;
}
.podium-card {
    border-radius: 16px;
    padding: 20px 18px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.3s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.3s ease !important;
}
.podium-card:hover {
    transform: translateY(-5px) scale(1.02) !important;
    box-shadow: 0 16px 40px rgba(15,28,46,0.14) !important;
}
.nav-section-label {
    font-size: 9.5px;
    font-weight: 700;
    color: rgba(255,255,255,0.25);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    padding: 16px 14px 6px;
}
</style>
""", unsafe_allow_html=True)

# ── JavaScript Animation Engine ────────────────────────────────────────────────
# Runs on every Streamlit re-render; uses MutationObserver to detect page switches
# and re-applies animation classes to all animatable elements.
st.markdown("""
<script>
(function() {

  /* ── Easing helpers ── */
  function easeOutExpo(t) { return t === 1 ? 1 : 1 - Math.pow(2, -10 * t); }
  function easeOutBack(t) {
    const c1 = 1.70158, c3 = c1 + 1;
    return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
  }

  /* ── Counter animation for metric values ── */
  function animateCounter(el) {
    const raw = el.innerText.replace(/[^0-9.]/g, '');
    const target = parseFloat(raw);
    if (!target || isNaN(target)) return;
    const prefix = el.innerText.replace(/[0-9.,]+.*/, '');
    const suffix = el.innerText.replace(/^[^0-9]*[0-9.,]+/, '');
    const duration = 900;
    const start = performance.now();
    function tick(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = easeOutExpo(progress);
      const current = target * eased;
      const formatted = target < 10
        ? current.toFixed(2)
        : Math.round(current).toLocaleString('en-IN');
      el.innerText = prefix + formatted + suffix;
      if (progress < 1) requestAnimationFrame(tick);
      else el.innerText = prefix + target.toLocaleString('en-IN') + suffix;
    }
    requestAnimationFrame(tick);
  }

  /* ── Staggered fade-up for a NodeList ── */
  function staggerFadeUp(els, baseDelay=0, step=60) {
    Array.from(els).forEach((el, i) => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(20px)';
      el.style.transition = 'none';
      setTimeout(() => {
        el.style.transition = `opacity 0.45s cubic-bezier(0.16,1,0.3,1),
                                transform 0.45s cubic-bezier(0.16,1,0.3,1)`;
        el.style.opacity = '1';
        el.style.transform = 'translateY(0)';
      }, baseDelay + i * step);
    });
  }

  /* ── Scale pop for metric cards ── */
  function scalePopCards(els, baseDelay=0, step=70) {
    Array.from(els).forEach((el, i) => {
      el.style.opacity = '0';
      el.style.transform = 'scale(0.9) translateY(14px)';
      el.style.transition = 'none';
      setTimeout(() => {
        el.style.transition = `opacity 0.5s cubic-bezier(0.34,1.56,0.64,1),
                                transform 0.5s cubic-bezier(0.34,1.56,0.64,1)`;
        el.style.opacity = '1';
        el.style.transform = 'scale(1) translateY(0)';
      }, baseDelay + i * step);
    });
  }

  /* ── Slide-in from left for sidebar ── */
  function slideFromLeft(els, baseDelay=0, step=50) {
    Array.from(els).forEach((el, i) => {
      el.style.opacity = '0';
      el.style.transform = 'translateX(-18px)';
      el.style.transition = 'none';
      setTimeout(() => {
        el.style.transition = `opacity 0.32s ease, transform 0.32s ease`;
        el.style.opacity = '1';
        el.style.transform = 'translateX(0)';
      }, baseDelay + i * step);
    });
  }

  /* ── Shimmer progress bar at top ── */
  function showProgressBar() {
    const existing = document.getElementById('iq-progress');
    if (existing) existing.remove();
    const bar = document.createElement('div');
    bar.id = 'iq-progress';
    Object.assign(bar.style, {
      position: 'fixed', top: '0', left: '0', height: '2.5px',
      width: '0%', zIndex: '99999', pointerEvents: 'none',
      background: 'linear-gradient(90deg, #3b82f6, #06b6d4, #8b5cf6)',
      borderRadius: '0 2px 2px 0',
      transition: 'width 0.5s cubic-bezier(0.16,1,0.3,1), opacity 0.3s ease',
      boxShadow: '0 0 10px rgba(59,130,246,0.6)',
    });
    document.body.appendChild(bar);
    requestAnimationFrame(() => { bar.style.width = '85%'; });
    setTimeout(() => {
      bar.style.width = '100%';
      setTimeout(() => {
        bar.style.opacity = '0';
        setTimeout(() => bar.remove(), 350);
      }, 200);
    }, 500);
  }

  /* ── Fade-in for chart containers ── */
  function fadeInCharts(els, baseDelay=80, step=100) {
    Array.from(els).forEach((el, i) => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(10px)';
      el.style.transition = 'none';
      setTimeout(() => {
        el.style.transition = `opacity 0.6s ease, transform 0.6s cubic-bezier(0.16,1,0.3,1)`;
        el.style.opacity = '1';
        el.style.transform = 'translateY(0)';
      }, baseDelay + i * step);
    });
  }

  /* ── Page title dramatic entrance ── */
  function animateTitle() {
    const titles = document.querySelectorAll('.page-title');
    titles.forEach(el => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(-16px)';
      el.style.transition = 'none';
      setTimeout(() => {
        el.style.transition = 'opacity 0.4s cubic-bezier(0.16,1,0.3,1), transform 0.4s cubic-bezier(0.16,1,0.3,1)';
        el.style.opacity = '1';
        el.style.transform = 'translateY(0)';
      }, 30);
    });
    const subs = document.querySelectorAll('.page-subtitle');
    subs.forEach(el => {
      el.style.opacity = '0';
      setTimeout(() => {
        el.style.transition = 'opacity 0.5s ease';
        el.style.opacity = '1';
      }, 120);
    });
  }

  /* ── Main animation orchestrator ── */
  function runPageAnimations() {
    showProgressBar();
    animateTitle();

    // Metric cards
    setTimeout(() => {
      scalePopCards(document.querySelectorAll('[data-testid="metric-container"]'), 60, 65);
    }, 50);

    // Metric values count up
    setTimeout(() => {
      document.querySelectorAll('[data-testid="stMetricValue"]').forEach(el => animateCounter(el));
    }, 300);

    // Plotly charts
    setTimeout(() => {
      fadeInCharts(document.querySelectorAll('[data-testid="stPlotlyChart"]'), 100, 110);
    }, 80);

    // Dataframes
    setTimeout(() => {
      staggerFadeUp(document.querySelectorAll('[data-testid="stDataFrame"]'), 200, 80);
    }, 150);

    // Buttons
    setTimeout(() => {
      staggerFadeUp(document.querySelectorAll('.stButton'), 80, 40);
    }, 100);

    // Section labels
    setTimeout(() => {
      document.querySelectorAll('.section-label').forEach((el, i) => {
        el.style.opacity = '0';
        setTimeout(() => {
          el.style.transition = 'opacity 0.4s ease';
          el.style.opacity = '1';
        }, 150 + i * 60);
      });
    }, 50);

    // Sidebar nav items
    setTimeout(() => {
      slideFromLeft(
        document.querySelectorAll('[data-testid="stSidebar"] .stRadio label'),
        80, 45
      );
    }, 100);

    // Custom HTML cards (podium, tenure, etc.)
    setTimeout(() => {
      staggerFadeUp(
        document.querySelectorAll('[data-testid="column"] > div > div > div'),
        60, 55
      );
    }, 100);
  }

  /* ── Observe DOM changes (page switches trigger re-render) ── */
  let debounceTimer;
  let lastContent = '';

  const observer = new MutationObserver((mutations) => {
    const mainEl = document.querySelector('.main .block-container');
    if (!mainEl) return;
    const currentContent = mainEl.innerHTML.substring(0, 200);
    if (currentContent === lastContent) return;
    lastContent = currentContent;
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(runPageAnimations, 80);
  });

  function startObserving() {
    const target = document.querySelector('.main') || document.body;
    observer.observe(target, { childList: true, subtree: true });
  }

  /* ── Boot ── */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      startObserving();
      setTimeout(runPageAnimations, 200);
    });
  } else {
    startObserving();
    setTimeout(runPageAnimations, 200);
  }

  /* ── Hover micro-interactions via JS for dynamic elements ── */
  document.addEventListener('mouseover', (e) => {
    const chart = e.target.closest('[data-testid="stPlotlyChart"]');
    if (chart && !chart._hoverBound) {
      chart._hoverBound = true;
      chart.style.transition = 'transform 0.30s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.30s ease, border-color 0.25s ease';
      chart.addEventListener('mouseenter', () => {
        chart.style.transform = 'translateY(-4px) scale(1.008)';
        chart.style.boxShadow = '0 18px 48px rgba(37,99,235,0.13), 0 4px 12px rgba(15,28,46,0.08)';
        chart.style.borderColor = '#93a8d0';
      });
      chart.addEventListener('mouseleave', () => {
        chart.style.transform = 'translateY(0) scale(1)';
        chart.style.boxShadow = '0 6px 24px rgba(15,28,46,0.09), 0 1px 4px rgba(15,28,46,0.05)';
        chart.style.borderColor = '#dde3ef';
      });
    }

    const card = e.target.closest('[data-testid="metric-container"]');
    if (card && !card._hoverBound) {
      card._hoverBound = true;
      card.addEventListener('mouseenter', () => {
        card.style.transition = 'transform 0.32s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.32s ease, border-color 0.25s ease';
        card.style.transform = 'translateY(-5px) scale(1.025)';
        card.style.boxShadow = '0 12px 36px rgba(37,99,235,0.14), 0 2px 8px rgba(15,28,46,0.08)';
        card.style.borderColor = '#93a8d0';
      });
      card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0) scale(1)';
        card.style.boxShadow = '0 1px 4px rgba(15,28,46,0.07)';
        card.style.borderColor = '#dde3ef';
      });
    }
  });

})();
</script>
""", unsafe_allow_html=True)


# ── Chart theme — light, crisp, executive ──────────────────────────────────────
CHART_BG    = "#ffffff"
CHART_PAPER = "#ffffff"
GRID_COLOR  = "#f0f4fa"
AXIS_COLOR  = "#c8d4e8"
TEXT_COLOR  = "#6b7fa3"
FONT_FAMILY = "DM Sans"

def chart_layout(height=360, margin=None):
    if margin is None:
        margin = dict(l=0, r=24, t=20, b=0)
    return dict(
        height=height,
        paper_bgcolor=CHART_PAPER,
        plot_bgcolor="#ffffff",
        font=dict(family=FONT_FAMILY, color=TEXT_COLOR, size=11),
        margin=margin,
        showlegend=False,
        xaxis=dict(
            showgrid=True, gridcolor=GRID_COLOR, zeroline=False,
            tickfont=dict(color=TEXT_COLOR, size=10.5),
            linecolor=AXIS_COLOR, showline=True,
        ),
        yaxis=dict(
            showgrid=True, gridcolor=GRID_COLOR, zeroline=False,
            tickfont=dict(color=TEXT_COLOR, size=10.5),
            linecolor=AXIS_COLOR, showline=False,
        ),
    )


# ── Palette pools — vivid but professional on white ────────────────────────────
BLUE_SCALE   = ["#dbeafe", "#3b82f6", "#1d4ed8"]
VIOLET_SCALE = ["#ede9fe", "#8b5cf6", "#5b21b6"]
GREEN_SCALE  = ["#d1fae5", "#34d399", "#059669"]
AMBER_SCALE  = ["#fef3c7", "#fbbf24", "#d97706"]
CYAN_SCALE   = ["#cffafe", "#22d3ee", "#0891b2"]
ROSE_SCALE   = ["#ffe4e6", "#fb7185", "#e11d48"]
PROC_COLORS  = ["#2563eb","#0891b2","#059669","#d97706","#7c3aed",
                "#e11d48","#0284c7","#65a30d","#ea580c","#9333ea"]


# ── Data ────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file:
        return pd.read_excel(uploaded_file)
    return None

def compute_summary(df):
    return {
        "total_agents":        len(df),
        "active":              int((df["Status"] == "Active").sum()) if "Status" in df.columns else len(df),
        "inactive":            int((df["Status"] == "Inactive").sum()) if "Status" in df.columns else 0,
        "total_source_bkgs":   float(df["Source Bkgs"].sum()),
        "total_issued_bkgs":   float(df["Issued Bkgs."].sum()),
        "total_source_ape":    float(df["Source APE"].sum()),
        "total_issued_ape":    float(df["Issued APE"].sum()),
        "total_wtd_ape":       float(df["Wtd APE"].sum()),
        "total_incentive":     float(df["Final Incentive"].sum()),
        "avg_incentive":       float(df["Final Incentive"].mean()),
        "zero_issuance_agents":int((df["Issued Bkgs."] == 0).sum()),
        "issuance_rate_pct":   round(df["Issued Bkgs."].sum() / df["Source Bkgs"].sum() * 100, 2),
        "ape_conversion_pct":  round(df["Issued APE"].sum() / df["Source APE"].sum() * 100, 2),
    }

EMBEDDED_SUMMARY = {
    "total_agents": 1877, "active": 1805, "inactive": 72,
    "total_source_bkgs": 40055, "total_issued_bkgs": 27194,
    "total_source_ape": 1204002220.0, "total_issued_ape": 1009678298.6,
    "total_wtd_ape": 845895383.68, "total_incentive": 54619469.40,
    "avg_incentive": 29099.34, "zero_issuance_agents": 113,
    "issuance_rate_pct": 67.89, "ape_conversion_pct": 83.86,
}

TOP_AGENTS_DATA = [
    {"Rank":"🥇","Agent":"Anjali Dilip Meshram","Process":"Booking (Self Emp.)","Src Bkgs":16,"Issued Bkgs":8.36,"Issued APE (₹L)":23.42,"Incentive (₹L)":5.56,"TL":"Niraj J. Yadav"},
    {"Rank":"🥈","Agent":"Umang","Process":"Ipru_APE_Ggn","Src Bkgs":53,"Issued Bkgs":30.40,"Issued APE (₹L)":21.27,"Incentive (₹L)":2.73,"TL":"Ajay Tyagi"},
    {"Rank":"🥉","Agent":"Sumit Singh","Process":"Ipru_APE_Ggn","Src Bkgs":30,"Issued Bkgs":22.07,"Issued APE (₹L)":19.60,"Incentive (₹L)":2.33,"TL":"Tanisha Chaudhary"},
    {"Rank":"4","Agent":"Meghavat Rakesh","Process":"Telugu Inbound","Src Bkgs":55,"Issued Bkgs":45.85,"Issued APE (₹L)":18.36,"Incentive (₹L)":2.13,"TL":"Ruchita S. Chinta"},
    {"Rank":"5","Agent":"Nimmarajula Sai Teja","Process":"Hyd Bday","Src Bkgs":47,"Issued Bkgs":33.46,"Issued APE (₹L)":17.98,"Incentive (₹L)":2.07,"TL":"Dunna V. Varma"},
    {"Rank":"6","Agent":"Dhananjay Sharma","Process":"Ipru_APE_Ggn","Src Bkgs":45,"Issued Bkgs":35.26,"Issued APE (₹L)":19.13,"Incentive (₹L)":1.95,"TL":"Nikhil Kumar"},
    {"Rank":"7","Agent":"Ravindra K. Chhapre","Process":"Inbound","Src Bkgs":63,"Issued Bkgs":45.09,"Issued APE (₹L)":19.40,"Incentive (₹L)":1.91,"TL":"Rohit D. Patil"},
    {"Rank":"8","Agent":"Mohammad Sohail","Process":"NRI","Src Bkgs":22,"Issued Bkgs":14.97,"Issued APE (₹L)":31.36,"Incentive (₹L)":1.91,"TL":"Ashish Choudhary"},
    {"Rank":"9","Agent":"Sourabh Anand","Process":"Dedicated FOS","Src Bkgs":34,"Issued Bkgs":26.00,"Issued APE (₹L)":14.60,"Incentive (₹L)":1.87,"TL":"Rahul Bhatia"},
    {"Rank":"10","Agent":"Manikandan Raman","Process":"Dedicated FOS","Src Bkgs":51,"Issued Bkgs":33.89,"Issued APE (₹L)":12.63,"Incentive (₹L)":1.82,"TL":"Vinoth Gnanavel"},
]

PROCESS_DATA = [
    {"Process Group":"APE_Salaried","Agents":572,"Avg Issued Bkgs":14.83,"Avg Wtd APE (₹L)":4.51,"Avg Incentive (₹)":30714,"Total Incentive (₹L)":175.68},
    {"Process Group":"Inbound/b'day","Agents":254,"Avg Issued Bkgs":25.74,"Avg Wtd APE (₹L)":7.69,"Avg Incentive (₹)":48884,"Total Incentive (₹L)":124.17},
    {"Process Group":"Ipru & HDFC","Agents":153,"Avg Issued Bkgs":20.05,"Avg Wtd APE (₹L)":7.18,"Avg Incentive (₹)":48639,"Total Incentive (₹L)":74.42},
    {"Process Group":"APE_Self Emloyed","Agents":153,"Avg Issued Bkgs":15.47,"Avg Wtd APE (₹L)":4.01,"Avg Incentive (₹)":32678,"Total Incentive (₹L)":50.00},
    {"Process Group":"HNI_Salaried","Agents":87,"Avg Issued Bkgs":20.85,"Avg Wtd APE (₹L)":8.26,"Avg Incentive (₹)":48761,"Total Incentive (₹L)":42.42},
    {"Process Group":"Bkg_ Salaried","Agents":453,"Avg Issued Bkgs":5.60,"Avg Wtd APE (₹L)":0.97,"Avg Incentive (₹)":6397,"Total Incentive (₹L)":28.98},
    {"Process Group":"NRI","Agents":70,"Avg Issued Bkgs":12.81,"Avg Wtd APE (₹L)":9.71,"Avg Incentive (₹)":37633,"Total Incentive (₹L)":26.34},
    {"Process Group":"Bkgs_Self Employed","Agents":84,"Avg Issued Bkgs":7.17,"Avg Wtd APE (₹L)":1.69,"Avg Incentive (₹)":16380,"Total Incentive (₹L)":13.76},
    {"Process Group":"Regional","Agents":37,"Avg Issued Bkgs":11.69,"Avg Wtd APE (₹L)":3.13,"Avg Incentive (₹)":14514,"Total Incentive (₹L)":5.37},
    {"Process Group":"Chat","Agents":14,"Avg Issued Bkgs":32.53,"Avg Wtd APE (₹L)":8.50,"Avg Incentive (₹)":36118,"Total Incentive (₹L)":5.06},
]

TENURE_DATA = [
    {"Tenure Band":"0 – 3 M","Agents":451,"Avg Issued Bkgs":4.96,"Avg Wtd APE (₹L)":1.08,"Avg Incentive (₹)":5318},
    {"Tenure Band":"3 – 6 M","Agents":413,"Avg Issued Bkgs":12.10,"Avg Wtd APE (₹L)":3.14,"Avg Incentive (₹)":21220},
    {"Tenure Band":"6 – 12 M","Agents":261,"Avg Issued Bkgs":16.09,"Avg Wtd APE (₹L)":4.99,"Avg Incentive (₹)":34825},
    {"Tenure Band":"Above 12 M","Agents":752,"Avg Issued Bkgs":20.96,"Avg Wtd APE (₹L)":7.14,"Avg Incentive (₹)":45702},
]
TENURE_PALETTE = ["#f59e0b", "#f97316", "#3b82f6", "#10b981"]

MANAGER_DATA = [
    {"Manager":"K Narasimha Raja","Team":150,"Bkgs Issued":2222,"Avg/Agent (₹)":44419,"Total Incentive (₹L)":66.63},
    {"Manager":"Anesh Abraham","Team":130,"Bkgs Issued":2596,"Avg/Agent (₹)":50029,"Total Incentive (₹L)":65.04},
    {"Manager":"Vishal Kumar","Team":135,"Bkgs Issued":3474,"Avg/Agent (₹)":39628,"Total Incentive (₹L)":53.50},
    {"Manager":"Sujay Sanjay Mhatre","Team":218,"Bkgs Issued":2692,"Avg/Agent (₹)":23721,"Total Incentive (₹L)":51.71},
    {"Manager":"Roshan Jha","Team":128,"Bkgs Issued":2486,"Avg/Agent (₹)":28877,"Total Incentive (₹L)":36.96},
    {"Manager":"Jimmy Mahendra Shetty","Team":63,"Bkgs Issued":1431,"Avg/Agent (₹)":51182,"Total Incentive (₹L)":32.24},
    {"Manager":"Sulagno Chatterjee","Team":107,"Bkgs Issued":1132,"Avg/Agent (₹)":28706,"Total Incentive (₹L)":30.72},
    {"Manager":"Raveendaran G","Team":86,"Bkgs Issued":1134,"Avg/Agent (₹)":33818,"Total Incentive (₹L)":29.08},
    {"Manager":"Sachin Katoch","Team":58,"Bkgs Issued":1272,"Avg/Agent (₹)":48454,"Total Incentive (₹L)":28.10},
    {"Manager":"Niharika Verma","Team":82,"Bkgs Issued":1783,"Avg/Agent (₹)":31852,"Total Incentive (₹L)":26.12},
]

SYSTEM_PROMPT = f"""You are an expert HR and sales analytics assistant for Term Agent Inc.
You have full access to structured agent performance data for 1,877 agents.

KEY METRICS: {json.dumps(EMBEDDED_SUMMARY)}
TOP 10 AGENTS: {json.dumps(TOP_AGENTS_DATA)}
PROCESS PERFORMANCE: {json.dumps(PROCESS_DATA)}
TENURE PERFORMANCE: {json.dumps(TENURE_DATA)}
MANAGER PERFORMANCE: {json.dumps(MANAGER_DATA)}

DEFINITIONS: AON/Tenure = Age on Network. APE = Annualized Premium Equivalent. Wtd APE = weighted APE. Source Bkgs = attempted bookings. Issued Bkgs = converted. NRI = Non-Resident Indian.
RULES: Be concise and data-driven. Format: ₹X.XX L or ₹X.XX Cr. Use bullet points. Say so if data isn't available."""

def fmt_inr(n):
    n = float(n)
    if n >= 10_000_000: return f"₹{n/10_000_000:.2f} Cr"
    if n >= 100_000:    return f"₹{n/100_000:.1f} L"
    return f"₹{n:,.0f}"


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:20px 16px 10px;border-bottom:1px solid rgba(255,255,255,0.08);margin-bottom:8px;'>
        <div style='display:flex;align-items:center;gap:10px;'>
            <div style='width:36px;height:36px;border-radius:10px;
                        background:linear-gradient(135deg,#2563eb 0%,#7c3aed 100%);
                        display:flex;align-items:center;justify-content:center;font-size:18px;
                        box-shadow:0 4px 14px rgba(37,99,235,0.4);'>⚡</div>
            <div>
                <div style='font-family:Syne,sans-serif;font-weight:800;font-size:15px;color:#f0f6ff;letter-spacing:-0.01em;'>AgentIQ</div>
                <div style='font-size:10px;color:rgba(255,255,255,0.3);letter-spacing:0.08em;text-transform:uppercase;'>Analytics Platform</div>
            </div>
        </div>
    </div>
    <div class="nav-section-label">Navigation</div>
    """, unsafe_allow_html=True)

    page = st.radio("", [
        "⚡ Overview", "🏆 Top Agents", "📊 By Process",
        "🕐 By Tenure", "👥 Managers", "🤖 AI Chatbot"
    ], label_visibility="collapsed")

    st.markdown("""<div style='border-top:1px solid #1e2d45;margin:12px 0;'></div>
    <div class="nav-section-label">Data Source</div>""", unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload Excel", type=["xlsx","xls"], label_visibility="collapsed")
    if uploaded:
        st.markdown("<div style='font-size:11px;color:#10b981;padding:6px 0;'>✓ File loaded successfully</div>", unsafe_allow_html=True)

    st.markdown("""<div style='border-top:1px solid #1e2d45;margin:12px 0;'></div>
    <div class="nav-section-label">AI Settings</div>""", unsafe_allow_html=True)

    api_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...", label_visibility="collapsed")
    st.markdown("<div style='font-size:10.5px;color:#3d4f6a;padding:4px 2px;'>Required for AI Chatbot tab</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='position:absolute;bottom:20px;left:16px;right:16px;'>
        <div style='font-size:10px;color:rgba(255,255,255,0.25);line-height:1.6;'>
            1,877 agents &nbsp;·&nbsp; ₹5.46 Cr incentives<br>
            Data: Term Agent Inc
        </div>
    </div>""", unsafe_allow_html=True)


# ── Load data ──────────────────────────────────────────────────────────────────
df_raw = load_data(uploaded) if uploaded else None
summary = compute_summary(df_raw) if df_raw is not None else EMBEDDED_SUMMARY


# ════════════════════════════════════════════════════════════════════════
# PAGE 1: OVERVIEW
# ════════════════════════════════════════════════════════════════════════
if page == "⚡ Overview":
    st.markdown("""
    <div class='page-header-wrap' style='background:linear-gradient(130deg,#1e3a5f 0%,#2563eb 55%,#0891b2 100%);'>
        <div class='page-header-inner'>
            <div class='page-header-left'>
                <div class='page-title'>Performance Overview</div>
                <div class='page-subtitle'>Real-time KPIs across 1,877 agents — incentives, conversions &amp; APE.</div>
            </div>
            <div class='page-header-icon'>⚡</div>
            <div class='page-header-badge'>📅 Monthly Report</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Row 1 — rich styled cards ──
    kpi_row1 = [
        {
            "label": "Total Agents", "value": f"{summary['total_agents']:,}",
            "sub": f"▲ {summary['active']:,} active · {summary['inactive']} inactive",
            "icon": "👥", "color": "#2563eb", "light": "#dbeafe", "bg": "#eff6ff",
            "bar": 100, "tag": "Workforce",
        },
        {
            "label": "Total Incentive", "value": fmt_inr(summary['total_incentive']),
            "sub": f"avg {fmt_inr(summary['avg_incentive'])} / agent",
            "icon": "💰", "color": "#059669", "light": "#d1fae5", "bg": "#f0fdf4",
            "bar": 100, "tag": "Payout",
        },
        {
            "label": "Issuance Rate", "value": f"{summary['issuance_rate_pct']}%",
            "sub": f"{summary['total_issued_bkgs']:,.0f} of {summary['total_source_bkgs']:,.0f} bookings",
            "icon": "📈", "color": "#d97706", "light": "#fef3c7", "bg": "#fffbeb",
            "bar": int(summary['issuance_rate_pct']), "tag": "Conversion",
        },
        {
            "label": "APE Conversion", "value": f"{summary['ape_conversion_pct']}%",
            "sub": f"{fmt_inr(summary['total_issued_ape'])} issued premium",
            "icon": "🎯", "color": "#7c3aed", "light": "#ede9fe", "bg": "#f5f3ff",
            "bar": int(summary['ape_conversion_pct']), "tag": "Premium",
        },
    ]

    cols1 = st.columns(4)
    for i, (col, kpi) in enumerate(zip(cols1, kpi_row1)):
        col.markdown(f"""
        <div class="iq-kpi-card" style="
            background: linear-gradient(145deg, #ffffff 0%, {kpi['bg']} 100%);
            border: 1px solid #dde3ef;
            border-top: 3px solid {kpi['color']};
            border-radius: 16px;
            padding: 20px 18px 16px;
            box-shadow: 0 2px 8px rgba(15,28,46,0.07), 0 0 0 1px rgba(15,28,46,0.03);
            cursor: default;
            animation: kpiSlideUp 0.5s cubic-bezier(0.34,1.56,0.64,1) {i*0.08:.2f}s both;
            position: relative; overflow: hidden;">
            <!-- corner glow -->
            <div style="position:absolute;top:-24px;right:-24px;width:100px;height:100px;
                border-radius:50%;background:{kpi['color']};opacity:0.06;
                transition:opacity 0.3s ease,transform 0.35s ease;" class="iq-glow"></div>
            <!-- top row -->
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
                <span style="font-size:9.5px;font-weight:700;color:{kpi['color']};
                    text-transform:uppercase;letter-spacing:0.1em;">{kpi['tag']}</span>
                <span style="font-size:18px;line-height:1;">{kpi['icon']}</span>
            </div>
            <!-- label -->
            <div style="font-size:11px;font-weight:600;color:#6b7fa3;margin-bottom:4px;
                letter-spacing:0.02em;">{kpi['label']}</div>
            <!-- value -->
            <div style="font-family:'Syne',sans-serif;font-size:24px;font-weight:800;
                color:#0f1c2e;letter-spacing:-0.03em;line-height:1.1;margin-bottom:6px;">
                {kpi['value']}
            </div>
            <!-- sub -->
            <div style="font-size:10.5px;color:#6b7fa3;margin-bottom:12px;line-height:1.4;">
                {kpi['sub']}
            </div>
            <!-- progress bar -->
            <div style="height:4px;background:#e8eef8;border-radius:99px;overflow:hidden;">
                <div class="iq-bar" style="
                    height:100%;border-radius:99px;
                    background:linear-gradient(90deg,{kpi['light']},{kpi['color']});
                    width:0%;
                    transition:width 1.1s cubic-bezier(0.16,1,0.3,1) {0.3 + i*0.12:.2f}s;"
                    data-width="{kpi['bar']}">
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin:10px 0;'></div>", unsafe_allow_html=True)

    # ── KPI Row 2 ──
    kpi_row2 = [
        {
            "label": "Active Agents", "value": f"{summary['active']:,}",
            "sub": f"▼ {summary['inactive']} inactive this period",
            "icon": "✅", "color": "#0891b2", "light": "#cffafe", "bg": "#ecfeff",
            "bar": int(summary['active'] / summary['total_agents'] * 100), "tag": "Active",
        },
        {
            "label": "Source APE", "value": fmt_inr(summary['total_source_ape']),
            "sub": "total premium sourced by agents",
            "icon": "📋", "color": "#2563eb", "light": "#dbeafe", "bg": "#eff6ff",
            "bar": 100, "tag": "Sourced",
        },
        {
            "label": "Issued APE", "value": fmt_inr(summary['total_issued_ape']),
            "sub": "successfully issued premium",
            "icon": "🏦", "color": "#059669", "light": "#d1fae5", "bg": "#f0fdf4",
            "bar": int(summary['ape_conversion_pct']), "tag": "Issued",
        },
        {
            "label": "Zero-Issuance", "value": str(summary['zero_issuance_agents']),
            "sub": "agents with 0 bookings this month",
            "icon": "⚠️", "color": "#e11d48", "light": "#fecdd3", "bg": "#fff1f2",
            "bar": int(summary['zero_issuance_agents'] / summary['total_agents'] * 100), "tag": "At Risk",
        },
    ]

    cols2 = st.columns(4)
    for i, (col, kpi) in enumerate(zip(cols2, kpi_row2)):
        col.markdown(f"""
        <div class="iq-kpi-card" style="
            background: linear-gradient(145deg, #ffffff 0%, {kpi['bg']} 100%);
            border: 1px solid #dde3ef;
            border-top: 3px solid {kpi['color']};
            border-radius: 16px;
            padding: 20px 18px 16px;
            box-shadow: 0 2px 8px rgba(15,28,46,0.07), 0 0 0 1px rgba(15,28,46,0.03);
            cursor: default;
            animation: kpiSlideUp 0.5s cubic-bezier(0.34,1.56,0.64,1) {0.32 + i*0.08:.2f}s both;
            position: relative; overflow: hidden;">
            <div style="position:absolute;top:-24px;right:-24px;width:100px;height:100px;
                border-radius:50%;background:{kpi['color']};opacity:0.06;
                transition:opacity 0.3s ease,transform 0.35s ease;" class="iq-glow"></div>
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
                <span style="font-size:9.5px;font-weight:700;color:{kpi['color']};
                    text-transform:uppercase;letter-spacing:0.1em;">{kpi['tag']}</span>
                <span style="font-size:18px;line-height:1;">{kpi['icon']}</span>
            </div>
            <div style="font-size:11px;font-weight:600;color:#6b7fa3;margin-bottom:4px;
                letter-spacing:0.02em;">{kpi['label']}</div>
            <div style="font-family:'Syne',sans-serif;font-size:24px;font-weight:800;
                color:#0f1c2e;letter-spacing:-0.03em;line-height:1.1;margin-bottom:6px;">
                {kpi['value']}
            </div>
            <div style="font-size:10.5px;color:#6b7fa3;margin-bottom:12px;line-height:1.4;">
                {kpi['sub']}
            </div>
            <div style="height:4px;background:#e8eef8;border-radius:99px;overflow:hidden;">
                <div class="iq-bar" style="
                    height:100%;border-radius:99px;
                    background:linear-gradient(90deg,{kpi['light']},{kpi['color']});
                    width:0%;
                    transition:width 1.1s cubic-bezier(0.16,1,0.3,1) {0.62 + i*0.12:.2f}s;"
                    data-width="{kpi['bar']}">
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Inject KPI animation styles + JS ──
    st.markdown("""
    <style>
    @keyframes kpiSlideUp {
        0%   { opacity:0; transform: translateY(24px) scale(0.94); }
        60%  { transform: translateY(-3px) scale(1.01); }
        100% { opacity:1; transform: translateY(0) scale(1); }
    }
    .iq-kpi-card {
        transition:
            transform 0.32s cubic-bezier(0.34,1.56,0.64,1),
            box-shadow 0.32s ease,
            border-color 0.25s ease !important;
        will-change: transform;
    }
    .iq-kpi-card:hover {
        transform: translateY(-6px) scale(1.03) !important;
        box-shadow: 0 16px 40px rgba(37,99,235,0.16),
                    0 4px 12px rgba(15,28,46,0.08),
                    0 0 0 1.5px rgba(37,99,235,0.18) !important;
        border-color: #93c5fd !important;
        z-index: 10;
    }
    .iq-kpi-card:hover .iq-glow {
        opacity: 0.15 !important;
        transform: scale(1.5) !important;
    }
    .iq-kpi-card:hover .iq-bar {
        filter: brightness(1.1) saturate(1.15);
    }
    .iq-kpi-card:active {
        transform: translateY(-2px) scale(1.01) !important;
        transition-duration: 0.1s !important;
    }
    </style>
    <script>
    (function animateBars() {
        function run() {
            document.querySelectorAll('.iq-bar').forEach(function(bar) {
                var w = bar.getAttribute('data-width');
                if (w && bar.style.width === '0%') {
                    setTimeout(function() { bar.style.width = w + '%'; }, 80);
                }
            });
        }
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', run);
        } else {
            run();
            setTimeout(run, 300);
        }
        var obs = new MutationObserver(function() { setTimeout(run, 120); });
        obs.observe(document.body, { childList: true, subtree: true });
    })();
    </script>
    """, unsafe_allow_html=True)

    # ── Chart row: Bar + Donut ──
    st.markdown("<div class='section-label'>Incentive Distribution by Process Group</div>", unsafe_allow_html=True)

    chart_col, donut_col = st.columns([2, 1])

    with chart_col:
        proc_df = pd.DataFrame(PROCESS_DATA).sort_values("Total Incentive (₹L)", ascending=True)
        fig_bar = go.Figure(go.Bar(
            x=proc_df["Total Incentive (₹L)"],
            y=proc_df["Process Group"],
            orientation="h",
            marker=dict(
                color=proc_df["Total Incentive (₹L)"],
                colorscale=[[0, "#dbeafe"], [0.4, "#3b82f6"], [1.0, "#1d4ed8"]],
                line=dict(width=0),
            ),
            text=proc_df["Total Incentive (₹L)"].apply(lambda x: f"₹{x:.1f}L"),
            textposition="outside",
            textfont=dict(color="#4a5e7a", size=10.5, family=FONT_FAMILY),
        ))
        fig_bar.update_layout(**chart_layout(380, dict(l=0, r=60, t=16, b=0)))
        fig_bar.update_xaxes(title=None)
        fig_bar.update_yaxes(title=None)
        st.plotly_chart(fig_bar, use_container_width=True)

    with donut_col:
        fig_donut = go.Figure(go.Pie(
            values=[summary["active"], summary["inactive"]],
            labels=["Active", "Inactive"],
            hole=0.65,
            marker=dict(colors=["#2563eb", "#e8eef8"], line=dict(color="#ffffff", width=3)),
            textfont=dict(color="#1e293b", size=12, family=FONT_FAMILY),
            textinfo="percent+label",
        ))
        fig_donut.add_annotation(
            text=f"<b>{summary['total_agents']:,}</b>",
            x=0.5, y=0.5, font=dict(size=22, color="#0f1c2e", family="Syne"),
            showarrow=False
        )
        fig_donut.update_layout(**chart_layout(240, dict(l=0,r=0,t=16,b=0)))
        st.plotly_chart(fig_donut, use_container_width=True)

    # ── Chart row: Tenure bar + Bubble ──
    st.markdown("<div class='section-label'>Tenure × Incentive Analysis</div>", unsafe_allow_html=True)
    t_col, b_col = st.columns([1, 1])

    with t_col:
        ten_df = pd.DataFrame(TENURE_DATA)
        fig_ten = go.Figure()
        fig_ten.add_trace(go.Bar(
            x=ten_df["Tenure Band"],
            y=ten_df["Avg Incentive (₹)"],
            marker=dict(color=TENURE_PALETTE, line=dict(width=0)),
            text=ten_df["Avg Incentive (₹)"].apply(lambda x: f"₹{x:,}"),
            textposition="outside",
            textfont=dict(color="#4a5e7a", size=10, family=FONT_FAMILY),
        ))
        fig_ten.update_layout(**chart_layout(290, dict(l=0,r=0,t=16,b=0)))
        st.plotly_chart(fig_ten, use_container_width=True)

    with b_col:
        proc_df2 = pd.DataFrame(PROCESS_DATA)
        fig_bubble = px.scatter(
            proc_df2,
            x="Avg Issued Bkgs",
            y="Avg Incentive (₹)",
            size="Agents",
            color="Process Group",
            color_discrete_sequence=PROC_COLORS,
            text="Process Group",
            size_max=42,
        )
        fig_bubble.update_traces(textposition="top center", textfont=dict(size=9, color="#6b7fa3"))
        layout = chart_layout(290, dict(l=0,r=0,t=16,b=0))
        layout.pop("showlegend")
        fig_bubble.update_layout(**layout, showlegend=False)
        st.plotly_chart(fig_bubble, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════
# PAGE 2: TOP AGENTS
# ════════════════════════════════════════════════════════════════════════
elif page == "🏆 Top Agents":
    st.markdown("""
    <div class='page-header-wrap' style='background:linear-gradient(130deg,#422006 0%,#d97706 50%,#f59e0b 100%);'>
        <div class='page-header-inner'>
            <div class='page-header-left'>
                <div class='page-title'>Top Agents Leaderboard</div>
                <div class='page-subtitle'>Ranked by final incentive payout — this month's star performers.</div>
            </div>
            <div class='page-header-icon'>🏆</div>
            <div class='page-header-badge'>🥇 Top 10 Ranked</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Podium top 3
    st.markdown("<div class='section-label'>Podium — Top 3</div>", unsafe_allow_html=True)
    p1, p2, p3 = st.columns(3)
    podium = [
        (p1, TOP_AGENTS_DATA[0], "🥇", "linear-gradient(135deg,#fffbeb,#fef3c7)", "#d97706", "#fde68a"),
        (p2, TOP_AGENTS_DATA[1], "🥈", "linear-gradient(135deg,#f8fafc,#f1f5f9)", "#64748b", "#e2e8f0"),
        (p3, TOP_AGENTS_DATA[2], "🥉", "linear-gradient(135deg,#fff7ed,#fef3c7)", "#ea580c", "#fed7aa"),
    ]
    for col, agent, medal, bg, accent, border in podium:
        with col:
            st.markdown(f"""
            <div style='background:{bg};border:1px solid {border}33;border-top:3px solid {accent};
                        border-radius:16px;padding:22px 18px 18px;text-align:center;'>
                <div style='font-size:32px;margin-bottom:10px;'>{medal}</div>
                <div style='font-family:Syne,sans-serif;font-weight:800;font-size:14.5px;color:#0f1c2e;line-height:1.3;margin-bottom:4px;'>{agent['Agent']}</div>
                <div style='font-size:11px;color:#6b7fa3;margin-bottom:14px;'>{agent['Process']}</div>
                <div style='font-size:24px;font-weight:800;font-family:Syne,sans-serif;color:{accent};letter-spacing:-0.02em;'>₹{agent['Incentive (₹L)']:.2f}L</div>
                <div style='font-size:10.5px;color:#6b7fa3;margin-top:6px;'>
                    APE ₹{agent['Issued APE (₹L)']:.2f}L &nbsp;·&nbsp; {agent['Issued Bkgs']:.1f} bkgs
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Leaderboard table
    st.markdown("<div class='section-label'>Full Leaderboard — Top 10</div>", unsafe_allow_html=True)
    df_agents = pd.DataFrame(TOP_AGENTS_DATA)

    def hl_top(row):
        colors = {"🥇":"background-color:#fffbeb;color:#92400e;font-weight:700",
                  "🥈":"background-color:#f8fafc;color:#475569;font-weight:700",
                  "🥉":"background-color:#fff7ed;color:#9a3412;font-weight:700"}
        style = colors.get(row["Rank"], "color:#334155")
        return [style]*len(row)

    styled = (
        df_agents.style
        .apply(hl_top, axis=1)
        .bar(subset=["Incentive (₹L)"], color="#dbeafe", vmin=0)
        .bar(subset=["Issued APE (₹L)"], color="#d1fae5", vmin=0)
        .format({"Issued Bkgs":"{:.1f}","Incentive (₹L)":"₹{:.2f}L","Issued APE (₹L)":"₹{:.2f}L"})
        .set_properties(**{"font-size":"12.5px","padding":"10px 14px",
                           "background-color":"#ffffff","color":"#1e293b"})
        .set_table_styles([
            {"selector":"thead th","props":[("background-color","#f8fafd"),("color","#6b7fa3"),
             ("font-size","10px"),("text-transform","uppercase"),("letter-spacing","0.1em"),
             ("padding","10px 14px"),("border-bottom","1px solid #1e2d45"),("font-weight","700")]},
            {"selector":"tbody tr:hover td","props":[("background-color","#eff6ff")]},
        ])
        .hide(axis="index")
    )
    st.dataframe(styled, use_container_width=True, height=420)

    # Scatter chart
    st.markdown("<div class='section-label'>Incentive vs APE — Value Map</div>", unsafe_allow_html=True)
    fig_sc = px.scatter(
        df_agents, x="Issued APE (₹L)", y="Incentive (₹L)",
        text="Agent", size=[32]*10,
        color="Incentive (₹L)",
        color_continuous_scale=[[0,"#0f2a4a"],[0.5,"#3b82f6"],[1.0,"#06b6d4"]],
    )
    fig_sc.update_traces(textposition="top center",
                         textfont=dict(size=9.5, color="#4a5e7a", family=FONT_FAMILY),
                         marker=dict(line=dict(width=1, color="#0d1117")))
    layout = chart_layout(320, dict(l=0,r=0,t=16,b=0))
    layout["coloraxis_showscale"] = False
    fig_sc.update_layout(**layout)
    st.plotly_chart(fig_sc, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════
# PAGE 3: BY PROCESS
# ════════════════════════════════════════════════════════════════════════
elif page == "📊 By Process":
    st.markdown("""
    <div class='page-header-wrap' style='background:linear-gradient(130deg,#2e1065 0%,#7c3aed 55%,#a855f7 100%);'>
        <div class='page-header-inner'>
            <div class='page-header-left'>
                <div class='page-title'>Process Group Performance</div>
                <div class='page-subtitle'>Incentive payout, bookings and APE broken down by sales channel.</div>
            </div>
            <div class='page-header-icon'>📊</div>
            <div class='page-header-badge'>🔀 10 Channels</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    df_proc = pd.DataFrame(PROCESS_DATA)
    df_asc  = df_proc.sort_values("Avg Incentive (₹)", ascending=True)
    df_bk   = df_proc.sort_values("Avg Issued Bkgs", ascending=True)

    cl, cr = st.columns(2)
    with cl:
        st.markdown("<div class='section-label'>Avg Incentive per Agent</div>", unsafe_allow_html=True)
        fig1 = go.Figure(go.Bar(
            x=df_asc["Avg Incentive (₹)"], y=df_asc["Process Group"], orientation="h",
            marker=dict(color=df_asc["Avg Incentive (₹)"],
                        colorscale=[[0,"#ede9fe"],[0.5,"#8b5cf6"],[1.0,"#5b21b6"]],
                        line=dict(width=0)),
            text=df_asc["Avg Incentive (₹)"].apply(lambda x: f"₹{x:,.0f}"),
            textposition="outside",
            textfont=dict(color="#4a5e7a", size=10, family=FONT_FAMILY),
        ))
        fig1.update_layout(**chart_layout(360, dict(l=0,r=60,t=16,b=0)))
        st.plotly_chart(fig1, use_container_width=True)

    with cr:
        st.markdown("<div class='section-label'>Avg Issued Bookings per Agent</div>", unsafe_allow_html=True)
        fig2 = go.Figure(go.Bar(
            x=df_bk["Avg Issued Bkgs"], y=df_bk["Process Group"], orientation="h",
            marker=dict(color=df_bk["Avg Issued Bkgs"],
                        colorscale=[[0,"#d1fae5"],[0.5,"#34d399"],[1.0,"#059669"]],
                        line=dict(width=0)),
            text=df_bk["Avg Issued Bkgs"].apply(lambda x: f"{x:.1f}"),
            textposition="outside",
            textfont=dict(color="#4a5e7a", size=10, family=FONT_FAMILY),
        ))
        fig2.update_layout(**chart_layout(360, dict(l=0,r=40,t=16,b=0)))
        st.plotly_chart(fig2, use_container_width=True)

    # Total incentive waterfall-style bar
    st.markdown("<div class='section-label'>Total Incentive Payout — All Channels</div>", unsafe_allow_html=True)
    df_total = df_proc.sort_values("Total Incentive (₹L)", ascending=False)
    fig3 = go.Figure(go.Bar(
        x=df_total["Process Group"],
        y=df_total["Total Incentive (₹L)"],
        marker=dict(color=PROC_COLORS[:len(df_total)], line=dict(width=0)),
        text=df_total["Total Incentive (₹L)"].apply(lambda x: f"₹{x:.1f}L"),
        textposition="outside",
        textfont=dict(color="#4a5e7a", size=10.5, family=FONT_FAMILY),
    ))
    fig3.update_layout(**chart_layout(280, dict(l=0,r=0,t=16,b=0)))
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("<div class='section-label'>Full Data Table</div>", unsafe_allow_html=True)
    styled_proc = (
        df_proc.style
        .bar(subset=["Total Incentive (₹L)"], color="#dbeafe", vmin=0)
        .bar(subset=["Avg Wtd APE (₹L)"],     color="#d1fae5", vmin=0)
        .format({"Avg Incentive (₹)":"₹{:,.0f}","Total Incentive (₹L)":"₹{:.2f}L",
                 "Avg Wtd APE (₹L)":"₹{:.2f}L","Avg Issued Bkgs":"{:.1f}"})
        .set_properties(**{"font-size":"12.5px","padding":"10px 14px",
                           "background-color":"#ffffff","color":"#1e293b"})
        .set_table_styles([
            {"selector":"thead th","props":[("background-color","#f8fafd"),("color","#6b7fa3"),
             ("font-size","10px"),("text-transform","uppercase"),("letter-spacing","0.1em"),
             ("padding","10px 14px"),("border-bottom","1px solid #1e2d45"),("font-weight","700")]},
            {"selector":"tbody tr:hover td","props":[("background-color","#eff6ff")]},
        ])
        .hide(axis="index")
    )
    st.dataframe(styled_proc, use_container_width=True, height=400)


# ════════════════════════════════════════════════════════════════════════
# PAGE 4: BY TENURE
# ════════════════════════════════════════════════════════════════════════
elif page == "🕐 By Tenure":
    st.markdown("""
    <div class='page-header-wrap' style='background:linear-gradient(130deg,#064e3b 0%,#059669 55%,#34d399 100%);'>
        <div class='page-header-inner'>
            <div class='page-header-left'>
                <div class='page-title'>Tenure-Based Performance</div>
                <div class='page-subtitle'>How agent experience (AON) shapes incentives, bookings and APE.</div>
            </div>
            <div class='page-header-icon'>🕐</div>
            <div class='page-header-badge'>📆 4 Tenure Bands</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tenure KPI cards
    st.markdown("<div class='section-label'>Avg Incentive by Tenure Band</div>", unsafe_allow_html=True)
    cols = st.columns(4)
    for i, (col, t) in enumerate(zip(cols, TENURE_DATA)):
        c = TENURE_PALETTE[i]
        col.markdown(f"""
        <div style='background:linear-gradient(145deg,#ffffff,#f8fbff);border:1px solid #dde3ef;border-top:3px solid {c};
                    border-radius:14px;padding:18px 16px;'>
            <div style='font-size:9.5px;font-weight:700;color:{c};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;'>{t['Tenure Band']}</div>
            <div style='font-family:Syne,sans-serif;font-size:22px;font-weight:700;color:#0f1c2e;letter-spacing:-0.02em;'>₹{t['Avg Incentive (₹)']:,}</div>
            <div style='font-size:10.5px;color:#3d4f6a;margin:4px 0 10px;'>avg incentive / agent</div>
            <div style='height:3px;background:#e8eef8;border-radius:99px;'>
                <div style='width:{int(t["Avg Incentive (₹)"]/45702*100)}%;height:100%;background:{c};border-radius:99px;'></div>
            </div>
            <div style='font-size:11px;color:#6b7fa3;margin-top:10px;font-weight:500;'>{t['Agents']:,} agents</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin:4px 0;'></div>", unsafe_allow_html=True)

    cl, cr = st.columns(2)
    df_ten = pd.DataFrame(TENURE_DATA)

    with cl:
        st.markdown("<div class='section-label'>Avg Incentive Growth</div>", unsafe_allow_html=True)
        fig_li = go.Figure()
        fig_li.add_trace(go.Bar(
            x=df_ten["Tenure Band"], y=df_ten["Avg Incentive (₹)"],
            marker_color=TENURE_PALETTE, marker_line_width=0,
            text=df_ten["Avg Incentive (₹)"].apply(lambda x: f"₹{x:,}"),
            textposition="outside",
            textfont=dict(color="#4a5e7a", size=10, family=FONT_FAMILY),
        ))
        fig_li.add_trace(go.Scatter(
            x=df_ten["Tenure Band"], y=df_ten["Avg Incentive (₹)"],
            mode="lines+markers",
            line=dict(color="#06b6d4", width=2, dash="dot"),
            marker=dict(size=7, color="#06b6d4", line=dict(width=2, color="#0d1117")),
            showlegend=False,
        ))
        fig_li.update_layout(**chart_layout(300, dict(l=0,r=0,t=16,b=0)))
        st.plotly_chart(fig_li, use_container_width=True)

    with cr:
        st.markdown("<div class='section-label'>Avg Issued Bookings</div>", unsafe_allow_html=True)
        fig_bk2 = go.Figure(go.Bar(
            x=df_ten["Tenure Band"], y=df_ten["Avg Issued Bkgs"],
            marker_color=TENURE_PALETTE, marker_line_width=0,
            text=df_ten["Avg Issued Bkgs"],
            textposition="outside",
            textfont=dict(color="#4a5e7a", size=10, family=FONT_FAMILY),
        ))
        fig_bk2.update_layout(**chart_layout(300, dict(l=0,r=0,t=16,b=0)))
        st.plotly_chart(fig_bk2, use_container_width=True)

    # Multi-metric radar
    st.markdown("<div class='section-label'>Multi-Metric Comparison</div>", unsafe_allow_html=True)
    max_inc = max(t["Avg Incentive (₹)"] for t in TENURE_DATA)
    max_bkg = max(t["Avg Issued Bkgs"] for t in TENURE_DATA)
    max_ape = max(t["Avg Wtd APE (₹L)"] for t in TENURE_DATA)

    fig_rad = go.Figure()
    for i, t in enumerate(TENURE_DATA):
        fig_rad.add_trace(go.Scatterpolar(
            r=[t["Avg Incentive (₹)"]/max_inc,
               t["Avg Issued Bkgs"]/max_bkg,
               t["Avg Wtd APE (₹L)"]/max_ape,
               t["Agents"]/max(d["Agents"] for d in TENURE_DATA),
               t["Avg Incentive (₹)"]/max_inc],
            theta=["Incentive","Issued Bkgs","Wtd APE","Agent Count","Incentive"],
            fill="toself",
            name=t["Tenure Band"],
            line=dict(color=TENURE_PALETTE[i], width=2),
            fillcolor=TENURE_PALETTE[i],
            opacity=0.15,
        ))
    fig_rad.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, showticklabels=False, gridcolor="#e8eef8", linecolor="#dde3ef"),
            angularaxis=dict(tickfont=dict(size=11, color="#6b7fa3", family=FONT_FAMILY), gridcolor="#e8eef8", linecolor="#dde3ef"),
            bgcolor="#ffffff",
        ),
        paper_bgcolor="#ffffff",
        font=dict(family=FONT_FAMILY, color=TEXT_COLOR),
        height=340,
        margin=dict(l=40,r=40,t=16,b=16),
        showlegend=True,
        legend=dict(font=dict(color="#4a5e7a", size=11), bgcolor="rgba(255,255,255,0.8)", bordercolor="#dde3ef", borderwidth=1),
    )
    st.plotly_chart(fig_rad, use_container_width=True)

    st.markdown("<div class='section-label'>Detailed Data Table</div>", unsafe_allow_html=True)
    styled_ten = (
        df_ten.style
        .bar(subset=["Avg Incentive (₹)"], color="#d1fae5", vmin=0)
        .bar(subset=["Avg Issued Bkgs"],   color="#dbeafe", vmin=0)
        .format({"Avg Incentive (₹)":"₹{:,.0f}","Avg Wtd APE (₹L)":"₹{:.2f}L","Avg Issued Bkgs":"{:.2f}"})
        .set_properties(**{"font-size":"12.5px","padding":"10px 14px",
                           "background-color":"#ffffff","color":"#1e293b"})
        .set_table_styles([
            {"selector":"thead th","props":[("background-color","#f8fafd"),("color","#6b7fa3"),
             ("font-size","10px"),("text-transform","uppercase"),("letter-spacing","0.1em"),
             ("padding","10px 14px"),("border-bottom","1px solid #1e2d45"),("font-weight","700")]},
        ])
        .hide(axis="index")
    )
    st.dataframe(styled_ten, use_container_width=True, height=220)


# ════════════════════════════════════════════════════════════════════════
# PAGE 5: MANAGERS
# ════════════════════════════════════════════════════════════════════════
elif page == "👥 Managers":
    st.markdown("""
    <div class='page-header-wrap' style='background:linear-gradient(130deg,#1e1b4b 0%,#4338ca 55%,#6366f1 100%);'>
        <div class='page-header-inner'>
            <div class='page-header-left'>
                <div class='page-title'>Manager Performance</div>
                <div class='page-subtitle'>Team output, average productivity and total incentive by manager.</div>
            </div>
            <div class='page-header-icon'>👥</div>
            <div class='page-header-badge'>🏢 10 Managers</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    df_mgr = pd.DataFrame(MANAGER_DATA).sort_values("Total Incentive (₹L)", ascending=False)

    cl, cr = st.columns(2)
    with cl:
        st.markdown("<div class='section-label'>Total Incentive Payout</div>", unsafe_allow_html=True)
        df_m1 = df_mgr.sort_values("Total Incentive (₹L)", ascending=True)
        fig_m1 = go.Figure(go.Bar(
            x=df_m1["Total Incentive (₹L)"], y=df_m1["Manager"], orientation="h",
            marker=dict(color=df_m1["Total Incentive (₹L)"],
                        colorscale=[[0,"#ede9fe"],[0.5,"#8b5cf6"],[1.0,"#5b21b6"]],
                        line=dict(width=0)),
            text=df_m1["Total Incentive (₹L)"].apply(lambda x: f"₹{x:.1f}L"),
            textposition="outside",
            textfont=dict(color="#4a5e7a", size=10, family=FONT_FAMILY),
        ))
        fig_m1.update_layout(**chart_layout(390, dict(l=0,r=55,t=16,b=0)))
        st.plotly_chart(fig_m1, use_container_width=True)

    with cr:
        st.markdown("<div class='section-label'>Avg Incentive per Agent</div>", unsafe_allow_html=True)
        df_m2 = df_mgr.sort_values("Avg/Agent (₹)", ascending=True)
        fig_m2 = go.Figure(go.Bar(
            x=df_m2["Avg/Agent (₹)"], y=df_m2["Manager"], orientation="h",
            marker=dict(color=df_m2["Avg/Agent (₹)"],
                        colorscale=[[0,"#cffafe"],[0.5,"#22d3ee"],[1.0,"#0891b2"]],
                        line=dict(width=0)),
            text=df_m2["Avg/Agent (₹)"].apply(lambda x: f"₹{x:,.0f}"),
            textposition="outside",
            textfont=dict(color="#4a5e7a", size=10, family=FONT_FAMILY),
        ))
        fig_m2.update_layout(**chart_layout(390, dict(l=0,r=65,t=16,b=0)))
        st.plotly_chart(fig_m2, use_container_width=True)

    # Team size vs bkgs scatter
    st.markdown("<div class='section-label'>Team Size vs Bookings Issued</div>", unsafe_allow_html=True)
    fig_ms = px.scatter(
        df_mgr, x="Team", y="Bkgs Issued",
        size="Total Incentive (₹L)", color="Avg/Agent (₹)",
        color_continuous_scale=[[0,"#1e0a3c"],[0.5,"#8b5cf6"],[1.0,"#c4b5fd"]],
        text="Manager", size_max=48,
    )
    fig_ms.update_traces(textposition="top center",
                         textfont=dict(size=9.5, color="#4a5e7a", family=FONT_FAMILY),
                         marker=dict(line=dict(width=1, color="#0d1117")))
    layout_ms = chart_layout(320, dict(l=0,r=0,t=16,b=0))
    layout_ms["coloraxis_showscale"] = False
    fig_ms.update_layout(**layout_ms)
    st.plotly_chart(fig_ms, use_container_width=True)

    st.markdown("<div class='section-label'>Manager Leaderboard</div>", unsafe_allow_html=True)
    styled_mgr = (
        df_mgr.style
        .bar(subset=["Total Incentive (₹L)"], color="#ede9fe", vmin=0)
        .bar(subset=["Avg/Agent (₹)"],        color="#cffafe", vmin=0)
        .format({"Total Incentive (₹L)":"₹{:.2f}L","Avg/Agent (₹)":"₹{:,.0f}","Bkgs Issued":"{:,.0f}"})
        .set_properties(**{"font-size":"12.5px","padding":"10px 14px",
                           "background-color":"#ffffff","color":"#1e293b"})
        .set_table_styles([
            {"selector":"thead th","props":[("background-color","#f8fafd"),("color","#6b7fa3"),
             ("font-size","10px"),("text-transform","uppercase"),("letter-spacing","0.1em"),
             ("padding","10px 14px"),("border-bottom","1px solid #1e2d45"),("font-weight","700")]},
            {"selector":"tbody tr:hover td","props":[("background-color","#eff6ff")]},
        ])
        .hide(axis="index")
    )
    st.dataframe(styled_mgr, use_container_width=True, height=420)


# ════════════════════════════════════════════════════════════════════════
# PAGE 6: AI CHATBOT
# ════════════════════════════════════════════════════════════════════════
elif page == "🤖 AI Chatbot":
    st.markdown("""
    <div class='page-header-wrap' style='background:linear-gradient(130deg,#0f172a 0%,#1e3a5f 40%,#0891b2 100%);'>
        <div class='page-header-inner'>
            <div class='page-header-left'>
                <div class='page-title'>AI Analytics Assistant</div>
                <div class='page-subtitle'>Ask anything about the agent data in plain English — powered by Claude.</div>
            </div>
            <div class='page-header-icon'>🤖</div>
            <div class='page-header-badge'>⚡ Powered by Claude</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not api_key:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#eff6ff,#dbeafe);border:1px solid #bfdbfe;border-left:3px solid #2563eb;
                    border-radius:12px;padding:20px 22px;margin-bottom:20px;'>
            <div style='font-size:13px;color:#1e40af;line-height:1.7;'>
                👈 &nbsp;Enter your <span style='color:#1d4ed8;font-weight:600;'>Anthropic API key</span> in the sidebar to activate the chatbot.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='section-label'>Example Questions</div>", unsafe_allow_html=True)
        for q in [
            "Who are the top 5 performers and what made them stand out?",
            "Which process group has the best average incentive per agent?",
            "How does tenure affect performance? Give me a full summary.",
            "Which manager leads the most productive team?",
            "What percentage of agents had zero issuance this month?",
        ]:
            st.markdown(f"""
            <div style='background:#ffffff;border:1px solid #dde3ef;border-radius:10px;box-shadow:0 1px 4px rgba(15,28,46,0.06);
                        padding:11px 16px;margin-bottom:8px;font-size:13px;color:#4a5e7a;'>
                💬 &nbsp;{q}
            </div>""", unsafe_allow_html=True)

    else:
        # Quick prompts
        st.markdown("<div class='section-label'>Quick Prompts</div>", unsafe_allow_html=True)
        suggested = [
            "Who are the top 5 performers?",
            "Which process earns most per agent?",
            "How does tenure affect incentives?",
            "Best manager by team output?",
            "What is the issuance rate?",
            "Agents with zero bookings?",
        ]
        c1, c2, c3 = st.columns(3)
        for i, s in enumerate(suggested):
            col = [c1, c2, c3][i % 3]
            if col.button(s, key=f"sug_{i}", use_container_width=True):
                if "messages" not in st.session_state:
                    st.session_state.messages = []
                st.session_state.messages.append({"role":"user","content":s})
                st.rerun()

        st.markdown("<div style='margin:10px 0;'></div>", unsafe_allow_html=True)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"], avatar="⚡" if msg["role"] == "assistant" else "👤"):
                st.markdown(msg["content"])

        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            with st.chat_message("assistant", avatar="⚡"):
                with st.spinner("Thinking…"):
                    try:
                        client = anthropic.Anthropic(api_key=api_key)
                        resp = client.messages.create(
                            model="claude-sonnet-4-20250514",
                            max_tokens=1000,
                            system=SYSTEM_PROMPT,
                            messages=st.session_state.messages,
                        )
                        reply = resp.content[0].text
                    except Exception as e:
                        reply = f"⚠️ Error: {str(e)}"
                    st.markdown(reply)
                    st.session_state.messages.append({"role":"assistant","content":reply})

        if prompt := st.chat_input("Ask about agents, processes, incentives, tenure…"):
            st.session_state.messages.append({"role":"user","content":prompt})
            st.rerun()

        if st.session_state.messages:
            if st.button("🗑️ Clear chat history", key="clear"):
                st.session_state.messages = []
                st.rerun()
