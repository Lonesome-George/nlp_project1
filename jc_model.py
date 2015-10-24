#encoding=utf-8

#使用给定的特征向量训练SVM模型

from utils import tokenize, del_stopwords, stat_wordfreq, print_list, print_dict
from sklearn.feature_extraction import DictVectorizer
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.neighbors import NearestNeighbors
from weight import tfidf

class jc_model:
    vectorizer = 0
    classifier = 0

    feature_file = "./Training/FeatureVector.txt"
    idf_file = "./Training/IDF.txt"
    chosen_dir = "./Training/ChosenSet"
    chosen_prefix = "SelectedTrainingSet50"
    idf_dict = {}
    stopset = {}.fromkeys([ line.rstrip() for line in open('./Dict/stop_words.txt') ])#读取停用词集

    def __init__(self):
        # 读取训练集
        training_files = []
        training_files.append(self.feature_file)
        trainfeats, targets = self.read_features(training_files)

        # 读取idf值
        self.read_idf(self.idf_file)

        # 训练模型
        print 'train on %d instances' % (len(trainfeats))
        # self.classifier = SVC(probability=True)
        self.classifier = BernoulliNB()
        print self.classifier
        self.classifier.fit(trainfeats, targets)

    def read_features(self, filenames):
        trainfeats  = []
        targets = []
        for filename in filenames:
            f = file(filename, 'r')
            while True:
                line = f.readline().decode("utf-8")
                if len(line) == 0: # Zero length indicates EOF
                    break
                id,label,text = self.proc_line(line)
                trainfeats.append(self.word_feats(text))
                targets.append(int(label))
            f.close()

        # 将dict转换成vector
        self.vectorizer = DictVectorizer()
        trainfeats = self.vectorizer.fit_transform(trainfeats).toarray()
        # print self.vectorizer.get_feature_names()
        return trainfeats, targets

    def read_idf(self, filename):
        f = open(filename, 'r')
        while True:
            line = f.readline().decode("utf-8")
            if len(line) == 0: # Zero length indicates EOF
                break
            line = line.rstrip(';\n')
            seg_list = line.split(';')
            for seg in seg_list:
                sp_list = seg.split(',')
                term = sp_list[0]
                weight = float(sp_list[1])
                self.idf_dict[term] = float(weight)
        f.close()

    # 处理一行文本
    def proc_line(self, line):
        sp_list = line.split('\t')
        return sp_list[0], sp_list[1], sp_list[2]

    # 读取特征词及其权重值
    def word_feats(self, text):
        dictfeats = {}
        text = text.rstrip(';\n') # 去除行尾的换行符和分号
        if text == '':
            return {}
        seg_list = text.split(';')
        for seg in seg_list:
            sp_list = seg.split(',')
            term = sp_list[0]
            weight = float(sp_list[1])
            dictfeats[term] = weight
        return dictfeats

    def classify(self, text):
        token_list = tokenize(text)
        token_list = del_stopwords(token_list, self.stopset)
        wordfreq_dict = stat_wordfreq(token_list)
        dictfeats = tfidf(wordfreq_dict, self.idf_dict)
        vecfeats = self.vectorizer.transform(dictfeats).toarray()
        # print_list(token_list)
        # print_dict(wordfreq_dict)
        # print_dict(dictfeats)
        return self.classifier.predict(vecfeats)[0]

    def classify_proba(self, text):
        token_list = tokenize(text)
        token_list = del_stopwords(token_list, self.stopset)
        wordfreq_dict = stat_wordfreq(token_list)
        dictfeats = tfidf(wordfreq_dict, self.idf_dict)
        vecfeats = self.vectorizer.transform(dictfeats).toarray()
        prob = self.classifier.predict_proba(vecfeats)
        return prob[0]
