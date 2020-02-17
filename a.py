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
		if len(header.find_all('a'))<2:
			continue
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


urls=['https://liquipedia.net/rainbowsix/Pro_League/Season_11/Europe',
      'https://liquipedia.net/rainbowsix/Pro_League/Season_11/Finals',
      'https://liquipedia.net/rainbowsix/Pro_League/Season_11/North_America',
      'https://liquipedia.net/rainbowsix/Pro_League/Season_11/Latin_America',
      'https://liquipedia.net/rainbowsix/Pro_League/Season_11/Asia_Pacific',
      'https://liquipedia.net/rainbowsix/Pro_League/Season_10/Finals',
      'https://liquipedia.net/rainbowsix/Six_Major/2019',
      'https://liquipedia.net/rainbowsix/Six_Invitational/2020',
      'https://liquipedia.net/rainbowsix/Six_Invitational/2020/Europe',
      'https://liquipedia.net/rainbowsix/Six_Invitational/2020/North_America',
      'https://liquipedia.net/rainbowsix/Six_Invitational/2020/Latin_America',
      'https://liquipedia.net/rainbowsix/Six_Invitational/2020/Asia_Pacific',
      'https://liquipedia.net/rainbowsix/DreamHack/2019/Montreal']
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
	if t.mapname=='Culbhouse':
		t.mapname='Clubhouse'
                
	if t.club1=='LSE':
		t.club1='LFO'
	if t.club2=='LSE':
		t.club2='LFO'
	if t.club1=='LFO':
		t.club1='Giants'
	if t.club2=='LFO':
		t.club2='Giants'
	win[t.club1]=0
	lost[t.club1]=0
	win[t.club2]=0
	lost[t.club2]=0
	elo[t.club1]=2000
	elo[t.club2]=2000

winrate=[]

maps=['Kafe Dostoyevsky','Villa','Clubhouse','Coastline','Border','Bank','Consulate','Oregon']
mapwl={}
for t in tot:
        mapwl[t.club1]={}
        mapwl[t.club2]={}
for t in tot:
        for m in maps:
                mapwl[t.club1][m]=0
                mapwl[t.club2][m]=0
		
for t in tot:
	mapwl[t.club1][t.mapname]+=t.score1-t.score2
	mapwl[t.club2][t.mapname]+=t.score2-t.score1
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

def best(d):
        mx=-100
        ans=''
        for m in maps:
                if d[m]>mx:
                        mx=d[m]
                        ans=m
        return ans
def worst(d):
        mx=100
        ans=''
        for m in maps:
                if d[m]<mx:
                        mx=d[m]
                        ans=m
        return ans

def teamap(tname,mname):
        ans=[]
        for t in tot:
                if t.club1==tname or t.club2==tname:
                        if t.mapname==mname:
                                ans.append(t)
        return ans


for m in teamap('NiP','Clubhouse'):
        print(m)
for m in teamap('SSG','Clubhouse'):
        print(m)


for x in winrate:
        if x[1]=='SSG':
                print(x[1])
                print(mapwl[x[1]])
        if x[1]=='NiP':
                print(x[1])
                print(mapwl[x[1]])
