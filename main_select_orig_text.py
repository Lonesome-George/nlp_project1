#encoding=utf-8

# 根据多次选择的语料id从rawset中选出原始语料

import os

chosen_dir = "./Training/ChosenSet"
chosen_prefix = "SelectedTrainingSet30"
stat_file = "./Training/ChosenSet/Stat.txt"
orig_file = "./Training/ChosenSet/TrainingSet200.txt"
rawset_filename = "./Training/RawTrainingSet10000.txt"

if __name__ == '__main__':
    files = []
    for parent,dirnames,filenames in os.walk(chosen_dir):
        for filename in filenames:
            if filename.startswith(chosen_prefix): # 忽略不以prefix为前缀的文件
                files.append(os.path.join(parent, filename))

    text_dict = {} #key:id;value:[label,text]
    for filename in files:
        f = open(filename, 'r')
        while True:
            line = f.readline().decode('utf-8')
            if line == '':
                break
            line = line.rstrip('\n')
            seg_list = line.split('\t')
            id = seg_list[0]
            label = seg_list[1]
            text = seg_list[2]
            text_dict[id] = [label, text]
        f.close()

    # 对字典排序
    text_list = sorted(text_dict.iteritems(), key=lambda x:int(x[0]))

    # 将排序的语料重新保存至文件
    f = open(stat_file, 'w')
    for text in text_list:
        string = text[0] + '\t' + text[1][0] + '\t' + text[1][1] + '\n'
        f.write(string.encode('utf-8'))
    f.close()

    # 从rawset中选出原始语料
    fi = open(rawset_filename, 'r')
    fo = open(orig_file, 'w')
    while True:
        line = fi.readline().decode('utf-8')
        if line == '':
            break
        line = line.rstrip('\n')
        seg_list = line.split('\t')
        id = seg_list[0]
        text = seg_list[1]
        if text_dict.has_key(id):
            label = text_dict[id][0]
            string = id + '\t' + label + '\t' + text + '\n'
            fo.write(string.encode('utf-8'))
    fi.close()
    fo.close()