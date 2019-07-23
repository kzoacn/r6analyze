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
		return "[%s] [%d] : [%d] [%s] [%s]" % (self.club1,self.score1,self.score2,self.club2,self.mapname)

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

def myhash(s):
	t=0
	for c in s:
		t=t*31+ord(c);
	return t%1000000007

def analyze(url):
	wb_data = requests.get(url)
	sp = BeautifulSoup(wb_data.text,features="html.parser")
	res=[]
	for html in sp.find_all(attrs={"class" :"bracket-popup"}):
		matches=process(html)
		for m in matches:
			res.append(m)
	return res

tot=[]
def add(lst):
	for m in lst:
		tot.append(m)


urls=['https://liquipedia.net/rainbowsix/Pro_League/Season_10/Latin_America',
	'https://liquipedia.net/rainbowsix/Pro_League/Season_10/North_America',
	'https://liquipedia.net/rainbowsix/Pro_League/Season_10/Europe',
	'https://liquipedia.net/rainbowsix/Pro_League/Season_10/Asia_Pacific/Australia_and_New_Zealand',
	'https://liquipedia.net/rainbowsix/Pro_League/Season_10/Asia_Pacific/Japan',
	'https://liquipedia.net/rainbowsix/Pro_League/Season_10/Asia_Pacific/South_East_Asia',
	'https://liquipedia.net/rainbowsix/Pro_League/Season_10/Asia_Pacific/South_Korea',
	'https://liquipedia.net/rainbowsix/DreamHack/2019/Montreal',
	'https://liquipedia.net/rainbowsix/Six_Major/2019',
	'https://liquipedia.net/rainbowsix/PG_Nationals/2019/Summer',
	'https://liquipedia.net/rainbowsix/ESL/Premiership/2019/Summer',
	'https://liquipedia.net/rainbowsix/Saturday_League/Season_1/Contender_Division',
	'https://liquipedia.net/rainbowsix/Circuito_Feminino/2019/Game_XP',
	'https://liquipedia.net/rainbowsix/DreamHack/2019/Valencia',
	'https://liquipedia.net/rainbowsix/Russian_Major_League/Season_2',
	'https://liquipedia.net/rainbowsix/ESL/Benelux/League/Season_3/Finals',
	'https://liquipedia.net/rainbowsix/Allied_Esports/2019/Las_Vegas',
	'https://liquipedia.net/rainbowsix/Pro_League/Season_9/Finals',
	'https://liquipedia.net/rainbowsix/Challenger_League/Season_9/Europe',
	'https://liquipedia.net/rainbowsix/Challenger_League/Season_9/North_America',
	'https://liquipedia.net/rainbowsix/Challenger_League/Season_9/Latin_America',
	'https://liquipedia.net/rainbowsix/Pro_League/Season_9/Europe',
	'https://liquipedia.net/rainbowsix/Pro_League/Season_9/Latin_America',
	'https://liquipedia.net/rainbowsix/Pro_League/Season_9/North_America',
	'https://liquipedia.net/rainbowsix/Pro_League/Season_9/Asia_Pacific',
	'https://liquipedia.net/rainbowsix/Brasileir%C3%A3o/2019/S%C3%A9rie_B',
	'https://liquipedia.net/rainbowsix/Brasileir%C3%A3o/2019/Relegation',
	'https://liquipedia.net/rainbowsix/Six_Major/2019/Asia_Pacific',
	'https://liquipedia.net/rainbowsix/Six_Major/2019/North_America',
	'https://liquipedia.net/rainbowsix/Six_Major/2019/Latin_America',
	'https://liquipedia.net/rainbowsix/Six_Major/2019/Europe',
	'https://liquipedia.net/rainbowsix/United_States_Nationals/2019/Stage_2/Eastern_Conference/Qualifier_4',
	'https://liquipedia.net/rainbowsix/United_States_Nationals/2019/Stage_2/Eastern_Conference/Qualifier_3',
	'https://liquipedia.net/rainbowsix/United_States_Nationals/2019/Stage_2/Western_Conference/Qualifier_3',
	'https://liquipedia.net/rainbowsix/DreamHack/2019/Valencia/BYOC',
	'https://liquipedia.net/rainbowsix/ESL/Premiership/2019/Summer/Group_Stage',
	'https://liquipedia.net/rainbowsix/Six_Major/2019/Asia_Pacific/Japan',
	'https://liquipedia.net/rainbowsix/Six_Major/2019/Asia_Pacific/South_East_Asia',
	'https://liquipedia.net/rainbowsix/United_States_Nationals/2019/Stage_2/Western_Conference/Qualifier_2',
	'https://liquipedia.net/rainbowsix/Six_Major/2019/Europe/Qualifier_1'
	]

win={'PR':1}
lost={'PR':1}
clubs=['PR']
cnt=0
for url in urls:
	add(analyze(url))
	cnt+=1
	print("%d/%d" % (cnt,len(urls)))	
	
tot.reverse()
elo={'PR':2000}


for t in tot:
	if t.club1=='LSE':
		t.club1='LFO'
	if t.club2=='LSE':
		t.club2='LFO'
	win[t.club1]=0
	lost[t.club1]=0
	win[t.club2]=0
	lost[t.club2]=0
	elo[t.club1]=2000
	elo[t.club2]=2000

winrate=[]
		
for t in tot:
	RA=elo[t.club1]
	RB=elo[t.club2]
	EA=1.0/(1+10**((RB-RA)/400.0))
	EB=1.0/(1+10**((RA-RB)/400.0))
	SA=0
	SB=0
	if t.score1==t.score2:
		SA=0.5
		SB=0.5
	if t.score1>t.score2:
		SA=1
		SB=0
	if t.score1<t.score2:
		SA=0
		SB=1
	K=32
	elo[t.club1]=RA+K*(SA-EA)
	elo[t.club2]=RB+K*(SB-EB)
	

clubs=list(win.keys())
for club in clubs:
	winrate.append( (elo[club],club) )

winrate.sort(reverse=True)

for x in winrate:
	print(x)
