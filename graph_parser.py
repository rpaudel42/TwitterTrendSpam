# ******************************************************************************
# classifier.py
#
# Date      Name       Description
# ========  =========  ========================================================
# 2/25/19   Paudel     Initial version,
# ******************************************************************************
import time, ast, csv, sys, nltk, re, requests, json
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

class GraphParser:

    SUB_CLASS_URI = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
    SPARQL_URL = "http://dbpedia.org/sparql"

    def __init__(self):
        print("\n\n----- Starting Graph Parser ----")

    def query(self, q, epr, f='application/json'):
        try:
            params = {'query': q}
            resp = requests.get(epr, params=params, headers={'Accept': f})
            return resp.text
        except Exception as e:
            print("Ontology Error: ", e)


    def generate_ontology(self, identifier, identifier_class):
        identifier_url = self.get_identifier_url(identifier, identifier_class)
        if identifier_url is not None:
            result = self.query(self.construct_query(identifier_url), self.SPARQL_URL)
            subclasses = self.get_subclasses_from_json(result)
            hierarchy = self.form_hierarchy(identifier_class, subclasses)
            hierarchy.append(self.get_subclass(identifier_url).replace("_",' '))
            return hierarchy
        else:
            return [identifier]

    def construct_query(self, identifier_url):
        return "CONSTRUCT WHERE {<"+identifier_url + "> a ?c1 ; a ?c2 . ?c1 rdfs:subClassOf ?c2 . ?c1 " \
                                               "rdfs:label ?label . FILTER (LANG(?label)='en')}"


    def get_subclasses_from_json(self, query_result):
        obj = json.loads(query_result)
        subclasses = {}
        for key in obj.keys():
            if key.startswith('http://dbpedia.org/ontology'):
                subclass = self.get_subclass(key)
                if subclass == "Agent":
                    continue
                else:
                    for ontology in obj[key][self.SUB_CLASS_URI]:
                        if ontology["value"].startswith('http://dbpedia.org/ontology'):
                            subclasses[self.get_subclass(ontology["value"])] = subclass
                            break;
        return subclasses


    def form_hierarchy(self, identifier_class, subclasses):
        hierarchy = []
        current_key = identifier_class
        for i in range(0, len(subclasses)):
            if current_key not in subclasses:
                break
            hierarchy.append(subclasses[current_key])
            current_key = subclasses[current_key]
        return hierarchy


    def get_subclass(self, url):
        return url.split('/')[-1]


    def format_identifier(self, identifier):
        words = identifier.title().split(' ')
        if len(words) == 1:
            return words[0]
        else:
            return "_".join(words)


    def get_identifier_url(self, identifier, identifier_class):
        request_url = "http://lookup.dbpedia.org/api/search/KeywordSearch?QueryClass={}&QueryString={}".format(identifier_class,identifier)
        results = requests.get(request_url,headers={'Accept': 'application/json'}).json()['results']
        if results:
            return results[0]['uri']


    def read_files(self, tweet_file, news_file):
        # read tweet
        t_list = {}
        with open(tweet_file, encoding = "ISO-8859-1") as tweet:
            t = csv.DictReader(tweet)
            try:
                i = 0
                for row in t:
                    t_list[i] = row
                    i += 1
            except csv.Error as e:
                sys.exit('Error in line %d: %s' % (t.line_num, e))

        # read Document
        n_list = {}
        with open(news_file, encoding="ISO-8859-1") as news:
            n = csv.DictReader(news)
            try:
                i = 0
                for row in n:
                    n_list[i] = row
                    i += 1
            except csv.Error as e:
                sys.exit('Error in line %d: %s' % (n.line_num, e))

        return t_list, n_list

    def get_nlp_results(self, text):
        chunked = ne_chunk(pos_tag(word_tokenize(text)))
        # print("Chunked: ", chunked)
        prev = None
        continuous_chunk = {}
        current_chunk = []
        label = "Agent"
        for i in chunked:
            if hasattr(i, 'label'):
                label = i.label()
            if type(i) == Tree:
                current_chunk.append(" ".join([token for token, pos in i.leaves()]))
            elif current_chunk:
                named_entity = " ".join(current_chunk)
                if named_entity not in continuous_chunk:
                    # continuous_chunk.append(named_entity)
                    continuous_chunk[named_entity] = label
                    current_chunk = []
            else:
                continue
        return continuous_chunk

    def get_textblob_tweet_sentiment(self, tweettext):
        blob = TextBlob(tweettext, analyzer=NaiveBayesAnalyzer())
        classification = blob.sentiment.classification
        return classification


    def have_valid_hashtags(self, hashtags):
        status = False
        stopwordlist = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()
        for hashtag in hashtags:
            if hashtag['text'].isalpha() and hashtag['text'] not in stopwordlist:
                return True
            elif hashtag['text'].isnumeric():
                return True
            elif re.search(r'\d', hashtag['text']):
                return True
            else:
                status = False
        return status

    def filter_hashtags(self, hashtag):
        stopwordlist = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()
        if hashtag.isalpha() and hashtag not in stopwordlist:
            return True, lemmatizer.lemmatize(hashtag)
        elif hashtag.isnumeric():
            return True, hashtag
        elif re.search(r'\d', hashtag):
            return True, hashtag
        else:
            return False, hashtag

    def filter_words(self, word_to_test):
        stopwordlist = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()
        if 'article' in word_to_test:
            return False, word_to_test
        if 'print' in word_to_test:
            return False, word_to_test

        if ' ' in word_to_test:
            words = word_to_test.split(' ')
            for w in words:
                if not w.strip('.').isnumeric():
                    if not w.strip('.').isalpha():
                        return False, word_to_test
            return True, word_to_test

        else:
            word_to_test = word_to_test.strip('\'').strip('.')
            if word_to_test.isalpha() and word_to_test not in stopwordlist:
                return True, lemmatizer.lemmatize(word_to_test)
            elif word_to_test.isnumeric():
                return True, word_to_test
            else:
                return False, word_to_test


    def get_nlp_keyword_results(self, textFile, flag):
        words = word_tokenize(textFile)
        #Remove all single character
        words = [word for word in words if len(word) > 2]
        #remove numbers
        words = [word for word in words if not word.isnumeric()]
        #Lowercase all words
        words = [word.lower() for word in words]
        #Remove stopwords
        stopwordlist = set(stopwords.words('english'))
        words = [word for word in words if word not in stopwordlist]
        #Lemmatize words
        lemmatizer = WordNetLemmatizer()
        words = [lemmatizer.lemmatize(word) for word in words]

        #Calculate token frequency
        fdist = nltk.FreqDist(words)

        if flag == 1: # if it is news return top 5 keywords
            count = 1
            keywords = {}
            for key, val in fdist.most_common(5):
                status, parsed_k = self.filter_words(key)
                if status and count <= 5:
                    keywords[parsed_k] = val
                    count += 1
            return keywords
        else: #if it is twitter just return 3 keyword only if they are repeated more than once
            count = 1
            keywords = {}
            for key, val in fdist.most_common(5):
                if val > 1 and 'http' not in key:
                    status, parsed_k = self.filter_words(key)
                    if status and count <= 3:
                        keywords[parsed_k] = val
                        count += 1
            return keywords


    def get_all_entities(self, text):
        try:
            entities = self.get_nlp_results(text)
            all_news_entites = []
            for key in entities.keys():
                status, parsed_key = self.filter_words(key.lower())
                if status is True:
                    identifier = key.lower()
                    if entities[key] == "GPE" or entities[key] == "GSP" or entities[key] == "FACILITY":
                        identifier_class = "Place"
                    else:
                        identifier_class = "Agent"

                    hierarcy = self.generate_ontology(identifier, identifier_class)
                    if hierarcy[0] == key.lower():
                        continue
                    else:
                        all_news_entites.append(hierarcy)
            return all_news_entites
        except Exception as e:
            print("Error in Ontology:" , e)


    def parse_tweet(self, tweetDump, tweetHandle, tweetNode, k):
        try:
            t = ast.literal_eval(tweetDump) #json.loads(tweetDump)
            if t['entities']['hashtags'] and self.have_valid_hashtags(t['entities']['hashtags']):
                fw.write("v " + str(k) + " \"hashtags\"\n")
                fw.write("d " + str(tweetNode) + " " + str(k) + " \"has\"\n")
                hashtag = k
                k += 1
                #check if this is a legitimate hastags..
                for h in t['entities']['hashtags']:
                    hashstatus, parsed_hash = self.filter_hashtags(h['text'].lower())
                    if hashstatus:
                        fw.write("v " + str(k) + " \"" + parsed_hash + "\"\n")
                        fw.write("d " + str(hashtag) + " " + str(k) + " \"is\"\n")
                        k += 1
            if t['entities']['user_mentions']:
                for m in t['entities']['user_mentions']:
                    fw.write("v " + str(k) + " \"handle\"\n")
                    fw.write("d " + str(tweetNode) + " " + str(k) + " \"mention\"\n")
                    mentionhandle = k
                    k += 1

            try:
                all_news_entites = self.get_all_entities(t['text'])
                entity_tree = {}
                for hierarcy in all_news_entites:
                    if len(hierarcy) > 1:
                        node_count = 0
                        prev_node = ""
                        for node in hierarcy:
                            if node not in entity_tree and node_count == 0:
                                fw.write("v " + str(k) + " \"" + node.lower() + "\"\n")
                                entity_tree[node] = k
                                fw.write("d " + str(tweetNode) + " " + str(entity_tree[node]) + " \"has\"\n")
                                k += 1
                            elif node not in entity_tree and node_count > 0:
                                entity_tree[node] = k
                                fw.write("v " + str(k) + " \"" + node.lower() + "\"\n")
                                fw.write(
                                    "d " + str(entity_tree[prev_node]) + " " + str(entity_tree[node]) + " \"is_a\"\n")
                                k += 1
                            node_count += 1
                            prev_node = node
            except Exception as e:
                print("Tweet Ontology Erro: ", e)

            # find top keywords from tweet Text
            tweetkeywords = self.get_nlp_keyword_results(t['text'], 2)
            if tweetkeywords:
                fw.write("v " + str(k) + " \"keywords\"\n")
                fw.write("d " + str(tweetNode) + " " + str(k) + " \"has\"\n")
                tkeyword = k
                k += 1
                for key in tweetkeywords:
                    fw.write("v " + str(k) + " \"" + key + "\"\n")
                    fw.write("d " + str(tkeyword) + " " + str(k) + " \"is\"\n")
                    k += 1
            return k
        except:
            print("Tweet NLP Parsing Error")
            return k


    def graph_parser(self, fw, xp, tweet_list, news_list):
        for i in news_list:
            if 1 == 1:
                #check if the news has twitter handle
                matching_tweet = [row for row in tweet_list if
                                  (tweet_list[row]['docid'] == news_list[i]['id'] and int(tweet_list[row]['docid']) <= 2)]# and int(tweet_list[row]['docid']) <= 20)]
                if len(matching_tweet) > 0:
                    for row in matching_tweet:
                        print(".... Graph: [ %s ] ....", (news_list[i]['id']))
                        k = 1
                        fw.write("XP # " + str(xp) + " //" + news_list[i]['id'] + "\n")
                        fw.write("v " + str(k) + " \"news\"\n")
                        news = k
                        k += 1
                        if news_list[i]['date'] != "N/A":
                            fw.write("v " + str(k) + " \"date\"\n")
                            fw.write("d " + str(news) + " " + str(k) + " \"published_on\"\n")
                            date = k
                            k += 1
                            fw.write("v " + str(k) + " \"" + "20" + news_list[i]['date'].split("/", 3)[2] + "\"\n")
                            fw.write("d " + str(date) + " " + str(k) + " \"year\"\n")
                            k += 1
                            fw.write("v " + str(k) + " \"" + news_list[i]['date'].split("/", 3)[0] + "\"\n")
                            fw.write("d " + str(date) + " " + str(k) + " \"month\"\n")
                            k += 1
                            fw.write("v " + str(k) + " \"" + news_list[i]['date'].split("/", 3)[1] + "\"\n")
                            fw.write("d " + str(date) + " " + str(k) + " \"day\"\n")
                            k += 1

                        if news_list[i]['author'] != "N/A":
                            fw.write("v " + str(k) + " \"author\"\n")
                            fw.write("d " + str(news) + " " + str(k) + " \"wrote_by\"\n")
                            author = k
                            k += 1
                            if "and" in news_list[i]['author'].lower():
                                authors = news_list[i]['author'].lower().split(" and ")
                                for aut in authors:
                                    fw.write("v " + str(k) + " \"" + aut.lower() + "\"\n")
                                    fw.write("d " + str(author) + " " + str(k) + " \"name\"\n")
                                    k += 1
                            else:
                                fw.write("v " + str(k) + " \"" + news_list[i]['author'].lower() + "\"\n")
                                fw.write("d " + str(author) + " " + str(k) + " \"name\"\n")
                                k += 1
                        fw.write("v " + str(k) + " \"media\"\n")
                        fw.write("d " + str(news) + " " + str(k) + " \"published_in\"\n")
                        media = k
                        k += 1
                        if "www." in news_list[i]['source']:
                            fw.write("v " + str(k) + " \"" + news_list[i]['source'].lower().split("www.",1)[1] + "\"\n")
                            fw.write("d " + str(media) + " " + str(k) + " \"name\"\n")
                            k += 1
                        elif "://" in news_list[i]['source']:
                            fw.write("v " + str(k) + " \"" + news_list[i]['source'].lower().split("://", 1)[1] + "\"\n")
                            fw.write("d " + str(media) + " " + str(k) + " \"name\"\n")
                            k += 1
                        else:
                            fw.write("v " + str(k) + " \"" + news_list[i]['source'].lower() + "\"\n")
                            fw.write("d " + str(media) + " " + str(k) + " \"name\"\n")
                            k += 1

                        #Find entites from News Body during first occurance else use same ontology.. avoid multiple call to dbpedia and nlp api
                        try:
                            all_news_entites = self.get_all_entities(news_list[i]['bodyTEXT'])
                            entity_tree = {}
                            for hierarcy in all_news_entites:
                                if len(hierarcy) > 1:
                                    node_count = 0
                                    prev_node = ""
                                    for node in hierarcy:
                                        if node not in entity_tree and node_count == 0:
                                            fw.write("v " + str(k) + " \"" + node.lower() + "\"\n")
                                            entity_tree[node] = k
                                            fw.write("d " + str(news) + " " + str(entity_tree[node]) + " \"has\"\n")
                                            k += 1
                                        elif node not in entity_tree and node_count > 0:
                                            entity_tree[node] = k
                                            fw.write("v " + str(k) + " \"" + node.lower() + "\"\n")
                                            fw.write("d " + str(entity_tree[prev_node]) + " " + str(entity_tree[node]) + " \"is_a\"\n")
                                            k += 1
                                        node_count += 1
                                        prev_node = node
                        except Exception as e:
                            print("Ontology Error: ", e)


                        handle_tracker = {}
                        if tweet_list[row]['screen name'] not in handle_tracker:
                            handle_tracker[tweet_list[row]['screen name']] = k
                            fw.write("v " + str(k) + " \"handle\"\n")
                            fw.write("d " + str(k) + " " + str(news) + " \"mention\"\n")
                            handle = k
                            k += 1

                            t = ast.literal_eval(tweet_list[row]['tweet'])
                            try:
                                all_news_entites = self.get_all_entities(t['user']['description'])
                                entity_tree = {}

                                for hierarcy in all_news_entites:
                                    if len(hierarcy) > 1:
                                        node_count = 0
                                        prev_node = ""
                                        for node in hierarcy:
                                            if node not in entity_tree and node_count == 0:
                                                fw.write("v " + str(k) + " \"" + node.lower() + "\"\n")
                                                entity_tree[node] = k
                                                fw.write("d " + str(handle) + " " + str(entity_tree[node]) + " \"is_about\"\n")
                                                k += 1
                                            elif node not in entity_tree and node_count > 0:
                                                entity_tree[node] = k
                                                fw.write("v " + str(k) + " \"" + node.lower() + "\"\n")
                                                fw.write(
                                                    "d " + str(entity_tree[prev_node]) + " " + str(
                                                        entity_tree[node]) + " \"is_a\"\n")
                                                k += 1
                                            node_count += 1
                                            prev_node = node

                                all_news_entites = self.get_all_entities(t['user']['location'])
                                entity_tree = {}
                                for hierarcy in all_news_entites:
                                    if len(hierarcy) > 1:
                                        node_count = 0
                                        prev_node = ""
                                        for node in hierarcy:
                                            if node not in entity_tree and node_count == 0:
                                                fw.write("v " + str(k) + " \"" + node.lower() + "\"\n")
                                                entity_tree[node] = k
                                                fw.write("d " + str(handle) + " " + str(entity_tree[node]) + " \"is_from\"\n")
                                                k += 1
                                            elif node not in entity_tree and node_count > 0:
                                                entity_tree[node] = k
                                                fw.write("v " + str(k) + " \"" + node.lower() + "\"\n")
                                                fw.write(
                                                    "d " + str(entity_tree[prev_node]) + " " + str(
                                                        entity_tree[node]) + " \"is_a\"\n")
                                                k += 1
                                            node_count += 1
                                            prev_node = node
                            except Exception as e:
                                print("Tweet Description Error: ", e)
                        else:
                            handle = handle_tracker[tweet_list[row]['screen name']]

                        fw.write("v " + str(k) + " \"tweet\"\n")
                        fw.write("d " + str(handle) + " " + str(k) + " \"post\"\n")
                        tweet = k
                        k += 1
                        if tweet_list[row]['tweet date']:
                            fw.write("v " + str(k) + " \"date\"\n")
                            fw.write("d " + str(tweet) + " " + str(k) + " \"post_on\"\n")
                            tdate = k
                            k += 1

                            time_struct = time.strptime(tweet_list[row]['tweet date'], "%m/%d/%y") #"%a %b %d %H:%M:%S +0000 %Y")  # Tue Apr 26 08:57:55 +0000 2011
                            fw.write("v " + str(k) + " \"" + str(time_struct.tm_year) + "\"\n")
                            fw.write("d " + str(tdate) + " " + str(k) + " \"year\"\n")
                            k += 1
                            fw.write("v " + str(k) + " \"" + str(time_struct.tm_mon) + "\"\n")
                            fw.write("d " + str(tdate) + " " + str(k) + " \"month\"\n")
                            k += 1
                            fw.write("v " + str(k) + " \"" + str(time_struct.tm_mday) + "\"\n")
                            fw.write("d " + str(tdate) + " " + str(k) + " \"day\"\n")
                            k += 1
                        #Parse Tweet JSON
                        k = self.parse_tweet(tweet_list[row]['tweet'], handle, tweet, k)
                        xp += 1