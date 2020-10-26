# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 18:41:02 2020

import data from   ...https://regionuppsala.se/det-har-gor-vi/vara-verksamheter/halso-och-sjukvard/information-om-coronaviruset/#nulagesbild-covid-19-region-uppsala
 on admitted patients gen ward, ICU. Also PCR tests, done and %positive
"""
import pandas as pd

import numpy.polynomial.polynomial as poly

import numpy as np

from matplotlib import pyplot as plt

#%% import excel from regionuppsala.se

# import PCR tests

url = 'https://regionuppsala.se/contentassets/bba2a35f5e6842c68b8cc39040e43714/201022-nulagesbild-covid-19-region-uppsala-excel.xlsx'

df_PCR = pd.read_excel (url, sheet_name='PCR per dag', header=2, usecols=[0,1,2,6])

df_PCR.rename( columns={'Datum':'Date', 'Antal prover':'PCR_done', 
                             'Antal positiva prov':'PCR_positive',
                             'Antal analys ej klar':'PCR_incomplete'}
              , inplace=True)

df_PCR.set_index ('Date', drop = True, inplace = True)

# import admitted

df_admitted = pd.read_excel (url, sheet_name='Slutenvård per dag', header=2, usecols=[0,1,2])

df_admitted.rename( columns={'Datum':'Date', 'Antal patienter':'Admitted', 
                             'Antal vårdade IVA':'ICU'}, inplace=True)                   

df_admitted.set_index ('Date', drop = True, inplace = True)

#%% calculates % positive PCR

df_PCR['PCR_positive%'] = df_PCR.PCR_positive / df_PCR.PCR_done

#%% plotting

f=plt.figure('Region Uppsala, admitted and %positive PCR',figsize=(10,10),facecolor=('0.9'),edgecolor='black')

#                               subplot admitted ward and ICU

ward = f.add_subplot(2,1,1)

ward.plot(df_admitted.Admitted[df_admitted.index.month>7])

ward.set_ylabel('In general ward')

ward.set_title('Region Uppsala. In-hospital patients in a given day')

icu= ward.twinx()

icu.plot(df_admitted.ICU[df_admitted.index.month>7], c = 'r')

icu.set_ylabel('In ICU')

#                               subplot PCR
pcr = f.add_subplot(2,1,2)

pcr.plot(df_PCR['PCR_positive%'][df_PCR.index.month>7] )

pcr.set_ylim(0,0.1)

pcr.set_title('% positive PCR of those done')


plt.show()
