"""Visual system for the Bike Sharing Demand app.

Night-shift mobility intelligence: deep petrol surfaces, mint signal light,
warm amber data accents, editorial type and machined double-bezel cards.
No extra dependencies beyond Streamlit — everything is injected as CSS/HTML.
"""

from __future__ import annotations

import html as _html

import streamlit as st


# ---------------------------------------------------------------------------
# Palette / tokens
# ---------------------------------------------------------------------------
BG = "#06141B"
SURFACE = "#0C222C"
MINT = "#6DF2C0"
AMBER = "#FFC46B"
CORAL = "#FF9A86"
INK = "#E9F5F1"
MUTED = "#8FA9AB"


CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root{
  --bg:#06141B; --bg-deep:#040F16; --surface:#0C222C; --surface-2:#102C37;
  --line:rgba(170,232,218,.14); --line-strong:rgba(170,232,218,.28);
  --ink:#E9F5F1; --muted:#8FA9AB; --mint:#6DF2C0; --amber:#FFC46B; --coral:#FF9A86;
  --ease:cubic-bezier(.22,1,.36,1);
}

/* ---------- Canvas ---------- */
html,body,[class*="st-emotion-cache"]{font-family:'Plus Jakarta Sans',system-ui,sans-serif !important;}
body{background:var(--bg-deep) !important;}
[data-testid="stAppViewContainer"]{
  background:
    radial-gradient(900px 520px at 88% -8%, rgba(109,242,192,.12), transparent 68%),
    radial-gradient(760px 460px at -8% 12%, rgba(255,196,107,.07), transparent 66%),
    linear-gradient(180deg,#07171F 0%,#05121A 55%,#040E15 100%) !important;
}
[data-testid="stAppViewContainer"]::before{
  content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
  background-image:linear-gradient(rgba(255,255,255,.014) 1px,transparent 1px),
                   linear-gradient(90deg,rgba(255,255,255,.014) 1px,transparent 1px);
  background-size:48px 48px;
  -webkit-mask-image:linear-gradient(to bottom,rgba(0,0,0,.8),transparent 72%);
  mask-image:linear-gradient(to bottom,rgba(0,0,0,.8),transparent 72%);
}
[data-testid="stHeader"]{background:transparent !important;}
[data-testid="stHeader"]::before{content:none;}
[data-testid="stMainBlockContainer"]{padding:2.6rem 3.6rem 8rem !important;max-width:1480px;}
[data-testid="stMain"]{position:relative;z-index:1;}

/* ---------- Sidebar rail ---------- */
[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#0B202A 0%,#081A22 62%,#06141B 100%) !important;
  border-right:1px solid var(--line) !important;
}
[data-testid="stSidebar"] > div:first-child{padding:1.6rem 1.1rem 2rem !important;}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p{color:var(--muted);}
[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3{color:var(--ink) !important;font-family:'Space Grotesk',sans-serif !important;}

/* Sidebar nav as pills */
[data-testid="stSidebar"] [data-testid="stRadio"] [data-testid="stWidgetLabel"]{display:none !important;}
[data-testid="stSidebar"] [data-testid="stRadioGroup"]{gap:.35rem !important;}
[data-testid="stSidebar"] [data-testid="stRadioOption"]{
  border-radius:14px !important;padding:.2rem !important;
  background:rgba(255,255,255,.025) !important;
  border:1px solid transparent !important;
  transition:transform .55s var(--ease),background .55s var(--ease),border-color .55s var(--ease) !important;
}
[data-testid="stSidebar"] [data-testid="stRadioOption"]:hover{transform:translateX(3px) !important;background:rgba(109,242,192,.07) !important;}
[data-testid="stSidebar"] [data-testid="stRadioOption"][data-selected="true"]{
  background:linear-gradient(110deg,rgba(109,242,192,.16),rgba(109,242,192,.05)) !important;
  border-color:rgba(109,242,192,.35) !important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.07),0 10px 30px -18px rgba(109,242,192,.6) !important;
}
[data-testid="stSidebar"] [data-testid="stRadioOption"] p{color:var(--ink) !important;font-weight:600 !important;font-size:.9rem !important;letter-spacing:-.01em;}
[data-testid="stSidebar"] [data-testid="stRadioOption"] div[class*="ex50key4"]{background:transparent !important;}
[data-testid="stSidebar"] [data-testid="stRadioOption"] div[class*="ex50key5"]{background:var(--mint) !important;box-shadow:0 0 12px rgba(109,242,192,.7) !important;}

/* ---------- Typography ---------- */
h1,h2,h3,h4,h5,h6,[data-testid="stHeading"]{font-family:'Space Grotesk',sans-serif !important;color:var(--ink) !important;letter-spacing:-.035em !important;}
h1{font-size:2.75rem !important;font-weight:600 !important;line-height:1.04 !important;}
h2{font-size:1.7rem !important;font-weight:600 !important;line-height:1.1 !important;}
h3{font-size:1.12rem !important;font-weight:600 !important;line-height:1.2 !important;}
p,label,span,div{color:var(--ink);}
[data-testid="stCaptionContainer"] p,[data-testid="stCaptionContainer"] span{color:var(--muted) !important;font-size:.78rem !important;letter-spacing:.01em;}
[data-testid="stMarkdownContainer"] p{line-height:1.65;}
.st-emotion-cache-1y4e5oc p, [data-testid="stWidgetLabel"] p{color:var(--muted) !important;font-size:.78rem !important;font-weight:600 !important;letter-spacing:.02em;}
hr,[data-testid="stDivider"]{border-color:var(--line) !important;opacity:1 !important;}

/* ---------- Cards: double-bezel shells ---------- */
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"]{
  background:linear-gradient(155deg,rgba(20,48,59,.88),rgba(9,27,36,.94)) !important;
  border:1px solid var(--line) !important;
  border-radius:26px !important;
  padding:24px 26px !important;
  box-shadow:0 26px 60px -34px rgba(0,0,0,.8),inset 0 1px 0 rgba(255,255,255,.06) !important;
  transition:border-color .7s var(--ease),transform .7s var(--ease) !important;
}
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"]:hover{border-color:var(--line-strong) !important;transform:translateY(-2px) !important;}
[data-testid="stHorizontalBlock"]{gap:1.15rem !important;}

/* ---------- Buttons ---------- */
[data-testid="stButton"] button,[data-testid="stDownloadButton"] button{
  border-radius:999px !important;padding:.62rem 1.25rem !important;
  border:1px solid var(--line) !important;
  background:rgba(255,255,255,.035) !important;color:var(--ink) !important;
  font-weight:600 !important;font-size:.84rem !important;letter-spacing:-.01em !important;
  transition:transform .55s var(--ease),background .55s var(--ease),border-color .55s var(--ease),box-shadow .55s var(--ease) !important;
}
[data-testid="stButton"] button:hover,[data-testid="stDownloadButton"] button:hover{
  transform:translateY(-2px) scale(.985) !important;
  border-color:rgba(109,242,192,.45) !important;
  background:rgba(109,242,192,.1) !important;
  box-shadow:0 16px 34px -20px rgba(109,242,192,.65) !important;
}
[data-testid="stButton"] button[kind="primary"],[data-testid="stDownloadButton"] button[kind="primary"]{
  background:linear-gradient(115deg,var(--mint),#48D9AC) !important;color:#04231B !important;border-color:transparent !important;
}
[data-testid="stButton"] button[kind="primary"]:hover,[data-testid="stDownloadButton"] button[kind="primary"]:hover{
  background:linear-gradient(115deg,#8CF8D0,var(--mint)) !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] button{width:100% !important;padding:.55rem .8rem !important;font-size:.78rem !important;}

/* Segmented controls */
[data-testid="stButtonGroup"] {background:rgba(255,255,255,.04) !important;border:1px solid var(--line) !important;border-radius:999px !important;padding:4px !important;gap:4px !important;}
[data-testid="stButtonGroup"] button{border-radius:999px !important;padding:.38rem .9rem !important;background:transparent !important;border:1px solid transparent !important;color:var(--muted) !important;box-shadow:none !important;}
[data-testid="stButtonGroup"] button[aria-pressed="true"],[data-testid="stButtonGroup"] button[aria-checked="true"]{
  background:var(--mint) !important;color:#05251C !important;box-shadow:0 8px 22px -12px rgba(109,242,192,.8) !important;
}

/* ---------- Inputs ---------- */
[data-testid="stTextInput"] input,[data-testid="stNumberInput"] input,[data-testid="stDateInput"] input{
  background:rgba(255,255,255,.04) !important;border:1px solid var(--line) !important;color:var(--ink) !important;border-radius:12px !important;
}
[data-baseweb="select"] > div{
  background:rgba(255,255,255,.04) !important;border:1px solid var(--line) !important;border-radius:12px !important;color:var(--ink) !important;
}
[data-baseweb="select"] input{color:var(--ink) !important;}
[data-testid="stSlider"] [data-testid="stSliderThumbValue"]{background:var(--mint) !important;color:#04231B !important;font-family:'Space Grotesk',sans-serif !important;font-weight:700 !important;}
[data-testid="stSlider"] [role="slider"]{box-shadow:0 0 0 4px rgba(109,242,192,.18) !important;}
[data-testid="stToggle"] [data-testid="stToggle"]{}

/* ---------- Alerts / metrics ---------- */
[data-testid="stAlertContainer"]{
  background:rgba(109,242,192,.06) !important;border:1px solid rgba(109,242,192,.22) !important;
  border-left:3px solid var(--mint) !important;border-radius:14px !important;color:var(--ink) !important;
}
[data-testid="stAlertContainer"] p{color:var(--ink) !important;font-size:.86rem !important;}
[data-testid="stAlertContentInfo"]{background:rgba(109,242,192,.06) !important;}
[data-testid="stAlertContentSuccess"]{background:rgba(109,242,192,.08) !important;}
[data-testid="stMetric"]{
  background:rgba(255,255,255,.025) !important;border:1px solid var(--line) !important;border-radius:18px !important;
  padding:16px 18px !important;box-shadow:inset 0 1px 0 rgba(255,255,255,.04) !important;
}
[data-testid="stMetricValue"]{font-family:'Space Grotesk',sans-serif !important;font-size:2rem !important;font-weight:600 !important;letter-spacing:-.05em !important;color:var(--ink) !important;font-variant-numeric:tabular-nums;}
[data-testid="stMetricLabel"] p{color:var(--muted) !important;font-size:.76rem !important;font-weight:600 !important;letter-spacing:.02em !important;}
[data-testid="stMetricDelta"]{font-family:'Space Grotesk',sans-serif !important;font-weight:600 !important;}

/* ---------- Charts / tables ---------- */
[data-testid="stLineChart"],[data-testid="stBarChart"],[data-testid="stScatterChart"],[data-testid="stDataFrame"]{
  border-radius:16px !important;overflow:hidden !important;
}
[data-testid="stTable"] table,[data-testid="stDataFrame"] table{color:var(--ink) !important;}

/* ---------- Custom HTML pieces ---------- */
.ui-shell{position:relative;border-radius:28px;padding:6px;background:rgba(255,255,255,.045);border:1px solid var(--line);
  box-shadow:0 34px 80px -46px rgba(0,0,0,.9);}
.ui-core{position:relative;border-radius:22px;background:linear-gradient(150deg,rgba(15,42,52,.96),rgba(8,25,33,.98));
  border:1px solid rgba(255,255,255,.05);box-shadow:inset 0 1px 0 rgba(255,255,255,.07);overflow:hidden;}
.ui-hero{position:relative;padding:44px 44px 38px;}
.ui-hero::after{content:"";position:absolute;right:-90px;top:-120px;width:340px;height:340px;border-radius:50%;
  background:radial-gradient(circle,rgba(109,242,192,.16),transparent 68%);pointer-events:none;}
.ui-eyebrow{display:inline-flex;align-items:center;gap:9px;font-size:.7rem;font-weight:600;letter-spacing:.18em;color:var(--mint);
  text-transform:none;margin-bottom:18px;}
.ui-eyebrow::before{content:"";width:22px;height:1px;background:var(--mint);opacity:.7;}
.ui-hero h1{font-family:'Space Grotesk',sans-serif;font-size:clamp(2.3rem,4vw,3.7rem);line-height:1.02;letter-spacing:-.055em;
  font-weight:600;margin:0 0 16px;color:var(--ink);max-width:17ch;}
.ui-hero p{color:var(--muted);font-size:.95rem;line-height:1.7;max-width:52ch;margin:0;}
.ui-hero-grid{display:grid;grid-template-columns:1.05fr .95fr;gap:34px;align-items:center;}
.ui-hero-art{position:relative;min-height:190px;}
.ui-bars{position:relative;height:190px;display:flex;align-items:flex-end;gap:3px;
  padding:16px 4px 28px;border-bottom:1px solid var(--line);}
.ui-bars::before{content:"";position:absolute;left:0;right:0;top:16px;bottom:28px;pointer-events:none;
  background:repeating-linear-gradient(to bottom,transparent 0,transparent calc(33.33% - 1px),
    rgba(255,255,255,.05) calc(33.33% - 1px),rgba(255,255,255,.05) 33.33%);}
.ui-bar{flex:1;min-width:2px;position:relative;z-index:1;border-radius:6px 6px 2px 2px;
  background:linear-gradient(180deg,var(--mint),rgba(109,242,192,.1));
  box-shadow:0 -3px 16px -7px rgba(109,242,192,.75);
  transition:height .9s var(--ease),transform .7s var(--ease);}
.ui-bar:hover{transform:scaleY(1.04);transform-origin:bottom;}
.ui-bar.peak{background:linear-gradient(180deg,var(--amber),rgba(255,196,107,.14));
  box-shadow:0 -3px 18px -6px rgba(255,196,107,.8);}
.ui-bars-axis{position:absolute;left:0;right:0;bottom:-21px;display:flex;justify-content:space-between;
  font-family:'Space Grotesk',sans-serif;font-size:.62rem;color:var(--muted);font-variant-numeric:tabular-nums;}
.ui-peak{position:absolute;right:6%;bottom:8%;font-family:'Space Grotesk',sans-serif;font-size:.72rem;color:var(--amber);
  letter-spacing:.02em;background:rgba(6,20,27,.75);border:1px solid rgba(255,196,107,.25);border-radius:999px;padding:6px 12px;}
.ui-section{display:flex;align-items:baseline;gap:16px;margin:42px 0 18px;}
.ui-section h2{font-family:'Space Grotesk',sans-serif;font-size:1.5rem;font-weight:600;letter-spacing:-.04em;margin:0;color:var(--ink);}
.ui-section .ui-rule{flex:1;height:1px;background:linear-gradient(90deg,var(--line-strong),transparent);}
.ui-section .ui-note{font-size:.76rem;color:var(--muted);letter-spacing:.01em;}
.ui-step{display:flex;align-items:center;gap:11px;margin-bottom:18px;}
.ui-step-index{display:grid;place-items:center;width:30px;height:30px;border-radius:10px;flex:none;
  background:rgba(109,242,192,.12);border:1px solid rgba(109,242,192,.3);color:var(--mint);
  font-family:'Space Grotesk',sans-serif;font-size:.75rem;font-weight:700;}
.ui-step-title{font-family:'Space Grotesk',sans-serif;font-size:1.02rem;font-weight:600;letter-spacing:-.02em;color:var(--ink);}
.ui-step-sub{font-size:.74rem;color:var(--muted);margin-left:auto;text-align:right;}
.ui-readout{display:flex;align-items:flex-end;gap:14px;flex-wrap:wrap;}
.ui-big-number{font-family:'Space Grotesk',sans-serif;font-size:clamp(3.4rem,6vw,5.4rem);line-height:.9;font-weight:600;
  letter-spacing:-.07em;color:var(--mint);font-variant-numeric:tabular-nums;}
.ui-big-unit{font-family:'Space Grotesk',sans-serif;font-size:.95rem;color:var(--muted);letter-spacing:.04em;margin-left:-6px;}
.ui-chip{display:inline-flex;align-items:center;gap:8px;border-radius:999px;padding:7px 13px;font-size:.74rem;font-weight:600;
  letter-spacing:.01em;border:1px solid var(--line-strong);background:rgba(255,255,255,.035);color:var(--ink);white-space:nowrap;}
.ui-chip .dot{width:7px;height:7px;border-radius:50%;background:var(--mint);box-shadow:0 0 10px var(--mint);}
.ui-chip.warn .dot{background:var(--amber);box-shadow:0 0 10px var(--amber);}
.ui-chip.low .dot{background:var(--coral);box-shadow:0 0 10px var(--coral);}
.ui-stat-row{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:24px;}
.ui-stat{padding:15px 16px;border-radius:16px;background:rgba(255,255,255,.03);border:1px solid var(--line);}
.ui-stat .k{font-size:.69rem;color:var(--muted);letter-spacing:.06em;margin-bottom:7px;}
.ui-stat .v{font-family:'Space Grotesk',sans-serif;font-size:1.3rem;font-weight:600;letter-spacing:-.04em;color:var(--ink);font-variant-numeric:tabular-nums;}
.ui-stat .v.mint{color:var(--mint);} .ui-stat .v.amber{color:var(--amber);}
.ui-mini-note{font-size:.74rem;color:var(--muted);line-height:1.6;}

/* Brand mark: two wheels and a frame, drawn in CSS */
.ui-mark{position:relative;width:36px;height:34px;flex:none;}
.ui-mark-wheel{position:absolute;bottom:2px;width:13px;height:13px;border-radius:50%;
  border:1.6px solid var(--mint);box-shadow:0 0 12px -4px var(--mint);}
.ui-mark-wheel.left{left:1px;} .ui-mark-wheel.right{right:1px;}
.ui-mark-frame{position:absolute;left:8px;bottom:9px;width:19px;height:13px;
  border-left:1.6px solid var(--amber);border-top:1.6px solid var(--amber);
  border-right:1.6px solid var(--amber);border-radius:4px 4px 0 0;transform:skewX(-9deg);}

/* Ranking bars on About */
.ui-rank{display:grid;grid-template-columns:190px 1fr 74px;gap:14px;align-items:center;padding:12px 4px;
  border-bottom:1px solid var(--line);font-size:.82rem;}
.ui-rank:last-child{border-bottom:none;}
.ui-rank .model{color:var(--ink);font-weight:600;}
.ui-rank .track{height:7px;border-radius:99px;background:rgba(255,255,255,.05);overflow:hidden;}
.ui-rank .fill{height:100%;border-radius:99px;background:linear-gradient(90deg,rgba(109,242,192,.35),var(--mint));}
.ui-rank .score{font-family:'Space Grotesk',sans-serif;color:var(--muted);text-align:right;font-variant-numeric:tabular-nums;}
.ui-rank.best .score{color:var(--mint);font-weight:700;}
.ui-rank.best .model::after{content:'  DEPLOYED';font-size:.6rem;letter-spacing:.14em;color:var(--mint);margin-left:8px;}

/* One orchestrated entrance */
@keyframes ui-rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
.ui-hero{animation:ui-rise 1s var(--ease) both;}
@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.01ms !important;transition-duration:.01ms !important;}
}

/* ---------- Responsive ---------- */
@media(max-width:1100px){
  [data-testid="stMainBlockContainer"]{padding:2rem 1.8rem 6rem !important;}
  .ui-hero{padding:32px 28px;}
  .ui-hero-grid{grid-template-columns:1fr;}
  .ui-hero-art{max-width:520px;}
}
@media(max-width:768px){
  [data-testid="stMainBlockContainer"]{padding:1.4rem 1rem 5rem !important;}
  .ui-hero{padding:26px 20px 24px;}
  .ui-hero h1{font-size:2.25rem;}
  .ui-stat-row{grid-template-columns:1fr;}
  .ui-section{flex-wrap:wrap;gap:8px;}
  .ui-section .ui-rule{display:none;}
  .ui-rank{grid-template-columns:1fr 60px;}
  .ui-rank .track{grid-column:1 / -1;grid-row:2;}
  [data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"]{padding:18px !important;border-radius:20px !important;}
}
</style>
"""


def inject() -> None:
    """Inject the design system once per app run."""
    st.html(CSS)


# ---------------------------------------------------------------------------
# Reusable components
# ---------------------------------------------------------------------------
def _sparkline(values) -> str:
    """A 24-bar demand field. Built from divs because Streamlit sanitizes SVG."""
    lo, hi = min(values), max(values)
    span = max(hi - lo, 1e-6)
    peak_i = max(range(len(values)), key=lambda i: values[i])
    bars = []
    for i, v in enumerate(values):
        pct = 10 + (v - lo) / span * 84
        bright = i == peak_i
        bars.append(
            f'<div class="ui-bar{" peak" if bright else ""}" '
            f'style="height:{pct:.1f}%'
            f'{" ;background:linear-gradient(180deg,#FFC46B,rgba(255,196,107,.14))" if bright else ""}"></div>'
        )
    return f"""
<div class="ui-bars" role="img" aria-label="Predicted hourly demand, peaking at {peak_i:02d}:00">
  {''.join(bars)}
  <div class="ui-bars-axis"><span>00</span><span>06</span><span>12</span><span>18</span><span>23</span></div>
</div>"""


def hero(eyebrow: str, title: str, body: str, curve=None, peak_label: str = "") -> None:
    """Editorial hero with an optional live demand sparkline."""
    art = ""
    if curve is not None:
        art = f"""<div class="ui-hero-art">
          {_sparkline(list(curve))}
          <div class="ui-peak">{_html.escape(peak_label)}</div>
        </div>"""
    st.html(f"""
<div class="ui-shell"><div class="ui-core ui-hero">
  <div class="ui-hero-grid">
    <div>
      <div class="ui-eyebrow">{_html.escape(eyebrow)}</div>
      <h1>{_html.escape(title)}</h1>
      <p>{_html.escape(body)}</p>
    </div>
    {art}
  </div>
</div></div>""")


def section(title: str, note: str = "") -> None:
    st.html(f"""
<div class="ui-section">
  <h2>{_html.escape(title)}</h2>
  <div class="ui-rule"></div>
  {f'<span class="ui-note">{_html.escape(note)}</span>' if note else ''}
</div>""")


def step(index: str, title: str, sub: str = "") -> None:
    st.html(f"""
<div class="ui-step">
  <div class="ui-step-index">{_html.escape(index)}</div>
  <div class="ui-step-title">{_html.escape(title)}</div>
  {f'<div class="ui-step-sub">{_html.escape(sub)}</div>' if sub else ''}
</div>""")


def readout(count, unit, chip, stats, note="") -> None:
    """The hero prediction readout: one big number + supporting stats."""
    stat_html = "".join(
        f'<div class="ui-stat"><div class="k">{_html.escape(k)}</div>'
        f'<div class="v {tone}">{_html.escape(str(v))}</div></div>'
        for k, v, tone in stats
    )
    st.html(f"""
<div class="ui-shell"><div class="ui-core" style="padding:30px 32px;">
  <div class="ui-readout">
    <div class="ui-big-number">{_html.escape(str(count))}</div>
    <div class="ui-big-unit">{_html.escape(unit)}</div>
    <div style="flex:1"></div>
    {chip}
  </div>
  <div class="ui-stat-row">{stat_html}</div>
  {f'<p class="ui-mini-note" style="margin:18px 0 0">{_html.escape(note)}</p>' if note else ''}
</div></div>""")


def chip(text: str, tone: str = "ok") -> str:
    return (f'<span class="ui-chip {tone}"><span class="dot"></span>'
            f'{_html.escape(text)}</span>')


def leaderboard(rows) -> None:
    """Rows of (model, score, best) rendered as ranking bars."""
    worst = max(r[1] for r in rows)
    parts = []
    for name, score, best in rows:
        pct = max(6, (1 - score / (worst * 1.12)) * 100)
        parts.append(f"""
<div class="ui-rank {'best' if best else ''}">
  <div class="model">{_html.escape(name)}</div>
  <div class="track"><div class="fill" style="width:{pct:.1f}%"></div></div>
  <div class="score">{score:.2f}</div>
</div>""")
    st.html(f'<div class="ui-shell"><div class="ui-core" style="padding:20px 26px;">{"".join(parts)}</div></div>')


def brand_mark() -> str:
    """CSS-drawn bicycle mark (Streamlit sanitizes inline SVG)."""
    return """<div class="ui-mark" aria-hidden="true">
  <div class="ui-mark-wheel left"></div>
  <div class="ui-mark-wheel right"></div>
  <div class="ui-mark-frame"></div>
</div>"""
