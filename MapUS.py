import pandas as pd
import folium
from sklearn.cluster import DBSCAN
import numpy as np
from math import radians, sin, cos, asin, sqrt

# Load data
location_data = pd.read_csv('/Users/haiderhassan/Downloads/location_data.csv')

# Convert radians to degrees
location_data['latitude'] = location_data['radlatitude'].apply(lambda rad: rad * (180 / np.pi))
location_data['longitude'] = location_data['radlongitude'].apply(lambda rad: rad * (180 / np.pi))

# Haversine formula
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon, dlat = lon2 - lon1, lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    return 6371 * c # Radius of earth in kilometers

# Clustering
coords = location_data[['latitude', 'longitude']]
db = DBSCAN(eps=(8 * 1.60934)/6371., min_samples=1, algorithm='ball_tree', metric='haversine')
location_data['cluster'] = db.fit_predict(np.radians(coords))

# Create map
map_us = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
for idx, row in location_data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Cluster: {row['cluster']}\n{row['vchtrackname']}, {row['vchcity']}, {row['vchregion']}",
        icon=folium.Icon(color='blue', icon='ok-sign'),
    ).add_to(map_us)

# Save map
map_us.save('/Users/haiderhassan/Downloads/us_cluster.html')
