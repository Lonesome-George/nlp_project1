#coding:utf-8

if __name__ == '__main__':
    from corpus import corpora
    cp = corpora()
    cp.read_txt()
    cp.save_ndocs(30)
