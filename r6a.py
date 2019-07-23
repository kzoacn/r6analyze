from bs4 import BeautifulSoup
import requests
import time
import json

class Match:
	def __init__(self):
		self.club1='n/a'
		self.club2='n/a'
		self.mapname='n/a'
		self.score1=0
		self.score2=0
		self.score1_att=0
		self.score1_def=0
		self.score2_att=0
		self.score2_def=0
	
	def __str__(self):
		return "%s %d : %d %s [%s]" % (self.club1,self.score1,self.score2,self.club2,self.mapname)

def mapfilter(tag):
	return tag.has_attr('style') and ('line-height:21px;overflow: hidden;text-overflow: ellipsis;white-space: nowrap;' in str(tag['style']))

def process(html):
	soup = BeautifulSoup(str(html),features="html.parser")
	header=soup.find(attrs={"class" :"bracket-popup-header"})
	matches=[]
	
	
	for bra in soup.find_all(attrs={"class" :"bracket-popup-body-match"}):
		match=Match()
		match.club1=header.find_all('a')[ 0].string
		match.club2=header.find_all('a')[-1].string

		match.score1=0
		match.score2=0
		
		
		nums=bra.find(attrs={"style" :"float:left;"}).find_all('td')
		for t in nums:
			try:
				x=int(t.string)
				match.score1=max(match.score1,x)
			except:
				pass
		nums=bra.find(attrs={"style" :"float:right;"}).find_all('td')
		for t in nums:
			try:
				x=int(t.string)
				match.score2=max(match.score2,x)
			except:
				pass
		if match.score1+match.score2==0:
			continue
		
		match.mapname=bra.find(mapfilter).a.string
		
		matches.append(match)
	
	return matches

def analyze(url):
	wb_data = requests.get(url)
	sp = BeautifulSoup(wb_data.text,features="html.parser")
	for html in sp.find_all(attrs={"class" :"bracket-popup"}):
		matches=process(html)
		for m in matches:
			print(m)

analyze('https://liquipedia.net/rainbowsix/Pro_League/Season_10/North_America')
