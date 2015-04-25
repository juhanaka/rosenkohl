psql -d deepdive_founder -c """DROP TABLE IF EXISTS founder_company CASCADE;"""

psql -d deepdive_founder -c \
"""
CREATE TABLE founder_company(
  founder text, 
  company text
);
"""

psql -d deepdive_founder -c """DROP TABLE IF EXISTS founder_sentences CASCADE;"""

psql -d deepdive_founder -c \
"""
CREATE TABLE founder_sentences(
  founder text, 
  company text, 
  sentence text,
  sentence_id text
);
"""


ghead -n -0 founder_company.tsv | psql -d deepdive_founder -c "copy founder_company from STDIN;"

psql -d deepdive_founder -c \
"""
INSERT INTO founder_sentences
SELECT founder_company.founder, 
       founder_company.company, 
       sentences.sentence,
       sentences.sentence_id
FROM founder_company, 
     people_mentions,
     sentences
WHERE founder_company.founder = people_mentions.text
  AND people_mentions.sentence_id = sentences.sentence_id;
"""