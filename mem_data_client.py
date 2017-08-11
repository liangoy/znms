import requests
import base64
import json

class Client():
    def __init__(self,host):
        self.host=host
    def shell(self,c):
        result=requests.post(url=self.host,data=c.encode('utf-8')).content.decode('utf-8')
        return result
    def get(self,data):
        c="self.data={'data':%s}"%(data)
        result=requests.post(url=self.host,data=c.encode('utf-8')).content.decode('utf-8')
        return json.loads(result)

#md=Client('http://139.196.88.54:1320') 
