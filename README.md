# DashBoard — Sentiment Analyser

A text sentiment and emotion analysis tool available as both a desktop app and a web app.

## Project Structure

```
DashBoard/
  engine/
    engine.py       ← NLP engine (sentiment + emotion analysis)
    emotions.txt    ← emotion lexicon
  assets/
    logo_dash.png
    easter1.png
  web/
    app.py          ← Streamlit web app
    requirements.txt
  desktop/
    gui.py          ← Dear PyGui desktop app
    requirements.txt
```

## Setup

Requires Python 3.10+. Install [pyenv](https://github.com/pyenv/pyenv) to manage your Python version, then run:

```bash
pyenv local 3.10.20
```

### Web App

```bash
pip install -r web/requirements.txt
streamlit run web/app.py
```

Or visit the hosted version at: *https://kuar-sentiengine.streamlit.app*

### Desktop App

```bash
pip install -r desktop/requirements.txt
python3 desktop/gui.py
```

## Features

- Sentiment analysis (positive / negative / neutral scores via VADER)
- Emotion detection mapped against a 400+ word lexicon
- Pie chart and bar chart emotion breakdown
- Analyse typed text or upload a `.txt` file

## First Run

The first run requires an internet connection to download NLTK data packages (`punkt_tab`, `stopwords`, `vader_lexicon`). Subsequent runs work offline.
