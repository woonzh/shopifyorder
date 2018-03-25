# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 14:42:58 2017

@author: woon.zhenhao
"""

from datetime import datetime
import pandas as pd

directory = 'log files/'

fileNames={
        'product': 'product_log_',
        'orders':'orders_log_',
        'inven updates': 'inven_updates_'
        }

fileOpener={
        'product': 'Log file for product inventory updates from shopify to shopee. Account:',
        'orders': 'Log file for order creation from shopee to UrbanFox IMS. Account:'
        }

message={
        'msg':''
        }

def timeStampGenerator():
    nowstr=datetime.now().strftime("%d-%m-%y_%H-%M-%S")
    return nowstr

def clearMsg():
    message['msg']=''

def logMsg(g):
    message['msg']=message['msg']+g+'\n'

def openfile(cat, account):
    name=directory+fileNames[cat]+str(account)+'_'+timeStampGenerator()+'.txt'
    
    file=open(name,'w')
    file.write(fileOpener[cat]+str(account)+'\n')
    
    return file

def log(cat, account, summary):    
    file=openfile(cat, account)
    file.write(summary+'\n')
    file.write(message['msg'])
    file.close()
    message['msg']=''
    

def invenUpdatesCSV(df, account):
    name = directory+fileNames['inven updates']+str(account)+'_'+timeStampGenerator()+'.csv'
    df.to_csv(name, header=True, index=False)