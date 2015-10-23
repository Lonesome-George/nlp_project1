#encoding=utf-8

from simple_model import simple_model
from jc_model import jc_model

testset_file = './Training/TestSet/testSet.txt'
# testset_file = './Training/TestSet/testSet2.txt'
# testset_file = './Training/TestSet/testSet50.txt'
# testset_file = './Training/TrainingSet50_cleaned.txt'

if __name__ == '__main__':
    model = jc_model()
    # model = simple_model()
    f = file(testset_file, 'r')
    nright = 0
    while True:
        line = f.readline().decode("utf-8")
        if len(line) == 0: # Zero length indicates EOF
            break
        line = line.rstrip()
        seg_list = line.split('\t')
        id = seg_list[0]
        label = int(seg_list[1])
        text = seg_list[2]
        # print text
        pred_label = model.classify(text)
        pred_right = False
        if label == pred_label:
            nright += 1
            # pred_right = True
        else:
            print 'pred_wrong ', id, label, model.classify_proba(text), text
    print 'num_right = ', nright
    f.close()