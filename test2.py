# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 22:47:01 2018

@author: woon.zhenhao
"""

import pandas as pd
import connector as cn
import keyRetriever as kr

df=pd.read_csv('template.csv')
df.to_csv()

mainurl=kr.getMainUrl('woonzh')
url=kr.getUrl(mainurl,"locations")
body=''
callType="get"

response=cn.connect(url,body, callType)

print(response)