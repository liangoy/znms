from w2v import W2v
import json
import mem_data_client
w2v=W2v('./w2v.json')
with open('./stock_fun_code') as f:stock_fun=json.loads(f.read())
w2v.name=list(map(lambda x:x['name'],stock_fun))
w2v.jieba_loads_stock_fun()
#precedence_table
pt={}

stock_list=list(map(lambda x:x['name'],filter(lambda x:x['type']=='stock' ,stock_fun)))
fun_list=list(map(lambda x:x['name'],filter(lambda x:x['type']=='fun' ,stock_fun)))

def n2c(name):
    return list(filter(lambda x:x['name']==name,stock_fun))[0]

def stock_fun_info(t):
    lis=list(map(lambda x:n2c(x) ,filter(lambda x:x in t,w2v.name)))
    if len(lis)==1:
        return lis[0]
    else :
        return None
pt[2]=stock_fun_info

def stock_vs(t):
    lis=list(map(lambda x:n2c(x)['code'] ,filter(lambda x:x in t,stock_list)))
    if len(lis)>=2:
        return {'code':lis}
    else:
        return None
pt[3]=stock_vs

def stock_fun_news(t):
    lis=list(map(lambda x:n2c(x) ,filter(lambda x:x in t,w2v.name)))
    if len(lis)==1 and ('资讯'in t or '新闻' in t):
        return lis[0]
    return None
pt[4]=stock_fun_news

def stock_stru(t):
    lis=list(map(lambda x:n2c(x) ,filter(lambda x:x in t,stock_list)))
    if len(lis)==1 and ('股权结构'in t or '股东'in t):
        return lis[0]
    return None
pt[5]=stock_stru

def stock_bsp(t):
    lis=list(map(lambda x:n2c(x) ,filter(lambda x:x in t,stock_list)))
    if len(lis)==1 and ('买卖点' in t):
        return lis[0]
    return None
pt[5.1]=stock_bsp

def good_stock(t):
    if '推荐'in t:
        return {}
    return None
pt[6]=good_stock

def index(t):
    if '大盘' in t:
        return {}
    return None
pt[7]=index


'''#######################################'''


def translate(value):#http://139.196.88.54:6677/?action=fn.translate&value={%22text%22:%22%E5%B7%A5%E5%95%86%E9%93%B6%E8%A1%8C%22,%22top%22:9}
    text=value['text']
    top=value.get('top',3)
    lis=[]
    for i in sorted(list(pt.keys()),reverse=1):
        resu=pt[i](text)
        if resu !=None:
            resu['action']=pt[i].__name__
            lis.append(resu)
    return lis[:top]


md= mem_data_client.Client('http://139.196.88.54:1320')
def get_news(value):#http://139.196.88.54:6677/?action=fn.get_news&value={%22name%22:%22%E5%B7%A5%E5%95%86%E9%93%B6%E8%A1%8C%22,%22top%22:9}
    code=value.get('code','')
    top=str(value.get('top',3))
    name=value.get('name','')
    if code!='':
        name=list(filter(lambda x:x['code']==code,stock_fun))[0]['name'] 
    #data=md.get("sorted(var['news'].map(lambda x:[x['score'][r'%s'],x['title'],x['time'],x['url']]),key=lambda x:x[0])[:%s]"%(name,top))['data']
    data=md.get("table['news'].filter(lambda x:r'%s' in x['content']).map(lambda x:[x['score'][r'%s'],x['title'],x['time'],x['url']])[:%s]"%(name,name,top))['data']
    lis=[]
    for i in data:
        d={
        'score':i[0],
        'title':i[1],
        'time':i[2],
        'url':i[3]
        }
        lis.append(d)
    return lis

def if_error(value):
    reason=int(value.get('reason',''))
    if reason==101:
        text='不好意思哦，您要的资源暂时找不到'
        return [{'action':'text','text':text}]
    else:
        text='您的话有点深奥哦，我先给您推荐股票吧！'
        d=good_stock('推荐')
        d['action']=good_stock.__name__
        return  [{'action':'text','text':text},d]
    
    
