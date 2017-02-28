#! /bin/python
#-*- coding:utf-8 -*-

import sys
import numpy

#reads libsvm format and returns pairs (LABEL,FEATVECT)
def read_libsvm(stream):
    for line in stream:
        line = line.strip()
        if line != '':
            entries = line.split(' ')
            label = int(entries[0])
            featvec = [int(feat[:-2]) for feat in entries [1:]]
            yield label,featvec
 #           for feat in entries[1:]:
 #               index,_,value = feat.partition(':')
 #               featvec.append(int(index))
            
                
    
class Perceptron(object):
    def __init__(self):
        self.weightvector = None
        self.averages = None
        self.numlabels = 0
        self.numfeatures = 0
        
        
    def save (self,filename):
        with open(filename,mode='w') as fout:
            print >> fout,self.numlabels
            print >> fout,self.numfeatures
            for l in range(self.numlabels):
                print >> fout, ' '.join(map(str,self.weightvector[l]))
        
    def load (self,filename):
        with open (filename, mode = 'r') as fin:
            self.numlables = int(fin.readline())
            self.numfeatures = int (fin.readline()) 
            for line in fin:
                line = line.strip()
                if line != '':
                    self.weightvector.append(map(float,line.split(' ')))       
    
    def train (self,data,epochs):
        #determine numlabels and numfeatures
        for label,featvec in data:
            if label >= self.numlabels:
                self.numlabels = label+1
            for feat in featvec:
                if feat >= self.numfeatures:
                    self.numfeatures = feat+1
                    
        #initialize the weight vector
        #self.weightvector = [0.0]*self.numlables*numfeatures     line version
        #matrix version
        #for _ in range(self.numlables):
         #   self.weightvector.append([0.0]*self.numlables*numfeatures)
        self.weightvector = numpy.zeros((self.numlabels,self.numfeatures))
        self.averages = numpy.zeros((self.numlabels,self.numfeatures))
       
        #train weight vector
        q = 0
        for e in range (epochs):
            for goldlabel,featvec in data:
                q +=1 
                predlabel = self.predict(featvec)
                if goldlabel != predlabel:
                    self.update(goldlabel, predlabel,featvec,q)
            print >> sys.stderr,'epoch %d done' % e  
        
        #average the weights    
        self.weightvector -= self.averages/q
    #return predicted label    
    
    def predict (self,featvec):
        #highest_score = None
        #best_label = None
        #for l in range(self.numlabels):
        #    score = 0.0
         #   for f in featvec:
        #       score += self.weightvector[l][f]
         #   if score > highest_score:
         #      highest_score = score
        #       best_label = l
        #return best_label    
         
        return self.weightvector[:,featvec].sum(1).argmax()       
        
    def update (self,goldlabel,predlabel,featvec,q):
        #for f in featvec:
        #    self.weightvector[goldlabel][f] +=0.5
        #    self.weightvector[goldlabel][f] +=0.5
            
        self.weightvector[goldlabel,featvec] +=0.5
        self.weightvector[predlabel,featvec] -=0.5
        self.averages[goldlabel,featvec] += q*0.5
        self.averages[predlabel,featvec] -= q*0.5
if __name__ == '__main__':
    import argparse
    
    argpar = argparse.ArgumentParser(description='train and apply a Perceptron')
    mode = argpar.add_mutually_exclusive_group(required=True)
    mode.add_argument('-t','--train',dest='train',action='store_true',help='run in training mode')
    mode.add_argument('-p','--predict',dest='predict',action='store_true',help='run in test mode')
    argpar.add_argument('-i','--input',dest='inputfile',required=True,help='the file containing training/test data')
    argpar.add_argument('-m','--model',dest='modelfile',required=True,help='the file containing the learned weight vector')
    argpar.add_argument('-o','--output',dest='outputfile',default = 'output.libsvm',help='output the file to write the predictions to')
    argpar.add_argument('-e','--epochs',dest='numepochs',default = 10,help='numbers of epochs to run the perceptron')
    
    args = argpar.parse_args()


    perceptron = Perceptron()
    if args.train:
        with open(args.inputfile) as fin:
            data = [datapoint for datapoint in read_libsvm(fin)]
            perceptron.train(data,int(args.numepochs))
            perceptron.save(args.modelfile)
    elif args.predict:
        perceptron.load(args.model(file))
        with open(args.inputfile) as fin:
            with open(args.outputfile,mode='w') as fout:
                data = [datapoint for datapoint in read_libsvm(fin)]
                predictions = [perceptron.predict(featvec) for (_,featvec)in data]
                print >> fout, '\n'.join(map(str,predictions))















