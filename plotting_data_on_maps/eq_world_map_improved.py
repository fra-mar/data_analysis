import json

from plotly.graph_objs import Scattergeo, Layout
from plotly import offline

filename = 'eq_all_week.json'

#--Read .json file

with open (filename, encoding='utf8') as f:  #enconding cause the original sent a "decodingerror 'charmap' unable...
    all_eq_data = json.load(f)


#--extracting location data
all_eq_dicts = all_eq_data['features'] #look at readable_eq_data.json to understand you pick a dict with all eq
mags,lons, lats =[] , [], []

for eq_dict in all_eq_dicts:
    mag = eq_dict['properties']['mag']
    lon = eq_dict['geometry']['coordinates'][0]
    lat = eq_dict['geometry']['coordinates'][1]
    if mag>1:       #mag can be negative if micro-eq due to log scale (look https://www.usgs.gov/faqs/how-can-earthquake-have-a-negative-magnitude?qt-news_science_products=0#qt-news_science_products
        mags.append(mag)
    lons.append(lon)
    lats.append(lat)

#map the earthquakes.
'''easiest way to specify the data will be plotted
data = [Scattergeo(lon = lons, lat = lats)]
'''
my_layout = Layout(title = str('Global Earthequakes magnitude >1.0 from'+ filename))

'''more effective way to plot data'''
data = [{'type': 'scattergeo',
         'lon': lons,
         'lat': lats,
         'marker': {'size': [5*mag for mag in mags],
                    'color': mags,
                    'colorscale': 'Viridis',
                    'reversescale': True,
                    'colorbar': {'title': 'Magnitude'},
                    },
         }]
fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='global_earthquakes.html')

