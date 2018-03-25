# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 10:37:40 2018

@author: woon.zhenhao
"""

import keyRetriever as kr
import connector as con
import masterReader as mr
import json
import pandas as pd
import datetime
import log

url = ''
ordHist=''
newRec = ''
account=''
totOrds=0
unfulfilOrds = 0
newUnfulfilOrds = 0
newLineItems = 0
summary=''

def init(acct,mainUrl):
    global totOrds, unfulfilOrds, newUnfulfilOrds, newLineItems, account, url, newRec, summary
    totOrds=0
    unfulfilOrds=0
    newUnfulfilOrds=0
    newLineItems = 0
    account=acct
    url = kr.getUrl(mainUrl, "orders")
    newRec = pd.DataFrame(columns = ['order number', 'price', 'date', 'account'])
    summary=''
    log.clearMsg()

def test():
    url=kr.testing("orders")
    success, response = con.connect(url, "", "get")
    response = json.loads(response)
    df=process(response)
    orders = listOrderLines(df)
    writeToFile("woonzh", orders)
    return response, df, orders

def main(acct, mainUrl):
    init(acct, mainUrl)
    global ordHist
    
    success, response = con.connect(url, "", "get")
    
    if success:
        found, ordHist = mr.getOrdList()
        orders = process(json.loads(response))
        orderDf = listOrderLines(orders)
        writeToFile(acct, orderDf)
        mr.writeToMaster(newRec)
        writeSummary()
        log.log("orders",account,summary)
    
    return orders

def writeSummary():
    global summary
    
    summary='\n'+str(totOrds)+' total orders, '+str(unfulfilOrds)+' unfulfilled orders, '+str(newUnfulfilOrds)+ ' new orders, '+str(newLineItems)+ ' new line items. \n'
    print(summary)
    summary+='\n'+'[SO number-SKU-quantity-unit price-SO price]\n'

def writeToFile(acct, orders):
    mr.writeToTemplate(orders, acct)

def listOrderLines(orders):
    df=pd.DataFrame(columns = ['so', 'sku', 'payment terms', 'ship date', 'ship time', 'ship contact', 'ship company', 
                               'ship add', 'ship add2', 'ship to unit', 'ship to postal', 'ship to phone', 'qty', 
                               'unit price', 'total price', 'remarks external', 'remarks internal', 'country'])
    
    count=1
    global newLineItems
    msg=''
    
    for ind in orders:
        i = orders[ind]
        so=i["order number"]
        paymentTerms = 'Paid'
        customer = i["customer"]
        contact = customer["first_name"]+ " " + customer["last_name"]
        address = customer["default_address"]
        addressLine = address["address1"]+ " " + address["address2"] + " " + address["country"] + " " + address["zip"]
        postal = address["zip"]
        country = address["country"]
        phone = customer["phone"]
        totPrice = i["total_price"]
        
        items = i["items"]
        
        for j in items:
            sku =j['sku']
            qty =j['quantity']
            unitPrice= j['price']
            
            ls=[so, sku, paymentTerms, '', '', contact, '', addressLine, '', '', postal, phone, qty, unitPrice,totPrice, '','',country]
            msg=str(so)+' - '+str(sku)+' - '+str(qty)+' - '+str(unitPrice)+' - '+str(totPrice)
            log.logMsg(msg)
            
            df.loc[str(count)]=ls
            count+=1
            newLineItems+=1
    
    return df  

def orderOk(tem):
    global unfulfilOrds, newUnfulfilOrds, ordHist
    
    try:
        if tem["financial_status"]=="authorized" and len(tem["fulfillments"])==0:
            unfulfilOrds+=1
            newUnfulfilOrds+=1
            ordNum = tem["order number"]
            for i in ordHist:
#                print(i)
                if str(ordNum) == str(i):
                    newUnfulfilOrds-=1
                    return False
            timenow=datetime.datetime.now()
            ls=[tem["order number"], tem["total_price"], timenow.strftime('%d-%m-%Y %H:%m'), account]
            newRec.loc[str(len(newRec)+1)]=ls
            return True
        else:
            return False
    except ValueError:
        return False
    
def process(response):
    global totOrds
    df = {}
    orders = response['orders']
    count = 1
    for i in orders:
        tem ={
            "billing address": i["billing_address"],
            "creation date": i["created_at"],
            "updated date": i["updated_at"],
            "customer": i["customer"],
            "items": i["line_items"],
            "order number": i["order_number"],
            "subtotal price": i["subtotal_price"],
            "total_price": i["total_price"],
            "total_weight": i["total_weight"],
            "financial_status":i["financial_status"],
            "fulfillments": i["fulfillments"]
                }
        totOrds+=1
        
        if orderOk(tem):  
            df[str(count)]=tem
            count +=1
            
    return df
       
#found, ordHist = mr.getOrdList() 
#response, df, orders=test()