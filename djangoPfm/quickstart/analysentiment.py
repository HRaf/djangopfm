import re
from twitterscraper import query_tweets
import datetime as dt
import pandas as pd
from textblob import TextBlob
from textblob_fr import PatternAnalyzer,PatternTagger


def scrap_sentiments_covid():
    debut = dt.date(2020, 1, 1)
    fin = dt.date(2020, 6, 1)
    mots = "Covid-19 OR Covid OR Corona OR Pandémie OR épidémie OR Coronavirus OR virus"

    tweets = query_tweets(query=mots, begindate=debut,
                          enddate=fin, lang="fr")

    tweets = pd.DataFrame(t.__dict__ for t in tweets)

    tweets.to_csv('tweet_covid.csv')


# Implémentation du pippeline NLP
def nlp_pipeline(text):

    text = text.lower()
    text = text.replace('\n', ' ').replace('\r', '')
    text = ' '.join(text.split())
    text = re.sub(r"[A-Za-z\.]*[0-9]+[A-Za-z%°\.]*", "", text)
    text = re.sub(r"(\s\-\s|-$)", "", text)
    text = re.sub(r"[,\!\?\;\%\(\)\/\"]", "", text)
    text = re.sub(r"\&\S*\s", "", text)
    text = re.sub(r"\&", "", text)
    text = re.sub(r"\+", "", text)
    text = re.sub(r"\#", "", text)
    text = re.sub(r"\$", "", text)
    text = re.sub(r"\£", "", text)
    text = re.sub(r"\%", "", text)
    text = re.sub(r"\:", "", text)
    text = re.sub(r"\@", "", text)
    text = re.sub(r"\-", "", text)
    text = re.sub(r"\=", "", text)
    text = re.sub(r"\§", "", text)
    text = re.sub(r"\_", "", text)



    return text

#Analyse de sentiment
def analysentiment(text):
    #tweet = pd.read_csv("tweet_covid.csv")
    #corpus = tweet['tweet']
    #corpus_clean = corpus.apply(nlp_pipeline)
    text=nlp_pipeline(text)
    pol=TextBlob(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer()).sentiment[0]
    return pol







if __name__ == '__main__':
    print(analysentiment('Achetter de ()(§§§(/;):nourri=)ture- me r-end encore ner_veu-x'))
