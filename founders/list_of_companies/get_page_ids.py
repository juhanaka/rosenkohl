import MySQLdb
BATCH_SIZE = 1000

def get_ids(input_filename,output_filename='ids_1',limited=0):
    # limited is for development/testing
    # ADD USER and PASSWD from credentials on remote machine
    db=MySQLdb.connect(host="commonswiki.labsdb",user="",passwd="",db="enwiki_p")
    cursor = db.cursor()
    sql_query = "SELECT page_id FROM page WHERE page_title IN (%s)"
    current_batch=[]
    with open(input_filename) as input_names:
        for i,name in enumerate(input_names):
            if i % BATCH_SIZE == 0 and i>0:
                try:
		    sql_query = "SELECT page_id FROM page WHERE page_title IN (%s)"
                    in_p =", ".join(map(lambda x: '%s', current_batch))
		    sql_query = sql_query % in_p 
		    #print current_batch
		    cursor.execute(sql_query,current_batch)
                #cursor.execute("SELECT page_id FROM page WHERE page_title IN (%s)"
		    data = cursor.fetchall()
                    #print data
		    write_out(output_filename,data)
                except:
                    continue
                current_batch=[]
	    if limited!=0 and i>=BATCH_SIZE+1:
                return
            current_batch.append(name.rstrip().replace (" ", "_"))



def write_out(output_filename,data):
    with open(output_filename,"a") as f:
        for i,line in enumerate(data):
            id = line[0]
            f.write(str(id)+"\n")
# initialize the file ids
open('ids_1', 'w').close()
get_ids('names.tsv')
