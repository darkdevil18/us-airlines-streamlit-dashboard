import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS


st.title("Sentiment Analysis of Tweets about US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets about US Airlines")

st.markdown("This application is a Streamlit dashboard to analyze the sentiment of Tweets.")
st.sidebar.markdown("This application is a Streamlit dashboard to analyze the sentiment of Tweets.")


DATA_URL = ("./Tweets.csv")

@st.cache_data(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()

st.sidebar.subheader("Show random tweet")
random_tweet = st.sidebar.radio('Sentiment', ('Positive', 'Neutral', 'Negative'))
random_tweet = random_tweet.lower()

st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[['text']].sample(n=1).iat[0, 0])

st.sidebar.markdown("### Number of tweets by sentiment")
select = st.sidebar.selectbox('Visualization Type', ['Histogram', 'Pie Chart'], key=1)

sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({
    'Sentiment': sentiment_count.index,
    'Tweets': sentiment_count.values
})

if not st.sidebar.checkbox('Hide', False, key='2'):
    st.markdown("### Number of tweets by sentiment")
    if select == 'Histogram':
        fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)


st.sidebar.subheader("Breakdown airline tweets by sentiment")
choice = st.sidebar.multiselect('Pick airlines', data['airline'].unique())

if len(choice) > 0:
    st.markdown("## Number of tweets by sentiments")
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x='airline', y='airline_sentiment', histfunc='count', color='airline_sentiment', facet_col='airline_sentiment', labels={'airline_sentiments': 'tweets'}, height=600, width=800)
    st.plotly_chart(fig_choice)


st.sidebar.header('Word Cloud')
word_sentiment = st.sidebar.radio('Display word cloud for what sentiment?', ('Positive', 'Neutral', 'Negative'))
word_sentiment = word_sentiment.lower()

if not st.sidebar.checkbox('Close', False, key='3'):
    st.header(f'Word cloud for {word_sentiment}')
    df = data[data['airline_sentiment'] == word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', height=640, width=800).generate(processed_words)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud)
    ax.set_axis_off()
    st.pyplot(fig)











