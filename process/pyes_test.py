__author__ = 'bxm'

#pyes 测试
import pyes

try:
    conn = pyes.ES('127.0.0.1:9200')
except Exception:
    print 'error'
conn.indices.create_index_if_missing("human")
mapping = {'firstname':
               {'index': 'analyzed',
                'type': 'string',
                'analyzer': 'ik'
               },
           'lastname':
               {'index': 'not_analyzed',
                'type': 'string'},
           'age':
               {'index': 'not_analyzed',
                'type': 'long'}
}
conn.indices.put_mapping('man',
                         {'properties': mapping},
                         ['human'])
conn.indices.put_mapping("woman",
                         {'properties': mapping},
                         ["human"])
conn.index({'firstname': 'David','lastname': 'White','age': 18},
           'human',
           'man',
           True)
conn.index({'firstname': 'Suzan', 'lastname': 'Black', 'age': 28},
           'human',
           'woman',
           True)

q = pyes.TermQuery('firstname', 'Suzan')
q=pyes.QueryStringQuery('Suzan')
res = conn.search(query=q)

if not res:
    print 'cdv'
for r in res:
    print type(res)