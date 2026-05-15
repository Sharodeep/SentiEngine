# DashBoard Engine V0.0.2
import os
import string
import nltk
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

_EMOTIONS_PATH = os.path.join(os.path.dirname(__file__), 'emotions.txt')
_NLTK_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'nltk_data')
_flair_model = None

nltk.data.path.insert(0, _NLTK_DATA_PATH)
nltk.download('punkt_tab', download_dir=_NLTK_DATA_PATH, quiet=True)
nltk.download('stopwords', download_dir=_NLTK_DATA_PATH, quiet=True)
nltk.download('vader_lexicon', download_dir=_NLTK_DATA_PATH, quiet=True)

MODELS_WEB = ['VADER', 'TextBlob', 'Flair', 'Mixed', 'SuperMixed']
MODELS_DESKTOP = ['VADER', 'TextBlob', 'Flair', 'Mixed', 'SuperMixed']

MODEL_DESCRIPTIONS = {
    'VADER':      'Rule-based model built for short social media text. Fast and lightweight but misses context in longer passages.',
    'TextBlob':   'General-purpose NLP model using a trained corpus. More balanced than VADER on formal text.',
    'Flair':      'Deep learning model trained on IMDB reviews. Best context understanding but binary — positive or negative only, no neutral score.',
    'Mixed':      'Averages VADER and TextBlob scores. Combines rule-based and corpus-based approaches for a more balanced result.',
    'SuperMixed': 'Averages all three models. Most balanced overall — smooths out the weaknesses of each individual model.',
}


def _format_sentiment(pos, neg, neu):
    result = f"Positive Score: {pos}\nNegative Score: {neg}\nNeutral Score: {neu}\n"
    if neg > pos and neg >= neu:
        result += f"\nThe overall sentiment is Negative with a score of {neg}"
    elif pos > neg and pos >= neu:
        result += f"\nThe overall sentiment is Positive with a score of {pos}"
    else:
        result += f"\nThe overall sentiment is Neutral with a score of {neu}"
    return result


def _sentiment_vader(text):
    scores = SentimentIntensityAnalyzer().polarity_scores(text)
    return _format_sentiment(scores['pos'], scores['neg'], scores['neu'])


def _sentiment_textblob(text):
    from textblob import TextBlob
    polarity = TextBlob(text).sentiment.polarity
    if polarity >= 0:
        pos, neg, neu = round(polarity, 3), 0.0, round(1 - polarity, 3)
    else:
        pos, neg, neu = 0.0, round(abs(polarity), 3), round(1 - abs(polarity), 3)
    return _format_sentiment(pos, neg, neu)


def _sentiment_flair(text):
    global _flair_model
    from flair.models import TextClassifier
    from flair.data import Sentence
    if _flair_model is None:
        _flair_model = TextClassifier.load('sentiment')
    sentence = Sentence(text)
    _flair_model.predict(sentence)
    label = sentence.labels[0]
    score = round(label.score, 3)
    if label.value == 'POSITIVE':
        pos, neg, neu = score, 0.0, round(1 - score, 3)
    else:
        pos, neg, neu = 0.0, score, round(1 - score, 3)
    return _format_sentiment(pos, neg, neu)


def _sentiment_mixed(text):
    vader_scores = SentimentIntensityAnalyzer().polarity_scores(text)
    v_pos, v_neg, v_neu = vader_scores['pos'], vader_scores['neg'], vader_scores['neu']

    from textblob import TextBlob
    polarity = TextBlob(text).sentiment.polarity
    if polarity >= 0:
        t_pos, t_neg, t_neu = polarity, 0.0, 1 - polarity
    else:
        t_pos, t_neg, t_neu = 0.0, abs(polarity), 1 - abs(polarity)

    pos = round((v_pos + t_pos) / 2, 3)
    neg = round((v_neg + t_neg) / 2, 3)
    neu = round((v_neu + t_neu) / 2, 3)
    return _format_sentiment(pos, neg, neu)


def _sentiment_supermixed(text):
    vader_scores = SentimentIntensityAnalyzer().polarity_scores(text)
    v_pos, v_neg, v_neu = vader_scores['pos'], vader_scores['neg'], vader_scores['neu']

    from textblob import TextBlob
    polarity = TextBlob(text).sentiment.polarity
    if polarity >= 0:
        t_pos, t_neg, t_neu = polarity, 0.0, 1 - polarity
    else:
        t_pos, t_neg, t_neu = 0.0, abs(polarity), 1 - abs(polarity)

    global _flair_model
    from flair.models import TextClassifier
    from flair.data import Sentence
    if _flair_model is None:
        _flair_model = TextClassifier.load('sentiment')
    sentence = Sentence(text)
    _flair_model.predict(sentence)
    label = sentence.labels[0]
    score = round(label.score, 3)
    if label.value == 'POSITIVE':
        f_pos, f_neg, f_neu = score, 0.0, round(1 - score, 3)
    else:
        f_pos, f_neg, f_neu = 0.0, score, round(1 - score, 3)

    pos = round((v_pos + t_pos + f_pos) / 3, 3)
    neg = round((v_neg + t_neg + f_neg) / 3, 3)
    neu = round((v_neu + t_neu + f_neu) / 3, 3)
    return _format_sentiment(pos, neg, neu)


def sentiment_analyse(text, model='VADER'):
    if model == 'TextBlob':
        return _sentiment_textblob(text)
    elif model == 'Flair':
        return _sentiment_flair(text)
    elif model == 'Mixed':
        return _sentiment_mixed(text)
    elif model == 'SuperMixed':
        return _sentiment_supermixed(text)
    return _sentiment_vader(text)


def loader(text):
    global clean_text, final_words
    lower_case = text.lower()
    clean_text = lower_case.translate(str.maketrans('', '', string.punctuation))
    token_words = word_tokenize(clean_text, "english")
    final_words = [word for word in token_words if word not in stopwords.words('english')]


def emotion_analyse(final_words):
    emotion_list = []
    with open(_EMOTIONS_PATH, 'r') as file:
        for line in file:
            clean_line = line.replace('\n', '').replace(',', '').replace("'", '').strip()
            word, emotion = clean_line.split(':')
            if word.strip() in final_words:
                emotion_list.append(emotion.strip())
    word_val = Counter(final_words)
    val = Counter(emotion_list)
    emoKey = list(val.keys())
    counts = list(word_val.values())
    if not emoKey:
        return_holder = "No emotion detected"
    elif len(counts) >= 2 and counts[0] > counts[1]:
        top_word = list(word_val.keys())[0]
        return_holder = f"The overall emotion is: {emoKey[0]}\n\nThe most used word is: {top_word}"
    else:
        return_holder = f"The overall emotion is: {emoKey[0]}"
    return return_holder, val


def ploter(vals):
    fig, ax1 = plt.subplots()
    ax1.bar(vals.keys(), vals.values())
    fig.autofmt_xdate()
    plt.savefig('graph.png')
    plt.show()


def is_flair_loaded():
    return _flair_model is not None


def main(text="Hello", model='VADER'):
    loader(text)
    sent_holder = sentiment_analyse(clean_text, model)
    emo_holder, emo_vals = emotion_analyse(final_words)
    return sent_holder, emo_holder, emo_vals


clean_text = ""
final_words = []
