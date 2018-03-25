# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 09:46:01 2018

@author: woon.zhenhao
"""

import requests
import keyRetriever as kr
import json

header={
        "Content-Type":"aplication/json",
        "Accept":"aplication/json"
        }

def connect(url, body, callType):
    if callType == "get":
        response=requests.get(url)
    
    if callType == "post":
        response = requests.post(url, data = body, headers= header)
        
    if response.status_code==200:
        return True, response.content
    else:
        return False, "Failed connection"
    

url=kr.testing("orders")

suc, response = connect(url,'','get')

df=json.loads(response)