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

psql -d deepdive_founder -c """DROP TABLE IF EXISTS company_sentences CASCADE;"""

psql -d deepdive_founder -c \
"""
CREATE TABLE company_sentences(
  company text, 
  founder text, 
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

psql -d deepdive_founder -c \
"""
INSERT INTO company_sentences
SELECT founder_company.company, 
       founder_company.founder, 
       sentences.sentence,
       sentences.sentence_id
FROM founder_company, 
     company_mentions,
     sentences
WHERE founder_company.company = company_mentions.text
  AND company_mentions.sentence_id = sentences.sentence_id;
"""