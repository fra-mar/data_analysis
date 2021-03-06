# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 16:25:14 2021

@author: maf011
"""


#Exploring data from neuroanestesi-SAS

#%% importing modules

import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'

import numpy as np

from scipy import stats

from matplotlib import pyplot as plt

#%% import file

df = pd.read_excel(r'C:/Users/maf011/Desktop/git/data_analysis_practice/neuroan_sas/jmf_timmar_210219.xlsx')

df.rename( columns={'Vecka()':'vecka', 'Patienttid (tim)':'pat_tid', 
                                 'Patienttid start (År)':'year',
                                 'Operationskategori':'elek_akut', 
                                 'Operationstid (tim)' : 'op_tid'}
                  , inplace=True)

df['procent_optid'] = df.op_tid / df.pat_tid

df['arstid'] = ""




f = lambda a: a.year

for i in range (0, len(df)):   
    
    df.year[i] = f( df.year[i] )  #write year instead of longer timestamp
    
    if df.vecka[i] >1 and df.vecka[i] < 23:   #create column with seasons
    
        df['arstid'][i]  = "v"
        
    if df.vecka[i] >22 and df.vecka[i] < 33:
        df['arstid'][i] = 's'
        
        
    if df.vecka[i] >32 and df.vecka[i] < 52:
        
        df['arstid'][i] = 'h'
    if df.vecka[i] >51 or df.vecka[i] <2 :
        
        df['arstid'][i] = 'j'

#%% Analysis example

c = df.pat_tid[ (df.year == 2019) & (df.elek_akut == 'Elektiv') ].describe()

#or

d = np.median ( df.pat_tid[ (df.year==2019) & (df.elek_akut == 'Elektiv')] )

# You can build NESTED LOOPS to go through years and elek/akut and build arrays or series
# or you can use groupby.

"""
# good df summoning whole year or season (hours / week)
#think of this as a final result, a repport itself, not a tool to, eg, build an
#image with
"""
by_year = df.groupby (['year' , 'elek_akut' ]).median()

by_year.drop( labels = ['vecka'] , axis = 1, inplace = True )

by_season = df.groupby (['year', 'arstid', 'elek_akut'  ] ). median()

by_season.drop (['vecka'] , axis = 1, inplace = True)


# next, by season

#%% Is normally distributed?  From scipy import stats, then you use stats.normaltest(obj)
#you have a note in evernote whith links to scipy documentation and other with which test to use

#example

stats.normaltest (df.op_tid[ df.year == 2019]  )

"""result statistic which is combination of skewness and kurtosis and pvalue 0.14
    so you can´t reject null hypothesis = it is not normally distributed
    """

# is there a statistical difference between spring 2019 and 2020 (when covid came) ?

#from scipy.stats import ranksums  #at the top you imported the whole stats so 
    #you really don´t need import ranksums

sample1 = np.array (df.pat_tid[ (df.year == 2019) & (df.arstid == 'v') &
                               (df.elek_akut == 'Elektiv') ] )

sample2 = np.array (df.pat_tid[ (df.year == 2020) & (df.arstid == 'v') 
                               & (df.elek_akut == 'Elektiv') ] )

s , pvalue = stats.ranksums (sample1, sample2)

print ('sample 1 vs sample 2 with ranksums have a p...{p:1.4f}\n'.format (p= pvalue) )

print ('statistic is ...{:2.4f}\n'.format (s) )

#%% Box and plots
  

data_v = df.pat_tid[ (df.arstid == 'v') & (df.year == 2019) & (df.elek_akut == 'Elektiv') ]
data_j = df.pat_tid[ (df.arstid == 'j') & (df.year == 2019) & (df.elek_akut == 'Elektiv') ]
data_s = df.pat_tid[ (df.arstid == 's') & (df.year == 2019) & (df.elek_akut == 'Elektiv') ] 
data_h = df.pat_tid[ (df.arstid == 'h') & (df.year == 2019) & (df.elek_akut == 'Elektiv') ] 
data = [data_j, data_v, data_s, data_h] 

fig = plt.figure(figsize =(10, 7)) 

# Creating axes instance 
ax = fig.add_axes([0, 0, 1, 1])   #difference between subplot and add_axes well explained in
## https://stackoverflow.com/questions/43326680/what-are-the-differences-between-add-axes-and-add-subplot

# Creating plot 
bp = ax.boxplot(data) 

ax.set_xticklabels ([ 'Jul', 'Vår' , 'Sommar' , 'Höst'] )

ax.set_ylabel ('timmar / vecka')

ax.set_title ('Neuroanestesi, elektiva patient-timmar 2019')

ax.axhline(y=135, color='r', linestyle='-')
ax.grid (axis = 'y', alpha =0.5)

# save and show plot 
plt.savefig('Elektiv2019.png', bbox_inches='tight')

plt.show() 
