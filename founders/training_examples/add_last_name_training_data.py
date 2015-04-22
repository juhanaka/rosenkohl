#!/usr/bin/env python

f2 = open('freebase_output2.tsv', 'w')

with open('freebase_output.tsv') as f:
    for line in f:
        name1, name2, name3 = line.split('\t')
        try:
            first, last = name2.split(' ')
            f2.write(name1 + '\t' + name2 + '\t' + name3)
            f2.write(name1 + '\t' + last + '\t' + name3)
        except:
            print 'middle name...'
        try:
            first, middle, last = name2.split(' ')
            f2.write(name1 + '\t' + name2 + '\t' + name3)
            f2.write(name1 + '\t' + last + '\t' + name3)
        except:
            pass

f2.close()