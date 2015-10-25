# nlp_project1
nlp_project1

IMPORTANT!<br>
To Predict:<br>
0.运行preprocess.py预处理文本。<br>
1.运行extract_features.py抽取特征词，抽取的特征词数目可在代码中设置；<br>
2.运行weight.py计算特征词的权重；<br>
3.运行main_pred.py预测文本类别。<br>
每次预测新文本集时只需运行main_pred.py，表示使用已抽取的特征词和训练集训练模型并预测；
如果要使用新的特征词训练模型，只需从第1步开始做即可。<br>

To Choose Corpus:<br>
0.Remove all files under the directory "Training/ChosenSet";<br>
1.Run preprocess.py to preprocess all texts;<br>
2.Run extract_features.py to extract feature words, you can set in code how many words to choose;<br>
3.Rum weight.py to compute the weight of every feature word;<br>
4.Run main_select_corpus.py, and you can get some(number can be set in code) weibo texts under the directory "Training/ChosenSet";<br>
5.Choose the texts you need and label them, then go back to step 2.<br>
When choosing corpus, you can do the loop as many times as you like until you get enough corpus.<br>
