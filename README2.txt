仅供娱乐：
1.特征抽取：unigram、bigram、sentiment/emotion bearing words and parts-of-speech information的组合。
2.对于上一次被选中但是下一次反而没有被选中的语料该怎么处理？丢弃还是保留？


Questions:
1.如何快速替换特征选取方法而不用修改很多代码？
为每一种特征抽取方法写一个函数；Input：label text的训练集；Output：feature,target列表。
2.在选出语料并且进行标注后如何将其加入训练集中？
3.如何保存模型？


针对中文微博的情感分析，本文采用了二步法，首先引入主题无关特征，即使用链接、表情符号、情感词典、情感短语、上下文等特征训练SVM对中文微博进行情感分类；
-摘自《基于层次结构的多策略中文微博情感分析和特征抽取》