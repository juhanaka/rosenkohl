import json
import requests
import re


BASE_URL = 'http://en.wikipedia.org/w/api.php?action=query&generator=categorymembers&rvsection=0&gcmtype=page&'
FORMAT = 'json'
PROP = 'revisions'
RVPROP = 'content'
GCMTITLE = 'Category:Companies_of_the_United_Kingdom'
GCMLIMIT = 'max'

URL = BASE_URL + 'gcmlimit={0}&gcmtitle={1}&prop={2}&rvprop={3}&format={4}'.format(GCMLIMIT,
                                                                                   GCMTITLE,
                                                                                   PROP,
                                                                                   RVPROP,
                                                                                   FORMAT)

WIKIDATA_BASE = 'http://www.wikidata.org/w/api.php?'
r = requests.get(URL)
entities = []

print 'Fetching entities based on query: {0}'.format(GCMTITLE)

while 'query-continue' in r.json():
    entities += [page[1] for page in r.json()['query']['pages'].items()]
    NEW_URL = URL + '&rvcontinue={0}'.format(r.json()['query-continue']['revisions']['rvcontinue'])
    r = requests.get(NEW_URL)

entities_with_article = [page for page in entities if 'revisions' in page]

print 'Found {0} entities with article'.format(len(entities_with_article))

entities_page_ids = [str(entity['pageid']) for entity in entities_with_article]

raw_wikidata_ids = []
for i in xrange(len(entities_page_ids) / 50):
    page_ids_qstring = '|'.join(entities_page_ids[i:i+50])
    url = 'http://en.wikipedia.org/w/api.php?limit=500&action=query&prop=pageprops&ppprop=wikibase_item&pageids={0}&format=json'.format(page_ids_qstring) 
    r = requests.get(url)
    raw_wikidata_ids += [page[1] for page in r.json()['query']['pages'].items()]

wikidata_ids = [item['pageprops']['wikibase_item'] if 'pageprops' in item else None for item in raw_wikidata_ids ]

founder_claims = []
for id_ in wikidata_ids:
    url = 'http://www.wikidata.org/w/api.php?action=wbgetclaims&entity={0}&property=P112&uselang=en&format=json'.format(id_)
    r = requests.get(url)
    claims = r.json()['claims']
    founder_claims.append(claims if claims else None)

founder_count = 0
infobox_count = 0
founder_in_data_and_box = 0
founder_in_data_but_not_box = 0
founder_in_box_but_not_data = 0

def get_infobox(entity):
    text = entity['revisions'][0]['*']
    infobox = re.search(r'\{\{Infobox.*?(?=\n\}\}\n\n)', text, re.DOTALL)
    if infobox is not None:
        return infobox.group(0).lower()


for i,entity in enumerate(entities_with_article):
    infobox = get_infobox(entity)
    if infobox:
        infobox_count += 1
    if infobox is not None and ('founder' in infobox or 'founders' in infobox):
        founder_count += 1
        if founder_claims[i] is not None:
            founder_in_data_and_box += 1
        else:
            founder_in_box_but_not_data += 1
    else:
        if founder_claims[i] is not None:
            founder_in_data_but_not_box += 1


print 'Pages with infoboxes: {0}'.format(infobox_count)
print 'Pages with founders in infobox: {0}'.format(founder_count)
print 'Pages with founders in wikidata: {0}'.format(len(founder_claims) - founder_claims.count(None))
print 'Pages with founders in wikidata but not infobox {0}'.format(founder_in_data_but_not_box)
print 'Pages with founders in infobox but not wikidata {0}'.format(founder_in_box_but_not_data)


