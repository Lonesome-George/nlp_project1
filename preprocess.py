# -*- coding: utf-8 -*-

import re


def  clean(text):
	'''
	参数text为原始微博
	有可能返回空字符串，比如说纯转发的微博
	'''
	#应该严格按照这个顺序进行处理
	text = del_reply(text)
	text = del_topic(text)
	text = del_source(text)
	text = del_email(text)
	text = del_link(text)
	text = del_quote(text)
	text = del_num(text)
	text = del_mark(text)
	return text.strip()+'\n'

#删除回复
def del_reply(text):
	regex = r"//@[\s\S]*$"
	return re.sub(regex, u''.encode('utf-8'), text).strip('\n')

#删除话题和标题
def del_topic(text):
	regex = r"我在#[\s\S]*?#|#[\s\S]*?#|\[[\s\S]*?\]|【[\s\S]*?】|『[\s\S]*?』|「[\s\S]*?」|＜[\s\S]*?＞"
	return re.sub(regex, u''.encode('utf-8'), text).strip('\n')

#删除来源
def del_source(text):
	regex = r"（分享自[\s\S]*?）|（来自[\s\S]*?）|\(分享自[\s\S]*?\)|\(来自[\s\S]*?\)"
	return re.sub(regex, u''.encode('utf-8'), text).strip('\n')

#删除E-mail
def del_email(text):
	regex = r"\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*"
	return re.sub(regex, u''.encode('utf-8'), text).strip('\n')

#删除链接
def del_link(text):
	regex = ur"[a-zA-z]+://[^\s，。]*|[a-zA-z]+\.[^\s，。]*"
	return re.sub(regex, u''.encode('utf-8'), text).strip('\n')

#删除@引用
def del_quote(text):
	regex = r"回复@[^\s]*?[:]"
	text = re.sub(regex, u''.encode('utf-8'), text)
	regex = ur"//[\s\S]*?[:]|@[^\s，。、：？~:]*?"
	return re.sub(regex, u''.encode('utf-8'), text).strip('\n')

#删除电话号码/邮政编码/ipv4地址/过长的数字串（五位及以上）
def del_num(text):
	regex = r"\d{3}-\d{8}|\d{4}-\d{7}|[1-9]\d{5}(?!\d)|\d+\.\d+\.\d+\.\d+|\d{5,}"
	return re.sub(regex, u''.encode('utf-8'), text).strip('\n')

#部分特殊符号
def del_mark(text):
	regex = r"→_→|\(≧▽≦\)|=\^_\^=|\([\s]*?\)|（[\s]*?）"
	return re.sub(regex, u''.encode('utf-8'), text).strip('\n')


if __name__ == '__main__':

	# src_file = "./Training/TrainingSet50.txt"
	# result_file = "./Training/TrainingSet50_cleaned.txt"
	src_file = "./Training/RawTrainingSet10000.txt"
	result_file = "./Training/RawTrainingSet10000_cleaned.txt"

	fi = file(src_file, 'r')
	fo = open(result_file, 'w')

	while True:
		#直接处理utf-8编码的字符，否则无法处理中文符号
		line = fi.readline()
		if len(line) == 0:
			break
		#print line.decode('utf-8')
		cleaned_text = clean(line)
		if len(cleaned_text) == 0:
			continue
		fo.write(cleaned_text) #文件utf-8编码

	fi.close()
	fo.close()
	print 'done!'
	