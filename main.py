#encoding=utf-8

#1.分词
#2.去除停用词
#3.将剩余的词集用于训练模型

import jieba
import nltk.classify.util
import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.classify import NaiveBayesClassifier

def procline(line):
    sp_list = line.split('\t')
    return sp_list[1], sp_list[2]

def tokenize(text):
    seg_list = list(jieba.cut(text, cut_all=False))# 精确模式
    return seg_list

def word_feats(words):
    return dict([(word, True) for word in words])

def word_feats(words, stopset):
    return dict([(word, True) for word in words if word not in stopset])

def bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])

#main
filename = "D:/Workspace/Yan/NLP/Training/TrainingSet50.txt"
stopset = {}.fromkeys([ line.rstrip() for line in open('./stop_words.txt') ])#读取停用词集
posfeats = []
negfeats = []

f = file(filename, 'r')
while True:
    line = f.readline().decode("utf-8")
    if len(line) == 0: # Zero length indicates EOF
        break
    label,text = procline(line)
    token_list = tokenize(text)
    if label == '1':
        # posfeats.append((word_feats(token_list, stopset), 'pos'))
        posfeats.append((bigram_word_feats(token_list), 'pos'))
    elif label == '-1':
        # negfeats.append((word_feats(token_list, stopset), 'neg'))
        negfeats.append((bigram_word_feats(token_list), 'neg'))
f.close()

negcutoff = len(negfeats)*3/4
poscutoff = len(posfeats)*3/4

trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))

classifier = NaiveBayesClassifier.train(trainfeats)
print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
classifier.show_most_informative_features()