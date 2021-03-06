

def load_aliases(aliases_filename):
    aliases = {}
    with open(aliases_filename) as f:
        for i,line in enumerate(f):
            line = line.split('\t')
            name = line[0]
            alias = line[1].rstrip()
            if name in aliases:
                aliases[name].append(alias)
            else:
                aliases[name] = [alias]
    return aliases

def extend_examples(example_filename,aliases_filename,output_filename='examples_with_aliases'):
    output = open(output_filename, 'w')
    aliases = load_aliases(aliases_filename)
    with open(example_filename) as f:
        for i,line in enumerate(f):
            tokens = line.split('\t')
            orig_name = tokens[0]
            # write original line
            output.write(line.rstrip()+'\n')
            if orig_name in aliases:
                for j,alias in enumerate(aliases[orig_name]):
                    new_line = [alias]
                    for l,token in enumerate(tokens[1:]):
                        new_line.append(token.rstrip())
                    print new_line
                    output.write('\t'.join(new_line)+'\n')
    output.close()


#extend_examples('data/names.tsv','data/aliases.tsv')

def write_everything(example_filename,aliases_filename,output_filename='names_with_aliases'):
    names = set()
    with open(example_filename) as f:
        for i, line in enumerate(f):
            names.add(line.rstrip())
    with open(aliases_filename) as f:
        for i,line in enumerate(f):
            line = line.split('\t')
            names.add(line[0])
            names.add(line[1].rstrip())
    with open(output_filename,'w') as out:
        for name in names:
            out.write(name+'\n')

write_everything('data/names.tsv','data/aliases.tsv')