"""Design system for the separate Metro Demand Studio UI.

Warm editorial paper, forest ink, fine rules, Fraunces display type.
Completely independent of streamlit_app.py and ui.py.
"""

from __future__ import annotations

import html as _html
import streamlit as st

INK = "#16231F"
TEAL = "#0E6B5E"
SAFFRON = "#D99A2B"


CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Manrope:wght@400;500;600;700&display=swap');
:root{
  --paper:#F7F4ED; --paper2:#EDE8DC; --card:#FFFEFB; --ink:#16231F; --soft:#55665F;
  --rule:rgba(22,35,31,.14); --rule2:rgba(22,35,31,.28);
  --teal:#0E6B5E; --teal-soft:rgba(14,107,94,.10); --saffron:#D99A2B; --saffron-text:#8A5A0B; --saffron-soft:rgba(217,154,43,.14);
}
html,body,[class*="st-emotion-cache"]{font-family:'Manrope',system-ui,sans-serif !important;color:var(--ink) !important;}
body{background:var(--paper) !important;}
[data-testid="stAppViewContainer"]{
  background:var(--paper) !important;
  background-image:radial-gradient(circle at 82% 0%,rgba(14,107,94,.045),transparent 34%);
}
[data-testid="stHeader"],[data-testid="stSidebar"]{display:none !important;}
[data-testid="stMainBlockContainer"]{max-width:1280px;margin:0 auto !important;padding:34px 40px 90px !important;}

/* type */
h1,h2,h3,h4,[data-testid="stHeading"]{font-family:'Fraunces',Georgia,serif !important;color:var(--ink) !important;letter-spacing:-.03em !important;}
p,label,span,div,[data-testid="stMarkdownContainer"] p{color:var(--ink);}
[data-testid="stCaptionContainer"] p,[data-testid="stCaptionContainer"] span{color:var(--soft) !important;font-size:.76rem !important;}
[data-testid="stMarkdownContainer"] p{line-height:1.7;}
hr,[data-testid="stDivider"]{border-color:var(--rule) !important;}

/* top navigation */
[data-testid="stRadio"] [data-testid="stWidgetLabel"]{display:none !important;}
[data-testid="stRadioGroup"]{flex-direction:row !important;gap:10px !important;background:transparent !important;}
[data-testid="stRadioOption"]{
  background:transparent !important;border:1px solid transparent !important;border-radius:999px !important;
  padding:8px 18px !important;transition:background .5s cubic-bezier(.22,1,.36,1),border-color .5s cubic-bezier(.22,1,.36,1),transform .5s cubic-bezier(.22,1,.36,1) !important;
}
[data-testid="stRadioOption"] p{font-size:.82rem !important;font-weight:600 !important;color:var(--soft) !important;margin:0 !important;}
[data-testid="stRadioOption"]:hover{background:var(--teal-soft) !important;transform:translateY(-1px) !important;}
[data-testid="stRadioOption"][data-selected="true"]{background:var(--ink) !important;border-color:var(--ink) !important;}
[data-testid="stRadioOption"][data-selected="true"] p{color:#fff !important;}
[data-testid="stRadioOption"] div[class*="ex50key4"]{display:none !important;}

/* cards */
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"]{
  background:var(--card) !important;border:1px solid var(--rule) !important;border-radius:18px !important;
  padding:24px 26px !important;
  box-shadow:0 1px 0 rgba(255,255,255,.8) inset,0 18px 44px -38px rgba(22,35,31,.35) !important;
}
[data-testid="stHorizontalBlock"]{gap:18px !important;}

/* widgets */
[data-testid="stWidgetLabel"] p{font-size:.72rem !important;font-weight:700 !important;color:var(--soft) !important;letter-spacing:.06em !important;}
[data-testid="stButton"] button,[data-testid="stDownloadButton"] button{
  border-radius:999px !important;border:1px solid var(--rule2) !important;background:transparent !important;
  color:var(--ink) !important;font-weight:600 !important;font-size:.8rem !important;padding:.55rem 1.1rem !important;
  transition:transform .5s cubic-bezier(.22,1,.36,1),background .5s cubic-bezier(.22,1,.36,1),border-color .5s cubic-bezier(.22,1,.36,1) !important;
}
[data-testid="stButton"] button:hover,[data-testid="stDownloadButton"] button:hover{background:var(--teal-soft) !important;border-color:var(--teal) !important;transform:translateY(-2px) !important;}
[data-testid="stButton"] button[kind="primary"],[data-testid="stDownloadButton"] button[kind="primary"]{
  background:var(--ink) !important;color:#fff !important;border-color:var(--ink) !important;
}
[data-baseweb="select"] > div,[data-testid="stTextInput"] input,[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] [role="group"],[data-testid="stDateInputField"],
[data-testid="stDateInputField"] > div,[data-testid="stDateInputFieldsScroller"]{
  background:#fff !important;border:1px solid var(--rule2) !important;border-radius:10px !important;
  color:var(--ink) !important;
}
[data-baseweb="select"] input,[data-testid="stSelectbox"] input,
[data-testid="stDateInputField"] [role="spinbutton"]{color:var(--ink) !important;background:transparent !important;}
[data-testid="stDateInputField"] svg,[data-testid="stSelectbox"] svg{color:var(--ink) !important;fill:currentColor !important;}
[data-testid="stWidgetLabel"] p{white-space:normal !important;overflow-wrap:anywhere !important;}
[data-testid="stDateInputField"] [role="spinbutton"]{min-width:32px !important;padding:0 3px !important;font-size:.82rem !important;}
[data-testid="stSlider"] [data-testid="stSliderThumbValue"]{background:var(--teal) !important;color:#fff !important;font-family:'Manrope',sans-serif !important;font-weight:700 !important;}
[data-testid="stSlider"] [role="slider"]{box-shadow:0 0 0 4px var(--teal-soft) !important;}
[data-testid="stButtonGroup"] > [data-testid="stWidgetLabel"]{display:block !important;margin-bottom:8px !important;}
[data-testid="stButtonGroup"] > [role="radiogroup"]{background:var(--paper2) !important;border-radius:999px !important;padding:4px !important;gap:4px !important;border:1px solid var(--rule) !important;display:flex !important;width:max-content !important;}
[data-testid="stButtonGroup"] button{border-radius:999px !important;padding:.35rem .85rem !important;background:transparent !important;border:1px solid transparent !important;color:var(--soft) !important;box-shadow:none !important;height:auto !important;}
[data-testid="stButtonGroup"] button[aria-pressed="true"],[data-testid="stButtonGroup"] button[aria-checked="true"]{background:var(--ink) !important;color:#fff !important;}
/* Widget label text must inherit the button colour, not the global ink colour */
[data-testid="stButton"] button[kind="primary"] *,[data-testid="stDownloadButton"] button[kind="primary"] *,
[data-testid="stFileUploaderDropzone"] button *{color:#fff !important;}
[data-testid="stButton"] button[kind="secondary"] *,[data-testid="stDownloadButton"] button[kind="secondary"] *,
[data-testid="stButtonGroup"] button *{color:var(--ink) !important;}
[data-testid="stButtonGroup"] button[aria-checked="true"] *,
[data-testid="stButtonGroup"] button[aria-pressed="true"] *{color:#fff !important;}

/* Dark-theme leaks: slider */
[data-testid="stSlider"] .st-emotion-cache-xuq335{
  background-image:none !important;background:var(--paper2) !important;border-radius:99px !important;}
[data-testid="stSlider"] .st-emotion-cache-r1tb5r{background:var(--teal) !important;}
[data-testid="stSlider"] > div[role="group"]{margin-top:24px !important;}
[data-testid="stSliderThumbValue"]{
  min-width:26px !important;width:26px !important;left:50% !important;
  transform:translateX(-50%) !important;top:-28px !important;
  display:flex !important;align-items:center !important;justify-content:center !important;
  padding:4px 6px !important;border-radius:8px !important;font-size:.78rem !important;font-weight:700 !important;}
[data-testid="stSliderThumbValue"] p{color:#fff !important;margin:0 !important;font-size:.78rem !important;}

/* Dark-theme leaks: date picker */
[data-testid="stDateInputCalendar"]{
  background:#fff !important;border:1px solid var(--rule2) !important;border-radius:12px !important;
  box-shadow:0 22px 50px -30px rgba(22,35,31,.55) !important;}
[role="grid"] th,[role="grid"] td,[role="grid"] button{color:var(--ink) !important;}
[role="gridcell"] > div[data-selected="true"]{background:var(--teal) !important;color:#fff !important;border-radius:8px !important;}

/* Dark-theme leaks: upload dropzone */
[data-testid="stFileUploaderDropzone"]{
  background:#fff !important;border:1.5px dashed var(--rule2) !important;border-radius:14px !important;color:var(--ink) !important;}
[data-testid="stFileUploaderDropzone"] *{color:var(--ink) !important;}
[data-testid="stFileUploaderDropzone"] button{background:var(--ink) !important;color:#fff !important;border-color:var(--ink) !important;}
[data-testid="stFileUploaderDropzone"] button p{color:#fff !important;}

/* Dark-theme leaks: code block */
[data-testid="stCode"] pre{
  background:#F3F0E8 !important;color:var(--ink) !important;border:1px solid var(--rule) !important;
  border-radius:12px !important;}
[data-testid="stCode"] pre code,[data-testid="stCode"] pre code span{color:var(--ink) !important;}
[data-testid="stCode"] pre code .token{color:var(--teal) !important;}
[data-testid="stCode"] div[class*="ej556a85"],[data-testid="stCode"] [data-testid="stElementToolbarButton"]{background:transparent !important;}
[data-testid="stCode"] button{color:var(--soft) !important;background:transparent !important;border:0 !important;}
[data-testid="stCode"] button p{color:var(--soft) !important;}

[data-testid="stAlertContainer"]{background:var(--teal-soft) !important;border:1px solid rgba(14,107,94,.25) !important;border-radius:12px !important;color:var(--ink) !important;}
[data-testid="stAlertContainer"] p{color:var(--ink) !important;}
[data-testid="stMetric"]{background:#fff !important;border:1px solid var(--rule) !important;border-radius:14px !important;padding:14px 16px !important;}
[data-testid="stMetricValue"]{font-family:'Fraunces',serif !important;font-size:1.9rem !important;color:var(--ink) !important;}
[data-testid="stMetricLabel"] p{color:var(--soft) !important;}
[data-testid="stLineChart"],[data-testid="stBarChart"],[data-testid="stScatterChart"],[data-testid="stDataFrame"]{border-radius:12px !important;overflow:hidden !important;}

/* ---------- custom HTML ---------- */
.v2-masthead{display:flex;align-items:center;justify-content:space-between;padding-bottom:20px;border-bottom:1px solid var(--rule2);margin-bottom:22px;}
.v2-brand{display:flex;align-items:center;gap:11px;}
.v2-logo{display:flex;align-items:flex-end;gap:3px;height:22px;}
.v2-logo i{display:block;width:4px;background:var(--teal);border-radius:1px;}
.v2-logo i:nth-child(1){height:9px}.v2-logo i:nth-child(2){height:15px}.v2-logo i:nth-child(3){height:22px}
.v2-brand strong{font-family:'Fraunces',serif;font-size:1.35rem;font-weight:600;letter-spacing:-.04em;}
.v2-brand span{font-size:.8rem;color:var(--soft);margin-left:2px;}
.v2-status{font-size:.74rem;color:var(--soft);display:flex;align-items:center;gap:8px;}
.v2-status b{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--teal);box-shadow:0 0 0 4px var(--teal-soft);}
.v2-kicker{font-size:.68rem;font-weight:700;letter-spacing:.16em;color:var(--teal);margin-bottom:14px;display:flex;align-items:center;gap:10px;}
.v2-kicker::before{content:"";width:26px;height:1px;background:var(--teal);}
.v2-hero{display:grid;grid-template-columns:1.15fr .85fr;gap:48px;align-items:center;padding:26px 0 46px;}
.v2-hero h1{font-family:'Fraunces',serif;font-size:clamp(2.7rem,5vw,4.4rem);font-weight:500;line-height:1.02;letter-spacing:-.055em;margin:0 0 18px;}
.v2-hero p{color:var(--soft);font-size:.96rem;line-height:1.75;max-width:50ch;margin:0;}
.v2-live{background:var(--card);border:1px solid var(--rule);border-radius:18px;padding:26px 28px;box-shadow:0 18px 44px -40px rgba(22,35,31,.45);}
.v2-live .label{font-size:.7rem;font-weight:700;letter-spacing:.13em;color:var(--soft);}
.v2-live .number{font-family:'Fraunces',serif;font-size:clamp(3.4rem,6vw,5rem);line-height:1;letter-spacing:-.06em;color:var(--ink);margin:10px 0 0;font-variant-numeric:tabular-nums;}
.v2-live .unit{font-family:'Manrope',sans-serif;font-size:.82rem;color:var(--soft);margin-left:8px;letter-spacing:0;}
.v2-live .foot{border-top:1px solid var(--rule);margin-top:18px;padding-top:14px;display:flex;justify-content:space-between;font-size:.75rem;color:var(--soft);}
.v2-live .foot b{color:var(--saffron-text);font-weight:700;}
.v2-section{display:flex;align-items:baseline;gap:18px;margin:16px 0 20px;}
.v2-section h2{font-family:'Fraunces',serif;font-size:1.55rem;font-weight:500;margin:0;letter-spacing:-.04em;}
.v2-section .line{flex:1;height:1px;background:var(--rule);}
.v2-section small{font-size:.72rem;color:var(--soft);}
.v2-label{font-size:.7rem;font-weight:700;letter-spacing:.12em;color:var(--soft);padding:4px 0 10px;border-bottom:1px solid var(--rule);margin-bottom:14px;}
.v2-bars{display:flex;align-items:flex-end;gap:3px;height:170px;padding:8px 2px 0;border-bottom:1px solid var(--rule);position:relative;}
.v2-bar{flex:1;min-width:2px;background:linear-gradient(180deg,var(--teal),rgba(14,107,94,.12));border-radius:5px 5px 0 0;position:relative;}
.v2-bar.peak{background:linear-gradient(180deg,var(--saffron),rgba(217,154,43,.15));}
.v2-bar:hover{filter:brightness(1.18);}
.v2-axis{display:flex;justify-content:space-between;font-size:.64rem;color:var(--soft);margin-top:7px;font-variant-numeric:tabular-nums;}
.v2-note{margin-top:16px;padding-top:14px;border-top:1px solid var(--rule);font-size:.8rem;color:var(--soft);line-height:1.65;}
.v2-note b{color:var(--ink);}
.v2-tag{display:inline-flex;align-items:center;gap:7px;font-size:.72rem;font-weight:700;border-radius:999px;padding:6px 12px;background:var(--teal-soft);color:var(--teal);}
.v2-tag.warm{background:var(--saffron-soft);color:#95631A;}
.v2-tag .dot{width:6px;height:6px;border-radius:50%;background:currentColor;}
.v2-scroll{overflow-x:auto;overflow-y:hidden;padding-bottom:6px;-webkit-overflow-scrolling:touch;}
.v2-heat{display:grid;grid-template-columns:34px repeat(24,1fr);gap:3px;align-items:center;min-width:540px;}
.v2-heat .rowlab{font-size:.64rem;color:var(--soft);font-weight:600;}
.v2-cell{height:15px;border-radius:3px;background:var(--teal-soft);}
.v2-cell.now{outline:1.5px solid var(--saffron);outline-offset:1px;}
.v2-heat-axis{display:grid;grid-template-columns:34px repeat(24,1fr);gap:3px;margin-top:8px;font-size:.58rem;color:var(--soft);text-align:center;}
.v2-compare{display:grid;gap:12px;}
.v2-comp .top{display:flex;justify-content:space-between;font-size:.76rem;margin-bottom:6px;}
.v2-comp .top b{font-variant-numeric:tabular-nums;}
.v2-comp .track{height:8px;border-radius:99px;background:var(--paper2);overflow:hidden;}
.v2-comp .fill{height:100%;border-radius:99px;background:var(--teal);opacity:.45;}
.v2-comp.active .top b{color:var(--teal);}
.v2-comp.active .fill{opacity:1;background:linear-gradient(90deg,var(--teal),#3BA894);}
.v2-rank{display:grid;grid-template-columns:200px 1fr 60px;gap:14px;align-items:center;padding:13px 2px;border-bottom:1px solid var(--rule);font-size:.8rem;}
.v2-rank:last-child{border:0;}
.v2-rank .track{height:7px;border-radius:99px;background:var(--paper2);overflow:hidden;}
.v2-rank .fill{height:100%;border-radius:99px;background:linear-gradient(90deg,rgba(14,107,94,.35),var(--teal));}
.v2-rank .score{font-variant-numeric:tabular-nums;text-align:right;color:var(--soft);}
.v2-rank.best .score{color:var(--teal);font-weight:700;}
/* Sticky workspace: controls scroll with the page, results stay in view */
[data-testid="stHorizontalBlock"]:has(#v2-controls){align-items:flex-start !important;}
[data-testid="stHorizontalBlock"]:has(#v2-controls) > div[data-testid="stColumn"]:last-child{
  position:sticky !important;top:12px !important;max-height:calc(100vh - 24px) !important;
  overflow-y:auto !important;overflow-x:hidden !important;padding-right:6px;
  scrollbar-width:thin;scrollbar-color:var(--rule2) transparent;}
[data-testid="stHorizontalBlock"]:has(#v2-controls) > div[data-testid="stColumn"]:last-child::-webkit-scrollbar{width:6px;}
[data-testid="stHorizontalBlock"]:has(#v2-controls) > div[data-testid="stColumn"]:last-child::-webkit-scrollbar-thumb{background:var(--rule2);border-radius:99px;}
[data-testid="stHorizontalBlock"]:has(#v2-controls) > div[data-testid="stColumn"]:first-child
  [data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"]{padding:18px 20px !important;}

/* Always-visible live readout */
.v2-hud{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:100;
  display:flex;align-items:center;gap:16px;background:rgba(255,254,251,.95);
  border:1px solid var(--rule2);border-radius:999px;padding:9px 20px;
  box-shadow:0 18px 44px -26px rgba(22,35,31,.55);font-size:.75rem;color:var(--soft);
  pointer-events:none;white-space:nowrap;}
.v2-hud b{font-family:'Fraunces',serif;font-size:1.15rem;color:var(--ink);font-variant-numeric:tabular-nums;}
.v2-hud .hud-peak{color:var(--saffron-text);font-weight:700;}
.v2-footer{text-align:center;color:var(--soft);font-size:.7rem;margin-top:54px;padding-top:20px;border-top:1px solid var(--rule);}
@keyframes v2-rise{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
.v2-hero{animation:v2-rise .9s cubic-bezier(.22,1,.36,1) both;}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms !important;transition-duration:.01ms !important;}}

/* ---------- Responsive: tablet ---------- */
@media(max-width:1100px){
  [data-testid="stMainBlockContainer"]{padding:24px 24px 80px !important;}
  .v2-hero{grid-template-columns:1fr;gap:28px;}
  .v2-hero .v2-live{max-width:560px;}
}
/* Stack every control sub-column instead of squeezing widgets */
@media(max-width:900px){
  [data-testid="stHorizontalBlock"]:has(#v2-controls){flex-wrap:wrap !important;}
  [data-testid="stHorizontalBlock"]:has(#v2-controls) > div[data-testid="stColumn"],
  [data-testid="stHorizontalBlock"]:has(#v2-controls) [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]{
    width:100% !important;max-width:100% !important;flex:1 1 100% !important;}
  [data-testid="stHorizontalBlock"]:has(#v2-controls) [data-testid="stHorizontalBlock"]{flex-wrap:wrap !important;}
}
/* ---------- Responsive: phone ---------- */
@media(max-width:760px){
  [data-testid="stHorizontalBlock"]:has(#v2-controls) > div[data-testid="stColumn"]:last-child{
    position:static !important;max-height:none !important;overflow:visible !important;}
  .v2-hud{left:8px;right:8px;bottom:8px;transform:none;border-radius:16px;
    justify-content:center;flex-wrap:wrap;white-space:normal;text-align:center;gap:4px 12px;padding:8px 14px;}
}
@media(max-width:680px){
  [data-testid="stMainBlockContainer"]{padding:18px 14px 110px !important;}
  [data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"]{padding:18px !important;border-radius:14px !important;}
  .v2-hero h1{font-size:2.4rem;}
  .v2-masthead{flex-direction:column;align-items:flex-start;gap:12px;}
  .v2-rank{grid-template-columns:1fr 55px;}
  .v2-rank .track{grid-column:1/-1;grid-row:2;}
  .v2-heat,.v2-heat-axis{min-width:540px;}
  .v2-bars{height:130px;}
  .v2-live{padding:20px;}
}
</style>
"""


def inject() -> None:
    st.html(CSS)


def masthead(status: str = "model online · RMSLE 0.53") -> None:
    st.html(f"""
<div class="v2-masthead">
  <div class="v2-brand">
    <div class="v2-logo"><i></i><i></i><i></i></div>
    <strong>metro</strong><span>demand studio</span>
  </div>
  <div class="v2-status"><b></b>{_html.escape(status)}</div>
</div>""")


def bars(curve, axis: bool = True) -> None:
    """Hourly demand bars, rendered as HTML/CSS (Streamlit strips inline SVG)."""
    lo, hi = min(curve), max(curve)
    span = max(hi - lo, 1e-6)
    peak_i = max(range(len(curve)), key=lambda i: curve[i])
    marks = "".join(
        f'<div class="v2-bar{" peak" if i == peak_i else ""}" '
        f'style="height:{10 + (v - lo) / span * 88:.1f}%"></div>'
        for i, v in enumerate(curve)
    )
    axes = ('<div class="v2-axis"><span>00</span><span>06</span><span>12</span>'
            '<span>18</span><span>23</span></div>') if axis else ""
    st.html(f'<div class="v2-bars">{marks}</div>{axes}')


def hero(kicker: str, headline: str, body: str, count, peak: str, curve,
         label: str = "ESTIMATED DEMAND", unit: str = "bikes / hour") -> None:
    lo, hi = min(curve), max(curve)
    span = max(hi - lo, 1e-6)
    peak_i = max(range(len(curve)), key=lambda i: curve[i])
    bars_html = "".join(
        f'<div class="v2-bar{" peak" if i == peak_i else ""}" '
        f'style="height:{10 + (v - lo) / span * 88:.1f}%"></div>'
        for i, v in enumerate(curve)
    )
    st.html(f"""
<div class="v2-hero">
  <div>
    <div class="v2-kicker">{_html.escape(kicker)}</div>
    <h1>{_html.escape(headline)}</h1>
    <p>{_html.escape(body)}</p>
  </div>
  <div class="v2-live">
    <div class="label">{_html.escape(label)}</div>
    <div class="number">{_html.escape(str(count))}<span class="unit">{_html.escape(unit)}</span></div>
    <div class="v2-bars">{bars_html}</div>
    <div class="v2-axis"><span>00</span><span>06</span><span>12</span><span>18</span><span>23</span></div>
    <div class="v2-foot"><span>Daily peak</span><b>{_html.escape(peak)}</b></div>
  </div>
</div>""")


def section(title: str, note: str = "") -> None:
    st.html(f"""
<div class="v2-section"><h2>{_html.escape(title)}</h2><div class="line"></div>
{f'<small>{_html.escape(note)}</small>' if note else ''}</div>""")


def label(text: str) -> None:
    st.html(f'<div class="v2-label">{_html.escape(text)}</div>')


def tag(text: str, warm: bool = False) -> str:
    return f'<span class="v2-tag{" warm" if warm else ""}"><span class="dot"></span>{_html.escape(text)}</span>'


def note(text: str) -> None:
    st.html(f'<div class="v2-note">{text}</div>')


def heatmap(matrix, row_labels, selected_col: int) -> None:
    """matrix: list of 7 rows, each 24 demand values."""
    lo = min(min(r) for r in matrix)
    hi = max(max(r) for r in matrix)
    span = max(hi - lo, 1e-6)
    rows = []
    for lab, row in zip(row_labels, matrix):
        cells = "".join(
            f'<div class="v2-cell{" now" if c == selected_col else ""}" '
            f'title="{c:02d}:00 · {v:.0f}" '
            f'style="background:rgba(14,107,94,{0.07 + 0.75 * (v-lo)/span:.3f})"></div>'
            for c, v in enumerate(row)
        )
        rows.append(f'<div class="rowlab">{_html.escape(lab)}</div>{cells}')
    st.html(f"""
<div class="v2-scroll">
  <div class="v2-heat">{''.join(rows)}</div>
  <div class="v2-heat-axis"><span></span>{''.join(f'<span>{h:02d}</span>' if h in (0,3,6,9,12,15,18,21,23) else '<span></span>' for h in range(24))}</div>
</div>""")


def compare(labels, values, selected: int) -> None:
    hi = max(values)
    parts = []
    for i, (lab, v) in enumerate(zip(labels, values)):
        pct = max(5, v / hi * 100)
        parts.append(f"""
<div class="v2-comp{" active" if i == selected else ""}">
  <div class="top"><span>{_html.escape(lab)}</span><b>{v:.0f}</b></div>
  <div class="track"><div class="fill" style="width:{pct:.1f}%"></div></div>
</div>""")
    st.html(f'<div class="v2-compare">{"".join(parts)}</div>')


def leaderboard(rows) -> None:
    worst = max(r[1] for r in rows)
    parts = "".join(
        f'<div class="v2-rank{" best" if best else ""}"><span>{_html.escape(name)}</span>'
        f'<div class="track"><div class="fill" style="width:{max(6,(1-score/(worst*1.12))*100):.1f}%"></div></div>'
        f'<span class="score">{score:.2f}</span></div>'
        for name, score, best in rows
    )
    st.html(f'<div style="border-top:1px solid var(--rule)">{parts}</div>')
