#encoding=utf-8

#使用50条语料训练出一个简单的模型
#1.分词
#2.去除停用词
#3.使用剩余的词集训练模型

import jieba
import nltk.classify.util
import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.classify import NaiveBayesClassifier

class simple_model:

    classifier = 0
    pos = '1'
    neg = '-1'

    filename = "./Training/TrainingSet50.txt"
    stopset = {}.fromkeys([ line.rstrip() for line in open('./stop_words.txt') ])#读取停用词集
    
    def __init__(self):
        posfeats = []
        negfeats = []
        f = file(self.filename, 'r')
        while True:
            line = f.readline().decode("utf-8")
            if len(line) == 0: # Zero length indicates EOF
                break
            label,text = self.procline(line)
            token_list = self.tokenize(text)
            feature = (self.word_feats(token_list, self.stopset), label)
            if label == self.pos:
                posfeats.append(feature)
            elif label == self.neg:
                negfeats.append(feature)
        f.close()

        trainfeats = negfeats + posfeats
        print 'train on %d instances' % (len(trainfeats))

        self.classifier = NaiveBayesClassifier.train(trainfeats)
        self.classifier.show_most_informative_features()


    def procline(self, line):
        sp_list = line.split('\t')
        return sp_list[1], sp_list[2]

    def tokenize(self, text):
        seg_list = list(jieba.cut(text, cut_all=False))# 精确模式
        return seg_list

    def word_feats(self, words):
        return dict([(word, True) for word in words])

    def word_feats(self, words, stopset):
        return dict([(word, True) for word in words if word not in stopset])

    # def bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    #     bigram_finder = BigramCollocationFinder.from_words(words)
    #     bigrams = bigram_finder.nbest(score_fn, n)
    #     return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])

    def classify(self, text):
        token_list = self.tokenize(text)
        prob = self.classifier.prob_classify(self.word_feats(token_list, self.stopset))
        res = dict()
        res[self.pos] = prob.prob(self.pos)
        res[self.neg] = prob.prob(self.neg)
        return res
