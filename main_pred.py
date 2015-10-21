#encoding=utf-8

from svm_model import svm_model

testset_file = './Training/testSet.txt'
# testset_file = './Training/TrainingSet50_cleaned.txt'

if __name__ == '__main__':
    model = svm_model()
    f = file(testset_file, 'r')
    nright = 0
    while True:
        line = f.readline().decode("utf-8")
        if len(line) == 0: # Zero length indicates EOF
            break
        line = line.rstrip()
        seg_list = line.split('\t')
        label = int(seg_list[1])
        text = seg_list[2]
        # print text
        pred_label = model.classify(text)
        if label == pred_label:
            nright += 1
        # print model.classify_proba(text)
    print 'num_right = ', nright
    f.close()