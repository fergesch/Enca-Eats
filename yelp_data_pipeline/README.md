# Getting Data From Yelp
## Setup virtual environment
```
python -m venv ./.venv
source ./.venv/bin/activate
pip install -r requirements.txt
```

## Yelp API Documentation
https://docs.developer.yelp.com/docs/fusion-intro

https://github.com/Yelp/yelp-fusion/blob/master/fusion/python/sample.py

## GeoJson Locations
- Hoboken
    - https://hoboken-mapping-hub-cityofhoboken.hub.arcgis.com/datasets/CityofHoboken::hoboken-city-limits-1/explore?location=40.746226%2C-74.032123%2C15.61
- Jersey City
    - https://data.jerseycitynj.gov/explore/dataset/jersey-city-neighborhoods/information/?location=14,40.75704,-74.043&basemap=mapbox.light
- NYC
    - https://www.nyc.gov/site/planning/data-maps/open-data/census-download-metadata.page
    - https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Census_Tracts_for_2020_US_Census/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson