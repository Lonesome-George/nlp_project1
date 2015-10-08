#encoding=utf-8

#选择语料
#选取正负向概率之差的绝对值最小的200条语料

from simple_model import simple_model
import math
import heapq

class corpora:

    rawset_filename = "./Training/RawTrainingSet10000.txt"
    nset_filename = "./Training/SelectedTrainingSet200.txt"
    docset = []
    max_pos_prob = 0
    classifier = 0

    def __init__(self):
    	# self.docset = heapq()
    	self.classifier = simple_model()

    def readtxt(self):
        f = file(self.rawset_filename, 'r')
        while True:
            line = f.readline().decode("utf-8")
            if len(line) == 0: # Zero length indicates EOF
                break
            index,text = self.procline(line)
            probs = self.classifier.classify(text)
            doc = [text, math.fabs(probs['1'] - probs['-1'])]
            heapq.heappush(self.docset, doc)
        f.close()

    def procline(self, line):
        sp_list = line.split('\t')
        return sp_list[0], sp_list[1]

    def save_ndocs(self, n):
    	docs = heapq.nsmallest(n, self.docset)
    	f = open(self.nset_filename, 'w')
    	for doc in docs:
    		f.write(doc[0].encode("utf-8"))
    	f.close()
