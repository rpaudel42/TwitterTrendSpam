import csv
import time

import requests

from src.news_parser import NewsParser
from src.twitter_api_client import TwitterApiClient
from src.utils import Util

twitter_api_client = TwitterApiClient()

news = open("../data/world_cup_news.csv", 'a')
news_writer = csv.writer(news)

user_tweet = open("../data/world_cup_tweets.csv", 'a')
tweet_writer = csv.writer(user_tweet)

news_id = 1;
tweet_id = 1;
max_tweet_id = "1019260988523196416"

for x in range(0, 20):
    result = twitter_api_client.search_tweets(q="fifa world cup", f="news", lang="en", count=100,
                                              max_id=max_tweet_id, until="2018-07-17")
    statuses = result['statuses']
    print(len(statuses))

    tweet_header = ['id', 'docid', 'news date', 'tweet date', 'screen name', 'tweets']
    for status in statuses:
        urls = status['entities']['urls']
        if len(urls) != 0:
            try:
                actual_url = requests.head(urls[0]['url'], allow_redirects=True).url
                if 'twitter.com' not in actual_url:
                    news_parser = NewsParser(actual_url)
                    title = news_parser.get_title().split(" |")[0]
                    if Util.find_sentence_similarity_ratio(title, status['text']) < 0.50:
                        if news_parser.get_publish_date() is not None:
                            published_date = time.strftime('%Y-%m-%d',
                                                           time.strptime(str(news_parser.get_publish_date())[:19],
                                                                         '%Y-%m-%d %H:%M:%S'))
                        else:
                            published_date = "N/A"
                        if len(news_parser.get_authors()) > 0:
                            author = news_parser.get_authors()[0]
                        else:
                            author = "N/A"

                        source_url = news_parser.get_source_url()
                        text = news_parser.get_text().replace("\n", " ")
                        news_row = [news_id, published_date, author, source_url, source_url, actual_url, text]
                        news_writer.writerow(news_row)
                        news_id += 1

                        tweet_date = time.strftime('%Y-%m-%d',
                                                   time.strptime(status['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
                        tweet_row = [tweet_id, tweet_id, published_date, tweet_date, status['user']['name'], status]
                        tweet_writer.writerow(tweet_row)
                        max_tweet_id = status['id']
                        tweet_id += 1
            except Exception as e:
                print(e)
                continue
    print(news_id, tweet_id)
