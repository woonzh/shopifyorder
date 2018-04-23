# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 10:37:40 2018

@author: woon.zhenhao
"""

import keyRetriever as kr
import connector as con
import json
import pandas as pd
import datetime
import masterReader as mr

url = ''
ordHist=''
newRec = ''
account=''
totOrds=0
unfulfilOrds = 0
newUnfulfilOrds = 0
newLineItems = 0
summary=''
check=True

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
    
def getAllFilteredData(shopName):
    global check, url
    mainUrl=kr.getMainUrl(shopName)
    init(shopName, mainUrl)
    check=False
    url=kr.addDate(url)
    print(url)
    success, response = con.connect(url, "", "get")
    return response
    if success:
        orders = process(json.loads(response))
        orderCount=0
        itemCount=0
        rev=0
        for i in orders:
            order=orders[i]
            price=float(order["total_price"])
            items=len(order["items"])
            orderCount+=1
            rev+=price
            itemCount+=items
        return orderCount,itemCount,rev
    else:
        return "fail"
    
def rawData(shopName):
    global url
    mainUrl=kr.getMainUrl(shopName)
    init(shopName, mainUrl)
    
    success, response = con.connect(url, "", "get")
    
    if success:
        orders = process(json.loads(response))
        return shopName, orders
    else:
        return "fail", response

def main(shopName):
    suc, response=rawData(shopName)
    if (suc == "fail"):
        return "fail", response
    else:
        orderDf = listOrderLines(response)
        name = shopName+' '+datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")+'.csv'
        writeSummary(shopName)
        return name, orderDf

def writeSummary(name):
    global summary
    
    summary='\n'+str(totOrds)+' total orders, '+str(unfulfilOrds)+' unfulfilled orders, '+str(newUnfulfilOrds)+ ' new orders, '+str(newLineItems)+ ' new line items. \n'
    print(name+summary)
    summary+='\n'+'[SO number-SKU-quantity-unit price-SO price]\n'

def writeToFile(acct, orders):
    mr.writeToTemplate(orders, acct)
    
def parseNone(word):
    if (word=="None"):
        return ""
    else:
        return ""

def listOrderLines(orders):
    df=pd.DataFrame(columns = ['SO Identifier', 'Item SKU', 'Payment Terms', 'Ship Date', 'Ship Time', 'Ship to Contact', 
                               'Ship to Company', 'Ship to Address 1', 'Ship to Address 2', 'Ship to Unit #', 
                               'Ship to Postal Code', 'Ship to Phone', 'Qty', 'Price per Item', 'Price per SO', 
                               'Remarks (Shipping) - visible to deliveryman', 'Remarks (WMS internal)', 'Country Name'])
    
    count=1
    global newLineItems
    msg=''
    
    for ind in orders:
        i = orders[ind]
        so=i["order number"]
        paymentTerms = i['financial_status']
        customer = i["customer"]
        contact = customer["first_name"]+ " " + customer["last_name"]
        address = customer["default_address"]
        print(address)
        addressLine = parseNone(address["address1"])+ " " + parseNone(address["address2"]) + " " + parseNone(address["country"]) + " " + parseNone(address["zip"])
        postal = address["zip"]
        country = address["country"]
        phone = address["phone"]
        totPrice = i["total_price"]
        
        items = i["items"]
        
        for j in items:
            sku =j['sku']
            qty =j['quantity']
            unitPrice= j['price']
            
            ls=[so, sku, paymentTerms, '', '', contact, '', addressLine, '', '', postal, phone, qty, unitPrice,totPrice, '','',country]
            msg=str(so)+' - '+str(sku)+' - '+str(qty)+' - '+str(unitPrice)+' - '+str(totPrice)
            
            df.loc[str(count)]=ls
            count+=1
            newLineItems+=1
    
    return df  

def orderOk(tem):
    global unfulfilOrds, newUnfulfilOrds, ordHist, check
    
    if (check==False):
        return True
    
    try:
#        if tem["financial_status"]=="authorized" and len(tem["fulfillments"])==0:
        if len(tem["fulfillments"])==0 and (tem["financial_status"]=="paid" or tem["financial_status"]=="authorized"):
            unfulfilOrds+=1
            newUnfulfilOrds+=1
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

#name,df=rawData('bundies-com')

#name,df=rawData("woonzh")
#df=getAllFilteredData("woonzh")
#order=getAllFilteredData("woonzh")
#df=json.loads(order)