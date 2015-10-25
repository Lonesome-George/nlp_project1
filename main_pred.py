#encoding=utf-8

# predict corpus and save results to a file

from preprocess import clean
from jc_model import jc_model

testset_file = '../TestSet/Test5000'
result_file1 = '../TestSet/Pred5000(byTrainSet50)'
result_file2 = '../TestSet/Pred5000(byTrainSet250)'

if __name__ == '__main__':
    model = jc_model()
    fi = open(testset_file, 'r')
    fo = open(result_file1, 'w')
    # fo = open(result_file2, 'w')
    while True:
        line = fi.readline().decode("utf-8")
        if len(line) == 0: # Zero length indicates EOF
            break
        line = line.rstrip('\n')
        seg_list = line.split('\t')
        id = seg_list[0]
        text = seg_list[1]
        text_cleaned = clean(text)
        pred_label = model.classify(text_cleaned)
        string = id + '\t' + str(pred_label) + '\t' + text + '\n'
        fo.write(string.encode('utf-8'))
    fi.close()
    fo.close()