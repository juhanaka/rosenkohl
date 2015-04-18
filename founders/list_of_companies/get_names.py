import json

WIKIDATA_IDS_PATH = 'wikidata_ids'
DATA_PATH = '/Volumes/Juhana_Ext/cs341data/'
LANG = 'en'

company_ids = []
with open(WIKIDATA_IDS_PATH) as fp:
    for line in fp:
        company_ids.append(line.strip())

company_ids = set(company_ids)


def parse_json(line,label_fp, alias_fp):
    obj = json.loads(line)
    id_ = obj['id'][1:]

    if not id_ in company_ids:
        return
    if 'labels' in obj and LANG in obj['labels']:
        label = obj['labels'][LANG]['value']
        label_fp.write((label.replace('\t', ' ').replace('\n', ' ') + '\n').encode('utf-8'))

    if 'aliases' in obj and LANG in obj['aliases']:
        aliases = [a['value'] for a in obj['aliases'][LANG]]
        for alias in aliases:
            alias_fp.write((alias.replace('\t', ' ').replace('\n', ' ') + '\n').encode('utf-8'))


with open(DATA_PATH + '/wikidata_dump.json', 'r') as f, \
    open('names.tsv', 'w') as label_fp, \
    open('aliases.tsv', 'w') as alias_fp:

    for i, line in enumerate(f):
        line = line.rstrip()
        if line == '[' or line == ']':
            continue
        # strip trailing commas
        line = line.rstrip(',')
        parse_json(line, label_fp, alias_fp)

