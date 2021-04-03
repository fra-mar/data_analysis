#This doesn´t work for big areas due probably to projection issues. But works fine for smaller areas.
#Request map with map_request_mapbox.py

import json
import matplotlib.pyplot as plt
from map_request_mapbox import bounds as bn

#--I got this from https://earthquake.usgs.gov/earthquakes/feed/. Chose geojson file and changed extension to json
#but you can download in excel and atom too

filename = 'eq_all_week.json'

#--Read .json file

with open (filename, encoding='utf8') as f:  #enconding cause the original sent a "decodingerror 'charmap' unable...
    all_eq_data = json.load(f)


#--Make a list of all earthquakes
img = plt.imread('my_map.jpg')

lon_west, lat_south = bn[0],bn[1]
lon_east, lat_north = bn[2], bn[3]
extents = [lon_west, lon_east,lat_south,lat_north]


#--extracting location data
all_eq_dicts = all_eq_data['features'] #look at readable_eq_data.json to understand you pick a dict with all eq
mags,lons, lats =[] , [], []

for eq_dict in all_eq_dicts:
    mag = eq_dict['properties']['mag']
    lon = eq_dict['geometry']['coordinates'][0]
    lat = eq_dict['geometry']['coordinates'][1]

    if lon > lon_west and lon < lon_east and lat > lat_south and lat < lat_north and mag > 1.0:
        lons.append(lon)
        lats.append(lat)
        mags.append(mag)
#control, point on  theoretical 0,0

lats.append(lat_south+1)
lons.append(lon_west+1)
#plotting
fig = plt.figure ('My way of plotting maps in pyplot')
ax = fig.add_subplot(1,1,1)

ax.imshow(img, aspect = 'auto',  extent = extents )#,
ax.set_aspect(aspect=bn[4]) #bn[4] es el ratio de la imagen con el mapa original
ax.scatter (lons, lats, s= 30)

plt.show()

