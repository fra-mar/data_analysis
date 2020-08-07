# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 15:13:27 2020

@author: maf011
"""


import pandas as pd
pd.options.mode.chained_assignment = None   #prevent uncomfortable warning messages

from matplotlib import pyplot as plt

#%% download table with Autonomous Communities (Spain) 2019 Wikipedia
url='https://en.wikipedia.org/wiki/Autonomous_communities_of_Spain'

df=pd.read_html(url)[1]  #[0] is right upper summarizing table

df.drop(['Flag'], axis=1, inplace=True)

df.rename(columns={'Autonomouscommunity':'Region', 'Area (km²)':'Area',
                   'Population (2019)': 'Population', 'Density (/km²)':'Density',
                   'GDP per capita (euros)':'GDP_capita'}, inplace=True)

#%% create df with just columns I need. 

#could use new = old.filter(['A','B','D'], axis=1) but will use drop

df_simple=df.drop(['Capital', 'President', 'Legislature', 'Government coalition',
       'Senate seats', 'Status'], axis=1)

#%% sort values in different ways, just for training with sorting

#print (' Regions sorted by GDP per capita\n \n')
 
#print(df_simple.sort_values( by=['GDP_capita']))

df_simple_density=df_simple.sort_values( by=['Density'])

#for compare with Sweden
df_es_final= df_simple.filter(['Region', 'Density', 'GDP_capita'], axis = 1)

df_es_final.sort_values(['Region'], inplace=True)
df_es_final.reset_index(inplace=True, drop=True)

#%% download table with Sweden Regions, population density

url_dens_se='https://www.statista.com/statistics/526617/sweden-population-density-by-county/'

df_se_dens=pd.read_html(url_dens_se)[0]
df_se_dens.rename(columns={'Unnamed: 0': 'Region', 
                      'Number of inhabitants per square kilometer': 'Density'}, inplace=True)

n=df_se_dens[df_se_dens['Region']=='Gotlands'].index
df_se_dens['Region'][n]= 'Gotland'
df_se_dens.sort_values(['Region'], inplace=True)
df_se_dens.reset_index(inplace=True, drop=True)

#download table with GDP_capita_ region (2017)    1 SEK .101805 eur 171231
conv=0.101805

url_gdp_se='http://www.regionfakta.com/vastra-gotalands-lan/in-english-/regional-economy/regional-gdp/'

df_se_gdp = pd.read_html(url_gdp_se)[1]

df_se_gdp.drop([21,22], axis=0, inplace=True)   #summarizing info I don´t need

df_se_gdp_filtered= df_se_gdp.filter(items=['Region', '2017'], axis=1)  #take columns I want

str_to_float= lambda x: float(x)
l=len(df_se_gdp_filtered)

for i in range(0,l):  #numbers loaded as str. Converted to float.
    df_se_gdp_filtered['2017'][i]=str_to_float (df_se_gdp_filtered['2017'][i])
    
 #SEK to euro conversion
df_se_gdp_filtered['2017']= df_se_gdp_filtered['2017'] * 1000 * conv  
    
df_se_gdp_filtered.rename( columns= {'2017':'GDP_capita'}, inplace=True)

#in column 'Region' word 'county' is removed.

for i in range (0,l):
    
    a = df_se_gdp_filtered['Region'][i].split()
    if len(a)>2:
        df_se_gdp_filtered['Region'][i] = a[0]+' ' +a[1]
    else:
        df_se_gdp_filtered['Region'][i] = a[0]
        
df_se_gdp_filtered.sort_values(['Region'], inplace=True)
df_se_gdp_filtered.reset_index(inplace=True, drop=True)

#df_se_gdp_filtered['in_dens']=df_se_gdp_filtered['Region'].isin(df_se_dens.Region)   

#%% df_se_final (concatenate df dens and gdp)

df_se_final=df_se_dens
df_se_final['GDP_capita'] = df_se_gdp_filtered['GDP_capita']

#print ('Sorted by population density \n')
#print (df_se.sort_values ( by=['Density']))

#%% save local copy of your data frames
df_es_final.to_csv('Spain_density_GDP.csv')

df_se_final.to_csv('Sweden_density_GDP.csv')

#%% Presenting information
print (df_es_final.sort_values(by=['Density']))

print ('\n',df_se_final.sort_values(by=['Density']))

print ('\n Don´t forget to put it nice in graphs')


#%% copied pattern


#short region names

Spain=df_es_final
Spain.Region=['Andalusia','Aragon','Balearic I', 'Basque AC', 'Canary I',
           'Cantabria', 'C Leon', 'CL Mancha', 'Catalonia', 'CC Navarre',
           'C Madrid', 'Extremadura', 'Galicia', 'Rioja', 'P Asturias',
           'R Murcia', 'Valencian C']
Sweden=df_se_final


both_countries = Spain,Sweden
names='Spain','Sweden'
count=-1
for country in both_countries:
    
    count=count+1
    #short by GDP
    country.sort_values(by=['Density'], inplace=True)

    #Create figure
    fig=plt.figure(figsize=(16,6))
    ax_side=fig.add_subplot(1,1,1)

    n = 1  # This is our first dataset (out of 2)
    t = 2 # Number of datasets
    d = len(country) # Number of sets of bars
    w = 0.8  # Width of each bar
    x_gdp = [t*element + w*n for element
             in range(d)]

    n = 2  # This is our second dataset (out of 2)
    #t = 2 # Number of datasets
    #d = 7 # Number of sets of bars
    #w = 0.8 # Width of each bar
    x_dens = [t*element + w*n for element
             in range(d)]

    ax_side_twin=ax_side.twinx()

    ax_side.bar(x_gdp,country.GDP_capita,color=(1.0, 0.47, 0.42), label='GDP per capita')
    ax_side_twin.bar(x_dens,country.Density,label='Population density')

    ax_side.set_xticks(range(1,2*d,2))
    ax_side.set_xticklabels(country['Region'],rotation=45)
    ax_side.set_ylabel('GDP (euro)/capita')
    ax_side_twin.set_ylabel('Population density')
    ax_side.legend(loc=1)
    ax_side_twin.legend(loc=2)
    
    ax_side.axhline(y=25000, ls='dotted', c='orange')
    ax_side_twin.axhline(y=100, ls='dotted', c='blue')
    
    co= 'GDP_capita and population density in '+ names[count]
    
    plt.title(co)
    plt.show()
    



#%%
#think about this...
plt.scatter (df_es_final.Density,df_es_final.GDP_capita, label='Spain')
plt.scatter (df_se_final.Density,df_se_final.GDP_capita, label='Sweden') 

plt.title('x=inhab/sqr Km, y= regional GDP_capita' )
plt.show()