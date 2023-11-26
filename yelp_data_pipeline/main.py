import functions_framework
import requests
import json
import utils

@functions_framework.http
def cat_refresh_http(_):
    # Yelp API Parameters
    yelp_key = utils.get_secret_value(utils.PROJECT_ID, 'yelp_api_key')
    headers = {'Authorization': f'Bearer {yelp_key}'}
    cat_url = 'https://api.yelp.com/v3/categories'
    params = {'locale': 'en_US'}

    # Get list of all categories
    cat_req = requests.get(cat_url, params = params, headers=headers)
    cat_parsed = json.loads(cat_req.text)
    cat_list = cat_parsed['categories']

    utils.batch_upsert(collection='categories', upsert_list=cat_list, id_field='alias', batch_size=500)

    cat_coll = utils.DB.collection("categories")
    cnt_qry = cat_coll.count()
    cnt = cnt_qry.get()[0][0].value
    return {'input size': len(cat_list), 'collection size': cnt}

@functions_framework.http
def cat_hier_refresh_http(_):
    cat_coll = utils.DB.collection("categories").stream()

    cat_list = []
    for doc in cat_coll:
        cat_list.append(doc.to_dict())

    tree = utils.build_tree(cat_list)

    hier_list = []
    for a in ['food', 'restaurants']:
        for i in tree.children(a):
            tmp_dict = {'alias': i.identifier,
                        'title': i.tag,
                        'children': []}
            for j in tree.expand_tree(i.identifier):
                child = tree.get_node(j)
                child_dict = {'alias': child.identifier,
                            'title': child.tag}
                tmp_dict['children'].append(child_dict)
            hier_list.append(tmp_dict)

    utils.batch_upsert(collection='category_hierarchy', upsert_list=hier_list, id_field='alias', batch_size=500)

    cat_coll = utils.DB.collection("category_hierarchy")
    cnt_qry = cat_coll.count()
    cnt = cnt_qry.get()[0][0].value
    return {'input size': len(hier_list), 'collection size': cnt}

if __name__ == "__main__":
    print(cat_refresh_http({}))
    print(cat_hier_refresh_http({}))