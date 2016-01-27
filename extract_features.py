#coding:utf-8

from utils import stop_set, emotion_set, tokenize, del_stopwords
import os
import heapq

chosen_dir = "./Training/ChosenSet"
chosen_prefix = "SelectedTrainingSet30"

# 分词并统计每篇文本的单词词频
def word_freq(filenames, stopset):
    wordset = set()   # 全部单词集
    freqset_list = [[],[]] # 分别保存负向和正向文本的词频
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
            token_list = tokenize(text)
            token_list = del_stopwords(token_list, stopset)
            wordfreq_dict = {}
            for token in token_list:
                wordset.add(token) # 将单词加入全部单词集
                if wordfreq_dict.has_key(token):
                    wordfreq_dict[token] += 1
                else:
                    wordfreq_dict[token] = 1
            doc = [id, label, wordfreq_dict] # 用列表记录每篇文本的id,label和词频
            # 将文本加入指定列表
            index = 0
            if label == '1':
                index = 1
                freqset_list[1].append(doc)
                icur = npos
                npos += 1
            elif label == '-1':
                index = 0
                freqset_list[0].append(doc)
                icur = nneg
                nneg += 1
            else:
                print 'tag-unknown text'
                continue
        fr.close()
        # 将特征词保存至文件中
        f = open('./Training/WordSet.txt', 'w')
        for word in wordset:
            string = word + '\n'
            f.write(string.encode("utf-8"))
        f.close()
        # 将原始词频保存至文件中
        f = open('./Training/WordFreq_Orig.txt', 'w')
        for i in range(2):
            for freqset in freqset_list[i]:
                id = freqset[0]
                label = freqset[1]
                freq_list = freqset[2]
                string = id + '\t' + label + '\t'
                for word in freq_list:
                    string += word + ',' + str(freq_list[word]) + ';'
                string += '\n'
                f.write(string.encode('utf-8'))
    return wordset, freqset_list

# 对于某一类，使用标准CHI算法计算每个单词的得分
def std_chi_scores(wordset, freqset_list): # freqset_list[0]表示负向文本词频，freqset_list[1]表示正向文本词频
    scores = dict()
    for word in wordset:
        A = B = C = D = 0 # A表示包含词w并且属于类c的微博条数，B表示包含词w但不属于类c的微博条数，
        # C表示不包含词w并且属于类c的微博条数，D表示不包含词w并且不属于类c的微博条数。
        # 遍历词频集
        neg_freqset_list = freqset_list[0]
        pos_freqset_list = freqset_list[1]
        for doc in neg_freqset_list:
            freqset_dict = doc[2]
            if freqset_dict.has_key(word):
                B += 1
            else:
                D += 1
        for doc in pos_freqset_list:
            freqset_dict = doc[2]
            if freqset_dict.has_key(word):
                A += 1
            else:
                C += 1
        # print A,B,C,D
        scores[word] = (B*C - A*D)**2 / ((A+B)*(C+D)+1) # 标准CHI，分母加1防止出现分母为零的情况
    return scores

# 对于某一类，使用优化的CHI算法计算每个单词的得分（考虑情感词）
def opt_chi_scores(wordset, freqset_list, emotionset):
    emo_scores = dict()    # 情感词的得分
    nonemo_scores = dict() # 非情感词的得分
    nonemo_total_score = 0 # 非情感词的总得分
    nonemo_size = 0        # 非情感词的总数
    for word in wordset:
        A = B = C = D = 0 # A表示包含词w并且属于类c的微博条数，B表示包含词w但不属于类c的微博条数，
        # C表示不包含词w并且属于类c的微博条数，D表示不包含词w并且不属于类c的微博条数。
        # 遍历词频集
        neg_freqset_list = freqset_list[0]
        pos_freqset_list = freqset_list[1]
        for doc in neg_freqset_list:
            freqset_dict = doc[2]
            if freqset_dict.has_key(word):
                B += 1
            else:
                D += 1
        for doc in pos_freqset_list:
            freqset_dict = doc[2]
            if freqset_dict.has_key(word):
                A += 1
            else:
                C += 1
        score = (B*C - A*D)**2 / ((A+B)*(C+D)+1) # 标准CHI，分母加1防止出现分母为零的情况
        if word in emotionset:
            emo_scores[word] = score
        else:
            nonemo_scores[word] = score
            nonemo_total_score += score
            nonemo_size += 1
        # 调整情感词的得分
        nonemo_avg_score = nonemo_total_score / nonemo_size
        for word in emo_scores:
            emo_scores[word] += 0.3 * nonemo_avg_score
    return dict(emo_scores.items() + nonemo_scores.items())

# 抽取CHI值最高的n个特征词，并保存至文件中，格式为[id	label word,freq;word,freq...]
def extract_features(freqset_list, scores, n):
    # # 对CHI值进行排序
    # scores = sorted(scores.iteritems(), key=lambda x:x[1], reverse=True)
    # 取得分最高的n个特征词
    word_dict = dict(heapq.nlargest(n, scores.items(), key=lambda x:x[1]))
    print 'extract ' + str(len(word_dict)) + ' feature words.'
    ex_freqset = [[],[]] # 抽取出来的特征词频，ex_freqs[0]表示负向文本词频，ex_freqs[1]表示正向文本词频
    # 遍历词频集
    for i in range(2):
        for doc in freqset_list[i]:
            id = doc[0]
            label = doc[1]
            freqset_dict = doc[2]
            new_freqset_dict = {}
            for word in freqset_dict:
                if word_dict.has_key(word): # 判断该单词是否是选出来的特征词
                    new_freqset_dict[word] = freqset_dict[word]
            new_doc = [id, label, new_freqset_dict]
            ex_freqset[i].append(new_doc)
    # 将选中的词及其频率保存至文件中
    f = open('./Training/WordFreq.txt', 'w')
    for i in range(2):
        for doc in ex_freqset[i]:
            id = doc[0]
            label = doc[1]
            freqset_dict = doc[2]
            string = id + '\t' + label + '\t'
            for word in freqset_dict:
                string += word + ',' + str(freqset_dict[word]) + ';'
            string += '\n'
            f.write(string.encode("utf-8"))
    f.close()
    return ex_freqset

def proc_line(line):
    sp_list = line.split('\t')
    return sp_list[0], sp_list[1], sp_list[2]


if __name__ == '__main__':
    stopset = stop_set('./Dict/stop_words.txt')
    emotionset = emotion_set('./Dict/emotion_words.csv')
    training_files = ['./Training/TrainingSet50_cleaned.txt']
    # # add 200 more training texts
    # for parent,dirnames,filenames in os.walk(chosen_dir):
    #     for filename in filenames:
    #         if filename.startswith(chosen_prefix): # 忽略不以prefix为前缀的文件
    #             training_files.append(os.path.join(parent, filename))
    wordset, freqset_list = word_freq(training_files, stopset)
    # scores = ef.std_chi_scores(wordset, freqset_list)
    scores = opt_chi_scores(wordset, freqset_list, emotionset)
    ex_freqset = extract_features(freqset_list, scores, 2500)
