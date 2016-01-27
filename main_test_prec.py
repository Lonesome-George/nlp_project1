#coding:utf-8

# 测试模型的正确率

from __future__ import division
from simple_model import simple_model
from jc_model import jc_model

# testset_file = './Training/TestSet/testSet.txt'
# testset_file = './Training/TestSet/testSet2.txt'
# testset_file = './Training/TestSet/testSet50.txt'
testset_file = './Training/TestSet/ts_Test500.txt'
# testset_file = './Training/TrainingSet50_cleaned.txt'

if __name__ == '__main__':
    model = jc_model()
    # model = simple_model()
    f = file(testset_file, 'r')
    ntotal = 0 # 语料总数
    nright = 0 # 预测正确的语料数目
    while True:
        line = f.readline().decode("utf-8")
        if len(line) == 0: # Zero length indicates EOF
            break
        ntotal += 1
        line = line.rstrip('\n')
        seg_list = line.split('\t')
        id = seg_list[0]
        label = int(seg_list[1])
        text = seg_list[2]
        pred_label = model.classify(text)
        if label == pred_label:
            nright += 1
        # print id, label, model.classify_proba(text), text
        # else:
        #     print 'pred_wrong ', id, label, model.classify_proba(text), text
    print 'precision = ', nright / ntotal
    f.close()
