from newspaper import Article, ArticleException


class NewsParser:
    def __init__(self, news_url):
        self.news_url = news_url
        self.article = Article(news_url)
        try:
            self.article.download()
            self.article.parse()
            self.parse_success = True
            self.publish_date = self.article.publish_date
        except ArticleException:
            self.parse_success = False

    def get_text(self):
        return self.article.text

    def get_authors(self):
        return self.article.authors

    def get_title(self):
        return self.article.title

    def get_source_url(self):
        return self.article.source_url

    def get_publish_date(self):
        return self.article.publish_date

    def get_summary(self):
        self.article.nlp()
        return self.article.summary

    def is_parse_successful(self):
        return self.parse_success
