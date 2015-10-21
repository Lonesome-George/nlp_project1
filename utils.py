#encoding=utf-8

import jieba

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