import requests

import src.config as config
from src.news_api_exception import NewsApiException


class NewsApiClient:
    TOP_HEADLINE_URL = "https://newsapi.org/v2/top-headlines"
    EVERYTHING_URL = "https://newsapi.org/v2/everything"

    def __init__(self):
        self.api_key = config.news_api_key

    def get_top_headlines(self, q=None, country=None, category=None, sources=None, pageSize=None, page=None):
        params = {'apiKey': self.api_key}
        if q is not None:
            if type(q) == str:
                params['q'] = q

        if category is not None:
            if type(category) == str:
                params['category'] = category

        if sources is not None:
            if type(sources) == str:
                params['sources'] = sources

        if pageSize is not None:
            if type(pageSize) == int:
                params['pageSize'] = pageSize

        if page is not None:
            if type(page) == int:
                params['page'] = page

        result = requests.get(url=self.TOP_HEADLINE_URL, params=params)
        return result.json()

    def get_everything(self, q=None, domains=None, category=None, sources=None, language=None, startDate=None,
                       endDate=None, sortBy=None, pageSize=None, page=None):
        params = {'apiKey': self.api_key}
        if q is not None:
            if type(q) == str:
                params['q'] = q

        if category is not None:
            if type(category) == str:
                params['category'] = category

        if sources is not None:
            if type(sources) == str:
                params['sources'] = sources

        if language is not None:
            if type(language) == str:
                params['language'] = language

        if startDate is not None:
            if type(startDate) == str:
                params['from'] = startDate

        if endDate is not None:
            if type(endDate) == str:
                params['to'] = endDate

        if sortBy is not None:
            if type(sortBy) == str:
                params['sortBy'] = sortBy

        if pageSize is not None:
            if type(pageSize) == int:
                params['pageSize'] = pageSize

        if page is not None:
            if type(page) == int:
                params['page'] = page

        result = requests.get(url=self.EVERYTHING_URL, params=params).json()
        if result['status'] != 'ok':
            print(result)
            raise NewsApiException(result)

        return result
