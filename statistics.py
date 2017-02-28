#! /bin/python
#-*- coding:utf-8 -*-
import argparse
import sys
import math

argpar = argparse.ArgumentParser(description = 'Computing statistics for words and sentences in corpus')
argpar.add_argument('-i','--input',dest='inputfile',nargs='+',required=True,help='Files to be caculated')

args = argpar.parse_args()



#function for store sentence in corpus list words in sentence list
def read_conll06 (filename):
    corpus = []
    sentence = []
    for line in open (filename):
        line = line.strip()
        if line == "": # found  the end of a sentence
            corpus.append(sentence)
            sentence = []
        else: # found token
            entries = line.split('\t')
            sentence.append(entries[1])
    return corpus

# read training file get the num of token and type from training file
sentence = []
trcorpus = []
doc = open ("wsj_train.conll06")  
for line in doc :
    line = line.strip()
    if line == "":
        trcorpus.append(sentence)
        sentence = []
    else:
        entries = line.split('\t')
        sentence.append(entries[1])

trtoken = []
for sentence in trcorpus:
    for word in sentence:
        trtoken.append(word) #get a list of token

trtypeset = set(trtoken) #get training type set
  
#loop through files returm list of corpus and sentence    
inputfile = args.inputfile
for filename in inputfile:
    corpus = read_conll06(filename)
    
    N = len(corpus)
#get num of sentence   
    print "Number of sentence: ",N
    
   
#store token in set and get num
    tokenlist = []
    sentlengths = []
    sen0 = 0
    sen1 = 0
    sen2 = 0
    sen3 = 0
    untoken_num = []
    
    for sentence in corpus:
        sentlengths.append(len(sentence))
        count = 0
        for word in sentence:
            tokenlist.append(word) 
            if word not in trtoken:
                count += 1
        untoken_num.append(count)
            
        if count == 0:
            sen0 += 1
        elif count == 1:
            sen1 += 1
        elif count == 2:
            sen2 += 1
        else:
            sen3 += 1
            
    typeset = set(tokenlist)
    
    untype = []
    for i in typeset:
        if i not in trtypeset:
            untype.append(i)
				
    #print untype[:20]
    differ_token = sum(untoken_num)
    differ_type = typeset - trtypeset

    #mean caculation
    sumlength = sum(sentlengths)
    avg = float(sumlength/len(corpus))
    
    sentlengths.sort()
    print "Average sentence length: ",'%.2f' %avg
    print "Maximum sentence length: ",sentlengths[-1]
    print "Minumum sentence length: ",sentlengths[0]
    print "Median of sentence length: ",sentlengths[len(sentlengths)/2]
    #standard daviation
    variance = 0.0
    for sentlen in sentlengths:
	    variance += (sentlen - avg)**2
    variance = variance/(N-1)
    stdev = math.sqrt(variance) # stdev is sqrt of variance
       
    print "Standard deviation of sentence lengths: ",'%.2f' %stdev
    print "Number of tokens: ",len(tokenlist)
    print "Number of types: ", len(typeset)
    print "Unknown tokens",differ_token
    print "Unknown tokens %",'%.2f' %float(differ_token*1.0/len(tokenlist)*100)
##    percentage_unknowntype = float(len(differ_type)/len(typeset))
##    print percentage_unknowntype 
    print "Unknown types",len(differ_type)
    print "Unknown types %",'%.2f' %float(len(differ_type)*1.0/ len(typeset)*100)
    avg_un_token = float(sum(untoken_num)/len(corpus))
    print "Average number of unknown tokens per sentence: ", '%.2f' %avg_un_token
    print "sents with 0 unk. tokens: ",sen0
    print "sents with 1 unk. tokens: ",sen1
    print "sents with 2 unk. tokens: ",sen2
    print "sents with >2 unk. tokens: ",sen3

    freq_words_set = [(word, untype.count(word)) for word in set(untype)]

    sorted_words_set = sorted(freq_words_set , key = lambda freq:freq[1],reverse=True)
    print "50 most frequent unknown types: ",sorted_words_set[:50]
