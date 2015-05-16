#! /usr/bin/env python

from __future__ import division
import matplotlib.pyplot as plt

expect = [0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
length= len(expect)

with open('results.tsv') as f:
    contents = f.read()
    arr = map(lambda x: x.strip(), contents.split('\n\n'))
    arr = [int(x) for x in arr if x != '']
    true_expect = arr[0:length]
    false_expect = arr[length:(2*length)]
    nb_predicted = arr[(2*length):(3*length)]
    nb_recall = arr[(3*length):(4*length)]
    nb_recall_tot = arr[4*length]
    precision = [true_expect[x]/(true_expect[x] + false_expect[x]) for x in range(length)]
    recall = [nb_recall[x]/nb_recall_tot for x in range(length)]

    fig=plt.figure()
    fig.suptitle("Estimation precision - recall", fontsize=16)
    ax = plt.subplot("222")
    ax.set_title("Precision")
    ax.scatter (expect, precision)

    ax = plt.subplot("212")
    ax.set_title("Number predicted")
    ax.scatter (expect, nb_predicted)

    ax = plt.subplot("221")
    ax.set_title("Recall")
    ax.scatter (expect, recall)



    plt.show()