# ******************************************************************************
# benevenuto.py
#
# Date      Name       Description
# ========  =========  ========================================================
# 2/25/19   Paudel     Initial version,
# ******************************************************************************

import ast, csv, sys
import validators

class Benevenuto():

    def __init__(self):
        print("\n\n----- Starting Benevenuto Implementation ----")
        pass

    tweet_list = {}
    news_list = {}
    black_list = []

    spam_id = []
    def read_spam_word(self, filename):
        with open(filename) as words:
            for w in words:
                self.black_list.append(w.strip('\n'))

    def count_spam_word(self, tweet):
        s_count = 0
        for w in tweet.split():
            if w in self.black_list:
                s_count += 1
        return s_count


    def read_files(self, filename):
        # read tweet
        with open(filename, encoding = "ISO-8859-1") as tweet:
            t = csv.DictReader(tweet)
            try:
                i = 0
                for row in t:
                    self.tweet_list[i] = row
                    i += 1
            except csv.Error as e:
                sys.exit('Error in line %d: %s' % (t.line_num, e))

    def is_real_word(self, w):
        if validators.url(w):
            return False
        elif '#' in w:
            return False
        elif '@' in w:
            return False
        else:
            return True

    def count_words(self, tweet):
        w_count = 0
        for w in tweet.split():
            if self.is_real_word(w):
                w_count += 1

        return w_count

    def count_hashtag(self, tweet):
        if tweet['entities']['hashtags']:
            return len(tweet['entities']['hashtags'])
        return 0

    def count_urls(self, tweet):
        url_count = 0
        for w in tweet.split():
            if validators.url(w):
                url_count += 1
        return url_count

    def count_user_mentions(self, tweet):
        if tweet['entities']['user_mentions']:
            return len(tweet['entities']['user_mentions'])
        return 0

    def RT_count(self, tweet):
        rt_count = 0
        words = tweet.split()
        for w in words:
            if words[0] == 'RT' and '@' in w:
                rt_count += 1
        return rt_count

    def is_reply(self, tweet):
        w = tweet.split()
        if w[0] == 'RT':
            return True
        return False

    def count_character(self, tweet):
        char = 0
        num = 0
        if len(tweet) > 0:
            for w in tweet.split():
                if self.is_real_word(w):
                    char += sum(c.isalpha() for c in w)
                    num += sum(c.isdigit() for c in w)
            return char, num
        return char, num

    def generate_features(self, dataset):
        self.read_spam_word('blacklist.txt')
        self.read_files(dataset.file_name)
        # Features to be generated for Benevenuto et. al works
        # number of words from a list of spam words
        # number of hashtags per words,
        # number of URLs per words,
        # number of words,
        # number of numeric characters on the text,
        # number of characters that are numbers,
        # number of URLs,
        # number of hashtags,
        # number of mentions,
        # number of times the tweet has been replied (counted by the presence of “RT @username” on the text),
        # and lastly we verified if the tweet was posted as a reply.
        # Define Data

        # # Open File
        # resultFyle = open("output.csv", 'w')
        #
        # # Write data to file
        # for r in RESULTS:
        #     resultFyle.write(r + "\n")
        # resultFyle.close()
        #
        wr = open(dataset.feature_file, 'w')
        wr = csv.writer(wr, dialect='excel')
        header = ['id', 'n_spam_word', 'hashtag_per_word', 'url_per_word', 'num_word', 'num_char', 'num_digit', 'num_url', 'num_hashtag', 'num_user_mention', 'num_rt', 'is_reply', 'is_spam']
        wr.writerow(header)

        for row in self.tweet_list:
            if 1==1: #row >= 0 and row <= 75:
                feature_row = []
                feature_row.append(row)
                tweet = ast.literal_eval(self.tweet_list[row]['tweet'])
                tweet_text = tweet['text']
                #print("Tweet : ", tweet_text)

                n_spam_word = self.count_spam_word(tweet_text) #need to generate this
                print("Spam Word: ", n_spam_word)
                feature_row.append(n_spam_word)

                w_count = self.count_words(tweet_text)
                #print("Word Count: ", w_count)

                hashtag_count = self.count_hashtag(tweet)
                #print("Hashtag Count: ", hashtag_count)
                feature_row.append(hashtag_count/w_count)


                url_count = self.count_urls(tweet_text)
                #print("URL Count: ", url_count)
                feature_row.append(url_count/w_count)
                feature_row.append(w_count)

                c_count, n_count = self.count_character(tweet_text)
                #print("Character Count: ", c_count, n_count)
                feature_row.append(c_count)
                feature_row.append(n_count)
                feature_row.append(url_count)
                feature_row.append(hashtag_count)

                u_mention_count = self.count_user_mentions(tweet)
                #print("User Mention Count: ", u_mention_count)

                feature_row.append(u_mention_count)

                rt_count = self.RT_count(tweet_text)
                #print("Tweet Reply Count: ", rt_count)

                feature_row.append(rt_count)

                reply = self.is_reply(tweet_text)
                #print("Is a Reply: ", reply)
                feature_row.append(reply)

                if row in dataset.spam_id:
                    is_spam = True
                else:
                    is_spam = False

                feature_row.append(is_spam)
                #print(" \n---------- \n\n")
                wr.writerow(feature_row)








