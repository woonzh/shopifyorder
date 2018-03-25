# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 17:34:54 2018

@author: woon.zhenhao
"""
from flask import Flask, request
from flask_restful import Resource, Api
from urllib import parse
import psycopg2 as ps
import os

app = Flask(__name__)
api = Api(app)

class Accounts(Resource):    
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
    
    def get(self):
        url="postgres://lpwrkshmpfsrds:f6d80a024a0defe3141d7bdb31279891768d47421020320c32c7ea26f9909255@ec2-23-21-217-27.compute-1.amazonaws.com:5432/d246lgdkkjq0sr"
        query="SELECT * FROM keys"
        lst=[]
        try:
            cur, conn=Accounts.connectToDatabase(url)
            
            cur.execute(query)
            for result in cur:
                name=result[1]
                lst.append(name)
                
            cur.close()
        except ps.Error as e:
            msg=e.pgerror
            lst.append(msg)
        
        return lst

api.add_resource(Accounts, '/accounts')

if __name__ == '__main__':
     app.run(debug=True)
    