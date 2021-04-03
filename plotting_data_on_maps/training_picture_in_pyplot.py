'''
learning goals:
-matplotlib tool for maps is basemap which is very complicated to install
-plotly has an easier tool
-I check if it´s doable to draw a map in the background and then .scatter(x,y)
where x are a list of longitudes and y of latitudes
-I see it´s doable, next step wonder is open street map let´s pick specific maps,
not just world maps
'''

import matplotlib.pyplot as plt

#will draw a world map with size after the image size
img = plt.imread('world_map_coastlines.jpg')
fig, ax = plt.subplots()
ax.imshow(img)        #extension is that of the original image
plt.show()

#Now let´s say we want to change the extension to 50x100

fig, ax = plt.subplots()
ax.imshow(img, extent =[0,100,0,50] ) #format xmin,xmax,ymin,ymax
plt.show()

#now let´s simulate coordinates

fig, ax = plt.subplots()
ax.imshow(img, extent =[-180,+180,-90,+90] ) #format xmin,xmax,ymin,ymax
plt.show()

#now import data from eq_explore_data.py
from eq_explore_data import lons,lats

fig, ax = plt.subplots()
ax.imshow(img, extent =[-180,+180,-90,+90] ) #format xmin,xmax,ymin,ymax
ax.scatter (lons, lats)
plt.show()
