#encoding=utf-8

from __future__ import division
import math

# 计算tf*idf
# 1.将每个文本的特征向量保存至文件
# 2.分别使用列表和字典保存每个term(word)的tf和idf值。
def tfidfs(file_in, tfidf_file_out, idf_file_out):
    ndoc = 0 #文本总数
    doc_tf_list = [] # 存储每个term的tf值;每条文本对应一个list=>list[0](str类型)保存id,list[1](str类型)保存label,list[2](dict类型)保存每个term的tf值。
    df_dict = {} # 保存每个term的df值
    idf_dict = {}# 保存每个term的idf值
    doc_tfidf_list = [] # 存储每个term的tf值;每条文本对应一个list=>list[0](str类型)保存id,list[1](str类型)保存label,list[2](dict类型)保存每个term的tf*idf值。

    f = file(file_in, 'r')
    while True:
        line = f.readline().decode("utf-8")
        if len(line) == 0: # Zero length indicates EOF
            break
        ndoc += 1
        id,label,text = proc_line(line)
        tf_list = tf(text, df_dict)
        doc_tf_list.append([id, label, tf_list])
    f.close()

    # 计算idf
    for term in df_dict:
        idf_dict[term] = math.log(ndoc/df_dict[term], 10)

    # 计算tf*idf值并保存至文件
    f = file(tfidf_file_out, 'w')
    for tf_list in doc_tf_list:
        # 计算tf*idf
        tfidf_dict = {}
        id = tf_list[0]
        label = tf_list[1]
        tf_dict = tf_list[2]
        string = id + '\t' + label + '\t'
        for term in tf_dict:
            tfidf = tf_dict[term] * idf_dict[term]
            tfidf_dict[term] = tfidf
            string += term + ',' + str(tfidf) + ";"
            # string += term + ',' + str(1) + ";" # for test
        doc_tfidf_list.append([id, label, tfidf_dict])
        # 写入文件
        string += '\n'
        f.write(string.encode("utf-8"))
    f.close()

    # 将idf值保存至文件
    f = file(idf_file_out, 'w')
    string = ""
    for term in idf_dict:
        string += term + ',' + str(idf_dict[term]) + ';'
    f.write(string.encode('utf-8'))
    f.close()

def tfidf(wordfreq_dict, idf_dict):
    wg_dict = {} # 存储每个term的tfidf值
    nterm = 0
    # 统计term的总数
    for word in wordfreq_dict:
        nterm += int(wordfreq_dict[word])
    for word in wordfreq_dict:
        if idf_dict.has_key(word): # 去除训练集中不包含的单词
            freq = int(wordfreq_dict[word])
            weight = freq / nterm * idf_dict[word]
            wg_dict[word] = weight
    return wg_dict

def proc_line(line):
    sp_list = line.split('\t')
    return sp_list[0], sp_list[1], sp_list[2]

def tf(text, df_dict):
    tf_dict = {}
    text = text.rstrip(';\n') # 去除文本末尾的换行符和分号
    if text == '':
        return {}
    seg_list = text.split(';')
    nterm = 0 #term总数
    for seg in seg_list: # 统计term总数
        term_and_freq = seg.split(',')
        nterm += int(term_and_freq[1])
    for seg in seg_list: # 计算tf值
        term_and_freq = seg.split(',')
        term = term_and_freq[0]
        freq = term_and_freq[1]
        tf = float(freq) / nterm
        tf_dict[term] = tf
        if df_dict.has_key(term):
            df_dict[term] += 1
        else:
            df_dict[term] = 1
    return tf_dict

if __name__ == '__main__':
    file_in  = './Training/WordFreq.txt'
    tfidf_file_out = './Training/FeatureVector.txt'
    idf_file_out = './Training/IDF.txt'
    tfidfs(file_in, tfidf_file_out, idf_file_out)