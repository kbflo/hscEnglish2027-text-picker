"""
NSW HSC English 2027 – Interactive Text Picker
Helps teachers choose valid text combinations that satisfy NESA requirements.
"""
import base64
import csv
import io
from datetime import datetime
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components

from data import (
    ADVANCED_COMMON,
    ADVANCED_CRIT,
    ADVANCED_TC_PAIRS,
    STANDARD_COMMON,
    STANDARD_LIC,
    STANDARD_CLOSE,
    EALD_FA1,
    EALD_FA2,
    EALD_FA3,
    EXT1_ELECTIVE_FULL_NAMES,
    EXT1_ELECTIVE_NAMES,
    EXT1_TEXTS,
    Text,
    TextPair,
    count_remaining_combinations,
    count_remaining_standard,
    count_remaining_eald,
    generate_all_valid_combinations,
    generate_all_valid_standard_combinations,
    generate_all_valid_eald_combinations,
    generate_all_valid_ext1_combos,
    get_compatible_texts,
    get_standard_compatible_texts,
    get_eald_compatible_texts,
    get_ext1_available,
    is_selection_complete,
    is_valid_combination,
    is_valid_standard_combination,
    is_valid_eald_combination,
    is_print_ext1,
    broad_category,
)

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="NSW HSC English 2027 – Interactive Text Picker",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =============================================================================
# CSS — forced dark appearance
# =============================================================================
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=DM+Sans:wght@400;500;600;700&display=swap');

/* ── Global — forced dark, near-black background ── */
.stApp {
    font-family: 'DM Sans', sans-serif;
    background-color: #111318 !important;
    color: #d4d4d8 !important;
}
h1, h2, h3, h4 {
    font-family: 'Source Serif 4', serif !important;
    color: #e4e4e7 !important;
}
[data-testid="stAppViewContainer"] { background-color: #111318 !important; }
[data-testid="stHeader"]           { background-color: #111318 !important; }
[data-testid="stSidebar"]          { background-color: #0e1016 !important; }

/* ── Prevent horizontal overflow at all viewport widths ── */
html, body { overflow-x: hidden !important; }
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    overflow-x: hidden !important;
    max-width: 100% !important;
}

/* Force all text light */
.stApp p, .stApp span, .stApp label, .stApp div,
.stApp [data-testid="stMarkdownContainer"],
.stApp [data-testid="stText"] {
    color: #d4d4d8 !important;
}

/* Force markdown containers to always be full width */
.stApp [data-testid="stMarkdownContainer"] {
    width: 100% !important;
}

/* Info box */
.stApp [data-testid="stAlert"]   { background-color: rgba(59,130,246,0.1) !important; color: #93c5fd !important; border-color: rgba(59,130,246,0.3) !important; }
.stApp [data-testid="stAlert"] p { color: #93c5fd !important; }

/* ── ALL buttons — forced dark ── */
.stApp .stButton > button,
.stApp .stDownloadButton > button {
    background-color: #1c1e24 !important;
    color: #d4d4d8 !important;
    border: 1px solid #2e3038 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
.stApp .stButton > button:hover,
.stApp .stDownloadButton > button:hover {
    background-color: #282a32 !important;
    border-color: #3e4048 !important;
    color: #f0f0f0 !important;
}
.stApp .stButton > button[kind="primary"] {
    background-color: #0f3460 !important;
    color: white !important;
    border-color: #1a4a80 !important;
}

/* Selectbox */
.stApp .stSelectbox > div > div {
    background-color: #1c1e24 !important;
    color: #d4d4d8 !important;
    border-color: #2e3038 !important;
}

/* Dividers */
.stApp hr { border-color: #1e2028 !important; }

/* Caption */
.stApp [data-testid="stCaptionContainer"],
.stApp [data-testid="stCaptionContainer"] p { color: #71717a !important; }

/* ── Hide Streamlit anchor links ── */
.stApp a.header-anchor,
.stApp [data-testid="stHeaderActionElements"],
.stApp .stMarkdown h1 a,
.stApp .stMarkdown h2 a,
.stApp .stMarkdown h3 a {
    display: none !important;
}

/* ── Reduce default Streamlit top padding ── */
[data-testid="stMainBlockContainer"] { padding-top: 0.75rem !important; }

/* ── Header banner — deep forest green ── */
.header-banner {
    background: linear-gradient(135deg, #0a2016 0%, #112e22 50%, #193a2a 100%);
    color: white;
    padding: 0.8rem 1.5rem;
    border-radius: 10px;
    margin-bottom: 0.7rem;
}
.header-banner h1 {
    margin: 0; font-size: 1.85rem; font-weight: 700; letter-spacing: -0.02em;
    color: white !important;
}
.header-banner p { margin: 0.2rem 0 0 0; opacity: 0.85; font-size: 0.95rem; color: white !important; }
.header-banner p .footnote { font-size: 0.76rem; opacity: 0.6; }

/* ── Focus area section headers ── */
.focus-area-header {
    border-left: 4px solid #475569;
    padding: 0.7rem 1rem;
    margin: 0.6rem 0 0.5rem 0;
    border-radius: 0 8px 8px 0;
    font-family: 'Source Serif 4', serif;
    font-weight: 600;
    font-size: 1.25rem;
    background: #181a20 !important;
    color: #e4e4e7 !important;
}
.fa-common  { border-left-color: #60a5fa; }
.fa-tc      { border-left-color: #6bb8ae; }
.fa-crit    { border-left-color: #e03028; }
.fa-ext1    { border-left-color: #9070e0; }
.fa-ext1-0  { border-left-color: #e03028; }
.fa-ext1-1  { border-left-color: #6bb8ae; }
.fa-ext1-2  { border-left-color: #60a5fa; }
.fa-ext1-3  { border-left-color: #5cb87a; }
.fa-ext1-4  { border-left-color: #9070e0; }
.fa-fav     { border-left-color: #f59e0b; }

/* ── PICKER ROW — CSS Grid layout for radio + card ── */
.picker-row {
    display: grid;
    grid-template-columns: 2.2rem 1fr;
    gap: 0.5rem;
    align-items: start;
    margin: 0.15rem 0;
    max-width: 940px;
    width: 100%;
}
.picker-radio {
    width: 2.2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    padding-top: 0.65rem;
    font-size: 1.1rem;
}
.picker-radio .radio-circle {
    width: 1.8rem;
    height: 1.8rem;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    cursor: pointer;
    color: #94a3b8;
    transition: background-color 0.15s;
}
.picker-radio .radio-circle:hover {
    filter: brightness(1.3);
}
.radio-common  .radio-circle { background-color: #123060; }
.radio-tc      .radio-circle { background-color: #224a46; }
.radio-crit    .radio-circle { background-color: #420c0c; }
.radio-ext1    .radio-circle { background-color: #2c2050; }
.radio-ext1-0  .radio-circle { background-color: #420c0c; }
.radio-ext1-1  .radio-circle { background-color: #224a46; }
.radio-ext1-2  .radio-circle { background-color: #123060; }
.radio-ext1-3  .radio-circle { background-color: #1a3018; }
.radio-ext1-4  .radio-circle { background-color: #2c2050; }
.picker-card {
    min-width: 0;
}

/* ── TEXT CARD ── */
.text-card {
    border-radius: 10px;
    padding: 0.75rem 1rem;
    box-sizing: border-box;
}
.text-card .text-line {
    display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap; padding: 0.15rem 0;
}
.text-card .author  { font-weight: 600; color: #f1f5f9; font-size: 0.95rem; }
.text-card .sep     { color: rgba(148,163,184,0.5); }
.text-card .title   { font-family: 'Source Serif 4', serif; font-style: italic; color: #cbd5e1; font-size: 0.95rem; }
.text-card .meta    { font-size: 0.78rem; color: #a0aab8; margin-top: 0.1rem; padding-left: 0.1rem; }

/* Section colours — background stays constant; only border changes on selection */
.card-common          { background: #163d72; border: 1px solid #235090; }
.card-common.selected { background: #163d72; border: 2px solid #60a5fa; }
.card-tc              { background: #1a3a38; border: 1px solid #2d4a47; }
.card-tc.selected     { background: #1a3a38; border: 2px solid #6bb8ae; }
.card-crit            { background: #4a0e0e; border: 1px solid #7a1818; }
.card-crit.selected   { background: #4a0e0e; border: 2px solid #e03028; }
.card-ext1            { background: #221840; border: 1px solid #352860; }
.card-ext1.selected   { background: #221840; border: 2px solid #9070e0; }
/* Per-elective card colours for Extension 1 */
.card-ext1-0          { background: #4a0e0e; border: 1px solid #7a1818; }
.card-ext1-0.selected { background: #4a0e0e; border: 2px solid #e03028; }
.card-ext1-1          { background: #1a3a38; border: 1px solid #2d4a47; }
.card-ext1-1.selected { background: #1a3a38; border: 2px solid #6bb8ae; }
.card-ext1-2          { background: #163d72; border: 1px solid #235090; }
.card-ext1-2.selected { background: #163d72; border: 2px solid #60a5fa; }
.card-ext1-3          { background: #1a3820; border: 1px solid #2d5030; }
.card-ext1-3.selected { background: #1a3820; border: 2px solid #5cb87a; }
.card-ext1-4          { background: #221840; border: 1px solid #352860; }
.card-ext1-4.selected { background: #221840; border: 2px solid #9070e0; }

/* ── Type badges — frosted neutral background, coloured text + border ── */
/* rgba(255,255,255,0.10) lifts the badge off any card background equally,    */
/* so the same badge reads consistently across the blue, teal, and wine cards. */
.type-badge {
    display: inline-flex; align-items: center; gap: 0.2rem;
    padding: 0.12rem 0.5rem; border-radius: 4px;
    font-size: 0.7rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.03em; vertical-align: middle; white-space: nowrap; line-height: 1.4;
    background: rgba(255,255,255,0.10);
}
/* Double-class selectors give (0,2,0) specificity, beating .stApp span (0,1,1) */
.type-badge.type-prose       { color: #82bae0 !important; border: 1.5px solid rgba(130,186,224,0.65); }
.type-badge.type-poetry      { color: #d498c0 !important; border: 1.5px solid rgba(212,152,192,0.65); }
.type-badge.type-drama       { color: #d4b860 !important; border: 1.5px solid rgba(212,184, 96,0.65); }
.type-badge.type-nonfiction  { color: #74c4a0 !important; border: 1.5px solid rgba(116,196,160,0.65); }
.type-badge.type-film        { color: #a898d0 !important; border: 1.5px solid rgba(168,152,208,0.65); }
.type-badge.type-media       { color: #e8a840 !important; border: 1.5px solid rgba(232,168,64,0.65); }
.type-badge.type-shakespeare { color: #ddd8c4 !important; border: 1.5px solid rgba(221,216,196,0.65); }

/* ── Complete banner ── */
.complete-banner {
    background: #22252d;
    border: 1px solid #3a3e48;
    color: white; padding: 0.5rem 0.9rem; border-radius: 8px;
    margin: 0.4rem 0; display: inline-block;
}
.complete-banner h3 { color: #d4d4d8 !important; margin: 0; font-size: 0.95rem; }
.complete-banner p  { color: #8a8f9e !important; margin: 0.15rem 0 0 0; font-size: 0.82rem; }


/* ── Favourites ── */
.fav-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; max-width: 1100px; }
.fav-table th {
    text-align: left; padding: 0.4rem 0.6rem;
    border-bottom: 2px solid #2a2e38;
    font-weight: 600; color: #94a3b8 !important;
    font-size: 0.78rem; letter-spacing: 0.02em;
}
.fav-table td {
    padding: 0.5rem 0.6rem;
    border-bottom: 1px solid rgba(100,116,139,0.15);
    vertical-align: top; color: #d4d4d8 !important;
}
.fav-table .fav-author { font-weight: 600; color: #e4e4e7 !important; }
.fav-table .fav-title  { font-family: 'Source Serif 4', serif; font-style: italic; color: #94a3b8 !important; }
.fav-hdr-row {
    display: flex; align-items: center; gap: 0.6rem;
    margin: 1rem 0 0.3rem 0;
}
.fav-course-heading {
    font-family: 'Source Serif 4', serif; font-weight: 600; font-size: 1.1rem;
    color: #e4e4e7 !important;
}
.fav-csv-btn {
    display: inline-block; text-decoration: none;
    padding: 0.15rem 0.45rem; border-radius: 5px;
    background-color: #1c1e24; color: #94a3b8 !important;
    border: 1px solid #2e3038; font-size: 0.72rem;
    transition: background-color 0.15s, border-color 0.15s;
}
.fav-csv-btn:hover { background-color: #282a32 !important; border-color: #3e4048 !important; color: #d4d4d8 !important; }
/* ── All-combinations custom download link-button ── */
.custom-dl-btn {
    display: block; width: 100%; box-sizing: border-box;
    text-align: center; text-decoration: none;
    padding: 0.38rem 0.6rem; border-radius: 6px;
    background-color: #1c1e24; color: #d4d4d8 !important;
    border: 1px solid #2e3038; font-size: 0.76rem; line-height: 1.4;
    transition: background-color 0.15s, border-color 0.15s;
}
.custom-dl-btn:hover { background-color: #282a32 !important; border-color: #3e4048 !important; color: #f0f0f0 !important; }
.custom-dl-btn strong { font-weight: 900; color: #ffffff; }

/* ── Fav row delete button (inside first table cell) ── */
.fav-del {
    display: block;
    cursor: pointer;
    opacity: 0.65;
    font-size: 1.15rem;
    margin-top: 0.3rem;
    transition: opacity 0.15s;
    user-select: none;
}
.fav-del:hover { opacity: 1.0; }

/* ── Course buttons — per-course colours ── */
/* Must match specificity of .stApp .stButton > button to override it */
.stApp .stButton > button.course-btn-adv { background-color: #0e1e38 !important; border-color: #1e3660 !important; color: #7ab0e8 !important; }
.stApp .stButton > button.course-btn-adv:hover { background-color: #152a50 !important; border-color: #2a4880 !important; color: #a0c8f0 !important; }
.stApp .stButton > button.course-btn-adv[data-testid="baseButton-primary"] { background-color: #0d2a50 !important; border-color: #60a5fa !important; color: #bdd8f8 !important; }
.stApp .stButton > button.course-btn-std { background-color: #0c2018 !important; border-color: #183828 !important; color: #7ab8a0 !important; }
.stApp .stButton > button.course-btn-std:hover { background-color: #112a20 !important; border-color: #2a5040 !important; color: #a0d8c0 !important; }
.stApp .stButton > button.course-btn-std[data-testid="baseButton-primary"] { background-color: #0a2820 !important; border-color: #6bb8ae !important; color: #b0e0d8 !important; }
.stApp .stButton > button.course-btn-eald { background-color: #261c08 !important; border-color: #483010 !important; color: #c8a060 !important; }
.stApp .stButton > button.course-btn-eald:hover { background-color: #362808 !important; border-color: #604018 !important; color: #e0b870 !important; }
.stApp .stButton > button.course-btn-eald[data-testid="baseButton-primary"] { background-color: #3a2000 !important; border-color: #f59e0b !important; color: #fcd34d !important; }
.stApp .stButton > button.course-btn-ext1 { background-color: #1e1638 !important; border-color: #3a2860 !important; color: #c0b0e8 !important; }
.stApp .stButton > button.course-btn-ext1:hover { background-color: #2a1e50 !important; border-color: #5040a0 !important; color: #d8ccfc !important; }
.stApp .stButton > button.course-btn-ext1[data-testid="baseButton-primary"] { background-color: #1c1040 !important; border-color: #9070e0 !important; color: #c4b0f8 !important; }

/* ── Course-coloured instruction boxes ── */
.course-info {
    padding: 0.55rem 1rem; border-radius: 6px; margin: 0.4rem 0;
    font-size: 0.92rem; border-left: 4px solid;
}
.course-info-adv  { background: rgba(96,165,250,0.16);  border-left-color: #60a5fa; color: #c4dffb !important; }
.course-info-std  { background: rgba(107,184,174,0.16); border-left-color: #6bb8ae; color: #c0e8e0 !important; }
.course-info-eald { background: rgba(245,158,11,0.16);  border-left-color: #f59e0b; color: #fde68a !important; }
.course-info-ext1 { background: rgba(144,112,224,0.16); border-left-color: #9070e0; color: #d4c8fc !important; }
.course-info strong, .course-info b { color: inherit !important; }
</style>
""", unsafe_allow_html=True)

# Inject JS via same-origin iframe (window.parent.document access).
# Two separate problems need two separate solutions:
#   1. HIDING the "select" buttons: done via a <style> tag injected into the
#      parent document's <head>. CSS rules are immune to React overwriting inline
#      styles on re-render, so the buttons stay hidden permanently.
#   2. CLICKING on a card row: done via document-level event delegation.
#      Never stores references to specific button elements, so there are no
#      stale-closure issues when React replaces elements on re-render. At click
#      time it walks forward from the clicked row to find the live button.
components.html("""
<script>
(function () {
  try {
    var p = window.parent, doc = p.document;

    // ── 1. CSS injection (runs once; persists across rerenders) ──────────────
    // Hide every element-container that immediately follows a picker-row
    // container and contains a button. Uses :has() — Chrome 105+, Safari 15.4+,
    // Firefox 121+, which covers all modern browsers as of 2026.
    if (!p.__pickerStyle) {
      var s = doc.createElement('style');
      s.textContent =
        '[data-testid="stVerticalBlock"]>div:has(.picker-row)+div:has(button){' +
        'height:0!important;overflow:hidden!important;' +
        'margin:0!important;padding:0!important;}';
      doc.head.appendChild(s);
      p.__pickerStyle = s;
    }

    // ── 2. Document-level click delegation (runs once; no per-element wiring) ─
    // On every click, check if it landed inside a .picker-row. If so, walk
    // forward through the DOM siblings to find the nearest "select" button and
    // programmatically click it. Dynamic lookup means no stale references.
    if (!p.__pickerClick) {
      p.__pickerClick = true;
      doc.addEventListener('click', function (e) {
        // ── Picker row click → find and fire its "select" button ──
        var row = e.target.closest('.picker-row');
        if (row) {
          var el = row, rowCont = null;
          while (el && el.parentElement) {
            if (el.parentElement.getAttribute('data-testid') === 'stVerticalBlock') {
              rowCont = el; break;
            }
            el = el.parentElement;
          }
          if (rowCont) {
            var sibs = Array.from(rowCont.parentElement.children);
            var idx  = sibs.indexOf(rowCont);
            for (var i = idx + 1; i < sibs.length; i++) {
              if (sibs[i].querySelector('.picker-row')) break;
              var btn = sibs[i].querySelector('button');
              var t = btn.textContent.trim();
              if (btn && (t === 'select' || t === 'deselect')) { btn.click(); return; }
            }
          }
          return;
        }

        // ── Fav delete click → find and fire the Nth hidden delete button ──
        var del = e.target.closest('.fav-del');
        if (del) {
          var delSeq = parseInt(del.getAttribute('data-del') || '0');
          var el2 = del, delCont = null;
          while (el2 && el2.parentElement) {
            if (el2.parentElement.getAttribute('data-testid') === 'stVerticalBlock') {
              delCont = el2; break;
            }
            el2 = el2.parentElement;
          }
          if (delCont) {
            var sibs2 = Array.from(delCont.parentElement.children);
            var idx2  = sibs2.indexOf(delCont);
            var btnCount = 0;
            for (var j = idx2 + 1; j < sibs2.length; j++) {
              if (sibs2[j].querySelector('.fav-table')) break;
              var btn2 = sibs2[j].querySelector('button');
              if (btn2) {
                if (btnCount === delSeq) { btn2.click(); return; }
                btnCount++;
              }
            }
          }
          return;
        }
      });
    }

    // ── 3. Pointer cursor on picker rows + course button colouring ──
    var courseBtnMap = {'Advanced':'course-btn-adv','Standard':'course-btn-std','EAL/D':'course-btn-eald','Extension 1':'course-btn-ext1'};
    function refreshDOM() {
      doc.querySelectorAll('.picker-row').forEach(function (r) { r.style.cursor = 'pointer'; });
      doc.querySelectorAll('button').forEach(function (btn) {
        var t = btn.textContent.trim();
        if (courseBtnMap[t]) btn.classList.add(courseBtnMap[t]);
      });
      // Hide fav delete buttons (those immediately after a fav-table, until a non-delete element)
      doc.querySelectorAll('[data-testid="stVerticalBlock"]').forEach(function(vb) {
        var children = Array.from(vb.children), afterTable = false;
        for (var k = 0; k < children.length; k++) {
          var child = children[k];
          if (child.querySelector('.fav-table')) { afterTable = true; continue; }
          if (afterTable) {
            var btn = child.querySelector('button');
            if (btn) {
              child.style.height = '0'; child.style.overflow = 'hidden';
              child.style.margin = '0'; child.style.padding = '0';
            } else { afterTable = false; }
          }
        }
      });
    }
    refreshDOM();
    if (!p.__pickerObs) {
      p.__pickerObs = new MutationObserver(function () {
        if (p.__pickerRaf) p.cancelAnimationFrame(p.__pickerRaf);
        p.__pickerRaf = p.requestAnimationFrame(refreshDOM);
      });
      p.__pickerObs.observe(doc.body, { childList: true, subtree: true });
    }

  } catch (e) { console.warn('picker-wire:', e); }
})();
</script>
""", height=0, scrolling=False)

# =============================================================================
# SESSION STATE
# =============================================================================
_LIST_KEYS = {"favourites", "chosen_ext1_text_idxs"}
for key in ["favourites", "chosen_pair_idx", "chosen_crit_idx", "chosen_common_idx",
            "chosen_std_common_idx", "chosen_std_lic_idx", "chosen_std_close_idx",
            "chosen_eald_fa1_idx", "chosen_eald_fa2_idx", "chosen_eald_fa3_idx",
            "chosen_ext1_elective_idx", "chosen_ext1_text_idxs"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key in _LIST_KEYS else None
if "last_course" not in st.session_state:
    st.session_state.last_course = None  # no pre-selection on first run
if "picker_active" not in st.session_state:
    st.session_state.picker_active = True


def reset_picker():
    for k in ["chosen_pair_idx", "chosen_crit_idx", "chosen_common_idx",
              "chosen_std_common_idx", "chosen_std_lic_idx", "chosen_std_close_idx",
              "chosen_eald_fa1_idx", "chosen_eald_fa2_idx", "chosen_eald_fa3_idx",
              "chosen_ext1_elective_idx"]:
        st.session_state[k] = None
    st.session_state.chosen_ext1_text_idxs = []
    st.session_state.picker_active = True


def clear_favourites():
    st.session_state.favourites = []


# =============================================================================
# HELPERS
# =============================================================================
def type_badge(cat: str) -> str:
    c = cat.lower()
    if "shakespeare" in c:
        return '<span class="type-badge type-shakespeare">Shakespeare \U0001F3AD</span>'
    if "prose" in c:
        return '<span class="type-badge type-prose">Prose fiction \U0001F4D6</span>'
    if "poetry" in c:
        return '<span class="type-badge type-poetry">Poetry \U0001FAB6</span>'
    if "drama" in c:
        return '<span class="type-badge type-drama">Drama \U0001F3AD</span>'
    if "nonfiction" in c:
        return '<span class="type-badge type-nonfiction">Nonfiction \U0001F4CB</span>'
    if "film" in c:
        return '<span class="type-badge type-film">Film \U0001F3AC</span>'
    if "media" in c:
        return '<span class="type-badge type-media">Media \U0001F4FA</span>'
    return f'<span class="type-badge type-prose">{cat}</span>'


def text_line_html(text: Text) -> str:
    sels = f'<div class="meta">{text.selections}</div>' if text.selections else ""
    return (
        f'<div class="text-line">'
        f'<span class="author">{text.author}</span>'
        f'<span class="sep"> · </span>'
        f'<span class="title">{text.title}</span>'
        f'{type_badge(text.text_type_category)}'
        f'</div>'
        f'{sels}'
    )


def fav_cell(text: Text) -> str:
    return f'<span class="fav-author">{text.author}</span><br><span class="fav-title">{text.title}</span>'


def _text_rows_csv(writer, combo_num: int, focus_area: str, text: Text):
    writer.writerow([combo_num, focus_area, text.author, text.title, text.text_type_category, text.selections or ""])


def make_fav_csv(course_filter: str) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Option #", "Focus area", "Author", "Title", "Category", "Selections"])
    combo_num = 0
    for fav in st.session_state.favourites:
        if fav["course"] != course_filter:
            continue
        combo_num += 1
        if course_filter == "English Advanced":
            pair, crit, common = fav["pair"], fav["crit"], fav["common"]
            _text_rows_csv(writer, combo_num, "Texts and human experiences", common)
            _text_rows_csv(writer, combo_num, "Textual conversations", pair.text_a)
            _text_rows_csv(writer, combo_num, "Textual conversations", pair.text_b)
            _text_rows_csv(writer, combo_num, "Critical study of literature", crit)
        elif course_filter == "English EAL/D":
            fa1, fa2, fa3 = fav["fa1"], fav["fa2"], fav["fa3"]
            _text_rows_csv(writer, combo_num, "Texts and human experiences", fa1)
            _text_rows_csv(writer, combo_num, "Language, identity and culture", fa2)
            _text_rows_csv(writer, combo_num, "Close study of text", fa3)
        elif course_filter == "English Extension 1":
            e_idx = fav["elective_idx"]
            elective_name = EXT1_ELECTIVE_FULL_NAMES[e_idx]
            for ti in fav["text_idxs"]:
                _text_rows_csv(writer, combo_num, elective_name, EXT1_TEXTS[e_idx][ti])
        else:
            common, lic, close = fav["common"], fav["lic"], fav["close"]
            _text_rows_csv(writer, combo_num, "Texts and human experiences", common)
            _text_rows_csv(writer, combo_num, "Language, identity and culture", lic)
            _text_rows_csv(writer, combo_num, "Close study of literature", close)
    return output.getvalue()


def make_all_combos_csv(course: str) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Option #", "Focus area", "Author", "Title", "Category", "Selections"])
    if course == "English Advanced":
        for i, (pair, crit, common) in enumerate(generate_all_valid_combinations(), 1):
            _text_rows_csv(writer, i, "Texts and human experiences", common)
            _text_rows_csv(writer, i, "Textual conversations", pair.text_a)
            _text_rows_csv(writer, i, "Textual conversations", pair.text_b)
            _text_rows_csv(writer, i, "Critical study of literature", crit)
    elif course == "English Standard":
        for i, (common, lic, close) in enumerate(generate_all_valid_standard_combinations(), 1):
            _text_rows_csv(writer, i, "Texts and human experiences", common)
            _text_rows_csv(writer, i, "Language, identity and culture", lic)
            _text_rows_csv(writer, i, "Close study of literature", close)
    elif course == "English EAL/D":
        for i, (fa1, fa2, fa3) in enumerate(generate_all_valid_eald_combinations(), 1):
            _text_rows_csv(writer, i, "Texts and human experiences", fa1)
            _text_rows_csv(writer, i, "Language, identity and culture", fa2)
            _text_rows_csv(writer, i, "Close study of text", fa3)
    elif course == "English Extension 1":
        for i, (e_idx, t1, t2, t3) in enumerate(generate_all_valid_ext1_combos(), 1):
            elective_name = EXT1_ELECTIVE_FULL_NAMES[e_idx]
            for ti in [t1, t2, t3]:
                _text_rows_csv(writer, i, elective_name, EXT1_TEXTS[e_idx][ti])
    return output.getvalue()


# =============================================================================
# Selection helpers
# =============================================================================
def adv_sel_count():
    return sum(1 for k in ["chosen_pair_idx", "chosen_crit_idx", "chosen_common_idx"]
               if st.session_state[k] is not None)

def std_sel_count():
    return sum(1 for k in ["chosen_std_common_idx", "chosen_std_lic_idx", "chosen_std_close_idx"]
               if st.session_state[k] is not None)

def eald_sel_count():
    return sum(1 for k in ["chosen_eald_fa1_idx", "chosen_eald_fa2_idx", "chosen_eald_fa3_idx"]
               if st.session_state[k] is not None)

def ext1_sel_count():
    return len(st.session_state.chosen_ext1_text_idxs)

def is_complete(course_: str) -> bool:
    if course_ == "English Advanced":
        return adv_sel_count() == 3
    if course_ == "English EAL/D":
        return eald_sel_count() == 3
    if course_ == "English Extension 1":
        return ext1_sel_count() == 3
    return std_sel_count() == 3

def add_current_as_favourite(course_: str):
    if course_ == "English Advanced":
        pair = ADVANCED_TC_PAIRS[st.session_state.chosen_pair_idx]
        crit = ADVANCED_CRIT[st.session_state.chosen_crit_idx]
        common = ADVANCED_COMMON[st.session_state.chosen_common_idx]
        fav = {"course": "English Advanced", "pair": pair, "crit": crit, "common": common}
        already = any(
            f.get("course") == "English Advanced" and
            f.get("pair", object()).label == pair.label and
            f.get("crit", object()).author == crit.author and
            f.get("common", object()).author == common.author
            for f in st.session_state.favourites)
        if not already:
            st.session_state.favourites.append(fav)
    elif course_ == "English EAL/D":
        fa1 = EALD_FA1[st.session_state.chosen_eald_fa1_idx]
        fa2 = EALD_FA2[st.session_state.chosen_eald_fa2_idx]
        fa3 = EALD_FA3[st.session_state.chosen_eald_fa3_idx]
        fav = {"course": "English EAL/D", "fa1": fa1, "fa2": fa2, "fa3": fa3}
        already = any(
            f.get("course") == "English EAL/D" and
            f.get("fa1", object()).author == fa1.author and
            f.get("fa2", object()).author == fa2.author and
            f.get("fa3", object()).author == fa3.author
            for f in st.session_state.favourites)
        if not already:
            st.session_state.favourites.append(fav)
    elif course_ == "English Extension 1":
        e_idx = st.session_state.chosen_ext1_elective_idx
        t_idxs = list(st.session_state.chosen_ext1_text_idxs)
        fav = {"course": "English Extension 1", "elective_idx": e_idx, "text_idxs": t_idxs}
        already = any(
            f.get("course") == "English Extension 1" and
            f.get("elective_idx") == e_idx and
            sorted(f.get("text_idxs", [])) == sorted(t_idxs)
            for f in st.session_state.favourites)
        if not already:
            st.session_state.favourites.append(fav)
    else:
        common = STANDARD_COMMON[st.session_state.chosen_std_common_idx]
        lic = STANDARD_LIC[st.session_state.chosen_std_lic_idx]
        close = STANDARD_CLOSE[st.session_state.chosen_std_close_idx]
        fav = {"course": "English Standard", "common": common, "lic": lic, "close": close}
        already = any(
            f.get("course") == "English Standard" and
            f.get("common", object()).author == common.author and
            f.get("lic", object()).author == lic.author and
            f.get("close", object()).author == close.author
            for f in st.session_state.favourites)
        if not already:
            st.session_state.favourites.append(fav)
    st.session_state.picker_active = False


# =============================================================================
# HEADER
# =============================================================================
st.markdown("""
<div class="header-banner">
    <h1 style="margin:0;">NSW HSC English 2027 – interactive text picker</h1>
    <p>Build valid text combinations for 2027–2030 (Advanced, Standard, EAL/D, Extension 1)*. Each selected combination is added to a downloadable favourites list.<br><span class="footnote">*Based on NESA prescriptions D2025/464194</span></p>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# TOP CONTROLS — course selection
# =============================================================================
course = st.session_state.last_course

st.markdown('<div class="focus-area-header">📚 Create New Text Combination</div>', unsafe_allow_html=True)

c_adv, c_std, c_eald, c_ext1, c_dl = st.columns([1, 1, 1, 1.2, 2])

with c_adv:
    if st.button("Advanced", use_container_width=True,
                 type="primary" if course == "English Advanced" else "secondary",
                 key="course_btn_adv"):
        st.session_state.last_course = "English Advanced"
        reset_picker()
        st.rerun()

with c_std:
    if st.button("Standard", use_container_width=True,
                 type="primary" if course == "English Standard" else "secondary",
                 key="course_btn_std"):
        st.session_state.last_course = "English Standard"
        reset_picker()
        st.rerun()

with c_eald:
    if st.button("EAL/D", use_container_width=True,
                 type="primary" if course == "English EAL/D" else "secondary",
                 key="course_btn_eald"):
        st.session_state.last_course = "English EAL/D"
        reset_picker()
        st.rerun()

with c_ext1:
    if st.button("Extension 1", use_container_width=True,
                 type="primary" if course == "English Extension 1" else "secondary",
                 key="course_btn_ext1"):
        st.session_state.last_course = "English Extension 1"
        reset_picker()
        st.rerun()

with c_dl:
    if course is not None:
        if course == "English Advanced":
            all_csv = make_all_combos_csv("English Advanced")
            valid_count = len(generate_all_valid_combinations())
        elif course == "English EAL/D":
            all_csv = make_all_combos_csv("English EAL/D")
            valid_count = len(generate_all_valid_eald_combinations())
        elif course == "English Extension 1":
            all_csv = make_all_combos_csv("English Extension 1")
            valid_count = len(generate_all_valid_ext1_combos())
        else:
            all_csv = make_all_combos_csv("English Standard")
            valid_count = len(generate_all_valid_standard_combinations())
        csv_b64 = base64.b64encode(all_csv.encode()).decode()
        fname = f"HSC_{course.replace(' ', '_')}_all_valid_combinations.csv"
        st.markdown(
            f'<a href="data:text/csv;base64,{csv_b64}" download="{fname}" class="custom-dl-btn">'
            f'📥 Download all {valid_count} valid combinations for <strong>{course}</strong></a>',
            unsafe_allow_html=True,
        )

st.markdown("---")

if course is None:
    st.markdown('<p style="color:#71717a;text-align:center;padding:1rem 0;">Select a course above to begin.</p>', unsafe_allow_html=True)
else:
    # Check if combination just completed
    if is_complete(course) and st.session_state.picker_active:
        add_current_as_favourite(course)


# =============================================================================
# RENDER PICKER SECTION
# The key insight: render the radio indicator + card as a SINGLE HTML block,
# then immediately follow with a hidden st.button for click capture.
# This avoids st.columns entirely for picker rows, so no responsive stacking.
# =============================================================================
def render_section(label: str, texts, available, chosen_idx, state_key: str,
                   key_prefix: str, card_class: str, fa_class: str,
                   radio_class: str, is_pair: bool = False):
    st.markdown(f'<div class="focus-area-header {fa_class}">{label}</div>', unsafe_allow_html=True)
    for i, item in enumerate(texts):
        is_selected = (chosen_idx == i)
        if not st.session_state.picker_active and not is_selected:
            continue
        if st.session_state.picker_active and not is_selected and item not in available:
            continue

        # Build the radio indicator
        if is_selected:
            radio_html = '<div class="picker-radio"><span style="font-size:1.1rem;">✅</span></div>'
        elif st.session_state.picker_active:
            radio_html = f'<div class="picker-radio {radio_class}"><div class="radio-circle">○</div></div>'
        else:
            radio_html = '<div class="picker-radio"></div>'

        # Build card content
        if is_pair:
            card_content = text_line_html(item.text_a) + text_line_html(item.text_b)
        else:
            card_content = text_line_html(item)

        sel_cls = "  selected" if is_selected else ""
        card_html = f'<div class="picker-card"><div class="text-card card-{card_class}{sel_cls}">{card_content}</div></div>'

        # Render entire row as one HTML block
        st.markdown(f'<div class="picker-row">{radio_html}{card_html}</div>', unsafe_allow_html=True)

        # Button for click capture — hidden and wired to card row by JS injection
        if not is_selected and st.session_state.picker_active:
            if st.button("select", key=f"{key_prefix}_{i}"):
                st.session_state[state_key] = i
                st.rerun()


# =============================================================================
# ADVANCED PICKER
# =============================================================================
if course == "English Advanced":
    chosen_pair = ADVANCED_TC_PAIRS[st.session_state.chosen_pair_idx] if st.session_state.chosen_pair_idx is not None else None
    chosen_crit = ADVANCED_CRIT[st.session_state.chosen_crit_idx] if st.session_state.chosen_crit_idx is not None else None
    chosen_common = ADVANCED_COMMON[st.session_state.chosen_common_idx] if st.session_state.chosen_common_idx is not None else None

    avail_pairs, avail_crits, avail_commons = get_compatible_texts(chosen_pair, chosen_crit, chosen_common)
    complete = not st.session_state.picker_active

    if adv_sel_count() == 0 and st.session_state.picker_active:
        st.markdown('<div class="course-info course-info-adv"><strong>CLICK ANY TEXT</strong> from any focus area below to start building a combination. Incompatible choices will be eliminated as you go.</div>', unsafe_allow_html=True)
    elif st.session_state.picker_active:
        parts = []
        if chosen_common: parts.append(f"THE: **{chosen_common.author}**")
        if chosen_pair: parts.append(f"TC: **{chosen_pair.label}**")
        if chosen_crit: parts.append(f"Crit: **{chosen_crit.author}**")
        st.markdown(f"**Selected** ({adv_sel_count()}/3): " + " · ".join(parts))

    if complete:
        st.markdown('<div class="complete-banner"><h3>✅ Combination added to favourites</h3><p>Scroll down to see your favourites, or start a new combination.</p></div>', unsafe_allow_html=True)

    render_section("Texts and human experiences", ADVANCED_COMMON, avail_commons,
                   st.session_state.chosen_common_idx, "chosen_common_idx", "common",
                   "common", "fa-common", "radio-common")
    render_section("Textual conversations", ADVANCED_TC_PAIRS, avail_pairs,
                   st.session_state.chosen_pair_idx, "chosen_pair_idx", "pair",
                   "tc", "fa-tc", "radio-tc", is_pair=True)
    render_section("Critical study of literature", ADVANCED_CRIT, avail_crits,
                   st.session_state.chosen_crit_idx, "chosen_crit_idx", "crit",
                   "crit", "fa-crit", "radio-crit")

    if complete:
        if st.button("＋ New combination", key="bottom_new_adv"):
            reset_picker()
            st.rerun()


# =============================================================================
# STANDARD PICKER
# =============================================================================
elif course == "English Standard":
    chosen_common = STANDARD_COMMON[st.session_state.chosen_std_common_idx] if st.session_state.chosen_std_common_idx is not None else None
    chosen_lic = STANDARD_LIC[st.session_state.chosen_std_lic_idx] if st.session_state.chosen_std_lic_idx is not None else None
    chosen_close = STANDARD_CLOSE[st.session_state.chosen_std_close_idx] if st.session_state.chosen_std_close_idx is not None else None

    avail_commons, avail_lics, avail_closes = get_standard_compatible_texts(chosen_common, chosen_lic, chosen_close)
    complete = not st.session_state.picker_active

    if std_sel_count() == 0 and st.session_state.picker_active:
        st.markdown('<div class="course-info course-info-std"><strong>CLICK ANY TEXT</strong> from any focus area below to start building a combination. Incompatible choices will be eliminated as you go.</div>', unsafe_allow_html=True)
    elif st.session_state.picker_active:
        parts = []
        if chosen_common: parts.append(f"THE: **{chosen_common.author}**")
        if chosen_lic: parts.append(f"LIC: **{chosen_lic.author}**")
        if chosen_close: parts.append(f"Close: **{chosen_close.author}**")
        st.markdown(f"**Selected** ({std_sel_count()}/3): " + " · ".join(parts))

    if complete:
        st.markdown('<div class="complete-banner"><h3>✅ Combination added to favourites</h3><p>Scroll down to see your favourites, or start a new combination.</p></div>', unsafe_allow_html=True)

    render_section("Texts and human experiences", STANDARD_COMMON, avail_commons,
                   st.session_state.chosen_std_common_idx, "chosen_std_common_idx", "std_common",
                   "common", "fa-common", "radio-common")
    render_section("Language, identity and culture", STANDARD_LIC, avail_lics,
                   st.session_state.chosen_std_lic_idx, "chosen_std_lic_idx", "std_lic",
                   "tc", "fa-tc", "radio-tc")
    render_section("Close study of literature", STANDARD_CLOSE, avail_closes,
                   st.session_state.chosen_std_close_idx, "chosen_std_close_idx", "std_close",
                   "crit", "fa-crit", "radio-crit")

    if complete:
        if st.button("＋ New combination", key="bottom_new_std"):
            reset_picker()
            st.rerun()


# =============================================================================
# EAL/D PICKER
# =============================================================================
elif course == "English EAL/D":
    chosen_fa1 = EALD_FA1[st.session_state.chosen_eald_fa1_idx] if st.session_state.chosen_eald_fa1_idx is not None else None
    chosen_fa2 = EALD_FA2[st.session_state.chosen_eald_fa2_idx] if st.session_state.chosen_eald_fa2_idx is not None else None
    chosen_fa3 = EALD_FA3[st.session_state.chosen_eald_fa3_idx] if st.session_state.chosen_eald_fa3_idx is not None else None

    avail_fa1, avail_fa2, avail_fa3 = get_eald_compatible_texts(chosen_fa1, chosen_fa2, chosen_fa3)
    complete = not st.session_state.picker_active

    if eald_sel_count() == 0 and st.session_state.picker_active:
        st.markdown('<div class="course-info course-info-eald"><strong>CLICK ANY TEXT</strong> from any focus area below to start building a combination. Incompatible choices will be eliminated as you go.</div>', unsafe_allow_html=True)
    elif st.session_state.picker_active:
        parts = []
        if chosen_fa1: parts.append(f"THE: **{chosen_fa1.author}**")
        if chosen_fa2: parts.append(f"LIC: **{chosen_fa2.author}**")
        if chosen_fa3: parts.append(f"Close: **{chosen_fa3.author}**")
        st.markdown(f"**Selected** ({eald_sel_count()}/3): " + " · ".join(parts))

    if complete:
        st.markdown('<div class="complete-banner"><h3>✅ Combination added to favourites</h3><p>Scroll down to see your favourites, or start a new combination.</p></div>', unsafe_allow_html=True)

    render_section("Texts and human experiences", EALD_FA1, avail_fa1,
                   st.session_state.chosen_eald_fa1_idx, "chosen_eald_fa1_idx", "eald_fa1",
                   "common", "fa-common", "radio-common")
    render_section("Language, identity and culture", EALD_FA2, avail_fa2,
                   st.session_state.chosen_eald_fa2_idx, "chosen_eald_fa2_idx", "eald_fa2",
                   "tc", "fa-tc", "radio-tc")
    render_section("Close study of text", EALD_FA3, avail_fa3,
                   st.session_state.chosen_eald_fa3_idx, "chosen_eald_fa3_idx", "eald_fa3",
                   "crit", "fa-crit", "radio-crit")

    if complete:
        if st.button("＋ New combination", key="bottom_new_eald"):
            reset_picker()
            st.rerun()


# =============================================================================
# EXTENSION 1 PICKER
# =============================================================================
elif course == "English Extension 1":
    e_idx    = st.session_state.chosen_ext1_elective_idx
    t_idxs   = st.session_state.chosen_ext1_text_idxs
    complete = not st.session_state.picker_active

    # ── No elective yet: show all 5 electives with all their texts ──────────
    if e_idx is None:
        st.markdown('<div class="course-info course-info-ext1"><strong>CLICK ANY TEXT</strong> to begin. Choosing a text locks you into that elective — then pick 2 more from it.</div>', unsafe_allow_html=True)
        for elec_i, full_name in enumerate(EXT1_ELECTIVE_FULL_NAMES):
            st.markdown(
                f'<div class="focus-area-header fa-ext1-{elec_i}" style="font-size:1rem;margin-top:0.8rem;">'
                f'{full_name}</div>',
                unsafe_allow_html=True)
            for text_i, text in enumerate(EXT1_TEXTS[elec_i]):
                radio_html = f'<div class="picker-radio radio-ext1-{elec_i}"><div class="radio-circle">○</div></div>'
                card_html  = (f'<div class="picker-card">'
                              f'<div class="text-card card-ext1-{elec_i}">{text_line_html(text)}</div>'
                              f'</div>')
                st.markdown(f'<div class="picker-row">{radio_html}{card_html}</div>', unsafe_allow_html=True)
                if st.button("select", key=f"ext1_init_{elec_i}_{text_i}"):
                    st.session_state.chosen_ext1_elective_idx = elec_i
                    st.session_state.chosen_ext1_text_idxs   = [text_i]
                    st.rerun()

    # ── Elective chosen: show only that elective's texts ────────────────────
    else:
        elective_texts = EXT1_TEXTS[e_idx]
        available_idxs = get_ext1_available(e_idx, t_idxs) if len(t_idxs) < 3 else []

        col_hdr, col_change = st.columns([5, 1])
        with col_hdr:
            st.markdown(
                f'<div class="focus-area-header fa-ext1-{e_idx}">'
                f'{EXT1_ELECTIVE_FULL_NAMES[e_idx]}</div>',
                unsafe_allow_html=True)
        with col_change:
            if st.session_state.picker_active:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("↩ Change", key="ext1_change_elective", use_container_width=True):
                    st.session_state.chosen_ext1_elective_idx = None
                    st.session_state.chosen_ext1_text_idxs   = []
                    st.rerun()

        if st.session_state.picker_active and len(t_idxs) < 3:
            remaining = 3 - len(t_idxs)
            print_needed = max(0, 2 - sum(1 for i in t_idxs if is_print_ext1(elective_texts[i])))
            st.markdown(
                f'<div class="course-info course-info-ext1">Select <strong>{remaining} more text{"s" if remaining > 1 else ""}</strong> · '
                f'at least {print_needed} must be extended print (prose fiction, nonfiction, poetry, or drama)</div>',
                unsafe_allow_html=True)

        if complete:
            st.markdown('<div class="complete-banner"><h3>✅ Combination added to favourites</h3><p>Scroll down to see your favourites, or start a new combination.</p></div>', unsafe_allow_html=True)

        for i, text in enumerate(elective_texts):
            is_selected  = i in t_idxs
            is_available = i in available_idxs

            if not st.session_state.picker_active and not is_selected:
                continue
            if st.session_state.picker_active and not is_selected and not is_available:
                continue

            if is_selected:
                radio_html = '<div class="picker-radio"><span style="font-size:1.1rem;">✅</span></div>'
            elif st.session_state.picker_active:
                radio_html = f'<div class="picker-radio radio-ext1-{e_idx}"><div class="radio-circle">○</div></div>'
            else:
                radio_html = '<div class="picker-radio"></div>'

            sel_cls   = " selected" if is_selected else ""
            card_html = (f'<div class="picker-card">'
                         f'<div class="text-card card-ext1-{e_idx}{sel_cls}">{text_line_html(text)}</div>'
                         f'</div>')
            st.markdown(f'<div class="picker-row">{radio_html}{card_html}</div>', unsafe_allow_html=True)

            if st.session_state.picker_active:
                if is_selected:
                    if st.button("deselect", key=f"ext1_text_rm_{i}"):
                        st.session_state.chosen_ext1_text_idxs.remove(i)
                        st.rerun()
                else:
                    if st.button("select", key=f"ext1_text_{i}"):
                        st.session_state.chosen_ext1_text_idxs.append(i)
                        st.rerun()

        if complete:
            if st.button("＋ New combination", key="bottom_new_ext1"):
                reset_picker()
                st.rerun()


# =============================================================================
# FAVOURITES
# =============================================================================
st.markdown("---")

fav_count = len(st.session_state.favourites)
col_fav_hdr, col_fav_clear = st.columns([5, 1])
with col_fav_hdr:
    st.markdown(f'<div class="focus-area-header fa-fav">⭐ Favourites ({fav_count})</div>', unsafe_allow_html=True)
with col_fav_clear:
    if fav_count > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Clear all", use_container_width=True):
            clear_favourites()
            st.rerun()

if not st.session_state.favourites:
    st.caption("No favourites yet. Complete a combination above and it will be added automatically.")
else:
    adv_favs  = [(i, f) for i, f in enumerate(st.session_state.favourites) if f["course"] == "English Advanced"]
    std_favs  = [(i, f) for i, f in enumerate(st.session_state.favourites) if f["course"] == "English Standard"]
    eald_favs = [(i, f) for i, f in enumerate(st.session_state.favourites) if f["course"] == "English EAL/D"]
    ext1_favs = [(i, f) for i, f in enumerate(st.session_state.favourites) if f["course"] == "English Extension 1"]

    # --- ADVANCED FAVOURITES ---
    if adv_favs:
        adv_csv = make_fav_csv("English Advanced")
        adv_csv_b64 = base64.b64encode(adv_csv.encode()).decode()
        adv_fname = f"HSC_Advanced_favourites_{datetime.now():%Y%m%d_%H%M}.csv"
        st.markdown(
            f'<div class="fav-hdr-row"><span class="fav-course-heading">English Advanced</span>'
            f'<a href="data:text/csv;base64,{adv_csv_b64}" download="{adv_fname}" class="fav-csv-btn">📥 CSV</a></div>',
            unsafe_allow_html=True)

        rows_html = (
            '<tr><th style="width:3rem;">Option&nbsp;#</th>'
            '<th>Texts and human experiences</th>'
            '<th>Textual conversations</th>'
            '<th>Critical study of literature</th></tr>'
        )
        for seq, (orig_idx, fav) in enumerate(adv_favs):
            pair, crit, common = fav["pair"], fav["crit"], fav["common"]
            tc_cell = f'{fav_cell(pair.text_a)}<br><span style="color:#64748b;font-size:0.78rem;">+</span><br>{fav_cell(pair.text_b)}'
            rows_html += (
                f'<tr><td style="text-align:center;"><div style="font-weight:600;">{seq+1}</div>'
                f'<span class="fav-del" data-del="{seq}">🗑</span></td>'
                f'<td>{fav_cell(common)}</td><td>{tc_cell}</td><td>{fav_cell(crit)}</td></tr>'
            )
        st.markdown(f'<table class="fav-table">{rows_html}</table>', unsafe_allow_html=True)
        for seq, (orig_idx, fav) in enumerate(adv_favs):
            if st.button(f"🗑 {seq}", key=f"rm_adv_{orig_idx}"):
                st.session_state.favourites.pop(orig_idx)
                st.rerun()

    # --- STANDARD FAVOURITES ---
    if std_favs:
        std_csv = make_fav_csv("English Standard")
        std_csv_b64 = base64.b64encode(std_csv.encode()).decode()
        std_fname = f"HSC_Standard_favourites_{datetime.now():%Y%m%d_%H%M}.csv"
        st.markdown(
            f'<div class="fav-hdr-row"><span class="fav-course-heading">English Standard</span>'
            f'<a href="data:text/csv;base64,{std_csv_b64}" download="{std_fname}" class="fav-csv-btn">📥 CSV</a></div>',
            unsafe_allow_html=True)

        rows_html = (
            '<tr><th style="width:3rem;">Option&nbsp;#</th>'
            '<th>Texts and human experiences</th>'
            '<th>Language, identity and culture</th>'
            '<th>Close study of literature</th></tr>'
        )
        for seq, (orig_idx, fav) in enumerate(std_favs):
            common, lic, close = fav["common"], fav["lic"], fav["close"]
            rows_html += (
                f'<tr><td style="text-align:center;"><div style="font-weight:600;">{seq+1}</div>'
                f'<span class="fav-del" data-del="{seq}">🗑</span></td>'
                f'<td>{fav_cell(common)}</td><td>{fav_cell(lic)}</td><td>{fav_cell(close)}</td></tr>'
            )
        st.markdown(f'<table class="fav-table">{rows_html}</table>', unsafe_allow_html=True)
        for seq, (orig_idx, fav) in enumerate(std_favs):
            if st.button(f"🗑 {seq}", key=f"rm_std_{orig_idx}"):
                st.session_state.favourites.pop(orig_idx)
                st.rerun()

    # --- EAL/D FAVOURITES ---
    if eald_favs:
        eald_csv = make_fav_csv("English EAL/D")
        eald_csv_b64 = base64.b64encode(eald_csv.encode()).decode()
        eald_fname = f"HSC_EALD_favourites_{datetime.now():%Y%m%d_%H%M}.csv"
        st.markdown(
            f'<div class="fav-hdr-row"><span class="fav-course-heading">English EAL/D</span>'
            f'<a href="data:text/csv;base64,{eald_csv_b64}" download="{eald_fname}" class="fav-csv-btn">📥 CSV</a></div>',
            unsafe_allow_html=True)

        rows_html = (
            '<tr><th style="width:3rem;">Option&nbsp;#</th>'
            '<th>Texts and human experiences</th>'
            '<th>Language, identity and culture</th>'
            '<th>Close study of text</th></tr>'
        )
        for seq, (orig_idx, fav) in enumerate(eald_favs):
            fa1, fa2, fa3 = fav["fa1"], fav["fa2"], fav["fa3"]
            rows_html += (
                f'<tr><td style="text-align:center;"><div style="font-weight:600;">{seq+1}</div>'
                f'<span class="fav-del" data-del="{seq}">🗑</span></td>'
                f'<td>{fav_cell(fa1)}</td><td>{fav_cell(fa2)}</td><td>{fav_cell(fa3)}</td></tr>'
            )
        st.markdown(f'<table class="fav-table">{rows_html}</table>', unsafe_allow_html=True)
        for seq, (orig_idx, fav) in enumerate(eald_favs):
            if st.button(f"🗑 {seq}", key=f"rm_eald_{orig_idx}"):
                st.session_state.favourites.pop(orig_idx)
                st.rerun()

    # --- EXTENSION 1 FAVOURITES ---
    if ext1_favs:
        ext1_csv = make_fav_csv("English Extension 1")
        ext1_csv_b64 = base64.b64encode(ext1_csv.encode()).decode()
        ext1_fname = f"HSC_Extension1_favourites_{datetime.now():%Y%m%d_%H%M}.csv"
        st.markdown(
            f'<div class="fav-hdr-row"><span class="fav-course-heading">English Extension 1</span>'
            f'<a href="data:text/csv;base64,{ext1_csv_b64}" download="{ext1_fname}" class="fav-csv-btn">📥 CSV</a></div>',
            unsafe_allow_html=True)

        rows_html = (
            '<tr><th style="width:3rem;">Option&nbsp;#</th>'
            '<th>Elective</th><th>Text 1</th><th>Text 2</th><th>Text 3</th></tr>'
        )
        for seq, (orig_idx, fav) in enumerate(ext1_favs):
            e_idx  = fav["elective_idx"]
            t_idxs = fav["text_idxs"]
            elective_name = EXT1_ELECTIVE_NAMES[e_idx]
            texts = EXT1_TEXTS[e_idx]
            rows_html += (
                f'<tr><td style="text-align:center;"><div style="font-weight:600;">{seq+1}</div>'
                f'<span class="fav-del" data-del="{seq}">🗑</span></td>'
                f'<td style="font-size:0.82rem;color:#c4b8f0;">{elective_name}</td>'
                f'<td>{fav_cell(texts[t_idxs[0]])}</td>'
                f'<td>{fav_cell(texts[t_idxs[1]])}</td>'
                f'<td>{fav_cell(texts[t_idxs[2]])}</td></tr>'
            )
        st.markdown(f'<table class="fav-table">{rows_html}</table>', unsafe_allow_html=True)
        for seq, (orig_idx, fav) in enumerate(ext1_favs):
            if st.button(f"🗑 {seq}", key=f"rm_ext1_{orig_idx}"):
                st.session_state.favourites.pop(orig_idx)
                st.rerun()


# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.caption(
    "Data source: NESA HSC English Prescriptions 2027–2030 (D2025/464194, © 2026 NSW Education Standards Authority). "
    "This tool is unofficial and provided for planning purposes only. Always verify against the official NESA prescriptions document."
)
