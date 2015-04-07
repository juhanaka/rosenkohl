import sys
import json
from sets import Set
from apiclient.discovery import build
from apiclient.http import BatchHttpRequest

OUTPUT_FNAME = 'freebase_output'
output_fp = open(OUTPUT_FNAME, 'w')

if len(sys.argv) < 3:
    print 'Usage: python freebase_collect [api_key_filepath] [companies_filepath]'
    exit()

with open(sys.argv[1]) as fp:
    api_key = fp.readline().strip()

companies = []
with open(sys.argv[2]) as fp:
    for line in fp:
        companies.append(line.strip())

print 'About to execute with {0} companies.\nPlease press y to confirm'.format(len(companies))
if sys.stdin.read(1).lower() != 'y':
    print 'Exiting...'
    exit()

service = build('freebase', 'v1', developerKey=api_key)
batch = BatchHttpRequest()

founders_query_id = '/organization/organization/founders'
board_members_query_id = '/organization/organization/board_members./organization/organization_board_membership/member'
leadership_query_id = '/organization/organization/leadership./organization/leadership/person'

query_ids = [founders_query_id, board_members_query_id, leadership_query_id]

output = '({0})'.format(' '.join(query_ids))

positive_examples = []
negative_examples = []

def write_to_file(company_name, people, label):
    for person in people:
        output_fp.write('\t'.join([company_name, person, str(label)]).encode('utf-8') + '\n')

# Callback to handle a single API response
def handle_company(request_id, response, exception):
    resp_dict = json.loads(response)
    if not resp_dict['result']:
        return
    result = resp_dict['result'][0]

    # if founders not found, don't do anything
    if not founders_query_id in result['output'][founders_query_id] or \
        not result['output'][founders_query_id]:
        return

    founders = [person['name'] for person in result['output'][founders_query_id][founders_query_id]]
    others = []
    try:
        if leadership_query_id.split('.')[1] in result['output'][leadership_query_id]:
            others += map(lambda person: person['name'], result['output'][leadership_query_id][leadership_query_id.split('.')[1]])

        if board_members_query_id.split('.')[1] in result['output'][board_members_query_id]:
            others += map(lambda person: person['name'], result['output'][board_members_query_id][board_members_query_id.split('.')[1]])
    except KeyError:
        pass

    positive_names = Set(founders)
    negative_names = Set(others).difference(positive_names)

    write_to_file(result['name'], positive_names, 1)
    write_to_file(result['name'], negative_names, 0)

for company in companies:
    batch.add(service.search(query=company, output=output), callback=handle_company)


batch.execute()












