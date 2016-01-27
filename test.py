#coding:utf-8
#注意设置文件的编码格式为utf-8

# from simple_model import simple_model
# model = simple_model()
# res = model.classify("可恶的长滩岛某酒店服务员、可恶的长滩岛警察局、可恶的美亚保险，让我太失望了！")

import jieba

def tokenize(text):
    seg_list = list(jieba.cut(text, cut_all=False))# 精确模式
    # 去除单词前后的空格，如果整个单词是由空格构成则删除
    seg_newlist = []
    for seg in seg_list:
        # seg.strip()
        print seg
        if seg != ' ':
            seg_newlist.append(seg)
    return seg_newlist

if __name__ == '__main__':
    # string = ' '.strip()
    # print string
    seg_list = tokenize("fuck！手机通讯录和信息一开机就全没了！！fuck！！！死人三星！！fuck。")
    # print "Default Mode:", "/".join(seg_list)  # 精确模式
