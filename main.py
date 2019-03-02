# ******************************************************************************
# main.py
#
# Date      Name       Description
# ========  =========  ========================================================
# 2/25/19   Paudel     Initial version,
# ******************************************************************************

from dataset import Dataset
from benevenuto import Benevenuto
from chen import Chen
from anantharam import Anantharam
from classifier import Classifier
from graph_parser import GraphParser
import time, os

# Spam List for each dataset
n_spam_id = [249, 252, 256, 270, 610, 841, 843, 1097, 1142, 1440, 1630]
f_spam_id = [6, 8, 257, 351, 513, 627, 701, 719, 744, 767, 793, 832, 853, 863, 864, 866, 884, 1016, 1098, 1137, 1180, 1206]
o_spam_id = []

#Dataset Description ....
#DataName = [<Name>, <tweet file>, <spam list>, <feature file for Benevenuto et al.>, <feature file for Chen et al. >, <resample size if needed, default 0> <news file>]
FIFA = ['FIFA', 'data/world-cup/world_cup_tweets.csv', f_spam_id, 'data/world-cup/benevenuto_fifa_feature.csv','data/world-cup/chen_fifa_feature.csv', 22, 'data/world-cup/world_cup_news.csv']
NATO = ['NATO', 'data/nato/nato_tweets.csv', n_spam_id, 'data/nato/benevenuto_nato_feature.csv','data/nato/chen_nato_feature.csv', 11, 'data/nato/nato_news.csv']
OSCAR = ['OSCAR', 'data/oscar/oscar_tweet.csv', o_spam_id, 'data/oscar/benevenuto_oscar_feature.csv', 'data/oscar/chen_oscar_feature.csv', 0, 'data/oscar/oscar_news.csv']


def print_result(result):
    print ("\nClassification Report: ")
    print("-----------------------")
    p=0
    r=0
    f1=0
    g=0
    for i in result:
        p += result[i]['p']
        r += result[i]['r']
        f1 += result[i]['f1']
        g += result[i]['g']

    print("Precision: ", p/len(result))
    print("Recall:    ", r/len(result))
    print("F1-Score:  ", f1/len(result))
    print("G-Mean:    ", g/len(result))

def benevenuto_et_al(d):
    #Open this section for feature generation
    # ds = Dataset()
    # data = ds.initialize_dataset(d)
    #
    # bv = Benevenuto()
    # bv.generate_features(data)

    result = {}
    print("\n------------ Benevenuto et. al ---------------")
    for i in range(0, 10):
        cs = Classifier(d[3], "B", d[5])  # 75
        result[i] = cs.svm_classify()
    print_result(result)

def chen_et_al(d):
    # Open this section for feature generation
    # ds = Dataset()
    # data = ds.initialize_dataset(NATO)
    #
    # ch = Chen()
    # ch.generate_features(data)
    result = {}
    print("\n------------ Chen et. al ---------------")
    for i in range(0, 10):
        cs = Classifier(d[4], "C", d[5])
        result[i] = cs.random_forest()
    print_result(result)

def anantharam_et_al(d):
    trusted_file = {"NATO":"data/nato/nato_trusted_news.csv", "FIFA": "data/world-cup/world_cup_trusted_news.csv", "OSCAR": "data/oscar/oscar_trusted_news.csv"}
    data_file = d[6]
    trusted_source_file = trusted_file[d[0]]

    at = Anantharam()

    #open this for creating trusted news source
    #at.trusted_news_builder(data_file, trusted_source_file)
    print("\n------------ Anantharam et. al ---------------")
    at.get_similarity(data_file, trusted_source_file)

def implement_baseline(data):
    benevenuto_et_al(data)
    chen_et_al(data)
    anantharam_et_al(data)

def run_anomaly_detection(data_file, flag, graph_file, parameters):
    output_file = data_file+ "_" + flag + "_result.txt"
    graph_command = "bin/gbad " + parameters + graph_file + " >>" + output_file
    print("Graph Command: ", graph_command)
    os.system(graph_command)
    return output_file

#make a list of all datasets
data_list = [FIFA, NATO]

#make a list of GBAD parameter for each dataset
gbad_parameter = {"FIFA":" -minsize 5 -maxsize 12 -norm 1 -mps 0.25 -maxAnomalousScore 24 ", "NATO":" -minsize 9 -maxsize 9 -norm 2 -mps 0.35 -maxAnomalousScore 52 -minAnomalousScore 52 "}

mixed_graph_files = {"FIFA": "data/graphs/fifa-total.g", "NATO": "data/graphs/nato-total.g"}
tweet_graph_files = {"FIFA": "data/graphs/fifa-tweet.g", "NATO": "data/graphs/nato-tweet.g"}

def main():
    for d in data_list:
        print("\n\n===========================================")
        print("------------ %s DATASET ---------------"%d[0])
        print("===========================================")

        mixed_graph = mixed_graph_files[d[0]]
        tweet_graph = tweet_graph_files[d[0]]

        # Open graph parser if you need to create graph files

        # gp = GraphParser()
        # tweet_list, news_list = gp.read_files(d[1], d[6])
        #
        # print("----- Finish reading tweets/news ----")
        # time.sleep(2)
        # print("----- Starting Graph Construction ----")
        #
        # fw = open(graph_files[d[0]], "w")
        # xp = 1
        # gp.graph_parser(fw, xp, tweet_list, news_list)

        #run Graph-Based Anomaly ..
        #It might take around 1 hour to finish...

        # tweet Graph
        result = run_anomaly_detection(d[0], "T", tweet_graph, gbad_parameter[d[0]])
        print("Graph-based anomaly result in Tweet Graph is in: ", result)

        #mixed Graph
        result = run_anomaly_detection(d[0], "M",  mixed_graph, gbad_parameter[d[0]])
        print("Graph-based anomaly result in Mixed Graph is in: ", result)


        print("\n\nImplement baseline approaches....")
        implement_baseline(d)

        #Open this if you open graph parser...
        #del gp


if __name__ == '__main__':
    main()