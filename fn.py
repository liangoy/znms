from w2v import W2v
import json
import mem_data_client
w2v=W2v('./w2v.json','./stock_fun_list','./jieba_stock_fun_dict')
with open('./stock_fun_code') as f:stock_fun_code=json.loads(f.read())

#precedence_table
pt={}

def n2c(name):
    return list(filter(lambda x:x['name']==name,stock_fun_code))[0]

def _2_stock_info(t):
    lis=[]
    for i in w2v.name:
        if i in  t:
            lis.append(n2c(i))
    if len(lis)==1:
        return lis[0]
    else :
        return None
pt[2]=_2_stock_info

def _3_stock_vs(t):
    lis=[]
    for i in w2v.name:
        if i in t:
            lis.append(n2c(i))
    if len(lis)>=2:
        return lis
    else:
        return None
pt[3]=_3_stock_vs

def _4_stock_news(t):
    lis=[]
    for i in w2v.name:
        if i in t:
            lis.append(n2c(i))
    if len(lis)==1:
        if '资讯'in t or '新闻' in t:
            return lis[0]
    return None
pt[4]=_4_stock_news

def _5_stock_stru(t):
    lis=[]
    for i in w2v.name:
        if i in t:
            lis.append(n2c(i))
    if len(lis)==1:
        if '股权结构'in t or '股东'in t:
            return lis[0]
    return None
pt[5]=_5_stock_stru

def _51_stock_mn(t):
    lis=[]
    for i in w2v.name:
        if i in t:
            lis.append(n2c(i))
    if len(lis)==1:
        if '买卖点' in t:
            return lis[0]
    return None
pt[5.1]=_51_stock_mn

def _6_good_stock(t):
    if '推荐'in t:
        return 'recommend'
    return None
pt[6]=_6_good_stock

def _7_total(t):
    if '大盘' in t:
        return 'index'
    return None
pt[7]=_7_total


'''#######################################'''


def translate(value):#http://139.196.88.54:6677/?action=fn.translate&value={%22text%22:%22%E5%B7%A5%E5%95%86%E9%93%B6%E8%A1%8C%22,%22top%22:9}
    text=value['text']
    top=value.get('top',3)
    lis=[]
    for i in sorted(list(pt.keys()),reverse=1):
        resu=pt[i](text)
        if resu:
            lis.append([i,resu])
    return lis[:top]







md= mem_data_client.Client('http://139.196.88.54:1320')
def get_news(value):#http://139.196.88.54:6677/?action=fn.get_news&value={%22name%22:%22%E5%B7%A5%E5%95%86%E9%93%B6%E8%A1%8C%22,%22top%22:9}
    code=value.get('code','')
    top=str(value.get('top',3))
    name=value.get('name','')
    if code!='':
        name=list(filter(lambda x:x['code']==code,stock_fun_code))[0]['name'] 
    data=md.get("sorted(var['news'].map(lambda x:[x['score'][r'%s'],x['title'],x['time'],x['url']]),key=lambda x:x[0])[:%s]"%(name,top))['data']
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
       
