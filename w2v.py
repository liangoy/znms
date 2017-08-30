import json
import numpy as np
import jieba.analyse as ja
import jieba
class W2v():
    def __init__(self,path,name_file=None,jieba_dict=None):
        with open(path) as f:
            self.w2v=json.loads(f.read())
            for i in self.w2v:
                self.w2v[i]=np.array(self.w2v[i])
        if name_file:
            with open(name_file) as f:
                self.name=json.loads(f.read())
        if jieba_dict:
            jieba.load_userdict(jieba_dict)
    
    def jieba_loads_stock_fund(self):
        with open('tmp_jieba_user_dict','w') as f:
            text=''
            for i in self.name:
                text+=(i+' 1000\n')
            f.write(text)
        jieba.load_userdict('./tmp_jieba_user_dict')
    
    def distance(self,w1,w2):
        return np.sqrt(np.sum((self.w2v[w1]-self.w2v[w2])**2))
    def distance_word_rank(self,w,top=7):
        dic={}
        for i in self.w2v:
            dic[i]=self.distance(w,i)
        return sorted(dic.items(),key=lambda x:x[1])[1:top+1]
            
    def distance_word_rank_percent(self,w,top=7):
        dic={}
        for i in self.w2v:
            dic[i]=self.distance(w,i)
        a=sum(dic.values())/len(dic)
        for i in dic:
            dic[i]/=a
        return sorted(dic.items(),key=lambda x:x[1])[1:top+1]

    def distance_text_rank(self,text,top=7,anal='textrank'):
        if anal=='textrank':
            fn=ja.textrank
        else:
            fn=ja.tfidf
        tr={'word':[],'weight':[]}
        all_word=list(self.w2v.keys())
        for i in fn(text,withWeight=True)[:32]:
            if i[0] in all_word:
                tr['word'].append(i[0])
                tr['weight'].append(i[1])        
        dic={}
        for i in self.name:
            s=0
            for j in range(len(tr['word'])):
                s+=self.distance(i,tr['word'][j])*tr['weight'][j]
            dic[i]=s/sum(tr['weight'])
        return sorted(dic.items(),key=lambda x:x[1])[:top]

    def distance_text_rank_percent(self,text,top=7,anal='textrank'):
        if anal=='textrank':
            fn=ja.textrank
        else:
            fn=ja.tfidf
        tr={'word':[],'weight':[]}
        all_word=list(self.w2v.keys())
        for i in fn(text,withWeight=True)[:32]:
            if i[0] in all_word:
                tr['word'].append(i[0])
                tr['weight'].append(i[1])        
        dic={}
        for i in self.name:
            s=0
            for j in range(len(tr['word'])):
                s+=self.distance(i,tr['word'][j])*tr['weight'][j]
            dic[i]=s/sum(tr['weight'])
        a=sum(dic.values())/len(dic)
        for i in dic:
            dic[i]/=a
        return sorted(dic.items(),key=lambda x:x[1])[:top]


    
