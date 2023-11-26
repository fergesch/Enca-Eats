import pandas as pd
import geopandas

hob = geopandas.read_file('geo_data/Hoboken_City_Limits.geojson')
nyc = geopandas.read_file('geo_data/nyc.geojson')
jc = geopandas.read_file('geo_data/jersey-city-neighborhoods.geojson')

jc['city'] = 'Jersey City'
jc['neighborhood'] = jc['area']

jc_cond = jc['area'] == 'Downtown'
jc.loc[jc['area'] == 'Downtown', 'neighborhood'] = jc.loc[jc_cond, 'area'] \
    + ' - ' \
    + jc.loc[jc_cond, 'neighborho']

geo_list = [
    hob[['NAME', 'GNIS_NAME', 'geometry']].rename(
        {'NAME': 'neighborhood', 'GNIS_NAME': 'city'}, axis=1),
    nyc[['NTAName', 'BoroName', 'geometry']].rename(
        {'NTAName': 'neighborhood', 'BoroName': 'city'}, axis=1),
    jc[['neighborhood', 'city', 'geometry']],
]
gdf = pd.concat(geo_list)

gdf = gdf.dissolve(by=['neighborhood', 'city'])
gdf.to_file("geo_data/uber.geojson", driver="GeoJSON")
