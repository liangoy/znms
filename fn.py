from w2v import W2v
import json
import mem_data_client
import bson
w2v=W2v('./w2v.json')
with open('./stock_fund_code') as f:stock_fund=json.loads(f.read())
w2v.name=list(map(lambda x:x['name'],stock_fund))
w2v.jieba_loads_stock_fund()


#precedence_table

def add_action(fn):
    def do(*args):
        r=fn(*args)
        if type(r)==dict:
            r['action']=fn.__name__
            return r
        else:
            return {}
    return do
    
pt={}

stock_list=list(map(lambda x:x['name'],filter(lambda x:x['type']=='stock' ,stock_fund)))
fund_list=list(map(lambda x:x['name'],filter(lambda x:x['type']=='fund' ,stock_fund)))

def n2c(name):
    return list(filter(lambda x:x['name']==name,stock_fund))[0]


@add_action
def stock_fund_info(t):
    lis=list(map(lambda x:n2c(x) ,filter(lambda x:x in t,w2v.name)))
    if len(lis)==1:
        d=lis[0].copy()
        d['add']=d['name']+'基本信息'
        return d
    else :
        return None
pt[2]=stock_fund_info

@add_action
def stock_vs(t):
    lis=list(map(lambda x:n2c(x) ,filter(lambda x:x in t,stock_list)))
    if len(lis)>=2:
        d={'code':[i['code'] for i in lis]}
        d['add']=lis[0]['name']+'与'+lis[1]['name']+'对比'
        return d
    else:
        return None
pt[3]=stock_vs

@add_action
def stock_fund_news(t):
    lis=list(map(lambda x:n2c(x) ,filter(lambda x:x in t,w2v.name)))
    if len(lis)==1 and ('资讯'in t or '新闻' in t):
        d=lis[0].copy()
        d['add']=d['name']+'新闻'
        return d
    return None
pt[4]=stock_fund_news

@add_action
def stock_stru(t):
    lis=list(map(lambda x:n2c(x) ,filter(lambda x:x in t,stock_list)))
    if len(lis)==1 and ('股权结构'in t or '股东'in t):
        d=lis[0].copy()
        d['add']=d['name']+'的股权结构信息'
        return d
    return None
pt[5]=stock_stru

@add_action
def stock_bsp(t):
    lis=list(map(lambda x:n2c(x) ,filter(lambda x:x in t,stock_list)))
    if len(lis)==1 and ('买卖点' in t):
        d=lis[0].copy()
        d['add']=d['name']+'买卖点'
        return d
    return None
pt[5.1]=stock_bsp

@add_action
def good_stock(t):
    if '推荐'in t:
        return {'add':'推荐股票'}
    return None
pt[6]=good_stock

@add_action
def index(t):
    if '大盘' in t:
        return {'add':'大盘行情'}
    return None
pt[7]=index


'''#######################################'''


def translate(value):#http://139.196.88.54:6677/?action=fn.translate&value={%22text%22:%22%E5%B7%A5%E5%95%86%E9%93%B6%E8%A1%8C%22,%22top%22:9}
    text=value['text']
    top=int(value.get('top',3))
    lis=list(filter(lambda x:x,map(lambda x:pt[x](text),sorted(list(pt.keys()),reverse=1))))
    if lis==[]:
        return if_error({'reason':100})
    d=lis[0]
    d.pop('add')
    d['_id']=str(bson.objectid.ObjectId())
    d['addition']=[i['add'] for i in lis[1:top]]
    return d


md= mem_data_client.Client('http://139.196.88.54:1320')
def get_news(value):#http://139.196.88.54:6677/?action=fn.get_news&value={%22name%22:%22%E5%B7%A5%E5%95%86%E9%93%B6%E8%A1%8C%22,%22top%22:9}
    code=value.get('code','')
    top=int(value.get('top',3))
    name=value.get('name','')
    if code!='':
        name=list(filter(lambda x:x['code']==code,stock_fund))[0]['name'] 
    #data=md.get("sorted(var['news'].map(lambda x:[x['score'][r'%s'],x['title'],x['time'],x['url']]),key=lambda x:x[0])[:%s]"%(name,top))['data']
    data=md.get("table['news'].filter(lambda x:r'%s' in x['content']).map(lambda x:[x['score'][r'%s'],x['title'],x['time'],x['url']])[:%s]"%(name,name,top))['data']
    lis=list(map(lambda i:{'score':i[0],'title':i[1],'time':i[2],'url':i[3]},data))
    return lis[:top]

def if_error(value):
    if not value.get('_id','') and value.get('reason',100000)>99:
        raise "ERROR:YOU SHOULD POST _id"
    reason=int(value.get('reason',''))
    if reason==101:
        text='不好意思哦，您要的资源暂时找不到'
        return {'action':'text','text':text,'addition':[]}
    
    elif reason==99：
        d=index
        d.pop('add')
        d['_id']=str(bson.objectid.ObjectId())
        d['addtion']=[]
    
    elif:
        text='您的话有点深奥哦，我先给您推荐股票吧！'
        d=good_stock('推荐')
        d['action']=good_stock.__name__
        return  {'action':'text','text':text,'addition':['推荐股票']}
    
    
