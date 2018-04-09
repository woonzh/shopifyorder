# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 17:34:54 2018

@author: woon.zhenhao
"""
import flask
from flask import Flask, request, make_response
from flask_cors import CORS
from flask_restful import Resource, Api
from urllib import parse
import psycopg2 as ps
import os
import json
import orderRetreiver as orr

app = Flask(__name__)
api = Api(app)
CORS(app)

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
                
            result={
                    "names":lst
                    }
            
            cur.close()
            conn.commit()
            resp = flask.Response(json.dumps(result))
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        except ps.Error as e:
            msg=e.pgerror
            return msg

class CreateAccount(Resource):
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
    
    def post(self):
        lst=[]
        lst.append(request.args.get("name" ,type = str))
        lst.append(request.args.get("email" ,type = str))
        lst.append(request.args.get("apikey" ,type = str))
        lst.append(request.args.get("password" ,type = str))
        lst.append(request.args.get("sharedsecret" ,type = str))
        url="postgres://lpwrkshmpfsrds:f6d80a024a0defe3141d7bdb31279891768d47421020320c32c7ea26f9909255@ec2-23-21-217-27.compute-1.amazonaws.com:5432/d246lgdkkjq0sr"
        query="INSERT INTO keys (shopname, email, apikey, pass, sharedsecret) VALUES ("
        for param in lst:
            query = query + "'"+param+"'"
        query+=")"
            
        try:
            cur, conn=Accounts.connectToDatabase(url)
            cur.execute(query)
            return query
        except ps.Error as e:
            return e.pgerror
        
class Orders(Resource):    
    def get(self):
        name = request.args.get("name" ,type = str)
        print(name)
        name, df=orr.main(name)
        resp = make_response(df.to_csv(header=True, index=False))
        resp.headers["Content-Disposition"] = "attachment; filename="+name
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers["Content-Type"] = "text/csv"
        return resp

api.add_resource(Accounts, '/accounts')
api.add_resource(Orders, '/orders')
api.add_resource(CreateAccount, "/createAccount")

if __name__ == '__main__':
     app.run(debug=True)