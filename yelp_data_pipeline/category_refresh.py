import functions_framework
import requests
import json
import utils
from google.cloud import firestore

@functions_framework.http
def entrypoint_http(_):
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

    batch_size = 500
    chunks = [cat_list[i:i+batch_size] for i in range(0, len(cat_list), batch_size)]

    batch = db.batch()
    for chunk in chunks:
        for value in chunk:
            doc_ref = db.collection('categories').document(value['alias'])
            batch.set(doc_ref, value)
        batch.commit()
    
    cat_coll = db.collection("categories")
    cnt_qry = cat_coll.count()
    cnt = cnt_qry.get()[0][0].value
    return {'input size': len(cat_list), 'collection size': cnt}

if __name__ == "__main__":
    print(hello_http({}))