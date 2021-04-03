#This code makes a request to mapbox and download a map.

import matplotlib.pyplot as plt
import requests

#you can go to https://docs.mapbox.com/playground/static/ and select a map (left column choose boundaries and not centered
#or write the coordinates you want
# watch the format to build other requests [lon_west,lat_south,lon_east,lat_north]
#I´ll write coordinates I want:
bounds = [-75.0 , -70.0, -45.0, -30.0]
ratio = abs( (bounds[3]-bounds[1]) / (bounds[2]-bounds[0]) )
y = int(300 * ratio)
bounds.append(ratio)

map_url = "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/"+\
          str(bounds[:4])+\
          "/300x"+ str(y) +"?access_token="+\
          "pk.eyJ1IjoibWFydGluZXp0b3JyZW50ZSIsImEiOiJja24xdXMwcHowOXAyMnhtbjl5aWZiMnJ0In0.1I1dR7W9XdYqKJcC6QtWWw"

map_data = requests.get(map_url).content
with open('my_map.jpg', 'wb') as handler:
    handler.write(map_data)

my_map=plt.imread('my_map.jpg')
plt.imshow(my_map)
plt.show()