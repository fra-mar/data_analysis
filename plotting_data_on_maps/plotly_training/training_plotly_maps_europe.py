import plotly.graph_objs as go
from plotly import offline

import csv

filename = 'concap.csv'


with open (filename,'r') as f:
    read_content = csv.reader(f)
    headers = next(f)
    capital, countryISO, lats, lons = [], [], [], []
    for row in read_content:
        cont = row[5]
        if cont == 'Europe':
            lats.append( row[2] )
            lons.append( row[3] )
            capital.append( row[1])
            countryISO.append(row[4])

#searching population in another file
population = [999 for x in capital]

for i in range(0, len(capital)):
    with open ('worldcities.csv', encoding='utf-8') as ff:
        read_content = csv.reader(ff)
        header_cities = next(ff)

        for row in read_content:
            if row[0] == capital[i]  and row[5] == countryISO[i]:
                population[i]=int(row[9])

marker_s=[0.3*float(s)/ 10e4 for s in population]
marker_size = [(p*30/60)+10 for p in marker_s]
#marker_size = 15

fig = go.Figure(data=go.Scattergeo(
    lon = lons,
    lat = lats,
    text= capital,
    marker= dict(size= marker_size,
                 color = population,
                 colorscale= 'Viridis',
                 reversescale= True,
                 colorbar= dict(title='population'))
))

fig.update_geos(fitbounds = 'locations', showcountries=True, countrycolor="RebeccaPurple")
fig.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})
'''               hovermode='x',
                  hover_data = {'lons': False,
                                'lats': False,  #dont know why hover doesn´t work
                                'capital':True,
                                'population':True})'''
offline.plot(fig, filename='European capitals.html')

fig.show()
