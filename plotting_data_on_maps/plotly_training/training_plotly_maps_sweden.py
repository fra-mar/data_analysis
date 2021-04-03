import plotly.express as px



#lon, lat for Uppsala, Stockholm, Arlanda airport, Madrid to test code works from known coordinates
lats = [59.8586126,59.3251172, 59.6212, 40.41]
lons = [17.6387436, 18.0710935, 17.9178,-3.70]

fig = px.scatter_geo(lat=lats, lon=lons)
fig.update_geos(fitbounds = 'locations')
fig.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})
fig.show()