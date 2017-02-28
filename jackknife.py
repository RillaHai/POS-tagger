#! /bin/python
#-*- coding:utf-8 -*-
import argparse

argpar = argparse.ArgumentParser(description = 'Computing statistics for words and sentences in corpus')
argpar.add_argument('-i','--input',dest='inputfile',nargs='+',required=True,help='Files to be caculated')

args = argpar.parse_args()

def read_conll09 (filename):
    corpus = []
    sentence = []
    for line in open (filename):
        line = line.strip()
        if line == "": # found  the end of a sentence
            corpus.append(sentence)
            sentence = []
        else: # found token
            entries = line.split('\t')
            sentence.append(entries)
    return corpus

for filename in args.inputfile:
    corpus = read_conll09(filename)
    
    N = len(corpus)
    
def chunks(l, n):
    if n < 1:
        n = 1
    return [l[i:i + n] for i in range(0, len(l), n)]
    
source = chunks(corpus,N/10)

for i in range(10):
    testfile=open(filename+"testfile%d"%i,'w')
    trainfile=open(filename+"trainfile%d"%i,'w')
    for j in range(10):
        if i == j:
            for sentence in source[i]:
                for line in sentence:
                    print >> testfile,'\t'.join(line)
                print >> testfile
        else:
            for sentences in source[j]:
                for lines in sentences:
                    print >> trainfile, '\t'.join(lines)
                print >> trainfile


