import time
from yelpapi import YelpAPI
from shapely.geometry import Point
from datetime import datetime
import utils
import geopandas

t_0 = datetime.now()

cat_coll = utils.DB.collection("category_hierarchy").stream()

cat_list = []
for doc in cat_coll:
    cat_list.append(doc.to_dict())


# Yelp API Parameters
yelp_key = utils.get_secret_value(utils.PROJECT_ID, 'yelp_api_key')
yelp_api = YelpAPI(yelp_key)


# Start pulling businesses within food and restaurants
# Split this up so we can do per location (NJ City, Hoboken, NY) 
bus_list = []
for cat_dict in cat_list:
    cat = cat_dict['alias']
    cnt = 0
    retry = 0
    # Get count of businesses for category
    while retry < 3:
        try:
            tot_cnt = yelp_api.search_query(categories=cat, location='Hoboken', limit=1)['total']
            retry = 3
        except:
            retry += 1
            time.sleep(10)
            tot_cnt = -1
    check_tot = 0
    while (cnt < tot_cnt) & (cnt < 900):
        time.sleep(1)
        retry = 0
        while retry < 3:
            try:
                # add radius in, per location configurable
                resp = yelp_api.search_query(categories=cat, location='Hoboken', limit=50, offset=cnt)
                if len(resp['businesses']) > 0:
                    for i in resp['businesses']:
                        cnt+=1
                        check_tot += 1
                        bus_list.append(i)
                else:
                    cnt = 1000
                retry = 3
            except:
                retry += 1
                print(cat, retry, cnt)
                time.sleep(5)
    print(cat, tot_cnt, check_tot)

# dedupe businesses
bus_ids = []
dedupe_list = []
for i in bus_list:
    if i['id'] not in bus_ids: 
        bus_ids.append(i['id'])
        dedupe_list.append(i)

print(len(bus_list), len(dedupe_list))
print('Fetch time:', datetime.now() - t_0)

t_dedupe = datetime.now()

neighborhoods = geopandas.read_file("geo_data/uber.geojson")
for index, bus in enumerate(dedupe_list):
    if (not(bus['coordinates']['longitude'] is None)) and (not(bus['coordinates']['latitude'] is None)):
        bus['neighborhood'] = utils.find_neighborhood(Point(bus['coordinates']['longitude'], bus['coordinates']['latitude']), neighborhoods)
    else:
        bus['neighborhood'] = 'Unknown'
    bus['url'] = bus['url'].split('?')[0]
    if index % 100 == 0:
        print(datetime.now(), f'completed {index}')

utils.batch_upsert('restaurants', dedupe_list, 'id', batch_size=500)
print('Load time:', datetime.now() - t_dedupe)
print('Total time:', datetime.now() - t_0)