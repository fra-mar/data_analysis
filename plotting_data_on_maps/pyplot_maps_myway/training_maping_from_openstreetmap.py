'''
Procedure:
go to openstreetmap.org and select the area you want to map.
With the export feature you see what are the longitudes and latitudes of the map.
You can try to share (second icon from the bottom at the right) or export...but doesn´t work
So I use skärmklipp verktyg an save with a name in which those lons and lats are included.
You need to be pretty accurate so coordinates match the right place.

For your learning, imshow parameters extent and aspect are of special interest.
'''

import matplotlib.pyplot as plt
#lon, lat for Uppsala, Stockholm, Arlanda airport, Wik castle to test code works from known coordinates
lats = [59.8586126,59.3251172, 59.6212, 59.736111]
lons = [17.6387436, 18.0710935, 17.9178,17.461667]

#function to convert coordinates in x/y coordinates
img = plt.imread('test_16&8311_18&7020_59&1633_59&9712.JPG')

lon_min, lon_max = 16.8311, 18.7020
lat_min, lat_max = 59.1633, 59.9712
extents = [lon_min, lon_max,lat_min,lat_max]

'''     This is to translate decimal coordinates into pixels x,y corresponding to image
dif_lon = lon_max-lon_min
dif_lat = lat_max-lat_min
sizes = img.shape
size_y, size_x= sizes[0], sizes[1]

lons_corr = [(l-lon_min)*size_x/dif_lon for l in  lons]
lats_corr = [size_y - ((l-lat_min)*size_y/dif_lat ) for l in  lats]
'''


fig = plt.figure ('My way of plotting maps in pyplot')
ax = fig.add_subplot(1,1,1)
#ax.imshow(img, aspect = 'auto', extent =[lon_min,lon_max,lat_min,lat_max] ) #format xmin,xmax,ymin,ymax
ax.imshow(img, aspect = 'auto', extent = extents ) #format xmin,xmax,ymin,ymax
ax.scatter (lons, lats, s= 30)

plt.show()
