import sys
import json
import urllib
from sets import Set

OUTPUT_FNAME_PAR = 'freebase_parents2'
OUTPUT_FNAME_CHI = 'freebase_children2'
OUTPUT_FNAME_SPO = 'freebase_spouse2'
OUTPUT_FNAME_SIB = 'freebase_siblings2'
LIMIT = 100
output_fp_par = open(OUTPUT_FNAME_PAR, 'w')
output_fp_chi = open(OUTPUT_FNAME_CHI, 'w')
output_fp_spo = open(OUTPUT_FNAME_SPO, 'w')
output_fp_sib = open(OUTPUT_FNAME_SIB, 'w')

if len(sys.argv) < 2:
    print 'Usage: python mql_collect [api_key_filepath]'
    exit()

# Read API key from provided path
with open(sys.argv[1]) as fp:
    api_key = fp.readline().strip()

def write_to_file(output, subject, people, label):
    for person in people:
        if person is None or subject is None:
            continue
        output.write('\t'.join([subject, person, str(label)]).encode('utf-8') + '\n')

# Callback to handle a single API response
def handle_result(result):

    for name in [result['name']]: #+ result['/common/topic/alias']:
        # Try catch for encoding errors
        try:
            #print result['sibling_s']
            siblings_rel = [x['sibling'] for x in result['sibling_s']]
            # flatten it 
            siblings= [str(item).translate(None,'\t').strip() for sublist in siblings_rel for item in sublist if item!=result['name']]
            #print result['name']
            spouses = [x['spouse'] for x in result['spouse_s']]
            spouses= [str(item).translate(None,'\t').strip() for sublist in spouses for item in sublist if item!=result['name']]
            #print spouses
            children = result['children']
            children = [str(child).translate(None,'\t').strip() for child in children]
            parents = result['parents']
            parents = [str(parent).strip().translate(None,'\t') for parent in parents]
            
            handle_parents(output_fp_par,str(name).translate(None,'\t'), parents,siblings,spouses,children)
            handle_spouses(output_fp_spo,str(name).translate(None,'\t'), parents,siblings,spouses,children)
            handle_children(output_fp_chi,str(name).translate(None,'\t'), parents,siblings,spouses,children)
            handle_siblings(output_fp_sib,str(name).translate(None,'\t'), parents,siblings,spouses,children)
        except UnicodeEncodeError:
            continue

def handle_parents(output, name, parents,siblings,spouses,children):
    positive_names = Set(parents)
    others = siblings + children + spouses
    negative_names = Set(others).difference(positive_names)
    write_to_file(output,name, positive_names, 1)
    write_to_file(output,name, negative_names, 0)

def handle_spouses(output, name, parents,siblings,spouses,children):
    positive_names = Set(spouses)
    others = siblings + children + parents
    negative_names = Set(others).difference(positive_names)
    write_to_file(output,name, positive_names, 1)
    write_to_file(output,name, negative_names, 0)

def handle_children(output, name, parents,siblings,spouses,children):
    positive_names = Set(children)
    others = siblings + parents + spouses
    negative_names = Set(others).difference(positive_names)
    write_to_file(output,name, positive_names, 1)
    write_to_file(output,name, negative_names, 0)

def handle_siblings(output, name, parents,siblings,spouses,children):
    positive_names = Set(siblings)
    others = children + parents + spouses
    negative_names = Set(others).difference(positive_names)
    write_to_file(output,name, positive_names, 1)
    write_to_file(output,name, negative_names, 0)

service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
query = [{'id': None,
          'name': None,
          'parents':[],
          'children':[],
          'sibling_s':[{'sibling': [],"optional": "optional"}],
          'spouse_s': [{'spouse':[],"optional": "optional"}],#[{'spouse': None}],
          'type': '/people/person'}]

params = {
        'query': json.dumps(query),
        'key': api_key,
        'limit': LIMIT,
        'cursor': ''
}
#intermediate_cursor = 'eNpVj01Ow0AMhQ_DphGK6r_xeCxUcY9RFqMEUCVooknpggVnZxBISb2y9d73bI-fdZ2rs8ToeXYyAhjyxRGNmS1JGspl8gfoEWPQNqs5e17WL8df63xzGA7ntfidpT71h7ePsrgmRGHZicmv_UkDMEDUrtvYhEkFwo61aMhKm6j_LKUUbccaQ7MA-Xtjb-fFMUJEYN409vqYCKjYCAIAKvhqcFdjfxJV7rq81Lm9dWwbWYzy0m75a_27z2uLD4Zkw3B8Ti-joExaArW0CUHpB-5yU8w='
url = service_url + '?' + urllib.urlencode(params)
response = json.loads(urllib.urlopen(url).read())
#print response
#response['cursor'] = intermediate_cursor

while 'cursor' in response and 'result' in response:
    for subject in response['result']:
        handle_result(subject)
    print 'Fetching {0} people'.format(LIMIT)
    params['cursor'] = response['cursor']
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())

