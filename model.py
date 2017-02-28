#! /bin/python
#-*- coding:utf-8 -*-
import sys
import argparse
import featrep

argpar = argparse.ArgumentParser(description = 'Map predictions from LibLinear back to CoNLL06')
   
argpar.add_argument('-i','--input',dest='inputfile',required=True,help='the file containing training/test data')
argpar.add_argument('-p','--prediction',dest='predfile',required=True,help='the predictions by the classifier')
argpar.add_argument('-f','--featmap',dest='featmapfile',required=True,help='the feature mapping used for training/testing')
argpar.add_argument('-o','--output',dest='outputfile',required=True,help='the output file')

args = argpar.parse_args()

#load the feature map
featmap = featrep.FeatureTable()
featmap.load_table(args.featmapfile)
int2lable = featmap.int2lable()

#load the predictions
predictions = []
with open (args.predfile) as pin:
    for line in pin:
	line = line.strip()
	if line != '':
	    predictions.append(int2lable.get(int(line),'<UNKNOWNPOS>'))
         
#read inputfile and write output file
with open (args.inputfile) as fin:
    with open (args.outputfile,mode = 'w') as fout:
        tokcnt = 0
        for line in fin:
            line = line.strip()
            if line != '':        
                 entries = line.split('\t')
                 entries[4] = predictions[tokcnt]
                 print >> fout, '\t'.join(entries)
                 tokcnt += 1   
            else:
                 print >> fout
