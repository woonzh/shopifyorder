# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 15:22:54 2018

@author: woon.zhenhao
"""

import requests
import json

url='https://shopifyorder.herokuapp.com/orders'

#param={"name":"woonzh"}
#
#response = requests.get(url, params=param)
#print(response.content)

param={
       "name":"test",
       "email":"woonzh@hotmail.com",
       "apikey":"97b0d33bfea5fabe4304059aad30e61d",
       "password":"e02949c37facc1bbecf27310042b1431",
       "sharedsecret":"144cae7063ffe3f23ede0911754420ba"
       }

url='https://shopifyorder.herokuapp.com/createAccount'
response = requests.get(url, params=param)
print(response.content)