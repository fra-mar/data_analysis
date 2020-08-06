# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 15:13:27 2020

@author: maf011
"""


import pandas as pd

#%% download table with Autonomous Communities (Spain) 2019 Wikipedia
url='https://en.wikipedia.org/wiki/Autonomous_communities_of_Spain'

df=pd.read_html(url)[1]  #[0] is right upper summarizing table

df.drop(['Flag'], axis=1, inplace=True)

df.rename(columns={'Autonomouscommunity':'Name', 'Area (km²)':'Area',
                   'Population (2019)': 'Population', 'Density (/km²)':'Density',
                   'GDP per capita (euros)':'GDP_capita'}, inplace=True)

#%% create df with just columns I need. 

#could use new = old.filter(['A','B','D'], axis=1) but will use drop

df_simple=df.drop(['Capital', 'President', 'Legislature', 'Government coalition',
       'Senate seats', 'Status'], axis=1)

#%% sort values in different ways

print (' Regions sorted by GDP per capita\n \n')
 
print(df_simple.sort_values( by=['GDP_capita']))

df_simple_density=df_simple.sort_values( by=['Density'])

print ('Sorted by population density \n')
print (df_simple_density)
