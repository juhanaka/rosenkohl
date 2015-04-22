import requests

FILE_PATH = 'wikidata_ids'
BASE_URL = 'http://wdq.wmflabs.org/api?'

query_string = '''q=CLAIM[31:783794]%20or%20\
                  CLAIM[31:4830453]%20or%20\
                  CLAIM[31:891723]%20or%20\
                  CLAIM[31:161726]%20or%20\
                  CLAIM[31:35127]%20or%20\
                  CLAIM[31:355]%20or%20\
                  CLAIM[31:3918]%20or%20\
                  CLAIM[31:902104]%20or%20\
                  CLAIM[31:79913]%20or%20\
                  CLAIM[31:157031]%20and%20\
                  link[enwiki]'''

r = requests.get(BASE_URL + query_string)

wikidata_ids = r.json()['items']


with open(FILE_PATH, 'w') as fp:
    for wid in wikidata_ids:
        fp.write(str(wid)+'\n')








