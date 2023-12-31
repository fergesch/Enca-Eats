import geopandas
from treelib import Tree
from google.cloud import secretmanager
from google.cloud import firestore

PROJECT_ID = 'enca-eats'
DB = firestore.Client(project=PROJECT_ID)

def get_secret_value(
    project_id: str, secret_id: str, version_id: str = 'latest'
) -> str:
    """
    Get information about the given secret version. It does not include the
    payload data.
    """
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()
    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    # Get the secret version.
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


def batch_upsert(collection, upsert_list, id_field, batch_size=500):
    chunks = [upsert_list[i:i+batch_size] for i in range(0, len(upsert_list), batch_size)]
    batch = DB.batch()
    for chunk in chunks:
        for value in chunk:
            doc_ref = DB.collection(collection).document(value[id_field])
            batch.set(doc_ref, value)
        batch.commit()


def find_neighborhood(p, neighborhoods):
    # neighborhoods = geopandas.read_file("geo_data/uber.geojson")
    for index, row in neighborhoods.iterrows():
        if row['geometry'].contains(p):
            return(row[['city','neighborhood']].to_dict())
    return({'city': 'Unknown', 'neighborhood': 'Unknown'})


def build_tree(cat_list):
    tree = Tree()
    tree.create_node('root','root')
    while len(cat_list) > 0:
        pop_list = []
        for i in range(len(cat_list)):
            try:
                if cat_list[i]['parent_aliases'] == []:
                    tree.create_node(cat_list[i]['title'], cat_list[i]['alias'], parent = 'root')
                else:
                    tree.create_node(cat_list[i]['title'], cat_list[i]['alias'], parent = cat_list[i]['parent_aliases'][0])
                pop_list.append(i)
            except:
                pass
        pop_list.sort(reverse = True)
        for i in pop_list:
            cat_list.pop(i)
    return(tree)


if __name__ == '__main__':
    # pass
    from shapely.geometry import Point
    p = Point(-74.02765511135665, 40.74387321381147) # 615 Hudson
    p = Point(-73.95591076059685, 40.778376628289436) # 155 E 84th
    print(find_neighborhood(p))