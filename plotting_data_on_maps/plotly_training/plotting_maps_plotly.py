#I got most information from https://plotly.com/python/map-configuration/
#good one https://plotly.com/python/scatter-plots-on-maps/

import plotly.graph_objects as go

fig = go.Figure(go.Scattergeo())
fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

#Here is a map with all physical features enabled and styled, at a larger-scale 1:50m resolution:
fig = go.Figure(go.Scattergeo())
fig.update_geos(
    resolution=50,
    showcoastlines=True, coastlinecolor="RebeccaPurple",
    showland=True, landcolor="LightGreen",
    showocean=True, oceancolor="LightBlue",
    showlakes=True, lakecolor="Blue",
    showrivers=True, rivercolor="Blue"
)
fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

#Here is a map with only cultural visible (political borders)
fig = go.Figure(go.Scattergeo())
fig.update_geos(
    visible=False, resolution=50,
    showcountries=True, countrycolor="RebeccaPurple"
)
fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

'''Map projections
The available projections are 'equirectangular', 'mercator', 'orthographic', 
'natural earth', 'kavrayskiy7', 'miller', 'robinson', 'eckert4', 
'azimuthal equal area', 'azimuthal equidistant', 'conic equal area', 
'conic conformal', 'conic equidistant', 'gnomonic', 'stereographic', 
'mollweide', 'hammer', 'transverse mercator', 'albers usa', 'winkel tripel', 'aitoff' and 'sinusoidal'.
'''
fig = go.Figure(go.Scattergeo())
fig.update_geos(projection_type="natural earth")
fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

'''Map projections can be rotated using the layout.geo.projection.rotation attribute, 
and maps can be translated using the layout.geo.center attributed, as well as truncated to
 a certain longitude and latitude range using the layout.geo.lataxis.range and layout.geo.lonaxis.range.
 '''
fig = go.Figure(go.Scattergeo())
fig.update_geos(
    center=dict(lon=-30, lat=-30),
    projection_rotation=dict(lon=30, lat=30, roll=30),
    lataxis_range=[-50,20], lonaxis_range=[0, 200]
)
fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

'''To automatically set the boundaries of the map according to the data to be plotted...fitbounds'''
import plotly.express as px

fig = px.line_geo(lat=[0,15,20,35], lon=[5,10,25,30])
fig.update_geos(fitbounds="locations")
fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

'''The available scopes are: 'world', 'usa', 'europe', 'asia', 'africa', 'north america', 'south america'.
'''
fig = go.Figure(go.Scattergeo())
fig.update_geos(
    visible=False, resolution=50, scope="north america",
    showcountries=True, countrycolor="Black",
    showsubunits=True, subunitcolor="Blue"
)
fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

'''Graticules'''
fig = go.Figure(go.Scattergeo())
fig.update_geos(lataxis_showgrid=True, lonaxis_showgrid=True)
fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

'''hover mode. There are other hover modes !!
https://plotly.com/python/hover-text-and-formatting/'''
import plotly.express as px

df = px.data.gapminder().query("continent=='Oceania'")

fig = px.line(df, x="year", y="lifeExp", color="country", title="layout.hovermode='closest' (the default)")
fig.update_traces(mode="markers+lines")

fig.show()
#_______________________________hovermode x, there is an 'y', 'x unified' and 'y unified'
import plotly.express as px

df = px.data.gapminder().query("continent=='Oceania'")

fig = px.line(df, x="year", y="lifeExp", color="country", title="layout.hovermode='x'")
fig.update_traces(mode="markers+lines", hovertemplate=None)
fig.update_layout(hovermode="x")

fig.show()
#___________________in graphic_objects
import plotly.graph_objects as go
import numpy as np
t = np.linspace(0, 2 * np.pi, 100)
fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=np.sin(t), name='sin(t)'))
fig.add_trace(go.Scatter(x=t, y=np.cos(t), name='cost(t)'))
fig.update_layout(hovermode='x unified')
fig.show()
#_________________changing data showed in hovermode
import plotly.express as px
import numpy as np
df = px.data.iris()
fig = px.scatter(df, x='petal_length', y='sepal_length', facet_col='species', color='species',
                 hover_data={'species':False, # remove species from hover data
                             'sepal_length':':.2f', # customize hover for column of y attribute
                             'petal_width':True, # add other column, default formatting
                             'sepal_width':':.2f', # add other column, customized formatting
                             # data not in dataframe, default formatting
                             'suppl_1': np.random.random(len(df)),
                             # data not in dataframe, customized formatting
                             'suppl_2': (':.3f', np.random.random(len(df)))
                            })
fig.update_layout(height=300)
fig.show()