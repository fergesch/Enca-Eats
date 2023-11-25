from google.cloud import firestore
import utils

db = firestore.Client(project=utils.PROJECT_ID)
cat_coll = db.collection("categories").stream()

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

print(len(hier_list))
# database.delete_container('category_hierarchy')
# database.create_container(id='category_hierarchy', partition_key=PartitionKey(path='/alias', kind='Hash'))
# for i in hier_list:
#     container_cat_hier.upsert_item(i)