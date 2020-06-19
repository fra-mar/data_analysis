#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Analysis from Folkhalsomyndigheten Covid 19 daily Excel file
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime
import scipy.stats

import warnings
warnings.filterwarnings("ignore")

#%%
import requests

url_fhm='https://www.arcgis.com/sharing/rest/content/items/b5e7488e117749c19881cce45db13f7e/data'
url_google='https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv?cachebust=3ec772aac6061acf'
url_apple='https://covid19-static.cdn-apple.com/covid19-mobility-data/2010HotfixDev21/v3/en-us/applemobilitytrends-2020-06-17.csv'

r_fhm=requests.get(url_fhm, allow_redirects=True)
r_google=requests.get(url_google, allow_redirects=True)
r_apple=requests.get(url_apple, allow_redirects=True)

open('data_fhm.xls','wb').write(r_fhm.content) 
open('data_google.csv','wb').write(r_google.content)  
open('data_apple.csv','wb').write(r_apple.content)  
# In[2]:


#Gather data from FolkHälsoMyndigheten
AntalDagRegionComplete=pd.read_excel(r'data_fhm.xls',
                            sheet_name='Antal per dag region')
AntalDagRegion=AntalDagRegionComplete.loc[11:,]

AntalDagRegion.reset_index(inplace=True,drop=True)
AntalDagRegion.rename(columns={'Totalt_antal_fall':'Sverige'},inplace=True)

#AntalDagRegion.info(verbose=True)
Region=input('Which region? (write "Sverige" for the whole country)')
reggoogle=Region


#Region="Uppsala"
select=AntalDagRegion[[Region]]
select.rename(columns={Region:"cases"},inplace=True)
select['dupnum']=0
select['accum']=0

#Calculates accumulated cases and doubling number
for i in range (1,len(select)):
    select['accum'].loc[i]=select.accum.loc[i-1]+select.cases.loc[i-1]
for i in range (0,len(select)-1):
    select['dupnum'].loc[i]=np.log(2)/np.log(select.accum.loc[i+1]/select.accum.loc[i])
    
#dupnum has a problem: it´s calculated on the accum number which is alway growing: so dupnum can´t be negative. Maybe that´s
# why R0 is more informative.


upperlimcases=select.cases.max()

AntalDagRegion['date']=AntalDagRegion['Statistikdatum']



#%% Test gather data from google
google_raw=pd.read_csv(r'data_google.csv',encoding='latin1')

google_mobility=google_raw.loc[(google_raw.country_region_code=='SE')].reset_index()

google_selected=google_mobility[['sub_region_1','date','retail_and_recreation_percent_change_from_baseline',
                                 'transit_stations_percent_change_from_baseline','parks_percent_change_from_baseline']]

google_selected.rename(columns={'sub_region_1':'regionOrig','date':'date',
                                'retail_and_recreation_percent_change_from_baseline':'retail_recreation'
                                ,'transit_stations_percent_change_from_baseline':'transit',
                                'parks_percent_change_from_baseline':'parks'},inplace=True)

google_selected['regionOrig'].fillna('Sverige', inplace=True)

def splitar(palabro):             #simplify regions names
    backup=palabro.split()
    return backup[0]

google_selected['regionOrig']=google_selected.regionOrig.apply(splitar)
google_selected.date=google_selected.date.apply(lambda x: datetime.strptime(x,'%Y-%m-%d'))

toplot=google_selected[(google_selected.regionOrig==reggoogle)]
toplot.reset_index(inplace=True,drop=True)



# In[4]:


#Gather data form apple, in https://www.apple.com/covid19/mobility SAVE as .csv!!! and not .xls
apple_mobility=pd.read_csv(r'data_apple.csv',encoding='latin1')

apple_land=apple_mobility[(apple_mobility.region=='Sweden')]
apple_land.reset_index(inplace=True,drop=True)
transposed_apple=apple_land.T.reset_index()

transposed_apple.drop(transposed_apple.index[[0,1,2,3,4,5]],axis=0,inplace=True)

transposed_apple.rename(columns={'index':'date',0:'driving',
                                1:'transit'
                                ,2:'walking'},inplace=True)
transposed_apple.date=transposed_apple.date.apply(lambda x: datetime.strptime(x,'%Y-%m-%d'))



transposed_apple.drop(transposed_apple.date.index
                      [(transposed_apple.date<'2020-02-15')],axis=0,inplace=True)

transposed_apple.reset_index(inplace=True,drop =True)

correction=transposed_apple.transit[0]


print (transposed_apple.head(40))


# In[5]:


#Draw the plots


#Daily cases
plt.figure(figsize=(10,5)) 
plt.grid(alpha=0.2)
foax=plt.subplot()


#plt.subplot (2,1,1)
#plt.plot(AntalDagRegion[Region],linestyle="",marker='^')
plt.bar(range(len(AntalDagRegion[Region])),AntalDagRegion[Region])
#plt.axis([10,90,0,(upperlimcases)*1.2])


#Functions for plotting x axis (time to string) in all graphs
xticks=lambda x: range(0,len(x),5)
def xticklabels(serie):
    lista_xticks=list(serie.apply(lambda x: datetime.strftime(x, '%d/%m')))
    lista_xticklabels=[lista_xticks[i] for i in range(0,len(serie),5)]
    return lista_xticklabels




foax.set_xticks(xticks(AntalDagRegion[Region]))
foax.set_xticklabels(xticklabels(AntalDagRegion.Statistikdatum),rotation=30)
title_foax="Day cases in ",Region
plt.title(title_foax)

#Finds x value that has date 30/04 to place a vertical line.
def find_x(serieX):
    xt=serieX.apply(lambda x: datetime.strftime(x, '%d/%m'))
    x=list(xt).index('30/04')
    return x

#plt.axvline(find_x(AntalDagRegion['Statistikdatum']),color='y')
# 
plt.show()

#Google
plt.figure(figsize=(10,5)) 
goax=plt.subplot()
plt.grid(alpha=0.2,ls='--')
plt.plot(toplot.transit,color="blue",label="Transit stations")
plt.plot(toplot.retail_recreation,color="orange",label="Retail and recreation")
plt.plot(toplot.parks,color="green",label="Parks")
goax.set_xticks(xticks(toplot.date))
goax.set_xticklabels(xticklabels(toplot.date),rotation=30)
#plt.axvline(find_x(toplot.date),color='y')

plt.legend(loc=2)
#plt.axis([10,90,-60,90])

title='Google: Mobility variation in', reggoogle
plt.title(title)
plt.show()

#Apple. Only data for land
if Region=="Sverige":
    plt.figure(figsize=(10,5)) 
    apax=plt.subplot()
    plt.grid(alpha=0.2,ls='--')
    plt.plot(transposed_apple.transit-correction,color="blue",label="Transit")
    plt.plot(transposed_apple.walking-correction,color="yellow",label="Walking")
    plt.plot(transposed_apple.driving-correction,color="gray",label="Driving")
    #plt.axvline(find_x(transposed_apple.date),color='y')
    plt.legend(loc=2)
    #plt.axis([10,90,-60,90])
    title='Apple: Mobility variation variation in Sweden'
    apax.set_xticks(xticks(transposed_apple.date))
    apax.set_xticklabels(xticklabels(transposed_apple.date),rotation=30)
    plt.title(title)
    plt.show() 

#Doubling number
plt.figure(figsize=(10,5)) 
doax=plt.subplot()
plt.plot(select.dupnum,linestyle="",marker="*")
plt.axis([10,90,0,55])
title='Duplication number in ', reggoogle
doax.set_xticks(xticks(AntalDagRegion[Region]))
doax.set_xticklabels(xticklabels(AntalDagRegion.Statistikdatum),rotation=30)
plt.title(title)
plt.show()



# In[ ]:




