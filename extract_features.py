#encoding=utf-8

import jieba
import heapq

src_dir = "./Training/ChosenSet"
chosen_prefix = "SelectedTrainingSet50"

# 分词并统计每篇文本的单词词频
def word_freq(filenames):
    wordset = set()   # 全部单词集
    freqset = [[],[]] # 分别保存负向和正向文本的词频
    npos = 0 # 当前正向文本的数目
    nneg = 0 # 当前负向文本的数目
    icur = 0 # 当前所指向的正向或负向文本的下标
    for filename in filenames:
        fr = file(filename, 'r')
        while True:
            line = fr.readline().decode("utf-8")
            if len(line) == 0: # Zero length indicates EOF
                break
            id,label,text = proc_line(line)
            index = 0
            doc = [id, label, dict()] # 用列表记录每篇文本的id,label和词频
            if label == '1':
                index = 1
                freqset[1].append(doc)
                icur = npos
                npos += 1
            elif label == '-1':
                index = 0
                freqset[0].append(doc)
                icur = nneg
                nneg += 1
            else:
                print 'tag-unknown text'
                continue
            tokens = tokenize(text)
            for token in tokens:
                wordset.add(token) # 将单词加入全部单词集
                if freqset[index][icur][2].has_key(token):
                    freqset[index][icur][2][token] += 1
                else:
                    freqset[index][icur][2][token] = 1
        fr.close()
    return wordset, freqset

# 对于某一类，计算每个单词的CHI值
def chi_scores(wordset, freqset): # freqset[0]表示负向文本词频，freqset[1]表示正向文本词频
    scores = dict()
    for word in wordset:
        A = B = C = D = 0 # A表示包含词w并且属于类c的微博条数，B表示包含词w但不属于类c的微博条数，
        # C表示不包含词w并且属于类c的微博条数，D表示不包含词w并且不属于类c的微博条数。
        # 遍历词频集
        for fq in freqset[0]:
            if fq[2].has_key(word):
                B += 1
            else:
                D += 1
        for fq in freqset[1]:
            if fq[2].has_key(word):
                A += 1
            else:
                C += 1
        # print A,B,C,D
        scores[word] = (B*C - A*D)**2 / ((A+B)*(C+D)+1) # 标准CHI，分母加1防止出现分母为零的情况
    return scores

# 抽取CHI值最高的n个特征词，并保存至文件中，格式为[id	label word,freq;word,freq...]
def extract_features(freqset, scores, n):
    # # 对CHI值进行排序
    # scores = sorted(scores.iteritems(), key=lambda x:x[1], reverse=True)
    # 取得分最高的n个特征词
    word_dict = dict(heapq.nlargest(n, scores.items(), key=lambda x:x[1]))
    ex_freqset = [[],[]] # 抽取出来的特征词频，ex_freqs[0]表示负向文本词频，ex_freqs[1]表示正向文本词频
    # 遍历词频集
    for i in range(2):
        for fq in freqset[i]:
            doc = [fq[0], fq[1], dict()]
            for word in fq[2]:
                if word_dict.has_key(word): # 判断该单词是否是选出来的特征词
                    doc[2][word] = fq[2][word]
            ex_freqset[i].append(doc)
    # 将特征向量保存至文件中
    f = open('./Training/FeatureVector.txt', 'w')
    for i in range(2):
        for fq in ex_freqset[i]:
            string = fq[0] + '\t' + fq[1] + '\t'
            for word in fq[2]:
                string += word + ',' + str(fq[2][word]) + ';'
            string += '\n'
            f.write(string.encode("utf-8"))
    f.close()
    return ex_freqset

def proc_line(line):
    sp_list = line.split('\t')
    return sp_list[0], sp_list[1], sp_list[2]

def tokenize(text):
    seg_list = list(jieba.cut(text, cut_all=False))# 精确模式
    return seg_list