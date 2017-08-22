1、
输入：http://139.196.88.54:6677/?action=fn.translate&value={"text":"工商银行买卖","top":9}
输出：
{"data": [["stock_bsp", {"name": "\u5de5\u5546\u94f6\u884c", "code": "601398", "type": "stock"}], ["stock_info", {"name": "\u5de5\u5546\u94f6\u884c", "code": "601398", "type": "stock"}]]}
解释：返回的列表中的数字代表优先级，数字越大优先级越高
stock_info：得到股票的基本信息，例如分钟线等，返回股票名字代码
stock_vs：得到两只股票的对比，返回的是两只股票的股票名字代码
stock_news：得到股票新闻，返回的是股票名字代码
stock_stru：得到股票的股权结构，返回的是股票名字代码
stock_bsp:得到股票的买卖点，返回的是股票名字代码
good_stock：想要我们返回推荐的股票代码
index：得到大盘行情
text:将文本内容打印出来

作用：将语句格式化
text：输入的语句
top：按照相关性返回的条数，默认为3

2
输入：http://139.196.88.54:6677/?action=fn.get_news&value={"name":"工商银行","code":"601398","top":1}
输出：
{'data': [{'content': '【环球网科技报道 '
                      '记者陈健】一直以来，中国制造的电子产品就占有世界的绝大多数，但是知名度并不高，随着近些年来，小米、华为、一加等产品在海外的畅销，越来越多的外国人开始关注除了三星、苹果以外的中国>
手机，而中国制造的手机也凭借出色的性能和过硬的品质越来越受到海外用户的追捧。\n',
           'score': 30.507676497715288,
           'time': 1502076076.7286077,
           'title': '外国人来中国代购小米 中国手机开始被世界追捧'}]}
作用：输入股票或者基金的代码（字符串）或者名字返回若干条相关新闻
name：股票或基金名称
code：股票或者基金代码
（name和code选择输入一个就可以）
top：返回的条数，默认3
                                                                                                                                                                                                        

                                                                                                                                                                                                        
