**Requirements**
=============

1. python (3.0)
2. Python packages:
	- matplotlib
	- scikit-learn
	- pandas
	- nltk
	- request
	- json
	- numpy


**Usage**
======

$ make

if Make is not installed
------------------------
$ python3 main.py


**Notes**
=====

1. Make sure "data" folder have "nato" and "world-cup" folder and the associated data files
2. Make sure you have "bin" and "src" folder
3. Go to "src" folder and run following commands:
    -make clean
    -make
    -make install
4. This code implements following paper:
    Paudel R, Kandel P, Eberle W. Detecting Spam Tweets in Trending Topics using Graph-Based Approach. (2019 March)
5. The implementation for ﻿Boididou et al. is done using the source code available in their [github repository](https://github.com/MKLab-ITI/computational-verification)

**Description**
In this work, we implement an unsupervised, two-step, graph-based approach
to detect anomalous tweets on trending topics. First, we extract named entities
(like place, person, organization, product, event, or activity) present in the tweet
and add them as key elements in the graph. As tweets on a certain topic share
the contextual similarity, we believe they also share same/similar named entities.
These named entities representing relevant/similar topics can have a relationship
(e.g., shared ontology) amongst themselves, which we believe if represented
properly, will provide broader insight on the overall context of the topic.
Using a well-known graph-based tool like GBAD, we
then discover the normal and anomalous behavior of a trending topic.
<br/>
Second, we propose adding hyperlinked document information because anomalies that
could not be detected from tweets alone could be detected using both the document
and tweets. It is our assumption that a better understanding of patterns
and anomalies associated with entities like person, place, or activity, cannot be
realized through a single information source, but better insight can be realized
using multiple information sources simultaneously. For instance, one can discover
interesting patterns of behavior about an individual through a single social media
account, but better insight into their overall behavior can be realized by
examining all of their social media actions simultaneously. Analyzing multiple
information sources for anomaly detection on Twitter has been explored in the
past.
<br/>
This code generate graphs from Tweets and News, run graph-based anomaly detection tool on the generated
graph for spam detection. Also, it implement following three baseline approaches used in the paper for
performance comparision.:
+ Benevenuto et al.
+ Chen et al. and
+ Anantharam et al.
<br/>
The result of the experiment is shown in following table. Our graph-based approach is superior to all 4 baseline approaches in terms of recall and f1-score.
![Performance Comparision for World Cup and NATO Summit Dataset](figures/results.png)
<br/>
If you have further inquiry please email at rpaudel42@students.tntech.edu