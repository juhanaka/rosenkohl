psql -d deepdive_founder -c """DROP TABLE IF EXISTS list_companies CASCADE;"""

psql -d deepdive_founder -c \
"""
CREATE TABLE list_companies(
  company text
);
"""

psql -d deepdive_founder -c """DROP TABLE IF EXISTS is_founder_interesting_companies CASCADE;"""

psql -d deepdive_founder -c \
"""
CREATE TABLE is_founder_interesting_companies(
  person_id text,
  company_id text,
  sentence_id text,
  description text,
  is_true boolean,
  relation_id text, -- unique identifier for is_founder
  id bigint, 
  category bigint,
  expectation double precision
);
"""

ghead -n -0 names.tsv | psql -d deepdive_founder -c "copy list_companies from STDIN;"

psql -d deepdive_founder -c \
"""
INSERT INTO is_founder_interesting_companies
SELECT DISTINCT person_id,
       company_id,
       is_founder_is_true_inference.sentence_id,
       description,
       is_true,
       relation_id, -- unique identifier for is_founder
       id,
       category, 
       expectation
FROM is_founder_is_true_inference,
     list_companies,
     company_mentions
WHERE is_founder_is_true_inference.company_id = company_mentions.mention_id
AND   lower(company_mentions.text) = lower(list_companies.company);
"""