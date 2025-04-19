import tweepy
import praw
from newsapi import NewsApiClient
import finnhub
import os
from dotenv import load_dotenv
from google.generativeai import GenerativeModel

load_dotenv()

def get_twitter_sentiment(ticker):
    # Example: fetch tweets and summarize with Gemini
    auth = tweepy.OAuth1UserHandler(
        os.getenv("TWEEPY_API_KEY"), os.getenv("TWEEPY_API_SECRET"),
        os.getenv("TWEEPY_ACCESS_TOKEN"), os.getenv("TWEEPY_ACCESS_TOKEN_SECRET"))
    api = tweepy.API(auth)
    tweets = api.search_tweets(q=ticker, count=20, lang='en')
    texts = [tweet.text for tweet in tweets]
    prompt = f"Summarize the sentiment of these tweets about {ticker}: {texts}"
    model = GenerativeModel(os.getenv("GEMINI_API_KEY"))
    response = model.generate_content(prompt)
    return response.text if hasattr(response, 'text') else response

def get_reddit_sentiment(ticker):
    reddit = praw.Reddit(
        client_id=os.getenv("PRAW_CLIENT_ID"),
        client_secret=os.getenv("PRAW_CLIENT_SECRET"),
        user_agent=os.getenv("PRAW_USER_AGENT"))
    posts = reddit.subreddit('stocks').search(ticker, limit=10)
    texts = [post.title + " " + post.selftext for post in posts]
    prompt = f"Summarize the sentiment of these Reddit posts about {ticker}: {texts}"
    model = GenerativeModel(os.getenv("GEMINI_API_KEY"))
    response = model.generate_content(prompt)
    return response.text if hasattr(response, 'text') else response

def get_news_sentiment(ticker):
    newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))
    articles = newsapi.get_everything(q=ticker, language='en', sort_by='relevancy', page_size=10)
    texts = [article['title'] + " " + article['description'] for article in articles['articles']]
    prompt = f"Summarize the sentiment of these news articles about {ticker}: {texts}"
    model = GenerativeModel(os.getenv("GEMINI_API_KEY"))
    response = model.generate_content(prompt)
    return response.text if hasattr(response, 'text') else response

def aggregate_sentiment(ticker):
    twitter = get_twitter_sentiment(ticker)
    reddit = get_reddit_sentiment(ticker)
    news = get_news_sentiment(ticker)
    summary_prompt = f"Twitter: {twitter}\nReddit: {reddit}\nNews: {news}\nProvide an overall sentiment summary for trading {ticker}."
    model = GenerativeModel(os.getenv("GEMINI_API_KEY"))
    response = model.generate_content(summary_prompt)
    return response.text if hasattr(response, 'text') else response
