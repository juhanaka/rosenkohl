#! /usr/bin/env bash

DBNAME=deepdive_founder

psql -d $DBNAME -c "drop table if exists temp_tags_raw;"

psql -d $DBNAME -c \
"""
CREATE TABLE temp_tags_raw
(
ROW_ID SERIAL PRIMARY KEY
,DATA  TEXT
);
COPY temp_tags_raw(DATA)
FROM '$APP_HOME/labeling/founder-precision_with_features/tags.json' DELIMITERS '#' CSV ;
"""

psql -d $DBNAME -c "drop table if exists temp_tags;"

psql -d $DBNAME -c \
"""
CREATE TABLE temp_tags
(ROW_ID   INT
,Relation_id VARCHAR(25) PRIMARY KEY
,is_correct VARCHAR(27)
  );

INSERT INTO temp_tags
SELECT
row_id
,TRIM(SPLIT_PART(SPLIT_PART(DATA, 'by_key:',2), ', is_correct',1)) AS Relation_id
,TRIM(replace(SPLIT_PART(SPLIT_PART(DATA, ', type:',2), ', type:',1), '}','')) AS is_correct
FROM temp_tags_raw;
"""

