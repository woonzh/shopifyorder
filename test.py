# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 15:22:54 2018

@author: woon.zhenhao
"""

import requests

url='https://shopifyorder.herokuapp.com/accounts'

response = requests.get(url)
#df=json.loads(response.content)

print(response.content)