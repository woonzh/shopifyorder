# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 15:22:54 2018

@author: woon.zhenhao
"""

import requests
import json

url='https://shopifyorder.herokuapp.com/orders'

param={"name":"k-bella-swim"}

#response = requests.get(url, params=param)
#print(response.content)

response = requests.post(url)
print(response.content)