#!/usr/bin/env python

f2 = open('founder_company.tsv', 'w')

with open('freebase_output.tsv') as f:
    for line in f:
        name1, name2, name3 = line.split('\t')
        if '1' in name3:
            try:
                first, last = name2.split(' ')
                f2.write(name2 + '\t' + name1 + '\n')
                f2.write(last + '\t' + name1 + '\n')
            except:
                print 'middle name...'
            try:
                first, middle, last = name2.split(' ')
                f2.write(name2 + '\t' + name1 + '\n')
                f2.write(last + '\t' + name1 + '\n')
            except:
                pass

f2.close()