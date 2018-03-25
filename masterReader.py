# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 15:57:31 2017

@author: woon.zhenhao
"""

from datetime import datetime
import pandas as pd

ordUpload='SV upload '
    
def writeToTemplate(df, account):    
    header =['SO Identifier', 'Item SKU', 'Payment Terms', 'Ship Date', 'Ship Time', 'Ship to Contact', 'Ship to Company', 'Ship to Address 1', 'Ship to Address 2', 'Ship to Unit #', 'Ship to Postal Code', 'Ship to Phone', 'Qty', 'Price per Item', 'Price per SO', 'Remarks (Shipping) - visible to deliveryman', 'Remarks (WMS internal)', 'Country Name']
    
    df.columns = header
        
    name = ordUpload+account+' '+datetime.now().strftime("%d-%m-%y_%H-%M-%S")+'.csv'
    df.to_csv(name, header=True, index=False)
        