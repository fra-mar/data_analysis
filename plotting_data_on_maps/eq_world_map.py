import json

from plotly.graph_objs import Scattergeo, Layout
from plotly import offline

filename = 'eq_1_day_m1.json'

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
    mags.append(mag)
    lons.append(lon)
    lats.append(lat)

#map the earthquakes.
'''easiest way to specify the data will be plotted
data = [Scattergeo(lon = lons, lat = lats)]
'''
my_layout = Layout(title = 'Global Earthequakes')

'''more effective way to plot data'''
data = [{'type': 'scattergeo',
         'lon': lons,
         'lat': lats,
         }]
fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='global_earthquakes.html')

