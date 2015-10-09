#encoding=utf-8

from corpus import corpora
cp = corpora()
cp.readtxt()
cp.save_ndocs(200)