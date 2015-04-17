import requests

FILE_PATH = 'wikidata_ids'
BASE_URL = 'http://wdq.wmflabs.org/api?'

query_string = 'q=CLAIM[31:783794]and%20link[enwiki]'

r = requests.get(BASE_URL + query_string)

wikidata_ids = r.json()['items']


with open(FILE_PATH, 'w') as fp:
    for wid in wikidata_ids:
        fp.write(str(wid)+'\n')








