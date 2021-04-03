#Explore the structure of the data. I follow chapter in Crash course python
#learning goals: extract data from json files, plot with plotly
import json

#--I got this from https://earthquake.usgs.gov/earthquakes/feed/. Chose geojson file and changed extension to json
#but you can download in excel and atom too

filename = 'eq_1_day_m1.json'
filename = 'eq_all_week.json'

#--Read .json file

with open (filename, encoding='utf8') as f:  #enconding cause the original sent a "decodingerror 'charmap' unable...
    all_eq_data = json.load(f)

#'''this creates a jason file which is more readable for humans but same thing as the original
readable_file = 'readable_eq_data.json'
with open (readable_file, 'w') as f:
    json.dump(all_eq_data, f, indent = 4)
#'''

#--Make a list of all earthquakes

'''Focused learning
Here you can focus in just the way you get magnitudes

all_eq_dicts = all_eq_data['features'] #look at readable_eq_data.json to understand you pick a dict with all eq
mags =[]
for eq_dict in all_eq_dicts:
    mag = eq_dict['properties']['mag']
    mags.append(mag) '''

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

'''by the way you can create a np.array by eq_array = np.array[lons,lats,mags] , (shape 3,180)'''

