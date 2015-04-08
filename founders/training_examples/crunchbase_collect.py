import pycrunchbase

KEY_PATH = '~/Desktop/Research/Wikipedia/API\ keys/crunchbase'
FILENAME = 'crunchbase_examples'

def retrieve_key():
    with open(KEY_PATH) as f:
        for i,line in f:
            key=line
    return key

def get_examples(filename_examples):
    # retrieve API key
    #key = retrieve_key()
    key = '84d68769d2c83a7889ba864594d00e81'
    cb = pycrunchbase.CrunchBase(key)
    pos_ex = {}
    neg_ex ={}

    with open(filename_examples) as f:
        for i,name in enumerate(f):
            
            try:
                company = cb.organization(name)

            # positive examples
                founders = [founder.name.encode('ascii','ignore') for founder in company.founders]

            # add them to dict of positive examples
                pos_ex[name] = founders

            # build negative examples from board members not in the founders
            
            # retrieve board members that are not founders and add them to dict
                board = [(mem.first_name+' '+mem.last_name).encode('ascii','ignore') for mem in 
                    company.board_members_and_advisors]
                neg_examples = [person for person in board if person not in founders]
                neg_ex[name] = neg_examples
            except Exception as e:
                pass

    write_to_file(pos_ex,neg_ex,FILENAME)

def write_to_file(pos,neg,filename):
    output = open(filename,'w+')
    for p_ex in pos:
        for k,founder in enumerate(pos[p_ex]):
            output.write(p_ex.rstrip()+'\t'+founder+'\t'+str(1)+'\n')
    for p_ne in neg:
        for k,notfounder in enumerate(neg[p_ne]):
            output.write(p_ne.rstrip()+'\t'+notfounder+'\t'+str(0)+'\n')

    

