#encoding=utf-8

import jieba

user_dict = './Dict/user_dict.txt'
jieba.load_userdict(user_dict)

def stop_set(filename):
    stopset = []
    f = file(filename, 'r')
    while True:
        line = f.readline().decode("utf-8")
        if len(line) == 0: # Zero length indicates EOF
            break
        stopset.append(line.rstrip())
    f.close()
    return stopset

def emotion_set(filename):
    emotionset = []
    f = file(filename, 'r')
    while True:
        line = f.readline().decode("utf-8")
        if len(line) == 0: # Zero length indicates EOF
            break
        text = line.rstrip()
        emotionset.append(text.split(',')[0])
    f.close()
    del emotionset[0] # 去除第一行，第一行是说明文字
    return emotionset

# 分词
def tokenize(text):
    text = text.rstrip('\n') # 去除行尾的换行符
    seg_list = list(jieba.cut(text, cut_all=False))# 精确模式
    seg_newlist = []
    for seg in seg_list:
        seg = seg.strip()# 去除单词前后的空格
        if seg != '':    # 如果整个单词由空格构成则删除
            seg_newlist.append(seg)
    return seg_newlist

# 去除停用词
def del_stopwords(word_list, stopset):
    word_newlist = []
    for word in word_list:
        if word not in stopset:
            word_newlist.append(word)
    return word_newlist

# 统计词频
def stat_wordfreq(token_list):
    wordfreq_dict = {}
    for token in token_list:
        if wordfreq_dict.has_key(token):
            wordfreq_dict[token] += 1
        else:
            wordfreq_dict[token] = 1
    return wordfreq_dict

# for test, 对要打印的数据格式有要求
def print_list(list):
    string = ''
    for elem in list:
        string += elem + '|'
    print string

def print_dict(dict):
    string = ''
    for elem in dict:
        string += elem + ',' + str(dict[elem]) + ';'
    print string