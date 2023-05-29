# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 22:30:35 2022

@author: yelar
"""

import pymongo
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
client=pymongo.MongoClient('mongodb://127.0.0.1:27017/')
mydb=client['nurition']
mydb1=client['groceries']
groceries=mydb1['groceries_list']
nutrition_values=mydb['nutrition_values']
temp=[]
for t in groceries.find({'Member_number':2000}):
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
    lat.append(dft[x].sum())
print(lat)
cc=pd.Series(lat)
cc=pd.DataFrame(cc)
cc.index=dft.columns
cc=cc.transpose()
cc.plot(kind='bar',figsize=(40,30),fontsize=30)
plt.title('nutrition intake',fontsize=100)
plt.xlabel('nutrition',fontsize=100)
plt.ylabel('values',fontsize=100)
plt.legend(fontsize = 30)
plt.show()

        
    

        