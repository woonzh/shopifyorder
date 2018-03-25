# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 10:38:55 2018

@author: woon.zhenhao
"""

import keyRetriever as kr
import orderRetreiver as ordRet

purpose = ["Retrieve orders", "Update Inventory (Not working)", "Retrieve order and update Inventory (Not working)", "end"]
check=0

def init():
    acct, shop_url=kr.getMainUrl()
    
    count = 1
    cont = True
    
    while cont: 
        print("Choose the purpose:")
        for i in purpose:
            print(str(count)+") "+i)
            count +=1
            
        choice = input ("Purpose index: ")
        check=choice
        
        try:
            choice = int(choice)
            if (choice > 0) and (choice <count):
                if (choice==1):
                    ordRet.main(acct, shop_url)
                if (choice==2):
                    t=1
                if (choice==3):
                    t=1
                    
                cont=False
            else:
                print("Please choose a value between 1 and " +str(count-1))
        except ValueError:
            print("Please choose a value between 1 and " +str(count-1))

while True:       
    init()