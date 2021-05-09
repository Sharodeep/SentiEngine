import string
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt


def sentiment_analyse(senti_text):
    senti_score = SentimentIntensityAnalyzer().polarity_scores(senti_text)
    neg_score = senti_score['neg']
    pos_score = senti_score['pos']
    neu_score = senti_score['neu']
    print("Positive Score:", pos_score, "Negative Score:", neg_score, "Neutral Score:", neu_score)
    if neg_score > pos_score and neg_score >= neu_score:
        print("The overall sentiment of the query is Negative with a score of", neg_score)
    elif pos_score > neg_score and pos_score >= neu_score:
        print("The overall sentiment of the query is Positive with a score of", pos_score)
    else:
        print("The overall sentiment of the query is Neutral with a score of", neu_score)


text = open('read.txt', encoding='utf-8').read()
lower_case = text.lower()
clean_text = lower_case.translate(str.maketrans('', '', string.punctuation))
token_words = word_tokenize(clean_text, "english")
final_words = []
for word in token_words:
    if word not in stopwords.words('english'):
        final_words.append(word)

def emotion_analyse(final_words):
    emotion_list = []
    with open('emotions.txt', 'r') as file:
        for line in file:
            clean_line = line.replace('\n', '').replace(',', '').replace("'", '').strip()
            word, emotion = clean_line.split(':')
            if word in final_words:
                emotion_list.append(emotion)
    print(emotion_list)
    word_val = Counter(final_words)
    val = Counter(emotion_list)
    print(val)
    emo = list(val.keys())
    mos = list(word_val.keys())
    print("The overall emotion is:", emo[0], "\nThe most used word is:", mos[0])
    ploter(val)

def ploter(vals):
    fig, ax1 = plt.subplots()
    ax1.bar(vals.keys(), vals.values())
    fig.autofmt_xdate()
    plt.savefig('graph.png')
    plt.show()

sentiment_analyse(clean_text)
emotion_analyse(final_words)

