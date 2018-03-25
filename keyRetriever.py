# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 10:12:00 2018

@author: woon.zhenhao
"""

import pandas as pd

link = 'keys/keys.csv'

urlExten={
        "inventory": "products.json",
        "orders": "orders.json"
        }

shop_url=''

def queryAcct():
    df = pd.read_csv(link)
    
    accList = df['shop name']
    count = 1
    
    cont = True
    df2={}
    
    while cont:
        print("Choose the shopify account")
        for i in list(accList):
            print(str(count)+") "+str(i))
            count+=1
        
        choice = input("Account index: ")
        
        try:
            choice = int(choice)
            if (choice > 0) and (choice<count):
                cont = False
                df2={}
                for j in list(df):
                    df2[j]=df[j][choice-1]
            else:
                print("Please choose a number between 0 and " + str(count-1))
        except ValueError:
            print("Please choose a number between 1 and " + str(count-1))

    return accList[choice-1],df2

def getMainUrl():
    acct, keys = queryAcct()
    shop_url = "https://%s:%s@%s.myshopify.com/admin/" % (keys['API Key'], keys['Password'], keys['shop name'])
    
    return acct, shop_url

def getUrl(url, name):
    
    final_url = url+urlExten[name]
    
    return final_url

def testing(name):
    df = pd.read_csv(link)
    
    shop_url = "https://%s:%s@%s.myshopify.com/admin/" % (df['API Key'][0], df['Password'][0], df['shop name'][0])
    
    final_url = shop_url + urlExten[name]
    
    return final_url

