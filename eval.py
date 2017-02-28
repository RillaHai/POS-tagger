#! /bin/python
#-*- coding:utf-8 -*-
import argparse
import sys
import itertools

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
		    sentence.append(entries[4])
    return corpus

argpar = argparse.ArgumentParser(description = 'evaluation PoS quality given two files in read')
argpar.add_argument('-g','--gold',dest='goldfile',required=True,help='the file containing the gold standard')
argpar.add_argument('-p','--pred',dest='predfile',required=True,help='the file containing the prediction standard')
args = argpar.parse_args()

gold = read_conll06(args.goldfile)
pred = read_conll06(args.predfile)

tp = {}
fp = {}
fn = {}
total = 0.0
for gsent, psent in itertools.izip(gold,pred):
    for gpos,ppos in itertools.izip(gsent,psent):
        #true positive found
        if gpos == ppos:
            if gpos not in tp:
                tp[gpos] = 1
            else:
                tp[gpos] += 1
        else:#found false positive for the gold class
            if gpos not in fn:
                fn[gpos] = 1
            else:
                fn[gpos] += 1
            #found false positive for the pred class
            if ppos not in fp:
                fp[ppos] = 1
            else:
                fp[ppos] += 1
        total +=1	
print 'accuracy over all classes',' %.2f'% (100*float(sum(tp.values()))/float(total))


#loop over all classes and compute pred rec f

for lable in sorted(set(tp.keys()+fp.keys()+fn.keys())):
	ltp = tp.get(lable,0)
	lfp = fp.get(lable,0)
	lfn = fn.get(lable,0)
	#true positive/(true positive + false positive)
	prec = ltp/float(ltp+lfp) if ltp > 0 or lfp > 0 else 0.0
	#true positve/(true positive + false nagetive)
	rec = ltp/float(ltp+lfn) if ltp > 0 or lfn > 0 else 0.0
	f = 2*prec*rec/float(prec+rec) if prec > 0 or rec > 0 else 0.0
	print ' %-10s prec: %6d/%6d = %6.2f rec: %6d/%6d = %6.2f f:%6.2f'% (lable,ltp,ltp+lfp,100*prec,ltp,ltp+lfn,100*rec,100*f)
	
