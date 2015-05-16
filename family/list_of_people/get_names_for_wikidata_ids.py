import json

WIKIDATA_IDS_PATH = 'results/ppl_wikidata_ids.txt'
DATA_PATH = '/Volumes/Juhana_Ext/cs341data/'
LANG = 'en'
RESULT_NAMES_FP = 'results/ppl_names.txt'
RESULT_ALIASES_FP = 'results/ppl_aliases.txt'

people_ids = []
with open(WIKIDATA_IDS_PATH) as fp:
    for line in fp:
        people_ids.append(line.strip())

people_ids_set = set(people_ids)


def parse_json(line,label_fp, alias_fp):
    obj = json.loads(line)
    if not obj['id'].startswith('Q'):
        return
    id_ = obj['id'][1:]
    label = None

    if not id_ in people_ids_set:
        return
    if 'labels' in obj and LANG in obj['labels']:
        label = obj['labels'][LANG]['value']
        label = (label.replace('\t', ' ').replace('\n', ' ')).encode('utf-8')
        label_fp.write(label + '\n')

    if label and 'aliases' in obj and LANG in obj['aliases']:
        aliases = [a['value'] for a in obj['aliases'][LANG]]
        for alias in aliases:
            alias_fp.write(label + '\t' + (alias.replace('\t', ' ').replace('\n', ' ') + '\n').encode('utf-8'))


with open(DATA_PATH + '/wikidata_dump.json', 'r') as f, \
    open(RESULT_NAMES_FP, 'w') as label_fp, \
    open(RESULT_ALIASES_FP, 'w') as alias_fp:

    for i, line in enumerate(f):
        line = line.rstrip()
        if line == '[' or line == ']':
            continue
        # strip trailing commas
        line = line.rstrip(',')
        parse_json(line, label_fp, alias_fp)

