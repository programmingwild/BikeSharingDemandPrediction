"""BikeShare Demand Studio — self-contained live Streamlit app.

The design system and the UI both live in this file, so Streamlit Cloud can
run it directly without importing another local module (which breaks on hot
reload with a KeyError on the imported module name).
"""
"""Design system for the BikeShare Demand Studio UI.

Warm editorial paper, forest ink, fine rules, Fraunces display type.
Completely independent of streamlit_app.py and ui.py.
"""

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
html,body,[class*="st-emotion-cache"]:not([data-testid="stIconMaterial"]){font-family:'Manrope',system-ui,sans-serif !important;color:var(--ink) !important;}
[data-testid="stIconMaterial"]{font-family:"Material Symbols Rounded" !important;font-size:1rem !important;line-height:1 !important;letter-spacing:normal !important;}
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
[data-testid="stSlider"] [class*="e13xtgje5"]{
  background-image:none !important;background:var(--paper2) !important;border-radius:99px !important;}
[data-testid="stSlider"] [class*="e13xtgje3"]{background:var(--teal) !important;}
[data-testid="stSlider"] > div[role="group"]{margin-top:24px !important;}
[data-testid="stSliderThumbValue"]{
  min-width:26px !important;width:26px !important;left:50% !important;
  transform:translateX(-50%) !important;top:-28px !important;
  display:flex !important;align-items:center !important;justify-content:center !important;
  padding:4px 6px !important;border-radius:8px !important;font-size:.78rem !important;font-weight:700 !important;}
[data-testid="stSliderThumbValue"] p{color:#fff !important;margin:0 !important;font-size:.78rem !important;}
[data-testid="stSlider"] input[type="range"]{opacity:0 !important;accent-color:var(--teal) !important;}

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
.v2-live .unit{font-family:'Manrope',sans-serif;font-size:.82rem;color:var(--soft);margin-left:12px;letter-spacing:0;display:inline-block;}
.v2-foot{border-top:1px solid var(--rule);margin-top:18px;padding-top:14px;display:flex;justify-content:space-between;align-items:baseline;gap:14px;flex-wrap:wrap;font-size:.75rem;color:var(--soft);}
.v2-foot span{flex:none;}
.v2-foot b{color:var(--saffron-text);font-weight:700;white-space:normal;text-align:right;}
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
.v2-hud{position:fixed;right:20px;bottom:16px;z-index:100;
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
@media(max-width:820px){
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
  .v2-hud{left:auto;right:8px;bottom:8px;transform:none;border-radius:14px;
    max-width:calc(100% - 16px);width:max-content;justify-content:flex-end;
    flex-wrap:nowrap;white-space:nowrap;text-align:right;gap:8px;padding:7px 12px;font-size:.66rem;}
}
@media(max-width:680px){
  [data-testid="stMainBlockContainer"]{padding:18px 14px 110px !important;}
  .v2-section{flex-wrap:wrap;gap:6px 10px;}
  .v2-section .line{display:none;}
  .v2-section small{flex-basis:100%;line-height:1.5;}
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
    <strong>BikeShare</strong><span>demand studio</span>
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


def hero(kicker: str, headline: str, body: str, count, peak: str, curve=None,
         label: str = "ESTIMATED DEMAND", unit: str = "bikes / hour",
         foot_label: str = "Daily peak") -> None:
    bars_html = ""
    if curve:
        lo, hi = min(curve), max(curve)
        span = max(hi - lo, 1e-6)
        peak_i = max(range(len(curve)), key=lambda i: curve[i])
        bars_html = "".join(
            f'<div class="v2-bar{" peak" if i == peak_i else ""}" '
            f'style="height:{10 + (v - lo) / span * 88:.1f}%"></div>'
            for i, v in enumerate(curve)
        )
    bars_block = (f'<div class="v2-bars">{bars_html}</div>'
                  f'<div class="v2-axis"><span>00</span><span>06</span><span>12</span>'
                  f'<span>18</span><span>23</span></div>') if curve else ""
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
    {bars_block}
    <div class="v2-foot"><span>{_html.escape(foot_label)}</span><b>{_html.escape(peak)}</b></div>
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

# Design-system helpers are defined above in this same module.
import sys as _sys
v2 = _sys.modules[__name__]

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
import pandas as pd
import numpy as np
import joblib
from src.features import add_features

st.set_page_config(page_title="BikeShare · Demand Studio", page_icon="🚲",
                   layout="wide", initial_sidebar_state="collapsed")
v2.inject()

SEASONS = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}
WEATHER = {1: "Clear", 2: "Mist", 3: "Light rain / snow", 4: "Heavy rain / snow"}
DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
REQUIRED_COLUMNS = ["datetime", "season", "holiday", "workingday", "weather",
                    "temp", "atemp", "humidity", "windspeed"]
PRESETS = {
    "Morning rush": dict(date="2012-06-15", hour=8, season=3, weather=1, workingday=1, t_c=20.0, hum=60, wind=10),
    "Evening rush": dict(date="2012-06-15", hour=18, season=3, weather=1, workingday=1, t_c=24.0, hum=55, wind=12),
    "Weekend midday": dict(date="2012-06-16", hour=14, season=3, weather=1, workingday=0, t_c=28.0, hum=50, wind=8),
    "Rainy commute": dict(date="2012-06-15", hour=9, season=2, weather=3, workingday=1, t_c=15.0, hum=85, wind=20),
}
DEFAULTS = dict(in_date="2012-06-15", in_hour=8, in_season=3, in_weather=1,
                in_workingday=1, in_holiday=0, in_t=22.0, in_at=24.0, in_hum=60, in_wind=12)
for k, val in DEFAULTS.items():
    st.session_state.setdefault(k, val)


def apply_preset(preset):
    """Runs before widgets are created, so keyed session values can be updated."""
    for k, val in preset.items():
        st.session_state[f"in_{k}"] = pd.to_datetime(val).date() if k == "date" else val
    st.session_state["in_at"] = preset["t_c"] + 2.0  # kept for compatibility


@st.cache_resource
def load_model():
    b = joblib.load("src/model.pkl")
    return b["model"], b["features"]


@st.cache_data
def load_train():
    return pd.read_csv("data/train.csv", parse_dates=["datetime"])


model, FEATURES = load_model()


def norm(t_c, at_c, hum, wind):
    return (t_c + 8) / 47.0, (at_c + 16) / 66.0, hum / 100.0, wind / 67.0


def row_for(date_str, hour, season, holiday, workingday, weather, temp, atemp, hum, wind):
    return add_features(pd.DataFrame([{
        "datetime": pd.to_datetime(f"{date_str} {hour:02d}:00"), "season": season,
        "holiday": holiday, "workingday": workingday, "weather": weather,
        "temp": temp, "atemp": atemp, "humidity": hum, "windspeed": wind}]))


def forecast(date_str, season, holiday, workingday, weather, temp, atemp, hum, wind):
    return [float(np.expm1(model.predict(row_for(date_str, h, season, holiday, workingday,
                                               weather, temp, atemp, hum, wind)[FEATURES])[0]))
            for h in range(24)]


def score_upload(file):
    """Validate and score an uploaded CSV, raising friendly ValueError messages."""
    raw = pd.read_csv(file)
    missing = [c for c in REQUIRED_COLUMNS if c not in raw.columns]
    if missing:
        raise ValueError("Missing columns: " + ", ".join(missing))
    raw["datetime"] = pd.to_datetime(raw["datetime"], errors="coerce")
    if raw["datetime"].isna().any():
        raise ValueError("Some datetime values could not be read.")
    if raw.empty:
        raise ValueError("The file has no rows.")
    df = add_features(raw)
    preds = np.expm1(model.predict(df[FEATURES])).clip(min=0).round().astype(int)
    return pd.DataFrame({"datetime": df["datetime"], "count": preds})


v2.masthead()
NAV_OPTIONS = ["Forecast", "Batch", "Insights", "About"]
requested = st.query_params.get("page", "Forecast")
nav_index = NAV_OPTIONS.index(requested) if requested in NAV_OPTIONS else 0
page = st.radio("Navigate", NAV_OPTIONS, horizontal=True, label_visibility="collapsed",
                index=nav_index, key="nav_page")

if page == "Forecast":
    s = st.session_state
    if isinstance(s["in_date"], str):
        s["in_date"] = pd.to_datetime(s["in_date"]).date()
    date0 = pd.to_datetime(s["in_date"]).strftime("%Y-%m-%d")
    t0, a0, h0, w0 = norm(float(s["in_t"]), float(s["in_t"]) + 2.0,
                          int(s["in_hum"]), int(s["in_wind"]))
    preview = forecast(date0, int(s["in_season"]), int(s["in_holiday"]),
                       int(s["in_workingday"]), int(s["in_weather"]), t0, a0, h0, w0)
    ph = int(np.argmax(preview))
    v2.hero("hourly ridership · capital bikeshare 2011–2012",
            "Read the city's rhythm.",
            "Twelve months of hourly rides, one fitted model. Set the conditions on the left "
            "and the whole day redraws itself on the right.",
            f"{preview[int(s['in_hour'])]:.0f}", f"{ph:02d}:00 · {preview[ph]:.0f} bikes", preview)

    v2.section("Shape the scenario", "controls scroll · results stay pinned")
    left, right = st.columns([0.9, 2.1], gap="large")
    with left:
        st.html('<div id="v2-controls" style="height:0"></div>')
        with st.container(border=True):
            v2.label("01 · WHEN")
            picked = st.date_input("Date", key="in_date")
            d_str = pd.to_datetime(picked).strftime("%Y-%m-%d")
            dow = pd.to_datetime(d_str).day_of_week
            hour = st.slider("Hour", 0, 23, key="in_hour")
            st.caption(f"{DOW[dow]} · " + ("weekend" if dow >= 5 else "weekday"))

            v2.label("02 · DAY TYPE")
            v2.label("Season")
            season = st.radio("Season", [1, 2, 3, 4], horizontal=True,
                              format_func=lambda x: SEASONS[x], label_visibility="collapsed",
                              key="in_season")
            v2.label("Weather")
            weather = st.radio("Weather", [1, 2, 3, 4], horizontal=True,
                               format_func=lambda x: WEATHER[x], label_visibility="collapsed",
                               key="in_weather")
            v2.label("Holiday")
            holiday = st.radio("Holiday", [0, 1], horizontal=True,
                               format_func=lambda x: "Yes" if x else "No", label_visibility="collapsed",
                               key="in_holiday")
            wd_auto = 0 if (holiday == 1 or dow >= 5) else 1
            v2.label("Working day")
            if "in_workingday" not in s:
                s["in_workingday"] = wd_auto
            workingday = st.radio("Working day", [0, 1], horizontal=True,
                                  format_func=lambda x: "Yes" if x else "No", label_visibility="collapsed",
                                  key="in_workingday")

            v2.label("03 · CONDITIONS")
            t_c = st.slider("Temperature °C", -8.0, 39.0, key="in_t")
            hum = st.slider("Humidity %", 0, 100, key="in_hum")
            wind = st.slider("Wind", 0, 67, key="in_wind")
            at_c = t_c + 2.0
            s["in_at"] = at_c

        with st.container(border=True):
            v2.label("QUICK SCENARIOS")
            for name, preset in PRESETS.items():
                st.button(name, use_container_width=True,
                          on_click=apply_preset, args=(preset,))

    temp, atemp, humidity, windspeed = norm(t_c, at_c, hum, wind)
    curve = forecast(d_str, season, holiday, workingday, weather, temp, atemp, humidity, windspeed)
    pred = max(0, int(round(curve[hour])))
    day_avg = float(np.mean(curve))
    peak_h, peak_v = int(np.argmax(curve)), float(max(curve))
    st.html(f'<div class="v2-hud"><span>{hour:02d}:00 forecast</span><b>{pred} bikes</b>'
            f'<span class="hud-peak">peak {peak_h:02d}:00 · {peak_v:.0f}</span></div>')
    if pred > 300:
        verdict, warm = "Extra bikes needed at this hour.", True
    elif pred > 100:
        verdict, warm = "Normal rebalancing covers this hour.", False
    else:
        verdict, warm = "Thin demand — hold stock for the next peak.", True

    with right:
        st.html('<div id="v2-results" style="height:0"></div>')
        with st.container(border=True):
            st.subheader("Demand through the day")
            v2.bars(curve)
            v2.note(f"<b>{DOW[dow]} {pd.to_datetime(d_str):%d %b}</b> · "
                    f"peak {peak_h:02d}:00 at {peak_v:.0f} bikes · daily average {day_avg:.0f} · "
                    f"selected hour {pred:.0f} ({pred-day_avg:+.0f} vs average)")

        with st.container(border=True):
            st.subheader("The week at a glance")
            st.caption("Seven days × 24 hours. The outlined tile is your selected hour.")
            base = pd.to_datetime(d_str)
            monday = base - pd.Timedelta(days=base.day_of_week)
            week = []
            for d in range(7):
                day = monday + pd.Timedelta(days=d)
                wd = 0 if day.day_of_week >= 5 else int(workingday)
                week.append(forecast(day.strftime("%Y-%m-%d"), season, 0, wd, weather,
                                     temp, atemp, humidity, windspeed))
            v2.heatmap(week, DOW, hour)

        c1, c2 = st.columns([1, 1], gap="large")
        with c1:
            with st.container(border=True):
                st.subheader("Weather sensitivity")
                st.caption("Same hour, four skies.")
                vals = [max(0.0, forecast(d_str, season, holiday, workingday, w,
                                          temp, atemp, humidity, windspeed)[hour])
                        for w in (1, 2, 3, 4)]
                v2.compare([WEATHER[w] for w in (1, 2, 3, 4)], vals, int(weather) - 1)
        with c2:
            with st.container(border=True):
                st.subheader("Fleet note")
                st.markdown(v2.tag(verdict, warm), unsafe_allow_html=True)
                v2.note(f"At <b>{hour:02d}:00</b> on a <b>{DOW[dow]}</b> with "
                        f"<b>{WEATHER[weather].lower()}</b>, the model expects <b>{pred} bikes</b>. "
                        f"Compare that with a daily average of {day_avg:.0f}.")


elif page == "Batch":
    v2.hero("bulk scoring", "A city in one file.",
            "Upload hourly records and score every row with the same model used above.",
            "—", "upload a CSV to begin", None,
            label="FILE READY", unit="awaiting upload", foot_label="Next step")
    v2.section("Score a file", "CSV columns: datetime, season, holiday, workingday, weather, temp, atemp, humidity, windspeed")
    left, right = st.columns([0.9, 2.1], gap="large")
    with left:
        with st.container(border=True):
            v2.label("SAMPLE")
            try:
                with open("data/test.csv", "rb") as fh:
                    st.download_button("Download test.csv", fh, "test.csv",
                                       use_container_width=True, type="primary")
            except FileNotFoundError:
                st.caption("Sample file unavailable.")
    with right:
        with st.container(border=True):
            f = st.file_uploader("Upload a CSV", type=["csv"])
            if f is not None:
                try:
                    out = score_upload(f)
                except ValueError as exc:
                    st.error(f"Could not score that file: {exc}")
                except Exception as exc:
                    st.error(f"Could not read that file: {exc}")
                else:
                    st.caption(f"{len(out):,} rows scored · average {out['count'].mean():.0f} · "
                               f"peak {out['count'].max():,}")
                    st.dataframe(out.head(15), use_container_width=True, hide_index=True)
                    st.download_button("Download predictions", out.to_csv(index=False),
                                       "submission.csv", use_container_width=True, type="primary")


elif page == "Insights":
    tr = load_train()
    tr["hour"] = tr["datetime"].dt.hour
    hourly = tr.groupby("hour")["count"].mean().tolist()
    v2.hero("from the training data", "What moves demand.",
            "Ten thousand eight hundred eighty-six hourly records. Hour of day dominates; "
            "weather and holidays write the footnotes.",
            f"{max(hourly):.0f}", "17:00 · 364 bikes", hourly,
            label="PEAK HOUR AVERAGE", unit="bikes / hour", foot_label="Busiest hour")
    v2.section("Signals", "the shape behind the predictions")
    c1, c2 = st.columns(2, gap="large")
    with c1:
        with st.container(border=True):
            st.subheader("Hourly profile")
            v2.bars(hourly)
            v2.note("Commuter peaks at <b>08:00</b> and <b>17:00–18:00</b>.")
    with c2:
        with st.container(border=True):
            st.subheader("Weather penalty")
            vals = tr.groupby("weather")["count"].mean().tolist()
            v2.compare([WEATHER[w] for w in (1, 2, 3, 4)], vals, -1)
            v2.note("Clear skies rent most; storms empty the racks.")


else:
    v2.hero("under the hood", "A model, not a mystery.",
            "Gradient-boosted trees learned the hourly rhythm of Capital Bikeshare. "
            "Every number you see is a prediction from that fitted model.",
            "0.53", "RMSLE · lower is better", None,
            label="MODEL ERROR", unit="RMSLE", foot_label="Leaderboard top")
    v2.section("Leaderboard", "held-out hours")
    v2.leaderboard([("Ridge baseline", 1.18, False), ("Random Forest", 0.71, False),
                    ("XGBoost", 0.65, False), ("HistGradientBoosting", 0.53, True)])
    v2.section("Reproduce", "four commands")
    with st.container(border=True):
        st.code("pip install -r requirements-dev.txt\npython src/train.py\n"
                "python src/predict.py\nstreamlit run app_v2.py", language="bash")

st.html('<div class="v2-footer">BikeShare demand studio · Capital Bikeshare 2011–2012 · '
        'built with Streamlit</div>')

