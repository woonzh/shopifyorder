# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 15:22:54 2018

@author: woon.zhenhao
"""

import requests
import json

url='https://shopifyorder.herokuapp.com/orders'

param={"name":"woonzh"}

response = requests.get(url, params=param)
print(response.content)

#param={
#       "name":"woonzh",
#       "email":"woonzh@hotmail.com",
#       "apikey":"d65bb311b92444b3ab661639c1ceeee9",
#       "password":"f973e5eabe90af1d7c9f3faeed311f8e",
#       "sharedsecret":"c73d622d538b5e1520967127bda26810"
#       }
#
#url='https://shopifyorder.herokuapp.com/createAccount'
#response = requests.post(url, params=param)
#print(response.content)