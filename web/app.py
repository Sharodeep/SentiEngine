import os
import sys
import logging
import streamlit as st
import matplotlib.pyplot as plt

ROOT = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, ROOT)
ASSETS = os.path.join(ROOT, 'assets')

from engine import main, is_flair_loaded
from engine.engine import MODELS_WEB, MODEL_DESCRIPTIONS

try:
    _log_level = st.secrets.get("LOG_LEVEL", os.environ.get("LOG_LEVEL", "WARNING")).upper()
except Exception:
    _log_level = os.environ.get("LOG_LEVEL", "WARNING").upper()
_log_level = getattr(logging, _log_level, logging.WARNING)

logger = logging.getLogger("dashboard")
if not logger.handlers:
    _handler = logging.FileHandler(os.path.join(ROOT, "dashboard.log"))
    _handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
    logger.addHandler(_handler)
logger.setLevel(_log_level)
logger.propagate = False

EMOTION_COLOURS = {
    "happy":       "#FFD700",
    "sad":         "#4A90D9",
    "angry":       "#E84040",
    "fearful":     "#9B59B6",
    "anxious":     "#E67E22",
    "surprise":    "#1ABC9C",
    "alone":       "#7F8C8D",
    "attached":    "#F1948A",
    "loved":       "#FF69B4",
    "powerless":   "#566573",
    "fearless":    "#2ECC71",
    "independent": "#27AE60",
    "focused":     "#3498DB",
    "adequate":    "#85C1E9",
    "esteemed":    "#F4D03F",
    "bored":       "#BDC3C7",
    "apathetic":   "#95A5A6",
    "embarrassed": "#E59866",
    "lustful":     "#C0392B",
    "obsessed":    "#8E44AD",
    "belittled":   "#A04000",
    "cheated":     "#D35400",
    "singled out": "#CB4335",
    "demoralized": "#717D7E",
    "lost":        "#616A6B",
    "free":        "#76D7C4",
    "safe":        "#A9DFBF",
    "attracted":   "#F9E79F",
    "entitled":    "#F0B27A",
    "average":     "#AAB7B8",
    "burdened":    "#784212",
    "derailed":    "#6E2F1A",
    "codependent": "#C39BD3",
    "ecstatic":    "#FDFEFE",
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Settings")
    if "model" not in st.session_state:
        st.session_state.model = "VADER"
    st.selectbox("Sentiment Model", MODELS_WEB, key="model")
    st.caption(MODEL_DESCRIPTIONS[st.session_state.model])

    with st.expander("Model Guide"):
        for model, desc in MODEL_DESCRIPTIONS.items():
            st.markdown(f"**{model}**")
            st.caption(desc)

# ── Header ────────────────────────────────────────────────────────────────────
_, logo_col, _ = st.columns([1, 2, 1])
with logo_col:
    st.image(os.path.join(ASSETS, "logo_dash.png"), width="stretch")

st.divider()

# ── Session state ─────────────────────────────────────────────────────────────
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0
if "results" not in st.session_state:
    st.session_state.results = None

# ── Input ─────────────────────────────────────────────────────────────────────
input_text = st.text_area("Enter text to analyse", placeholder="Type here!!", height=150, label_visibility="collapsed")
analyse = st.button("Analyse", width="stretch")

st.markdown("<div style='text-align:center; color:grey; margin: 8px 0'>— or —</div>", unsafe_allow_html=True)

uploaded = st.file_uploader("Upload a .txt file", type="txt", accept_multiple_files=False,
                             key=f"uploader_{st.session_state.uploader_key}")

def run_analysis(text, model):
    try:
        needs_flair = model in ('Flair', 'SuperMixed') and not is_flair_loaded()
        msg = "Loading Flair model for the first time, this may take a moment..." if needs_flair else "Analysing..."
        with st.spinner(msg):
            sent, emo, val = main(text, model)
        st.session_state.results = (sent, emo, val)
        logger.info(f"Analysis complete — model: {model}, emotion: {val.most_common(1)[0][0] if val else 'none'}")
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        st.error("Something went wrong during analysis. Check dashboard.log for details.")
        st.session_state.results = None

if uploaded:
    try:
        file_text = uploaded.read().decode("utf-8").strip()
        if not file_text:
            st.warning("Uploaded file is empty.")
        else:
            run_analysis(file_text, st.session_state.model)
            st.session_state.uploader_key += 1
            st.rerun()
    except Exception as e:
        logger.error(f"File read error: {e}")
        st.error("Could not read the uploaded file.")

if analyse:
    if not input_text:
        st.warning("Please enter some text or upload a file.")
    elif input_text == "Hello there":
        st.image(os.path.join(ASSETS, "easter1.png"))
        st.write("Ah General Kenobi You're a bold one")
        st.session_state.results = None
    else:
        run_analysis(input_text, st.session_state.model)

# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.results:
    sent, emo, val = st.session_state.results

    st.divider()
    col_sent, col_emo = st.columns(2)
    with col_sent:
        st.subheader("Sentiment")
        st.text(sent)
    with col_emo:
        st.subheader("Emotion")
        st.text(emo)

    if val:
        st.divider()
        st.subheader("Emotion Breakdown")

        labels = list(val.keys())
        values = list(val.values())
        colours = [EMOTION_COLOURS.get(l.strip(), "#e8a321") for l in labels]

        col_pie, col_bar = st.columns(2)

        with col_pie:
            fig_pie, ax_pie = plt.subplots()
            ax_pie.pie(values, labels=labels, autopct="%1.1f%%", startangle=90, colors=colours)
            ax_pie.axis("equal")
            fig_pie.patch.set_facecolor("#0e1117")
            ax_pie.set_facecolor("#0e1117")
            plt.setp(ax_pie.texts, color="white")
            st.pyplot(fig_pie)
            plt.close(fig_pie)

        with col_bar:
            fig_bar, ax_bar = plt.subplots()
            ax_bar.barh(labels, values, color=colours)
            ax_bar.set_xlabel("Score", color="white")
            ax_bar.tick_params(colors="white")
            ax_bar.spines[:].set_color("#444")
            fig_bar.patch.set_facecolor("#0e1117")
            ax_bar.set_facecolor("#0e1117")
            ax_bar.xaxis.label.set_color("white")
            st.pyplot(fig_bar)
            plt.close(fig_bar)

        st.subheader("Scores Table")
        st.dataframe(
            {"Emotion": labels, "Score": values},
            width="stretch",
            hide_index=True,
        )
