# coding=utf-8
# 将mongodb里的数据导入服务器的elasticsearch,服务器的elasticsearch容器做9200的端口映射
__author__ = 'bxm'

from utils.database import get_mongodb
from elasticsearch import Elasticsearch

# 建立连接
es_client = Elasticsearch(hosts=[{"host": "192.168.200.3", "port": 9200}])
index_name = "poi"
type_name = "ViewSpot"

if es_client.indices.exists(index_name):
    print("deleting '%s' index..." % (index_name))
    print(es_client.indices.delete(index=index_name, ignore=[400, 404]))

index_test = es_client.indices.create(index=index_name)

# ViewSpot的mappings
viewspot_map = {
    "ViewSpot": {
        "properties": {
            "desc": {
                "type": "string",
                "analyzer": "ik"
            },
            "details": {
                "type": "string",
                "analyzer": "ik"
            },
            "alias": {
                "type": "string",
                "analyzer": "ik"
            },
            "hotness": {
                "type": "double"
            },
            "ratings": {
                "type": "double"
            },
            "location": {
                "properties": {
                    "coordinates": {
                        "type": "geo_point"
                    },
                    "type": {
                        "type": "string"
                    }
                }
            }

        }
    }
}
es_client.indices.put_mapping(type_name, viewspot_map, index_name)

bulk_data = []

viewspot_conn = get_mongodb("poi", "ViewSpot", 'mongo')
cursor = viewspot_conn.find()

i = 0
for val in cursor:
    i = i + 1
    #元数据
    bulk_data.append({
        "index": {
            "_index": index_name,
            "_type": type_name,
            "_id": i
        }
    })

    doc = {}
    if val.has_key('desc'):
        doc['desc'] = val['desc']
    if val.has_key('details'):
        doc['details'] = val['details']
    if val.has_key('alias'):
        doc['alias'] = val['alias']
    if val.has_key('hotness'):
        doc['hotness'] = val['hotness']
    if val.has_key('ratings'):
        doc['ratings'] = val['ratings']
    if val.has_key('location'):
        doc['location'] = val['location']

    # bulk_data.append({ "desc": val['desc'],"alias":val['alias'],"hotness":val['hotness'],"rating":val['rating'],
    # "location":val['location']})

    bulk_data.append(doc)
    # 当累计有500条文档时，一次性写入Elasticsearch
    if i % 500 == 0:
        print("start bulk: %d" % i)
        res = es_client.bulk(index=index_name, body=bulk_data, refresh=True)
        print(res)
        bulk_data = []
        # break

if bulk_data:
    res = es_client.bulk(index=index_name, body=bulk_data, refresh=True)
    print(res)


# print bulk_data
# print("bulk indexing...")





# print("results:")
# for doc in es_client.search(index=index_name)['hits']['hits']:
# print(doc)

