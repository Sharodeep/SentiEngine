import os
import sys
import logging
import streamlit as st
import matplotlib.pyplot as plt

ROOT = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, ROOT)
ASSETS = os.path.join(ROOT, 'assets')

from engine import main

logging.basicConfig(
    filename=os.path.join(ROOT, "dashboard.log"),
    level=logging.WARNING,
    format="%(asctime)s %(levelname)s: %(message)s",
)

st.set_page_config(page_title="DashBoard", page_icon="📊", layout="centered")
st.image(os.path.join(ASSETS, "logo_dash.png"))
st.divider()

input_text = st.text_area("Enter text to analyse", placeholder="Type here!!", height=150)

col1, col2 = st.columns([1, 5])
with col1:
    analyse = st.button("Check", use_container_width=True)
with col2:
    uploaded = st.file_uploader("Upload a .txt file", type="txt", label_visibility="collapsed")

if uploaded:
    try:
        input_text = uploaded.read().decode("utf-8").strip()
    except Exception as e:
        logging.error(f"File read error: {e}")
        st.error("Could not read the uploaded file.")

if analyse or uploaded:
    if not input_text:
        st.warning("Enter valid input")
    elif input_text == "Hello there":
        st.image(os.path.join(ASSETS, "easter1.png"))
        st.write("Ah General Kenobi You're a bold one")
    else:
        try:
            sent, emo, val = main(input_text)

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

                emotion_colours = {
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
                bar_colours = [emotion_colours.get(label.strip(), "#e8a321") for label in labels]

                col_pie, col_bar = st.columns(2)

                with col_pie:
                    fig_pie, ax_pie = plt.subplots()
                    ax_pie.pie(values, labels=labels, autopct="%1.1f%%", startangle=90, colors=bar_colours)
                    ax_pie.axis("equal")
                    fig_pie.patch.set_facecolor("#0e1117")
                    ax_pie.set_facecolor("#0e1117")
                    plt.setp(ax_pie.texts, color="white")
                    st.pyplot(fig_pie)
                    plt.close(fig_pie)

                with col_bar:
                    fig_bar, ax_bar = plt.subplots()
                    ax_bar.barh(labels, values, color=bar_colours)
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
                    use_container_width=True,
                    hide_index=True,
                )

        except Exception as e:
            logging.error(f"Analysis error: {e}")
            st.error("Something went wrong during analysis. Check dashboard.log for details.")
