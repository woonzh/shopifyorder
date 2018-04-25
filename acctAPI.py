# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 17:34:54 2018

@author: woon.zhenhao
"""
import flask
from flask import Flask, request, make_response, render_template
from flask_cors import CORS
from flask_restful import Resource, Api
from urllib import parse
import psycopg2 as ps
import os
import json
import orderRetreiver as orr
import keyRetriever as kr

app = Flask(__name__)
api = Api(app)
CORS(app)

@app.route('/')
def hello():
    return render_template('test.html')

class Common():
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

class Accounts(Resource):        
    def get(self):
        url="postgres://lpwrkshmpfsrds:f6d80a024a0defe3141d7bdb31279891768d47421020320c32c7ea26f9909255@ec2-23-21-217-27.compute-1.amazonaws.com:5432/d246lgdkkjq0sr"
        query="SELECT * FROM keys"
        lst=[]
        try:
            cur, conn=Common.connectToDatabase(url)
            
            cur.execute(query)
            for result in cur:
                name=result[1]
                lst.append(name)
                
            result={
                    "names":lst
                    }
            
            print(result)
            
            cur.close()
            conn.commit()
            resp = flask.Response(json.dumps(result))
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        except ps.Error as e:
            msg=e.pgerror
            return msg
        
class AccountDetails(Resource):    
    def get(self):
        url="postgres://lpwrkshmpfsrds:f6d80a024a0defe3141d7bdb31279891768d47421020320c32c7ea26f9909255@ec2-23-21-217-27.compute-1.amazonaws.com:5432/d246lgdkkjq0sr"
        query="SELECT * FROM keys"
        defaultList=["email","shopname","apikey","pass","sharedsecret"]
        lst={}
        count=1
        try:
            cur, conn=Common.connectToDatabase(url)
            
            cur.execute(query)
            for result in cur:
                indiv={}
                for (det, head) in zip(result, defaultList):
                    indiv[head]=det
                
                lst[count]=indiv
                count+=1
            
            print(result)
            cur.close()
            conn.commit()
            resp = flask.Response(json.dumps(lst))
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        except ps.Error as e:
            msg=e.pgerror
            return msg
        
class DeleteAccount(Resource): 
    def get(self):
        name = request.args.get("name" ,type = str)

        result={}
        url="postgres://lpwrkshmpfsrds:f6d80a024a0defe3141d7bdb31279891768d47421020320c32c7ea26f9909255@ec2-23-21-217-27.compute-1.amazonaws.com:5432/d246lgdkkjq0sr"
        query="DELETE FROM keys WHERE shopname = '" +name+"'"
        
        print(query)
        try:
            cur, conn=Common.connectToDatabase(url)
            cur.execute(query)
            cur.close()
            conn.commit()
            
            result['result']="Success"
        except ps.Error as e:
            result['result']=str(e)
        
        print(result)
        resp = flask.Response(json.dumps(result))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    
class EditAccount(Resource):   
    def get(self):
        lst=[]
        result={}
        lst.append(request.args.get("name" ,type = str))
        lst.append(request.args.get("email" ,type = str))
        lst.append(request.args.get("apikey" ,type = str))
        lst.append(request.args.get("password" ,type = str))
        lst.append(request.args.get("sharedsecret" ,type = str))
        print("Edit account params received: name=%s, email=%s, apikey=%s, password=%s, sharedsecret=%s" % (lst[0],lst[1],lst[2],lst[3],lst[4]))
        
        acctValid=kr.validateAcct(lst[2],lst[3],lst[0])
        
        if acctValid:
            url="postgres://lpwrkshmpfsrds:f6d80a024a0defe3141d7bdb31279891768d47421020320c32c7ea26f9909255@ec2-23-21-217-27.compute-1.amazonaws.com:5432/d246lgdkkjq0sr"
            query="UPDATE keys SET shopname='%s', email='%s', apikey='%s', pass='%s', sharedsecret='%s' WHERE shopname='%s'" % (lst[0],lst[1],lst[2],lst[3],lst[4],lst[0])
            print(query)
            try:
                cur, conn=Common.connectToDatabase(url)
                cur.execute(query)
                cur.close()
                conn.commit()
                
                result['result']="Success"
            except ps.Error as e:
                result['result']=str(e)
            
        else:
            result['result']="Account credential invalid"
            
        print(result)
        resp = flask.Response(json.dumps(result))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

class CreateAccount(Resource):
    def get(self):
        lst=[]
        result={}
        lst.append(request.args.get("name" ,type = str))
        lst.append(request.args.get("email" ,type = str))
        lst.append(request.args.get("apikey" ,type = str))
        lst.append(request.args.get("password" ,type = str))
        lst.append(request.args.get("sharedsecret" ,type = str))
        print("Create Account params received: name=%s, email=%s, apikey=%s, password=%s, sharedsecret=%s" % (lst[0],lst[1],lst[2],lst[3],lst[4]))
        
        acctValid=kr.validateAcct(lst[2],lst[3],lst[0])
        
        if acctValid:
            lstLen=len(lst)
            track=1
            url="postgres://lpwrkshmpfsrds:f6d80a024a0defe3141d7bdb31279891768d47421020320c32c7ea26f9909255@ec2-23-21-217-27.compute-1.amazonaws.com:5432/d246lgdkkjq0sr"
            query="INSERT INTO keys (shopname, email, apikey, pass, sharedsecret) VALUES ("
            for param in lst:
                query = query + "'"+param+"'"
                if track<lstLen:
                    query+=","
                track+=1
            query +=")"
            print(query)
            try:
                cur, conn=Common.connectToDatabase(url)
                cur.execute(query)
                cur.close()
                conn.commit()
                
                result['result']="Success"
            except ps.Error as e:
                result['result']=str(e)
            
        else:
            result['result']="Account credential invalid"
            
        print(result)
        resp = flask.Response(json.dumps(result))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
        
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
    
class OrderData(Resource):    
    def get(self):
        t=Accounts
        acct=t.get('')
        resp=json.loads((acct.response)[0])
        names=resp["names"]
        result={}
        
        for name in names:
            
            ordCount, itemCount, rev=orr.getAllFilteredData(name)
            result[name]={
                    "ordCount":ordCount,
                    "itemCount":itemCount,
                    "rev":rev
                    }
            
        return result

api.add_resource(Accounts, '/accounts')
api.add_resource(Orders, '/orders')
api.add_resource(CreateAccount, "/createAccount")
api.add_resource(AccountDetails, "/accountDetails")
api.add_resource(DeleteAccount, "/deleteAccount")
api.add_resource(EditAccount, "/editaccount")
api.add_resource(OrderData, "/orderdata")

if __name__ == '__main__':
     app.run(debug=True)