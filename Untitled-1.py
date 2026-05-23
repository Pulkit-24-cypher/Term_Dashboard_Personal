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


/* ── Root variables ── */
:root {
    --bg-base:       #080b12;
    --bg-card:       #0d1117;
    --bg-card2:      #111827;
    --bg-hover:      #1a2235;
    --border:        #1e2d45;
    --border-bright: #2a3f5f;
    --text-primary:  #e8edf5;
    --text-secondary:#6b7fa3;
    --text-muted:    #3d4f6a;
    --accent-blue:   #3b82f6;
    --accent-cyan:   #06b6d4;
    --accent-green:  #10b981;
    --accent-amber:  #f59e0b;
    --accent-rose:   #f43f5e;
    --accent-violet: #8b5cf6;
}

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
}

.main { background-color: var(--bg-base) !important; }
.block-container { padding: 1.5rem 2rem 2rem !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #060910 !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div { padding-top: 0 !important; }
[data-testid="stSidebar"] * { color: var(--text-secondary) !important; }
[data-testid="stSidebar"] .stRadio > label { display: none; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap: 2px; display: flex; flex-direction: column; }
[data-testid="stSidebar"] .stRadio label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
    padding: 9px 14px !important;
    border-radius: 8px !important;
    transition: all 0.15s !important;
    border: 1px solid transparent !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: var(--bg-hover) !important;
    color: var(--text-primary) !important;
}
[data-testid="stSidebar"] .stRadio [aria-checked="true"] ~ div,
[data-testid="stSidebar"] .stRadio [data-checked="true"] ~ div {
    color: #fff !important;
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 20px 22px !important;
    position: relative;
    overflow: hidden;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.02em !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}
[data-testid="stMetricDelta"] {
    font-size: 0.75rem !important;
    font-weight: 500 !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 14px !important;
    overflow: hidden !important;
    border: 1px solid var(--border) !important;
    background: var(--bg-card) !important;
}
[data-testid="stDataFrame"] iframe { background: transparent !important; }

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    margin-bottom: 10px !important;
}

/* ── Inputs ── */
.stTextInput input, .stChatInput textarea {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput input:focus, .stChatInput textarea:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.15) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 1px dashed var(--border-bright) !important;
    border-radius: 12px !important;
    padding: 12px !important;
}

/* ── Buttons ── */
.stButton button {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-secondary) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 12.5px !important;
    transition: all 0.15s !important;
}
.stButton button:hover {
    border-color: var(--accent-blue) !important;
    color: var(--accent-blue) !important;
    background: rgba(59,130,246,0.07) !important;
}

/* ── Dividers ── */
hr { border-color: var(--border) !important; margin: 16px 0 !important; }

/* ── Success/info alerts ── */
.stSuccess, .stInfo {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

/* ── Hide branding ── */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: visible; }

/* ── Custom classes ── */
.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 26px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.02em;
    margin: 0 0 4px;
}
.page-subtitle {
    font-size: 13.5px;
    color: var(--text-secondary);
    margin-bottom: 28px;
    font-weight: 400;
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
}
.nav-section-label {
    font-size: 9.5px;
    font-weight: 700;
    color: #2a3f5f;
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
      chart.style.transition = 'transform 0.25s ease, box-shadow 0.25s ease';
      chart.addEventListener('mouseenter', () => {
        chart.style.transform = 'translateY(-2px)';
        chart.style.boxShadow = '0 16px 48px rgba(0,0,0,0.5), 0 0 0 1px rgba(59,130,246,0.1)';
      });
      chart.addEventListener('mouseleave', () => {
        chart.style.transform = 'translateY(0)';
        chart.style.boxShadow = 'none';
      });
    }
  });

})();
</script>
""", unsafe_allow_html=True)


# ── Chart theme ────────────────────────────────────────────────────────────────
CHART_BG    = "#0d1117"
GRID_COLOR  = "#1a2540"
TEXT_COLOR  = "#6b7fa3"
FONT_FAMILY = "DM Sans"

def chart_layout(height=360, margin=None):
    if margin is None:
        margin = dict(l=0, r=24, t=16, b=0)
    return dict(
        height=height,
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        font=dict(family=FONT_FAMILY, color=TEXT_COLOR, size=11),
        margin=margin,
        showlegend=False,
        xaxis=dict(showgrid=True, gridcolor=GRID_COLOR, zeroline=False,
                   tickfont=dict(color=TEXT_COLOR, size=10.5), linecolor=GRID_COLOR),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, zeroline=False,
                   tickfont=dict(color=TEXT_COLOR, size=10.5), linecolor=GRID_COLOR),
    )


# ── Palette pools ──────────────────────────────────────────────────────────────
BLUE_SCALE   = ["#0f2a4a", "#1d4ed8", "#3b82f6", "#7dd3fc"]
VIOLET_SCALE = ["#1e0a3c", "#6d28d9", "#8b5cf6", "#c4b5fd"]
GREEN_SCALE  = ["#052e1a", "#065f46", "#10b981", "#6ee7b7"]
AMBER_SCALE  = ["#2d1a00", "#b45309", "#f59e0b", "#fde68a"]
CYAN_SCALE   = ["#011f2d", "#0e7490", "#06b6d4", "#a5f3fc"]
ROSE_SCALE   = ["#2d0014", "#be123c", "#f43f5e", "#fda4af"]
PROC_COLORS  = ["#3b82f6","#06b6d4","#10b981","#f59e0b","#8b5cf6","#f43f5e","#22d3ee","#a3e635","#fb923c","#e879f9"]


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
    <div style='padding:20px 16px 10px;border-bottom:1px solid #1e2d45;margin-bottom:8px;'>
        <div style='display:flex;align-items:center;gap:10px;'>
            <div style='width:36px;height:36px;border-radius:10px;
                        background:linear-gradient(135deg,#3b82f6 0%,#8b5cf6 100%);
                        display:flex;align-items:center;justify-content:center;font-size:18px;'>⚡</div>
            <div>
                <div style='font-family:Syne,sans-serif;font-weight:800;font-size:15px;color:#e8edf5;letter-spacing:-0.01em;'>AgentIQ</div>
                <div style='font-size:10px;color:#3d4f6a;letter-spacing:0.08em;text-transform:uppercase;'>Analytics Platform</div>
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
        <div style='font-size:10px;color:#2a3f5f;line-height:1.6;'>
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
    st.markdown("<div class='page-title'>⚡ Performance Overview</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Real-time KPIs across 1,877 agents — incentives, conversions & APE.</div>", unsafe_allow_html=True)

    # ── KPI Row 1 ──
    c1, c2, c3, c4 = st.columns(4)
    kpis = [
        (c1, "Total Agents",    f"{summary['total_agents']:,}",         f"▲ {summary['active']:,} active",      "#3b82f6"),
        (c2, "Total Incentive", fmt_inr(summary['total_incentive']),    f"avg {fmt_inr(summary['avg_incentive'])}", "#10b981"),
        (c3, "Issuance Rate",   f"{summary['issuance_rate_pct']}%",     f"{summary['total_issued_bkgs']:,.0f} converted", "#f59e0b"),
        (c4, "APE Conversion",  f"{summary['ape_conversion_pct']}%",    fmt_inr(summary['total_issued_ape']),   "#8b5cf6"),
    ]
    for col, label, val, delta, _ in kpis:
        col.metric(label, val, delta)

    st.markdown("<div style='margin:6px 0;'></div>", unsafe_allow_html=True)
    c5, c6, c7, c8 = st.columns(4)
    kpis2 = [
        (c5, "Active Agents",      f"{summary['active']:,}",                      f"▼ {summary['inactive']} inactive"),
        (c6, "Source APE",         fmt_inr(summary['total_source_ape']),           "total sourced"),
        (c7, "Issued APE",         fmt_inr(summary['total_issued_ape']),           "successfully issued"),
        (c8, "Zero-Issuance",      str(summary['zero_issuance_agents']),           "agents with 0 bkgs"),
    ]
    for col, label, val, delta in kpis2:
        col.metric(label, val, delta)

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
                colorscale=[[0, "#0f2a4a"], [0.4, "#1d4ed8"], [1.0, "#06b6d4"]],
                line=dict(width=0),
            ),
            text=proc_df["Total Incentive (₹L)"].apply(lambda x: f"₹{x:.1f}L"),
            textposition="outside",
            textfont=dict(color="#6b7fa3", size=10.5, family=FONT_FAMILY),
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
            marker=dict(colors=["#3b82f6", "#1e2d45"], line=dict(color="#0d1117", width=3)),
            textfont=dict(color="#e8edf5", size=12, family=FONT_FAMILY),
            textinfo="percent+label",
        ))
        fig_donut.add_annotation(
            text=f"<b>{summary['total_agents']:,}</b>",
            x=0.5, y=0.5, font=dict(size=22, color="#e8edf5", family="Syne"),
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
            textfont=dict(color="#6b7fa3", size=10, family=FONT_FAMILY),
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
    st.markdown("<div class='page-title'>🏆 Top Agents Leaderboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Ranked by final incentive payout — this month's star performers.</div>", unsafe_allow_html=True)

    # Podium top 3
    st.markdown("<div class='section-label'>Podium — Top 3</div>", unsafe_allow_html=True)
    p1, p2, p3 = st.columns(3)
    podium = [
        (p1, TOP_AGENTS_DATA[0], "🥇", "linear-gradient(135deg,#1a0f00,#2d1900)", "#f59e0b", "#fde68a"),
        (p2, TOP_AGENTS_DATA[1], "🥈", "linear-gradient(135deg,#0a0f1a,#111827)", "#94a3b8", "#e2e8f0"),
        (p3, TOP_AGENTS_DATA[2], "🥉", "linear-gradient(135deg,#160c03,#221104)", "#f97316", "#fed7aa"),
    ]
    for col, agent, medal, bg, accent, border in podium:
        with col:
            st.markdown(f"""
            <div style='background:{bg};border:1px solid {border}33;border-top:3px solid {accent};
                        border-radius:16px;padding:22px 18px 18px;text-align:center;'>
                <div style='font-size:32px;margin-bottom:10px;'>{medal}</div>
                <div style='font-family:Syne,sans-serif;font-weight:800;font-size:14.5px;color:#e8edf5;line-height:1.3;margin-bottom:4px;'>{agent['Agent']}</div>
                <div style='font-size:11px;color:#6b7fa3;margin-bottom:14px;'>{agent['Process']}</div>
                <div style='font-size:24px;font-weight:800;font-family:Syne,sans-serif;color:{accent};letter-spacing:-0.02em;'>₹{agent['Incentive (₹L)']:.2f}L</div>
                <div style='font-size:10.5px;color:#3d4f6a;margin-top:6px;'>
                    APE ₹{agent['Issued APE (₹L)']:.2f}L &nbsp;·&nbsp; {agent['Issued Bkgs']:.1f} bkgs
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Leaderboard table
    st.markdown("<div class='section-label'>Full Leaderboard — Top 10</div>", unsafe_allow_html=True)
    df_agents = pd.DataFrame(TOP_AGENTS_DATA)

    def hl_top(row):
        colors = {"🥇":"background-color:#1a0f00;color:#fde68a;font-weight:700",
                  "🥈":"background-color:#0f1521;color:#e2e8f0;font-weight:700",
                  "🥉":"background-color:#160c03;color:#fed7aa;font-weight:700"}
        style = colors.get(row["Rank"], "color:#6b7fa3")
        return [style]*len(row)

    styled = (
        df_agents.style
        .apply(hl_top, axis=1)
        .bar(subset=["Incentive (₹L)"], color="#1a3a1a", vmin=0)
        .bar(subset=["Issued APE (₹L)"], color="#0f1f3a", vmin=0)
        .format({"Issued Bkgs":"{:.1f}","Incentive (₹L)":"₹{:.2f}L","Issued APE (₹L)":"₹{:.2f}L"})
        .set_properties(**{"font-size":"12.5px","padding":"10px 14px",
                           "background-color":"#0d1117","color":"#a8b8d0"})
        .set_table_styles([
            {"selector":"thead th","props":[("background-color","#060910"),("color","#3d4f6a"),
             ("font-size","10px"),("text-transform","uppercase"),("letter-spacing","0.1em"),
             ("padding","10px 14px"),("border-bottom","1px solid #1e2d45"),("font-weight","700")]},
            {"selector":"tbody tr:hover td","props":[("background-color","#111827")]},
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
                         textfont=dict(size=9.5, color="#6b7fa3", family=FONT_FAMILY),
                         marker=dict(line=dict(width=1, color="#0d1117")))
    layout = chart_layout(320, dict(l=0,r=0,t=16,b=0))
    layout["coloraxis_showscale"] = False
    fig_sc.update_layout(**layout)
    st.plotly_chart(fig_sc, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════
# PAGE 3: BY PROCESS
# ════════════════════════════════════════════════════════════════════════
elif page == "📊 By Process":
    st.markdown("<div class='page-title'>📊 Process Group Performance</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Incentive payout, bookings and APE broken down by sales channel.</div>", unsafe_allow_html=True)

    df_proc = pd.DataFrame(PROCESS_DATA)
    df_asc  = df_proc.sort_values("Avg Incentive (₹)", ascending=True)
    df_bk   = df_proc.sort_values("Avg Issued Bkgs", ascending=True)

    cl, cr = st.columns(2)
    with cl:
        st.markdown("<div class='section-label'>Avg Incentive per Agent</div>", unsafe_allow_html=True)
        fig1 = go.Figure(go.Bar(
            x=df_asc["Avg Incentive (₹)"], y=df_asc["Process Group"], orientation="h",
            marker=dict(color=df_asc["Avg Incentive (₹)"],
                        colorscale=[[0,"#1e0a3c"],[0.5,"#6d28d9"],[1.0,"#c4b5fd"]],
                        line=dict(width=0)),
            text=df_asc["Avg Incentive (₹)"].apply(lambda x: f"₹{x:,.0f}"),
            textposition="outside",
            textfont=dict(color="#6b7fa3", size=10, family=FONT_FAMILY),
        ))
        fig1.update_layout(**chart_layout(360, dict(l=0,r=60,t=16,b=0)))
        st.plotly_chart(fig1, use_container_width=True)

    with cr:
        st.markdown("<div class='section-label'>Avg Issued Bookings per Agent</div>", unsafe_allow_html=True)
        fig2 = go.Figure(go.Bar(
            x=df_bk["Avg Issued Bkgs"], y=df_bk["Process Group"], orientation="h",
            marker=dict(color=df_bk["Avg Issued Bkgs"],
                        colorscale=[[0,"#052e1a"],[0.5,"#065f46"],[1.0,"#6ee7b7"]],
                        line=dict(width=0)),
            text=df_bk["Avg Issued Bkgs"].apply(lambda x: f"{x:.1f}"),
            textposition="outside",
            textfont=dict(color="#6b7fa3", size=10, family=FONT_FAMILY),
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
        textfont=dict(color="#6b7fa3", size=10.5, family=FONT_FAMILY),
    ))
    fig3.update_layout(**chart_layout(280, dict(l=0,r=0,t=16,b=0)))
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("<div class='section-label'>Full Data Table</div>", unsafe_allow_html=True)
    styled_proc = (
        df_proc.style
        .bar(subset=["Total Incentive (₹L)"], color="#0f1f3a", vmin=0)
        .bar(subset=["Avg Wtd APE (₹L)"],     color="#052e1a", vmin=0)
        .format({"Avg Incentive (₹)":"₹{:,.0f}","Total Incentive (₹L)":"₹{:.2f}L",
                 "Avg Wtd APE (₹L)":"₹{:.2f}L","Avg Issued Bkgs":"{:.1f}"})
        .set_properties(**{"font-size":"12.5px","padding":"10px 14px",
                           "background-color":"#0d1117","color":"#a8b8d0"})
        .set_table_styles([
            {"selector":"thead th","props":[("background-color","#060910"),("color","#3d4f6a"),
             ("font-size","10px"),("text-transform","uppercase"),("letter-spacing","0.1em"),
             ("padding","10px 14px"),("border-bottom","1px solid #1e2d45"),("font-weight","700")]},
            {"selector":"tbody tr:hover td","props":[("background-color","#111827")]},
        ])
        .hide(axis="index")
    )
    st.dataframe(styled_proc, use_container_width=True, height=400)


# ════════════════════════════════════════════════════════════════════════
# PAGE 4: BY TENURE
# ════════════════════════════════════════════════════════════════════════
elif page == "🕐 By Tenure":
    st.markdown("<div class='page-title'>🕐 Tenure-Based Performance</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>How agent experience (AON) shapes incentives, bookings and APE.</div>", unsafe_allow_html=True)

    # Tenure KPI cards
    st.markdown("<div class='section-label'>Avg Incentive by Tenure Band</div>", unsafe_allow_html=True)
    cols = st.columns(4)
    for i, (col, t) in enumerate(zip(cols, TENURE_DATA)):
        c = TENURE_PALETTE[i]
        col.markdown(f"""
        <div style='background:#0d1117;border:1px solid #1e2d45;border-top:3px solid {c};
                    border-radius:14px;padding:18px 16px;'>
            <div style='font-size:9.5px;font-weight:700;color:{c};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;'>{t['Tenure Band']}</div>
            <div style='font-family:Syne,sans-serif;font-size:22px;font-weight:700;color:#e8edf5;letter-spacing:-0.02em;'>₹{t['Avg Incentive (₹)']:,}</div>
            <div style='font-size:10.5px;color:#3d4f6a;margin:4px 0 10px;'>avg incentive / agent</div>
            <div style='height:3px;background:#1e2d45;border-radius:99px;'>
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
            textfont=dict(color="#6b7fa3", size=10, family=FONT_FAMILY),
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
            textfont=dict(color="#6b7fa3", size=10, family=FONT_FAMILY),
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
            radialaxis=dict(visible=True, showticklabels=False, gridcolor="#1e2d45", linecolor="#1e2d45"),
            angularaxis=dict(tickfont=dict(size=11, color="#6b7fa3", family=FONT_FAMILY), gridcolor="#1e2d45", linecolor="#1e2d45"),
            bgcolor=CHART_BG,
        ),
        paper_bgcolor=CHART_BG,
        font=dict(family=FONT_FAMILY, color=TEXT_COLOR),
        height=340,
        margin=dict(l=40,r=40,t=16,b=16),
        showlegend=True,
        legend=dict(font=dict(color="#6b7fa3", size=11), bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig_rad, use_container_width=True)

    st.markdown("<div class='section-label'>Detailed Data Table</div>", unsafe_allow_html=True)
    styled_ten = (
        df_ten.style
        .bar(subset=["Avg Incentive (₹)"], color="#1a3a1a", vmin=0)
        .bar(subset=["Avg Issued Bkgs"],   color="#0f1f3a", vmin=0)
        .format({"Avg Incentive (₹)":"₹{:,.0f}","Avg Wtd APE (₹L)":"₹{:.2f}L","Avg Issued Bkgs":"{:.2f}"})
        .set_properties(**{"font-size":"12.5px","padding":"10px 14px",
                           "background-color":"#0d1117","color":"#a8b8d0"})
        .set_table_styles([
            {"selector":"thead th","props":[("background-color","#060910"),("color","#3d4f6a"),
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
    st.markdown("<div class='page-title'>👥 Manager Performance</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Team output, average productivity and total incentive by manager.</div>", unsafe_allow_html=True)

    df_mgr = pd.DataFrame(MANAGER_DATA).sort_values("Total Incentive (₹L)", ascending=False)

    cl, cr = st.columns(2)
    with cl:
        st.markdown("<div class='section-label'>Total Incentive Payout</div>", unsafe_allow_html=True)
        df_m1 = df_mgr.sort_values("Total Incentive (₹L)", ascending=True)
        fig_m1 = go.Figure(go.Bar(
            x=df_m1["Total Incentive (₹L)"], y=df_m1["Manager"], orientation="h",
            marker=dict(color=df_m1["Total Incentive (₹L)"],
                        colorscale=[[0,"#1e0a3c"],[0.5,"#6d28d9"],[1.0,"#c4b5fd"]],
                        line=dict(width=0)),
            text=df_m1["Total Incentive (₹L)"].apply(lambda x: f"₹{x:.1f}L"),
            textposition="outside",
            textfont=dict(color="#6b7fa3", size=10, family=FONT_FAMILY),
        ))
        fig_m1.update_layout(**chart_layout(390, dict(l=0,r=55,t=16,b=0)))
        st.plotly_chart(fig_m1, use_container_width=True)

    with cr:
        st.markdown("<div class='section-label'>Avg Incentive per Agent</div>", unsafe_allow_html=True)
        df_m2 = df_mgr.sort_values("Avg/Agent (₹)", ascending=True)
        fig_m2 = go.Figure(go.Bar(
            x=df_m2["Avg/Agent (₹)"], y=df_m2["Manager"], orientation="h",
            marker=dict(color=df_m2["Avg/Agent (₹)"],
                        colorscale=[[0,"#011f2d"],[0.5,"#0e7490"],[1.0,"#06b6d4"]],
                        line=dict(width=0)),
            text=df_m2["Avg/Agent (₹)"].apply(lambda x: f"₹{x:,.0f}"),
            textposition="outside",
            textfont=dict(color="#6b7fa3", size=10, family=FONT_FAMILY),
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
                         textfont=dict(size=9.5, color="#6b7fa3", family=FONT_FAMILY),
                         marker=dict(line=dict(width=1, color="#0d1117")))
    layout_ms = chart_layout(320, dict(l=0,r=0,t=16,b=0))
    layout_ms["coloraxis_showscale"] = False
    fig_ms.update_layout(**layout_ms)
    st.plotly_chart(fig_ms, use_container_width=True)

    st.markdown("<div class='section-label'>Manager Leaderboard</div>", unsafe_allow_html=True)
    styled_mgr = (
        df_mgr.style
        .bar(subset=["Total Incentive (₹L)"], color="#1e0a3c", vmin=0)
        .bar(subset=["Avg/Agent (₹)"],        color="#011f2d", vmin=0)
        .format({"Total Incentive (₹L)":"₹{:.2f}L","Avg/Agent (₹)":"₹{:,.0f}","Bkgs Issued":"{:,.0f}"})
        .set_properties(**{"font-size":"12.5px","padding":"10px 14px",
                           "background-color":"#0d1117","color":"#a8b8d0"})
        .set_table_styles([
            {"selector":"thead th","props":[("background-color","#060910"),("color","#3d4f6a"),
             ("font-size","10px"),("text-transform","uppercase"),("letter-spacing","0.1em"),
             ("padding","10px 14px"),("border-bottom","1px solid #1e2d45"),("font-weight","700")]},
            {"selector":"tbody tr:hover td","props":[("background-color","#111827")]},
        ])
        .hide(axis="index")
    )
    st.dataframe(styled_mgr, use_container_width=True, height=420)


# ════════════════════════════════════════════════════════════════════════
# PAGE 6: AI CHATBOT
# ════════════════════════════════════════════════════════════════════════
elif page == "🤖 AI Chatbot":
    st.markdown("<div class='page-title'>🤖 AI Analytics Assistant</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Ask anything about the agent data in plain English — powered by Claude.</div>", unsafe_allow_html=True)

    if not api_key:
        st.markdown("""
        <div style='background:#0d1117;border:1px solid #1e2d45;border-left:3px solid #3b82f6;
                    border-radius:12px;padding:20px 22px;margin-bottom:20px;'>
            <div style='font-size:13px;color:#6b7fa3;line-height:1.7;'>
                👈 &nbsp;Enter your <span style='color:#3b82f6;font-weight:600;'>Anthropic API key</span> in the sidebar to activate the chatbot.
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
            <div style='background:#0d1117;border:1px solid #1e2d45;border-radius:10px;
                        padding:11px 16px;margin-bottom:8px;font-size:13px;color:#6b7fa3;'>
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