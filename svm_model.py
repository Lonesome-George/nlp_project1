#encoding=utf-8

#使用给定的特征向量训练SVM模型

from utils import tokenize, del_stopwords, stat_wordfreq
from sklearn.feature_extraction import DictVectorizer
from sklearn.svm import SVC
from weight2 import tfidf

class svm_model:
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
        trainfeats, target = self.read_features(training_files)
        # print trainfeats, labels

        # 读取idf值
        self.read_idf(self.idf_file)

        # 训练模型
        # print 'train on %d instances' % (len(trainfeats))
        # self.classifier = SVC(probability=True)
        self.classifier = SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=3,
                              gamma=0.0, kernel='rbf', max_iter=-1, probability=True, random_state=None,
                              shrinking=True, tol=0.001, verbose=False)
        self.classifier.fit(trainfeats, target)

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
        dictfeats = dict()
        text = text.rstrip(';\n') # 去除行尾的换行符和分号
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
        prob = self.classifier.predict_proba(vecfeats)
        return prob[0]
