# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 18:41:02 2020

import data from   ...https://regionuppsala.se/det-har-gor-vi/vara-verksamheter/halso-och-sjukvard/information-om-coronaviruset/#nulagesbild-covid-19-region-uppsala
 on admitted patients gen ward, ICU. Also PCR tests, done and %positive
"""
import pandas as pd

import numpy as np

import numpy.polynomial.polynomial as poly #tried to fit the curves

from matplotlib import pyplot as plt

from datetime import *


#%% import excel from regionuppsala.se

# import PCR tests

try:
    
    today = datetime.now()  #builds url for todays report and try to download it
    
    today_str = today.strftime('%Y%m%d')
    
    today_str = today_str[2:]
    
    url_str = 'https://regionuppsala.se/contentassets/bba2a35f5e6842c68b8cc39040e43714/'
    
    url = url_str + today_str + '-nulagesbild-covid-19-region-uppsala-excel.xlsx'
    
    #url = 'https://regionuppsala.se/contentassets/bba2a35f5e6842c68b8cc39040e43714/210301-nulagesbild-covid-19-region-uppsala-excel.xlsx'
    
    df_PCR = pd.read_excel (url, sheet_name='PCR per dag', header=0, usecols=[0,1,2,6])
    print ('a')
    
    df_PCR.rename( columns={'Datum':'Date', 'Antal prover':'PCR_done', 
                                 'Antal positiva prov':'PCR_positive',
                                 'Antal analys ej klar':'PCR_incomplete'}
                  , inplace=True)
    print ('aa')
    df_PCR.set_index ('Date', drop = True, inplace = True)
    print ('b')
    # import admitted
    
    df_admitted = pd.read_excel (url, sheet_name='Slutenvård per dag', header=2, usecols=[0,1,2])
    print ('c')
    
    df_admitted.rename( columns={'Datum':'Date', 'Antal patienter':'Admitted', 
                                 'Antal vårdade IVA':'ICU'}, inplace=True)                   
    
    df_admitted.set_index ('Date', drop = True, inplace = True)
    
    #save backup file in case downloading fails
    
    with pd.ExcelWriter('RegUppsala_COVID_nubild_backup.xlsx') as writer:  
        
        df_PCR.to_excel(writer, sheet_name='PCR')
        
        df_admitted.to_excel(writer, sheet_name='Admitted')

except:
    
    print ('\nFAILED downloading from regionuppsala.se\n \nLoading backup file\n')
    
    df_PCR = pd.read_excel ( 'RegUppsala_COVID_nubild_backup.xlsx', sheet_name='PCR' )
    
    df_PCR.set_index ('Date', drop = True, inplace = True)
    
    df_admitted = pd.read_excel ('RegUppsala_COVID_nubild_backup.xlsx', sheet_name='Admitted')
    
    df_admitted.set_index ('Date', drop = True, inplace = True)

#%% calculates % positive PCR....actually it is reported in recent reports.

df_PCR['PCR_positive%'] = df_PCR.PCR_positive / df_PCR.PCR_done *100

#%%fitting curve  BETA. Stackoverflow recommends interpolate (see below)

def data_to_plot (df_row):

    
    df_toplot = pd.DataFrame (df_row[(df_row.index.month> from_month) | (df_row.index.year == 2021) ] )
    
    data_name = df_toplot.columns[0]
    
      
    x=np.arange(0, len(df_toplot)  ) #These are 3 core lines to get a fitted curve
       
    coefs = poly.polyfit (x, df_toplot[data_name],  9)
    
    ffit = poly.polyval (x, coefs)
    
    ffit[0:3] = np.nan
    ffit[-1:] = np.nan
    
    df_toplot['fitted'] = ffit 
    
    return df_toplot



#%% plotting

#Stating from after which month are we interested in

from_month = 7

d_0_PCR = df_PCR.index[0]
uppdated_date_PCR = str (d_0_PCR.year) + '-' + str (d_0_PCR.month) + '-' + str (d_0_PCR.day)

d_0_admitted = df_admitted.index[0]
uppdated_date_adm = str (d_0_admitted.year) + '-' + str (d_0_admitted.month) + '-' + str (d_0_admitted.day)

#df_PCR_toplot = pd.DataFrame ( df_PCR['PCR_positive%'][df_PCR.index.month> from_month] )

df_PCR_toplot = data_to_plot (df_PCR['PCR_positive%'])

df_ward_toplot = data_to_plot (df_admitted.Admitted) 

df_ICU_toplot = data_to_plot (df_admitted.ICU)

f=plt.figure('Region Uppsala, admitted and %positive PCR',figsize=(10,10),
             facecolor=('0.9'),edgecolor='black')

# subplot admitted ward and ICU


ward = f.add_subplot(2,1,1)

ward.plot(df_ward_toplot.Admitted, c = 'b', ls =  '--', alpha = 0.2)
ward.plot(df_ward_toplot.fitted, c = 'b')

ward.set_ylabel('In general ward (blue)')

title = 'Region Uppsala. In-hospital patients in a given day. Uppdated ' + uppdated_date_adm

ward.set_title(title)

icu= ward.twinx()

icu.plot(df_ICU_toplot.ICU, c = 'r', ls = ':', alpha = 0.2)
icu.plot(df_ICU_toplot.fitted, c = 'r')

icu.set_ylabel('In ICU (red)')

#                               subplot PCR
title = 'Region Uppsala. Uppdated ' + uppdated_date_PCR

pcr = f.add_subplot(2,1,2)

pcr.plot(df_PCR_toplot['PCR_positive%'], c = 'g', alpha = 0.2 )
pcr.plot(df_PCR_toplot.fitted, c = 'g', alpha = 1)

#pcr.set_ylim(0,20)

pcr.set_ylabel( 'Positive PCR (% of all done).')

pcr.set_title(title)

plt.show()



#%% other way fitting. More correct according to literature
from scipy.interpolate import make_interp_spline, BSpline

# 300 represents number of points to make between T.min and T.max

T = np.arange(0, len(df_PCR_toplot)  )

power = df_PCR_toplot
xnew = np.linspace(T.min(), T.max(), 50) 

spl = make_interp_spline(T, power, k=1)  # type: BSpline
power_smooth = spl(xnew)

#plt.plot(xnew, power_smooth)
#plt.show()


