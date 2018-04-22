# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 10:12:00 2018

@author: woon.zhenhao
"""

import pandas as pd
import os
from urllib import parse
import psycopg2 as ps
import connector as con
import datetime

link = 'keys/keys.csv'

urlExten={
        "inventory": "products.json",
        "orders": "orders.json",
        "locations":"locations/count.json"
        }

shop_url=''

def connectToDatabase(url):
    os.environ['DATABASE_URL'] = url
               
    parse.uses_netloc.append('postgres')
    url=parse.urlparse(os.environ['DATABASE_URL'])
    
    conn=ps.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
            )
    
    cur=conn.cursor()
    
    return cur, conn

def queryAcct(shopName):
    url="postgres://lpwrkshmpfsrds:f6d80a024a0defe3141d7bdb31279891768d47421020320c32c7ea26f9909255@ec2-23-21-217-27.compute-1.amazonaws.com:5432/d246lgdkkjq0sr"
    query="SELECT apikey, pass, shopname FROM keys WHERE shopname='"+str(shopName)+"'"
    cur, conn=connectToDatabase(url)
    cur.execute(query)
    
    data=cur.fetchone()
    key = data[0]
    password = data[1]
    name = data[2]
    
    conn.commit()    
    cur.close()
    conn.close()
        
    return key, password, name

def getMainUrl(shopName):
    key, password, name = queryAcct(shopName)
    shop_url = "https://%s:%s@%s.myshopify.com/admin/" % (key, password, name)
    
    return shop_url

def getUrl(url, name):
    
    final_url = url+urlExten[name]
    
    return final_url

def dateConvert():
    enddate=datetime.datetime.now()
    startdate=enddate-datetime.timedelta(days=1)
    
    edstr=enddate.strftime("%Y-%m-%dT%H:%M:%S")+"+12:00"
    sdstr=startdate.strftime("%Y-%m-%dT%H:%M:%S")+"+12:00"
    
    return sdstr,edstr

s,e=dateConvert()

def addDate(url):
    startdate, enddate=dateConvert()
    finalUrl=url+("?created_at_min=%s?created_at_max=%s" % (startdate, enddate))
    
    return finalUrl

def validateAcct(key, password, name):
    mainurl= "https://%s:%s@%s.myshopify.com/admin/" % (key, password, name)
    url=getUrl(mainurl,"locations")
    response=con.connect(url,"","get")
    if response[0]==True:
        return True
    else:
        return False

#url=getMainUrl("woonzh")