#!/bin/python
# -*- coding:utf-8 -*-  
#年度消费统计程序 2019.01.12 Shieber

import re, json
import requests
import numpy as np
import matplotlib.pyplot as plt

#编码错误就取消注释
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def string():
	'''返回匹配的字符串'''
	url = 'https://www.currencydo.com/'
	user_agent = 'Mozilla/4.0 (compatible; MSTE 5.5; Windows NT)'
	headers = {'User-Agent':user_agent}
	respon = requests.get(url,headers=headers)
	html = str(respon.text)

	cur_p = re.compile(r'今日1美元兑人民币汇率是：(\d\.\d+)人民币(.*)(\d\.\d+)美金')
	cur   = cur_p.search(html)

	return cur

def exchangerate():
	'''获取人民币兑美元的汇率'''
	curs = []
	cur  = string()

	try:	
		curs.append(float(cur.group(1)))
		curs.append(float(cur.group(3)))
	except AttributeError: #获取失败时以1返回
		curs = [1,1]
		print("未获取到美元汇率，以人民币结算!")

	return curs

def symbol(argv):
	'''确定是美元还是人民币单位制
	   给出标题的字符串'''
	items = ["JDpay","Alipay","Wechat","Total"]
	if len(argv) == 5:
		cur = exchangerate()[1]
		sym = 1
	else:
		cur = 1
		sym = 2

	title = argv[2] + ' ' + items[int(argv[3])-1] + ' Annual Expenditure of Shieber'

	return cur,sym,title

def data(argv,cur,items):
	'''获取数据并返回'''
	with open(argv[1],'r') as load_f:
		jsonData = json.load(load_f)
	year  = jsonData[argv[2]]
	month_num = len(year.keys()) -1
	months= ["1","2","3","4","5","6","7","8","9","10","11","12"]

	cost = []
	for i in range(len(year.keys()) -1):
		cost.append(year[months[i]][items[int(argv[3])-1]])

	cost = np.array(cost)
	cost = list(cost*cur)
	if cur != 1:
		for i in range(len(cost)):
			cost[i] = round(cost[i],2)

	return months,cost

def draw(sym,Title,X,Y):
	'''作成柱状图'''
	if sym == 2:
		Title += " (RMB/CN $)" 
	else:
		Title += " (USD $)" 

	plt.bar(X,Y,width=0.5,facecolor='green')
	plt.xlabel('Month')
	plt.ylabel('Expenditure')
	plt.title(Title.decode('utf-8'))
	for x,y in zip(X,Y):
		plt.text(x,y+0.3,str(y),ha='center',va='bottom')
	plt.show()

def expen2pic():
	'''main function'''
	argv = sys.argv
	if len(argv) < 4 or int(argv[3])>4 :
		print("Usage: python " + argv[0] + " expen.json 2016-2018 1-4 [US]")
		sys.exit()

	items = ["JDpay","Alipay","Wechat","Ztotal"]
	cur,sym,title= symbol(argv)
	month,cost = data(argv,cur,items)
	draw(sym,title,month,cost)

if __name__ == '__main__':
	'''主程序，开始执行'''
	expen2pic()
