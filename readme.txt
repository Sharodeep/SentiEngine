DashBoard — Sentiment Analyser
================================

Requires Python 3.10+.

WEB APP
-------
1. Install dependencies:
   pip install -r web/requirements.txt

2. Run:
   streamlit run web/app.py

DESKTOP APP
-----------
1. Install dependencies:
   pip install -r desktop/requirements.txt

2. Run:
   python3 desktop/gui.py

NOTE: The first run requires an active internet connection to download
NLTK data packages (punkt_tab, stopwords, vader_lexicon).
Subsequent runs work offline.
