# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 19:30:50 2022

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
for t in groceries.find({'Member_number':3180}):
    temp.append(t)
for i in range(len(temp)):
    print(temp[i]['Item'])
for records in nutrition_values.find({'name':{'$regex':temp[i]['Item']}}):
    print(records)
    x=pd.Series(records)
    df=pd.DataFrame(x)
    break
df=df.transpose()
for col in df.columns:
    df[col]=df[col].astype('str')
x=df.loc[0].values
print(x)
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
print(test)
t=pd.Series(test,index=[ 'calories', 'total_fat(g)', 'saturated_fat (g)',
       'cholesterol', 'sodium (mg)', 'vitamin_a (IU)', 'vitamin_a_rae (mcg)', 'vitamin_b12',
       'vitamin_b6', 'vitamin_c', 'vitamin_d', 'vitamin_e', 'vitamin_k',
       'calcium', 'irom', 'potassium', 'protein', 'glucose', 'carbohydrate',
       'sugars'])
w=pd.DataFrame(t)
w=w.transpose()
print(w)
for col in w.columns:
    w[col]=w[col].astype('float')
w.plot(kind='bar',figsize=(40,20),fontsize=30)
plt.title('NUTS',fontsize=100)
plt.xlabel('nutrition',fontsize=100)
plt.ylabel('values',fontsize=100)
plt.legend(fontsize = 30)
plt.show()












