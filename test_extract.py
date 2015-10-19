#encoding=utf-8
#注意设置文件的编码格式为utf-8

import extract_features as ef

def read_stopset(filename):
    stopset = []
    f = file(filename, 'r')
    while True:
        line = f.readline().decode("utf-8")
        if len(line) == 0: # Zero length indicates EOF
            break
        stopset.append(line.rstrip())
    f.close()
    return stopset

def read_emotionset(filename):
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

if __name__ == '__main__':
    # stopset = {}.fromkeys([ line.rstrip() for line in open('./Dict/stop_words.txt') ]) # 读取停用词集
    # emotion_text = [ line.rstrip() for line in open('./Dict/emotion_words.csv') ] # 读取情感词集
    # del emotion_text[0] # 去除第一行，第一行是说明文字
    # emotionset = []
    # for text in emotion_text:
    #     emotionset.append(text.split(',')[0])
    stopset = read_stopset('./Dict/stop_words.txt')
    emotionset = read_emotionset('./Dict/emotion_words.csv')
    wordset, freqset_list = ef.word_freq(['./Training/TrainingSet50_cleaned.txt'], stopset)
    # scores = ef.std_chi_scores(wordset, freqset_list)
    scores = ef.opt_chi_scores(wordset, freqset_list, emotionset)
    ex_freqset = ef.extract_features(freqset_list, scores, 1000)

