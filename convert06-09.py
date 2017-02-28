#! /bin/python
#-*- coding:utf-8 -*-
import sys

for filename in sys.argv[1:]:
    with open(filename)as fin:
        with open(filename + ".conll09",'w')as fout:
            for line in open(filename):
                line = line.strip()
                if line != '':
                    lst = line.split("\t")
                    lst[3]= lst[2]
                    print >> fout,'\t'.join(lst)
                else :
                    print >> fout
      
