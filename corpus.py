#encoding=utf-8

#选择语料
#选取正负向概率之差的绝对值最小的n条语料

import os
from simple_model import simple_model
from svm_model import svm_model
import math
import heapq

class corpora:
    # trainset_filename = "./Training/TrainingSet50.txt"
    rawset_filename = "./Training/RawTrainingSet10000.txt"
    chosen_dir = "./Training/ChosenSet"
    chosen_prefix = "SelectedTrainingSet50"
    chosen_indices = "./Training/ChosenSet/ChosenIndices.txt" # 保存已经选中的文本序号
    docset = []
    max_pos_prob = 0
    classifier = 0

    def __init__(self):
        if os.path.isdir(self.chosen_dir) == False:
            os.mkdir(self.chosen_dir)
        # self.classifier = simple_model()
        self.classifier = svm_model()

    def read_txt(self):
        # 读取已经选中的文本序号
        chosen_indices = []
        fi = 0
        try:
            fi = file(self.chosen_indices, 'r')
            idx_list = fi.readline().split('\t')
            for idx in idx_list:
                chosen_indices.append(idx)
            fi.close()
            print chosen_indices
        except IOError:
            pass
        # 读取rawset文档
        fr = file(self.rawset_filename, 'r')
        while True:
            line = fr.readline().decode("utf-8")
            if len(line) == 0: # Zero length indicates EOF
                break
            index,text = self.proc_line(line)
            if index not in chosen_indices:
                probs = self.classifier.classify_proba(text)
                doc = [index, text, math.fabs(probs[1] - probs[0])]
                heapq.heappush(self.docset, doc)
        fr.close()

    def proc_line(self, line):
        sp_list = line.split('\t')
        return sp_list[0], sp_list[1]

    def save_ndocs(self, n):
        docs = heapq.nsmallest(n, self.docset, key=lambda x:x[2])
        filename = self.find_filename(self.chosen_dir, self.chosen_prefix)
        fd = open(filename, 'w')
        fi = open(self.chosen_indices, 'a')
        for doc in docs:
            string = doc[0] + '\t\t' + doc[1]
            fd.write(string.encode("utf-8"))
            fi.write(str(doc[0]) + '\t')
        fd.close()
        fi.close()

    # 在指定目录下查找一个可用的文件名（格式为SelectedTrainingSet50_#.txt）
    def find_filename(self, dirname, prefix):
        index = 0
        filename = os.path.join(dirname, prefix + '_' + str(index) + ".txt")
        while os.path.isfile(filename):
            index += 1
            filename = os.path.join(dirname, prefix + '_' + str(index) + ".txt")
        return filename