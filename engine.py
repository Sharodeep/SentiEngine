# DashBoard Engine V0.0.2
import string
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt


def sentiment_analyse(senti_text):  # Sentiment Analysing unit
    senti_score = SentimentIntensityAnalyzer().polarity_scores(senti_text)
    neg_score = senti_score['neg']
    pos_score = senti_score['pos']
    neu_score = senti_score['neu']
    return_holder = "Positive Score:" + str(pos_score) + "\nNegative Score:" + str(neg_score) + "\nNeutral Score:" + str(
        neu_score)+"\n"
    if neg_score > pos_score and neg_score >= neu_score:
        return_holder1 = "\nThe overall sentiment of the query is Negative with a score of " + str(neg_score)
    elif pos_score > neg_score and pos_score >= neu_score:
        return_holder1 = "\nThe overall sentiment of the query is Positive with a score of " + str(pos_score)
    else:
        return_holder1 = "\nThe overall sentiment of the query is Neutral with a score of " + str(neu_score)
    return_holder = return_holder + return_holder1
    return return_holder


def loader(text):  # responsible for loading and cleaning text files and inputs
    global clean_text
    global final_words
    lower_case = text.lower()
    clean_text = lower_case.translate(str.maketrans('', '', string.punctuation))
    token_words = word_tokenize(clean_text, "english")
    final_words = []
    for word in token_words:
        if word not in stopwords.words('english'):
            final_words.append(word)


def emotion_analyse(final_words):  # Emotion mapping unit
    emotion_list = []
    with open('emotions.txt', 'r') as file:
        for line in file:
            clean_line = line.replace('\n', '').replace(',', '').replace("'", '').strip()
            word, emotion = clean_line.split(':')
            if word in final_words:
                emotion_list.append(emotion)
    # print(emotion_list)#for testing
    word_val = Counter(final_words)
    val = Counter(emotion_list)
    print(val)  # for testing
    emoKey = list(val.keys())
    emoVal = list(word_val.keys())
    if not emoKey or not emoVal:
        return_holder = "No emotion detected"
    else:
        return_holder = ("The overall emotion is:" + emoKey[0] + "\n\nThe most used word is:" + emoVal[0])
    # print(return_holder)#for testing
    # ploter(val)#not used
    return return_holder, val


def ploter(vals):  # used for plotting graphs (not used in GUI,GUI has it's own plotting librabry)
    fig, ax1 = plt.subplots()
    ax1.bar(vals.keys(), vals.values())
    fig.autofmt_xdate()
    plt.savefig('graph.png')
    plt.show()


def main(text=open('D:\\extras\\projects\\sentimentA\\file.txt', encoding='utf-8').read()):  # main loader responsible for calling all other functions
    loader(text)
    sent_holder = sentiment_analyse(clean_text)
    emo_holder, emo_vals = emotion_analyse(final_words)
    # print(emo_holder) #for testing
    return sent_holder, emo_holder, emo_vals


clean_text = ""
final_words = []
# main(text)
