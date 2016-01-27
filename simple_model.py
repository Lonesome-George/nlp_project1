#coding:utf-8

#使用50条语料训练出一个简单的模型
#1.分词
#2.去除停用词
#3.使用剩余的词集训练模型

import os
import jieba
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC

class simple_model:
    vectorizer = 0
    classifier = 0

    initial_file = "./Training/TrainingSet50.txt"
    chosen_dir = "./Training/ChosenSet"
    chosen_prefix = "SelectedTrainingSet50"
    stopset = {}.fromkeys([ line.rstrip() for line in open('./Dict/stop_words.txt') ])#读取停用词集

    def __init__(self):
        training_files = []
        training_files.append(self.initial_file)
        for parent,dirnames,filenames in os.walk(self.chosen_dir):
            for filename in filenames:
                if filename.startswith(self.chosen_prefix): # 忽略不以prefix为前缀的文件
                    training_files.append(os.path.join(parent, filename))
        trainfeats, target = self.extract_features(training_files)
        # trainfeats, target = self.bigram_features(filename)
        # print 'train on %d instances' % (len(trainfeats))
        # print trainfeats, labels
        # 训练模型
        # self.classifier = SVC(probability=True)
        self.classifier = SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=3,
                              gamma=0.0, kernel='rbf', max_iter=-1, probability=True, random_state=None,
                              shrinking=True, tol=0.001, verbose=False)
        self.classifier.fit(trainfeats, target)

    def extract_features(self, filenames):
        # print filenames
        trainfeats  = []
        target = []
        for filename in filenames:
            f = file(filename, 'r')
            while True:
                line = f.readline().decode("utf-8")
                if len(line) == 0: # Zero length indicates EOF
                    break
                label,text = self.proc_line(line)
                token_list = self.tokenize(text)
                trainfeats.append(self.word_feats(token_list, self.stopset))
                target.append(int(label))
            f.close()
        # 将dict转换成vector
        self.vectorizer = DictVectorizer()
        trainfeats = self.vectorizer.fit_transform(trainfeats).toarray()
        # print self.vectorizer.get_feature_names()
        return trainfeats, target

    # def bigram_features(self, filename):
    #     trainfeats  = []
    #     target = []
    #     f = file(filename, 'r')
    #     while True:
    #         line = f.readline().decode("utf-8")
    #         if len(line) == 0: # Zero length indicates EOF
    #             break
    #         label,text = self.proc_line(line)
    #         trainfeats.append(text)
    #         target.append(int(label))
    #     f.close()
    #     self.vectorizer = CountVectorizer(ngram_range=(1, 2), token_pattern=r'\b\w+\b', min_df=1)
    #     trainfeats = self.vectorizer.fit_transform(trainfeats).toarray()
    #     print self.vectorizer.get_feature_names()
    #     return trainfeats, target

    def proc_line(self, line):
        sp_list = line.split('\t')
        return sp_list[1], sp_list[2]

    def tokenize(self, text):
        text = text.rstrip('\n') # 去除行尾的换行符
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
        dictfeats = self.word_feats(token_list, self.stopset)
        vecfeats = self.vectorizer.transform(dictfeats).toarray()
        return self.classifier.predict(vecfeats)

    def classify_proba(self, text):
        token_list = self.tokenize(text)
        dictfeats = self.word_feats(token_list, self.stopset)
        vecfeats = self.vectorizer.transform(dictfeats).toarray()
        prob = self.classifier.predict_proba(vecfeats)
        return prob[0]
