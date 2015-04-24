import requests

FILE_PATH = 'wikidata_ids_entrepreneurs'
BASE_URL = 'http://wdq.wmflabs.org/api?'

query_string = '''q=CLAIM[106:131524]\
                  link[enwiki]'''

r = requests.get(BASE_URL + query_string)

wikidata_ids = r.json()['items']


with open(FILE_PATH, 'w') as fp:
    for wid in wikidata_ids:
        fp.write(str(wid)+'\n')
