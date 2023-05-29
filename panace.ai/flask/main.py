
# from http import client
from flask import Flask , redirect , url_for,render_template,request
from matplotlib import colors
from pymongo import MongoClient
import pymongo
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
client=MongoClient('mongodb://127.0.0.1:27017/')
mydb=client['nurition']
nutrition_values=mydb['nutrition_values']
mydb1=client['groceries']
groceries=mydb1['groceries_list']
mydb2=client['login']
ldetails=mydb2.login_deatils
app=Flask(__name__)
@app.route('/',methods=['POST','GET'])
def index():
    return render_template('signin.html')
@app.route('/dash')
def guest():
    return render_template('index.html')
@app.route('/home')
def main():
    return render_template('home.html')
@app.route('/sucess',methods=['POST','GET'])
def sucess():
    if request.method=='POST':
        id=request.form['search']
        id=int(id)
        temp=[]
        for t in groceries.find({'Member_number':id}):
            temp.append(t)
        for i in range(len(temp)):
            for records in nutrition_values.find({'name':{'$regex':temp[i]['Item']}}):
                   x=pd.Series(records)
                   df=pd.DataFrame(x)
                   break
            df=df.transpose()
            for col in df.columns:
                 df[col]=df[col].astype('str')
            x=df.loc[0].values
            test=[]
            for k in range(3,len(x)):
                strr=''
                for j in x[k]:
                    if(j.isdigit()):
                        strr=strr+j
                    elif(j==' ' or j.isalpha()):
                        continue
                    else:
                       strr=strr+j
                test.append(strr)
            t=pd.Series(test,index=[ 'calories', 'total_fat(g)', 'saturated_fat (g)',
           'cholesterol', 'sodium (mg)', 'vitamin_a (IU)', 'vitamin_a_rae (mcg)', 'vitamin_b12 (mcg)',
           'vitamin_b6 (mg)', 'vitamin_c (mg)', 'vitamin_d (IU)', 'vitamin_e (mg)', 'vitamin_k (mcg)',
           'calcium (mg)', 'iron (mg)', 'potassium (mg)', 'protein (g)', 'glucose (g)', 
           'carbohydrate (g)',
           'sugars (g)'])
            w=pd.DataFrame(t)
            if(i==0):
                dft=pd.DataFrame(w)
            else:
                dft=pd.concat([dft,w],axis=1)
    dft=dft.transpose()
    for x in dft.columns:
        dft[x]=dft[x].astype(float)
    lat=[]
    for x in dft.columns:
      lat.append(round(dft[x].sum(),3))
    cc=pd.Series(lat)
    cc=pd.DataFrame(cc)
    cc.index=dft.columns
    cc=cc.transpose()
    dd=cc.to_dict(orient='records')
    name=temp[0]['Item']
    labels=list(dft.columns)
    v=list(dd[0].values())
    v[4]=v[4]/1000
    


    return render_template('daigram.html',v=v,labels=labels)
@app.route('/nutrition',methods=['POST','GET'])
def nutrion():
        item=request.form['search']
        temp=[]
        for i in nutrition_values.find({'name':{'$regex':item}}):
            temp.append(i)
            break
        temp=list(temp[0].values())
        return render_template('login.html',x=temp,item=item)

@app.route('/login',methods=['POST','GET'])
def dash():
    return render_template('Login.js')
@app.route('/suc',methods=['POST','GET'])
def home():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        pas=ldetails.find({'email':email})
        pass_word=pas[0]['password']
        if(pass_word==password):
            msg='sucess'
            return render_template('login.html',email=email,password=password,msg=msg)
        else:
            return('wrong password')
if __name__ == '__main__':
    app.run(debug=True)




