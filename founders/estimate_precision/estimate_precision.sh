#! /usr/bin/env bash

DBNAME=deepdive_founder
threshold_expectation=0.9
file_name=tags.sql

if psql -lqt | cut -d \| -f 1 | grep -w $DBNAME; then
    echo "database " $DBNAME " already exists, adding new value"
  else
    echo "creating the db " $DBNAME
    createdb $DBNAME
fi

psql -d $DBNAME -c "drop table if exists permanent_tags_founder_precision_is_correct;"

psql -d $DBNAME < permanent_tags_founder_precision_is_correct.sql

if [ -f "$file_name" ]
  then
    perl -pi -e 's/tags_founder-precision_with_features_is_correct/tags_founder_precision_with_features_is_correct/' tags.sql

    psql $DBNAME < tags.sql

    psql -d $DBNAME -c \
    """
    CREATE TABLE IF NOT EXISTS permanent_tags_founder_precision_is_correct
    ( relation_id TEXT, 
      sentence_id TEXT, 
      is_correct TEXT, 
      description TEXT,
      expectation double precision
    );
    """

    psql -d $DBNAME -c \
    """
    DELETE FROM permanent_tags_founder_precision_is_correct
    where sentence_id IN 
    (SELECT tags_founder_precision_with_features_is_correct.sentence_id FROM tags_founder_precision_with_features_is_correct 
    where permanent_tags_founder_precision_is_correct.description = tags_founder_precision_with_features_is_correct.description);
    """

    psql -d $DBNAME -c \
    """
    INSERT INTO permanent_tags_founder_precision_is_correct
    SELECT t.relation_id, 
           t.sentence_id, 
           t.is_correct,
           t.description
    FROM tags_founder_precision_with_features_is_correct t;
    """
fi

psql -d $DBNAME -c \
"""
UPDATE permanent_tags_founder_precision_is_correct
SET expectation = 
(SELECT f.expectation
FROM is_founder_is_true_inference f
WHERE permanent_tags_founder_precision_is_correct.sentence_id= f.sentence_id
AND   permanent_tags_founder_precision_is_correct.description = f.description
LIMIT 1);
"""

pg_dump deepdive_founder -t permanent_tags_founder_precision_is_correct > permanent_tags_founder_precision_is_correct.sql

./create_graphs.sh