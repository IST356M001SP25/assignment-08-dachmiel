'''
map_dashboard.py
'''
import streamlit as st
import streamlit_folium as sf
import folium
import pandas as pd
import geopandas as gpd
# these constants should help you get the map to look better
# you need to figure out where to use them
CUSE = (43.0481, -76.1474)  # center of map
ZOOM = 14                   # zoom level
VMIN = 1000                 # min value for color scale
VMAX = 5000                 # max value for color scale

tickets = pd.read_csv('cache/top_locations_mappable.csv')

st.title('Top Locations for Parking Tickets within Syracuse')
st.caption('This dashboard shows the parking tickets that were issued in the top locations with $1,000 or more in total aggregate violation amounts.')

# convert to a geopandas dataframe
geo_df = gpd.GeoDataFrame(tickets, geometry= gpd.points_from_xy(tickets.lon, tickets.lat))
map = folium.Map(location = CUSE, zoom_start= ZOOM)

cuse_map = geo_df.explore( 
    geo_df['amount'],
    m = map,
    legend = True,
    legend_name = 'Amount',
    marker_type= 'circle',
    marker_kwds= {'radius': 15, 'fill': True} 
)

sf.folium_static(cuse_map, width = 800, height = 800)