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
    Paudel R, Kandel P, Eberle W. [Detecting Spam Tweets in Trending Topics using Graph-Based Approach](https://github.com/rpaudel42/rpaudel42.github.io/blob/master/assets/Spam_detection_in_trending_topic.pdf). (2019 March)
5. The implementation for ﻿Boididou et al. is done using the source code available in their [github repository](https://github.com/MKLab-ITI/computational-verification)

**Description**
This code generate graphs from Tweets and News, run graph-based anomaly detection tool on the generated graph for spam detection.
Also, it implement following three baseline approaches used in the paper for performance comparision.:
+ Benevenuto et al.
+ Chen et al. and
+ Anantharam et al.

