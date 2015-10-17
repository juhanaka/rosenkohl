#!/usr/local/bin/python

for relation in ['child', 'parent', 'sibling', 'spouse']:
	with open('./has_' + relation + '_result.tsv') as file_relation:
		with open('./' + relation + '_postprocessed.tsv', 'w') as f_write:
			count=0
			for line in file_relation:	
				count +=1
				if count <2:
					f_write.write(line)
				else:
					line_splits = line.split('\t')
					name1=line_splits[1].split("-")[0]
					name2=line_splits[1].split("-")[1]
					#Rule 1: if name2 is "Jr.", add the name of the parent
					if name2=='Jr' or name2=='Jr.':
						name2 = name1 + ', Jr.'
					#Rule 2: if name2 has only first name, add last name of name1
					if len(name2.split(" "))  <2 and len(name1.split(" ")) < 4:
						for i in name1.split(" ")[1:]:
							name2 = name2 + " " + i
						# print line_splits[0] + '\t' + name1+'-'+name2 + '\t' + line_splits[2]
					f_write.write(line_splits[0] + '\t' + name1+'-'+name2 + '\t' + line_splits[2])
