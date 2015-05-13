#! /usr/bin/env python

expect = [0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]

with open('results.tsv') as f:
    contents = f.read()
    arr = map(lambda x: x.strip(), contents.split('\n\n'))
    arr = [int(x) for x in arr if x != '']
    print arr