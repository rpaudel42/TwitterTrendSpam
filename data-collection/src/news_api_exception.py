class NewsApiException(Exception):
    def __init__(self, exception):
        self.exception = exception
