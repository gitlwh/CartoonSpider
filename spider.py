__author__='shen'
# -*- coding:utf-8 -*-
import re
import urllib
import urllib2
import os
import itertools
import sys

reload(sys)
sys.setdefaultencoding('utf8') 
class spider:

	def __init__(self):
		self.mainURL='http://www.dragonball-multiverse.com/cn/chapters.html'
		self.rootURL='http://www.dragonball-multiverse.com/cn/'
		self.user_agent='Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		self.headers={'User-Agent':self.user_agent}
		self.mkdir()
		self.count=itertools.count(1)
		self.charName=''

	def getMainPage(self):		
		request=urllib2.Request(self.mainURL,'',self.headers)		
		try:
			response=urllib2.urlopen(request,timeout=10)
		except urllib2.URLError,e:
			print e.reason
			exit()
		return response.read()

	def getPage(self,response):
		pattern=re.compile(r"<a href='(page-\d+.html)' class='(?:double ){0,1}'>(\d+)-*\d*</a>",re.S)
		items=re.findall(pattern,response)
		for item in items:
			print 'found',item[1]
			self.getPic(self.rootURL+item[0],item[1])
	def getPic(self,URL,name):
		print 'getting the',name,'image'
		request=urllib2.Request(URL,None,self.headers)
		try:
			response=urllib2.urlopen(request)
		except urllib2.URLError,e:
			print e.reason
			exit()		
		pattern=re.compile(r'<meta property="og:title" content="(.+) - .+ - Dragon Ball Multiverse" />.+width:\d+px; height:\d+px" class="img"><img src="/cn/(.+)" alt="" /></div>',re.S)
		a=response.read()
		items=re.findall(pattern,a)
                for item in items:
			if self.charName!=item[0]:
				self.charName=item[0]
				self.order=self.count.next()
			wholeName='Chapter'+str(self.order)+self.charName
                        self.storePic(self.rootURL+item[1],name,wholeName)
	def mkdir(self,name=''):
		if name:
			name='/'+name
		if not os.path.exists('images'+name):
			os.makedirs('images'+name)
	def storePic(self,picURL,name,wholeName):
         	print 'storing',name,'in',wholeName.encode('utf-8')
		picInf = urllib.urlopen(picURL)
         	data = picInf.read()
		self.mkdir(wholeName.encode('utf-8'))
		f = open(('images/'+wholeName+'/'+name+'.png').encode('utf-8'), 'wb')
         	f.write(data)
         	f.close()
		print 'done'
Spider=spider()
response=Spider.getMainPage()
Spider.getPage(response)
