import sys
import json
import urllib
from sets import Set

OUTPUT_FNAME = 'freebase_output'
LIMIT = 100
output_fp = open(OUTPUT_FNAME, 'w')
founders_query_id = '/organization/organization/founders'
board_members_query_id = '/organization/organization/board_members./organization/organization_board_membership/member'
leadership_query_id = '/organization/organization/leadership./organization/leadership/person'

parents_query_id = '/people/person/parents'
children_query_id = '/people/person/children'
siblings_query_id = '/people/person/sibling_s'
spouse_query_id = '/people/person/spouse_s'

if len(sys.argv) < 2:
    print 'Usage: python mql_collect [api_key_filepath]'
    exit()

# Read API key from provided path
with open(sys.argv[1]) as fp:
    api_key = fp.readline().strip()

def write_to_file(company_name, people, label):
    for person in people:
        if person is None or company_name is None:
            continue
        output_fp.write('\t'.join([company_name, person, str(label)]).encode('utf-8') + '\n')

# Callback to handle a single API response
def handle_company(result):
    # if founders not found, don't do anything
    founders = result['founders']
    if not founders:
        return
    for name in [result['name']] + result['/common/topic/alias']:
        employees = [x['person'] for x in result['/business/employer/employees']]
        board_members = [x['person'] for x in result['board_members']]
        others = employees + board_members

        positive_names = Set(founders)
        negative_names = Set(others).difference(positive_names)

        write_to_file(name, positive_names, 1)
        write_to_file(name, negative_names, 0)

service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
query = [{'id': None,
          'name': None,
          '/common/topic/alias': [],
          'founders':[],
          'board_members':[{'person': None}],
          '/business/employer/employees': [{'person': None}],
          'type': '/organization/organization'}]

params = {
        'query': json.dumps(query),
        'key': api_key,
        'limit': LIMIT,
        'cursor': ''
}
url = service_url + '?' + urllib.urlencode(params)
response = json.loads(urllib.urlopen(url).read())


while 'cursor' in response and 'result' in response:
    for company in response['result']:
        handle_company(company)
    print 'Fetching {0} companies'.format(LIMIT)
    params['cursor'] = response['cursor']
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
