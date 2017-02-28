#! /bin/python
#-*- coding:utf-8 -*-
import sys
import itertools
import argparse

class Token(object):
    #represents one token in the data
    def __init__(self,line):
        entries = line.strip().split('\t')
        self.form = entries[1]
        self.lemma = entries[2]
        self.pos = entries[4]

def read_conll06_sentence(filestream):
    #read file and return sentences list tokens
    #iterate function returning the data sentence by sentence
    sentence = []
    for line in filestream:
        line = line.strip()
        if line != '':
            sentence.append(Token(line))
        elif sentence != []:
            yield sentence  #stay at the status it calls next when need
            sentence = []
    if sentence != []:
        yield sentence

#mapping

class FeatureTable(object):
    def __init__ (self):
        self.featuremap = {}
        self.lablemap = {}#mapping lable to pos
    
    def save_table (self,filename):
        with open (filename,mode='w') as outstream:
            for key, value in self.featuremap.iteritems():
                 print >> outstream, key, value
	    print >> outstream
	    for key, value in self.lablemap.iteritems():
                 print >> outstream, key, value
    
    def load_table (self,filename):
        with open (filename,mode='r') as outstream:
            lablemap = False
	    for line in outstream:
	        line = line.strip()
	        if line == '':
	            lablemap = True
	        else:
	            key,_,value = line.partition(' ')
		    if not lablemap:
		        self.featuremap[key] = int(value)
		    else:
                self.lablemap[key] = int(value)
				
		        
				 	 
    #register feature if new ,otherwise return index
    #for training scenario
    def register_feature(self,feature):
        if feature not in self.featuremap:
            self.featuremap[feature] = self.numfeatures()
        return self.featuremap[feature]
    
    #map feature to index or return None for unseen feature
    #for testing scenario	
    def map_feature (self,feature):#for test
        return self.featuremap.get(feature,None)
	
    def numfeatures (self):
    #number of pairs
        return len(self.featuremap) 
			
    def register_lable (self, lable):
        if lable not in self.lablemap:
            self.lablemap[lable] = self.numlables()
        return self.lablemap[lable] 	
	
    def map_lable (self,lable):
        return self.lablemap.get(lable,-1)#None
        
    def numlables(self):
        return len(self.lablemap)

    def int2lable (self):
        return {v:k for (k,v)in self.lablemap.items()}

#create all feature for a givem token()list of string
def instantiate_feature_templates(tid,token,sentence):
    featurestringlist = []
    
    featurestringlist.append('FORM=%s'%token.form)
    featurestringlist.append('LEMMA=%s'%token.lemma) 
    featurestringlist.append('SUFFIX=%s'%token.form[-3:])
    featurestringlist.append('CAPITALIZATION=%s'%token.form[0])
    featurestringlist.append('PLURAL=%s'%token.form[-1:])
    featurestringlist.append('DIGITWITHCH' if token.form.isalnum == True else 'NOTDIGITWITHCH')
    featurestringlist.append('DIGIT' if token.form.isdigit == True else 'NOTDIGIT')
    featurestringlist.append('CHARACTER' if token.form.isalpha == True else 'NOTCHARACTER')
    #featurestringlist.append('HYPH' if token.form == '-' else 'NOTHYPH')
    #featurestringlist.append('COLON' if token.form ==':' or token.form == '--' or token.form == ';' else 'NOTCOLON')
    #featurestringlist.append('QUOTATION'if token.form == '\'\'' else 'NOTQUOTATION')
    #featurestringlist.append('UPPERCASE' if token.form.isupper == True else 'LOWERCASE')
    #featurestringlist.append('WORDLENGTH=%d'%len(token.form) if len(token.form)<25 else 'WORDLENGTH>=6' )

    form1a = sentence[tid+1].form if tid < len(sentence)-1 else '<FORM-END>'
    form1b = sentence[tid-1].form if tid >0 else '<FORM-BEGIN>'
    form2a = sentence[tid+2].form if tid < len(sentence)-2 else '<FORM-END>'
    form2b = sentence[tid-2].form if tid >1 else '<FORM-BEGIN>'
    form3b = sentence[tid-3].form if tid >2 else '<FORM-BEGIN>'
    form3a = sentence[tid+3].form if tid < len(sentence)-3 else '<FORM--END>'
    featurestringlist.append('FORM1B=%s'%form1b)
    
    featurestringlist.append('FORM1A=%s'%form1a)
    featurestringlist.append('FORM2B=%s'%form2b)
    featurestringlist.append('FORM2A=%s'%form2a)
    featurestringlist.append('FORM1ASUFFIX=%s'%form1a[-3:])
    featurestringlist.append('FORM1BSUFFIX=%s'%form1b[-3:])
    featurestringlist.append('FORM1APREFIX=%s'%form1a[0])
    featurestringlist.append('FORM1BPREFIX=%s'%form1b[0])
    #featurestringlist.append('FORM2BSUFFIX=%s'%form2b[0])
    #featurestringlist.append('FORM2ASUFFIX=%s'%form2a[0])
    #featurestringlist.append('FORM3A=%s'%form3a)
    #featurestringlist.append('FORM3B=%s'%form3b)
    #featurestringlist.append('PRE+FORM=%s%s'%(form1b,form2b))
    #featurestringlist.append('CONTEXT=%s%s%s%s'%(form2b,form1b,form1a,form2a))
    #featurestringlist.append('FORM3B2B1B=%s%s%s'%(form3a,form2a,form1a))
    #featurestringlist.append('FORM2AB/FORM1A=%s/%s'%(form1a,form2a))
    #print featurestringlist
    #more feature template
    return featurestringlist

#create the feature vector(list of integers)
#where the integers are indices to the dimentions containing 1
def map_to_numbers(stringlist,mapfunc):
    indexvector = []
    for featurestring in stringlist:
        indexvector.append(mapfunc(featurestring))
    #indexvector.discard(None)
    indexvector = [ind for ind in indexvector if ind != None]	
    return indexvector
def make_feature_vector (tid,token,sentence,mapfunc):
    stringlist = instantiate_feature_templates(tid,token,sentence)
    indexvector = map_to_numbers(stringlist,mapfunc)
    return indexvector
	
def write_indexvector_to_file(lableindex,indexvector,outputfile):
    print>> outputfile,'%d %s'% (lableindex,' '.join(['%d:1'% (i+1) for i in sorted(indexvector)]))

if __name__ =='__main__':#when import the following won't work
    import argparse
	
    argpar = argparse.ArgumentParser(description = 'Create feature representation in libsvm format')
    mode = argpar.add_mutually_exclusive_group(required=True)
    mode.add_argument('-t','--train',dest='train',action='store_true',help='run in training mode')
    mode.add_argument('-p','--predict',dest='predict',action='store_true',help='run in test mode')
    argpar.add_argument('-i','--input',dest='inputfile',required=True,help='the file containing training/test data')
    argpar.add_argument('-o','--output',dest='outputfile',required=True,help='the file that the feature representation is written to')
    argpar.add_argument('-f','--featmap',dest='featmapfile',required=True,help='the file from which to read or from which to write the feature')
    
    args = argpar.parse_args()

    feattable = FeatureTable()
    instream = open(args.inputfile)
    outstream = open(args.outputfile,mode='w')
     #training case
     #fill feature table and learn about new feature
    if args.train:
        for sentence in read_conll06_sentence(instream):
            for tid,token in enumerate(sentence):#index and value
                indexvector = make_feature_vector(tid,token,sentence,feattable.register_feature)
                lableindex = feattable.register_lable(token.pos)
                write_indexvector_to_file(lableindex,indexvector,outstream)
        feattable.save_table(args.featmapfile)
	#test case   
	#load predefined feature table and discard unseen features
    elif args.predict:
        feattable.load_table(args.featmapfile)
        for sentence in read_conll06_sentence(instream):
            for tid,token in enumerate(sentence):#index and value
                indexvector = make_feature_vector(tid,token,sentence,feattable.map_feature)
                lableindex = feattable.map_lable(token.pos)
                write_indexvector_to_file(lableindex,indexvector,outstream)