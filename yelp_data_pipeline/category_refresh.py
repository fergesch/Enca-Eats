import requests
import json
# from azure.cosmos import CosmosClient
# from azure.cosmos.partition_key import PartitionKey
import utils
from google.cloud import firestore



db = firestore.Client(project=utils.PROJECT_ID)

# Yelp API Parameters
yelp_key = utils.get_secret_value(utils.PROJECT_ID, 'yelp_api_key')
headers = {'Authorization': f'Bearer {yelp_key}'}
cat_url = 'https://api.yelp.com/v3/categories'
params = {'locale': 'en_US'}

# Get list of all categories
cat_req = requests.get(cat_url, params = params, headers=headers)
cat_parsed = json.loads(cat_req.text)
cat_list = cat_parsed['categories']

# Cleanup database and insert refreshed categories (Old cosmos)
# database.delete_container('categories')
# database.create_container(id='categories', partition_key=PartitionKey(path='/alias', kind='Hash'))
batch_size = 500
# groups = ceil(len(cat_list)/batch_size)
# np.array_split(cat_list, groups)

chunks = [cat_list[i:i+batch_size] for i in range(0, len(cat_list), batch_size)]

batch = db.batch()
for chunk in chunks:
    for value in chunk:
        doc_ref = db.collection('categories').document(value['alias'])
        batch.set(doc_ref, value)
    batch.commit()
print(len(cat_list))
print(len(set([i['alias'] for i in cat_list])))