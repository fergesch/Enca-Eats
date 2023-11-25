import json
import geopandas
from treelib import Node, Tree
from google.cloud import secretmanager

PROJECT_ID = 'enca-eats'

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


def find_neighborhood(p):
    neighborhoods = geopandas.read_file("yelp_data_pipeline/geo_data/uber.geojson")
    for index, row in neighborhoods.iterrows():
        if row['geometry'].contains(p):
            return(row[['city','neighborhood']].to_dict())
    return('Unknown')

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
    p = Point(-73.95591076059685, 40.778376628289436) #155 E 84th
    print(find_neighborhood(p))