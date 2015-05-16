# Usage: python freebase_collect [api_key_filepath] [companies_filepath]

import sys
import json
from sets import Set
from apiclient.discovery import build
from apiclient.http import BatchHttpRequest

OUTPUT_FNAME = 'freebase_siblings'
output_fp = open(OUTPUT_FNAME, 'w')

if len(sys.argv) < 3:
    print 'Usage: python freebase_collect [api_key_filepath] [people_filepath]'
    exit()

# Read API key from provided path
with open(sys.argv[1]) as fp:
    api_key = fp.readline().strip()

people = []
# Read person from provided path
with open(sys.argv[2]) as fp:
    for line in fp:
        people.append(line.strip())

print 'About to execute with {0} people.\nPlease press y to confirm'.format(len(people))
if sys.stdin.read(1).lower() != 'y':
    print 'Exiting...'
    exit()

service = build('freebase', 'v1', developerKey=api_key)
batch = BatchHttpRequest()

# Cryptic query freebase relation query ids
parents_query_id = '/people/person/parents'
children_query_id = '/people/person/children'
siblings_query_id = '/people/person/sibling_s'
spouse_query_id = '/people/person/spouse_s'

query_ids = [parents_query_id, children_query_id, siblings_query_id,spouse_query_id]

output = '({0})'.format(' '.join(query_ids))

positive_examples = []
negative_examples = []

def write_to_file(person_name, parents, label):
    for parent in parents:
        output_fp.write('\t'.join([person_name, parent, str(label)]).encode('utf-8') + '\n')

# Callback to handle a single API response
def handle_person(request_id, response, exception):
    resp_dict = json.loads(response)
    if not resp_dict['result']:
        return
    result = resp_dict['result'][0]

    # if founders not found, don't do anything
    if not siblings_query_id in result['output'][siblings_query_id] or \
        not result['output'][siblings_query_id]:
        return

    siblings = [sib['name'] for sib in result['output'][siblings_query_id][siblings_query_id]]
    others = []
    # Sometimes it seems that name is not found on a person, if so - discard
    try:
        if children_query_id.split('.')[1] in result['output'][children_query_id]:
            others += map(lambda per: per['name'], result['output'][children_query_id][children_query_id.split('.')[1]])

        if parents_query_id.split('.')[1] in result['output'][parents_query_id]:
            others += map(lambda per: per['name'], result['output'][parents_query_id][parents_query_id.split('.')[1]])

        if spouse_query_id.split('.')[1] in result['output'][spouse_query_id]:
            others += map(lambda per: per['name'], result['output'][spouse_query_id][spouse_query_id.split('.')[1]])
    except KeyError:
        pass

    positive_names = Set(parents)
    negative_names = Set(others).difference(positive_names)

    write_to_file(result['name'], positive_names, 1)
    write_to_file(result['name'], negative_names, 0)

# go through all people and batch the requests into one request. For each response, call the
# handle_person function
for person in people:
    batch.add(service.search(query=person, output=output), callback=handle_person)


batch.execute()

