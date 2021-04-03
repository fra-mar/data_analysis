#This doesn´t work for big areas due probably to projection issues. But works fine for smaller areas.
import json

import matplotlib.pyplot as plt

#--I got this from https://earthquake.usgs.gov/earthquakes/feed/. Chose geojson file and changed extension to json
#but you can download in excel and atom too

filename = 'eq_all_week.json'

#--Read .json file

with open (filename, encoding='utf8') as f:  #enconding cause the original sent a "decodingerror 'charmap' unable...
    all_eq_data = json.load(f)


#--Make a list of all earthquakes
img = plt.imread('africa_eq_-64&51_100&02_-43&71_59&36.JPG')

lon_min, lon_max = -64.51, 100.02
lat_min, lat_max = -39, 58.98
extents = [lon_min, lon_max,lat_min,lat_max]


#--extracting location data
all_eq_dicts = all_eq_data['features'] #look at readable_eq_data.json to understand you pick a dict with all eq
mags,lons, lats =[] , [], []

for eq_dict in all_eq_dicts:
    mag = eq_dict['properties']['mag']
    lon = eq_dict['geometry']['coordinates'][0]
    lat = eq_dict['geometry']['coordinates'][1]

    if lon > lon_min and lon < lon_max and lat > lat_min and lat < lat_max and mag > 1.0:
        lons.append(lon)
        lats.append(lat)
        mags.append(mag)
#control, point on Madrid and theoretical 0,0
lats.append(40.416775)
lons.append(-3.703790)
lats.append(lat_min+1)
lons.append(lon_min+1)
#plotting
fig = plt.figure ('My way of plotting maps in pyplot')
ax = fig.add_subplot(1,1,1)
ax.imshow(img, aspect = 'auto', extent = extents )
ax.scatter (lons, lats, s= 30)

plt.show()

