

dd_ext=set()
with open('extracted_companies') as f:
    for i,line in enumerate(f):
        try:
            line = line.split('-')
            dd_ext.add(line[1].rstrip())
        except:
# one error, no big deal
            continue


wiki = set()
with open('companies_with_founders.tsv') as f:
    for i,line in enumerate(f):
        wiki.add(line.rstrip())

print len(dd_ext-wiki)