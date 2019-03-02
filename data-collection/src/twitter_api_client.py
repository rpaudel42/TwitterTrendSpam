import numbers

import requests

import src.config as config


class TwitterApiClient:
    SEARCH_URL = "https://api.twitter.com/1.1/search/tweets.json"
    FIND_BY_ID_URL = "https://api.twitter.com/1.1/statuses/show.json"

    def __init__(self):
        self.api_key = "Bearer " + config.twitter_authorization_key

    def search_tweets(self, q=None, lang=None, result_type=None, count=None, until=None, since_id=None, max_id=None, f = None):
        headers = {'Authorization': self.api_key}
        params = {}
        if q is not None:
            if type(q) == str:
                params['q'] = q

        if lang is not None:
            if type(lang) == str:
                params['lang'] = lang

        if result_type is not None:
            if result_type in ["mixed", "recent", "popular"]:
                params['result_type'] = result_type

        if count is not None:
            if type(count) == int:
                params['count'] = count

        if until is not None:
            if type(until) == str:
                params['until'] = until

        if since_id is not None:
            if isinstance(since_id, numbers.Number):
                params['since_id'] = since_id

        if max_id is not None:
            if isinstance(max_id, numbers.Number):
                params['max_id'] = max_id

        if f is not None:
            if type(f) == str:
                params['filter'] = f

        result = requests.get(url=self.SEARCH_URL, headers=headers, params=params)
        return result.json()

    def find_by_id(self, tweet_id):
        headers = {'Authorization': self.api_key}
        params = {'id':tweet_id}
        result = requests.get(url=self.FIND_BY_ID_URL, headers=headers, params=params)
        return result.json()


