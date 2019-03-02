# ******************************************************************************
# anantharam.py
#
# Date      Name       Description
# ========  =========  ========================================================
# 3/1/19   Paudel     Initial version,
# ******************************************************************************


import csv

from similarity import Similarity

class Anantharam():

    def __init__(self):
        print("\n\n----- Starting Anantharam Implementation ----")
        pass

    def trusted_news_builder(self, data_file, trusted_source_file):
        news = open(data_file, 'r')
        news_reader = csv.reader(news, delimiter=',')
        news_sources = {}
        news_source_id = {}
        for row in news_reader:
            if row[6] not in news_sources:
                news_sources[row[6]] = 1
            else:
                news_sources[row[6]] += 1

            if news_sources[row[6]] >= 10:
                news_source_id[row[6]] = row[0]

        news_ids = []
        for x in news_source_id:
            news_ids.append(news_source_id[x])

        trusted_news = open(trusted_source_file, 'a')
        news_writer = csv.writer(trusted_news)

        news = open(data_file, 'r')
        trusted_news_reader = csv.reader(news, delimiter=',')
        for row in trusted_news_reader:
            if row[0] in news_ids:
                news_row = [row[0], row[1], row[2], row[3], row[4], row[5], row[6]]
                news_writer.writerow(news_row)

    def get_trusted_documents(self, trusted_source_file):
        trusted_news = open(trusted_source_file, 'r')
        trusted_news_reader = csv.reader(trusted_news, delimiter=',')

        trusted_documents = []

        for row in trusted_news_reader:
            trusted_documents.append(row[6])

        return trusted_documents

    def extract_anomalies(self, data_file, anomalous_source_file, anomalous_ids):
        news = open(data_file, 'r')
        news_reader = csv.reader(news, delimiter=',')

        anomalous_news = open(anomalous_source_file, 'a')
        news_writer = csv.writer(anomalous_news)

        for row in news_reader:
            if row[0] in anomalous_ids:
                news_row = [row[0], row[1], row[2], row[3], row[4], row[5], row[6]]
                news_writer.writerow(news_row)


    def get_similarity(self, data_file, trusted_source_file):
        similarity_service = Similarity()
        trusted_documents = self.get_trusted_documents(trusted_source_file)
        average_similarity = similarity_service.find_average_cosine_similarity_among_known_documents(trusted_documents)

        print("Average similarity", average_similarity)

        news = open(data_file, 'r')
        news_reader = csv.reader(news, delimiter=',')

        anomalous_news = []
        anomalous_count = 0
        for row in news_reader:
            document = row[6]
            max_similarity = similarity_service.find_max_cosine_similarity_with_known_documents(trusted_documents,
                                                                                                document)
            if max_similarity < average_similarity:
                anomalous_news.append(row[0])
                anomalous_count += 1
                print("Anamolous count", anomalous_count, row[0])