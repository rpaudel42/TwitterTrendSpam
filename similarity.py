###############################
#   Author: Prajjwal Kandel   #
#   Date created: 10/17/2018  #
###############################

import string

import nltk
import numpy
from sklearn.feature_extraction.text import TfidfVectorizer

#calculate cosine similarity

class Similarity:
    def __init__(self):
        self.stemmer = nltk.stem.porter.PorterStemmer()
        self.remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
        self.vectorizer = TfidfVectorizer(tokenizer=self.normalize, stop_words='english')

    def stem_tokens(self, tokens):
        return [self.stemmer.stem(item) for item in tokens]

    def normalize(self, text):
        return self.stem_tokens(nltk.word_tokenize(text.lower().translate(self.remove_punctuation_map)))

    def cosine_similarity(self, text1, text2):
        tfidf = self.vectorizer.fit_transform([text1, text2])
        return (tfidf * tfidf.T).A[0, 1]

    def cosine_similarity(self, documents):
        tfidf = self.vectorizer.fit_transform(documents)
        return (tfidf * tfidf.T).A

    def find_max_cosine_similarity_with_known_documents(self, known_documents, new_document):
        documents = known_documents
        documents.append(new_document)
        length = len(documents)
        tfidf = self.vectorizer.fit_transform(documents)
        values = (tfidf * tfidf.T).A[length - 1]
        # remove last element as it is the similarity of new_document with itself
        values = numpy.delete(values, -1)
        return max(values)

    def find_average_cosine_similarity_among_known_documents(self, known_documents):
        sum = 0;
        n = len(known_documents) * (len(known_documents) - 1)
        tfidf = self.vectorizer.fit_transform(known_documents)
        similarity_matrix = (tfidf * tfidf.T).A
        for i in range(len(known_documents)):
            for j in range(len(known_documents)):
                if i == j:
                    continue
                sum += similarity_matrix[i, j]
        return sum / n