# -*- coding: utf-8 -*-


pwd

import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt


# THE RFM SCORE MODEL

moddata = pd.read_excel("CycleCustomerDataset.xlsx")

moddata.info()

moddata.head()

#now model building
#First do RFM scores
#then do clustering process

#the total amt earned by company= listedprice-standardcost
moddata['Price'] = moddata['list_price']-moddata['standard_cost']

#recency = latestdate- lastinvoice data, Frequency= no of transactions, 
#monetary = sum of tot amt of each customer

moddata.sort_values(by=['transaction_date'], inplace=True,ascending= False)
moddata.head()
#so the last transaction happendedin 30 12 2017

#setting up the latest date to a variable last is 30 and setting as 31 
Latest_date = dt.datetime(2017,12,31)

#create rfm score for each customer using single line of code
rfmscr = moddata.groupby('customer_id').agg({'transaction_date': lambda 
                                              x: (Latest_date - x.max()).days, 'transaction_id': 
                                              lambda x: len(x), 'Price': lambda x: x.sum()})

#convert trans date into int to do math easily
rfmscr['transaction_date'] = rfmscr['transaction_date'].astype(int)

#rename col to recenancy, freq, monetry
rfmscr.rename(columns={'transaction_date': 'recency', 
                         'transaction_id': 'frequency',
                         'Price': 'monetary'}, inplace= True)
rfmscr.reset_index().head()

#descriptive stat on recency
rfmscr.recency.describe()

#recency distribtion plot
m = rfmscr['recency']
sn.distplot(m)

#recency is left skewed...

#descriptive on freq
rfmscr.frequency.describe()

#plot on freq
n = rfmscr['frequency']
sn.distplot(n)

#descriptive for monetory
rfmscr.monetary.describe()

#plot monetary
o = rfmscr['monetary']
sn.distplot(o)

#spliting as quantile(as 4)
quant = rfmscr.quantile(q=[0.25,0.5,0.75])
quant = quant.to_dict()#convert to dictionary
quant
#quantile can be reframed as per the business requirements

#functions for r f m segments
def rscore(x,p,d):
  if x <= d[p][0.25]:
    return 1              #Assign 1 to lower recency since lower rec more value
  elif x <= d[p][0.5]:
    return 2
  elif x <= d[p][0.75]:
    return 3
  else:
    return 4

def f_and_mscore(x,p,d):
  if x <= d[p][0.25]:
    return 4            #Assign 4 to lower fandm since lowere f&m gives more value
  elif x <= d[p][0.5]:
    return 3
  elif x <= d[p][0.75]:
    return 2
  else:
    return 1

#Giving rfm scr to the columns
rfmscr['R'] = rfmscr['recency'].apply(rscore, args= ('recency', quant,))
rfmscr['F'] = rfmscr['frequency'].apply(f_and_mscore, args= ('frequency', quant,))
rfmscr['M'] = rfmscr['monetary'].apply(f_and_mscore, args= ('monetary', quant,))
rfmscr.head()

#calculate rfm grp and rfm scroe
#rfm grop and it will be usefull on later
rfmscr['rfmgrp'] = rfmscr.R.map(str) + rfmscr.F.map(str) + rfmscr.M.map(str)

#rfm scrores
rfmscr['rfmscore'] = rfmscr[['R','F','M']].sum(axis = 1)
rfmscr.head()

#Assign loyality
loyal_level = ['Diamond','Plattinum','Gold', 'Silver']
scr_cuts = pd.qcut(rfmscr.rfmscore, q =4, labels=loyal_level)#q for no of loyal levels
rfmscr['Loyality_of_Customer'] = scr_cuts.values
rfmscr.reset_index().head()

#taking only diamond customers(the high part of diamond since more diamond cus are still in queue)
rfmscr[rfmscr['rfmgrp']=='111'].sort_values('monetary', ascending= False).reset_index()

#therefore there are 166 topdiamond customers to give concern(still more diamond and platinum and gold customers still in queue)
#So we can give more cross product suggestions
#giving elite customer experience and same day shipping
#rfm values with 444 are meant to be churned customers we can give some offers to trigger to them buy

