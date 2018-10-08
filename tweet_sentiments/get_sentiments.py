#!/usr/bin/python2.7
import argparse
from textblob import TextBlob
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
import re


def get_sent(x):
    #nearer to 1 means a positive sentiment and values nearer to -1 means a negative sentiment
    if x==0:
        mode = "neutral"
    elif x<0:
        mode = "negative"
    elif x>0:
        mode = "positive"
    return mode
    

def plot_graph(df, yourtext, user):
    sent = df["sentiment"]

    ## use Counter to count how many times each sentiment appears
    ## and save each as a variable
    counter = Counter(sent)
    positive = counter['positive']
    negative = counter['negative']
    neutral = counter['neutral']

    labels = ['Positive', 'Negative', 'Neutral']
    if not positive:
        labels[0]=''
    if not negative:
        labels[1]=''
    if not neutral:
        labels[2]=''
    sizes = [positive, negative, neutral]
    colors = ['green', 'red', 'grey']

    ## use matplotlib to plot the chart
    plt.pie(sizes, labels = labels, colors = colors, shadow = True, startangle = 90)
    if user:
        plt.title("Sentiment of %s Tweets about %s for user:%s "%(len(df),yourtext, user))
    else:
        plt.title("Sentiment of %s Tweets about %s"%(len(df),yourtext))
    plt.show()

def get_sentiments(tweet_file, text, user):
    df = pd.read_csv(tweet_file)
    df.columns = [x.strip() for x in list(df.columns)]
    if text:
        df = df[df['tweets'].str.contains(text,flags=re.IGNORECASE)]
    else:
        text='everything'
    if user:
        if '*' in user:
            user=user.replace('*','')
            df = df[df['user'].str.contains(user,flags=re.IGNORECASE)]
        else:
            df = df[df['user']==user]

    if not len(df):
        print "No any data found in tweets regarding %s"%text
        return
    df[['polarity', 'subjectivity']] = df['tweets'].apply(lambda Text: pd.Series(TextBlob(Text).sentiment))
    df['sentiment']=df['polarity'].apply(lambda val: get_sent(val))
    plot_graph(df, text, user)

 
def get_parser():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f','-tweet_file', dest='tweet_file', required=True, help='file having tweet info')
    parser.add_argument('-t','-text', dest='text', default=None, help='text about which sentiment data is required')
    parser.add_argument('-u','-user', dest='user', default=None, help='provide username to analyze data on user basis')

    return parser.parse_args()
    


if __name__=="__main__":
    op = get_parser()
    tweet_file = op.tweet_file
    text = op.text
    user = op.user
    get_sentiments(tweet_file, text, user)
