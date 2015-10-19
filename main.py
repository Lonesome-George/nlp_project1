#encoding=utf-8

from corpus import corpora
cp = corpora()
cp.read_txt()
cp.save_ndocs(50)