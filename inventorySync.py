# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 18:03:46 2018

@author: woon.zhenhao
"""

import masterReader as mr
import keyRetriever as kr
import connector as con

url=''

def main(acct, mainUrl):
    global url
    url = kr.getUrl(mainUrl, "inventory")