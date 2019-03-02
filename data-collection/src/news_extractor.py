from src.news_parser import NewsParser


def main():
    url = "http://zeenews.india.com/sports/fifa/croatia-vs-england-fifa-world-cup-2018-semifinal-live-updates-2124045.html"
    print(extract(url))


def extract(url):
    news_parser = NewsParser(url)
    return news_parser.get_text().replace("\n", " ")


if __name__ == '__main__':
    main()
