#encoding=utf-8

#选择语料
#选取正负向概率之差的绝对值最小的200条语料

import os
from simple_model import simple_model
import math
import heapq

class corpora:
    # trainset_filename = "./Training/TrainingSet50.txt"
    rawset_filename = "./Training/RawTrainingSet10000.txt"
    chosen_dir = "./Training/ChosenSet"
    chosen_prefix = "SelectedTrainingSet50"
    # 可以创建一个文件保存所有已选中的语料序号
    docset = []
    max_pos_prob = 0
    classifier = 0

    def __init__(self):
        if os.path.isdir(self.chosen_dir) == False:
            os.mkdir(self.chosen_dir)
        self.classifier = simple_model()

    def read_txt(self):
        f = file(self.rawset_filename, 'r')
        while True:
            line = f.readline().decode("utf-8")
            if len(line) == 0: # Zero length indicates EOF
                break
            index,text = self.proc_line(line)
            probs = self.classifier.classify(text)
            doc = [index, text, math.fabs(probs[1] - probs[0])]
            heapq.heappush(self.docset, doc)
        f.close()

    def proc_line(self, line):
        sp_list = line.split('\t')
        return sp_list[0], sp_list[1]

    def save_ndocs(self, n):
        docs = heapq.nsmallest(n, self.docset, key=lambda s: s[2])
        filename = self.find_filename(self.chosen_dir, self.chosen_prefix)
        f = open(filename, 'w')
        for doc in docs:
            string = doc[0] + '\t1\t' + doc[1]
            f.write(string.encode("utf-8"))
        f.close()

    # 在指定目录下查找一个可用的文件名（格式为SelectedTrainingSet50_#.txt）
    def find_filename(self, dirname, prefix):
        index = 0
        filename = os.path.join(dirname, prefix + '_' + str(index) + ".txt")
        while os.path.isfile(filename):
            index += 1
            filename = os.path.join(dirname, prefix + '_' + str(index) + ".txt")
        return filename