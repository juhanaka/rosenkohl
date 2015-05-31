#! /usr/bin/env bash

rm results.tsv
DBNAME=deepdive_family


array=(0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95)
for i in "${array[@]}"
do
  psql -d $DBNAME -c "SELECT count(*) FROM permanent_tags_family_parent_precision_is_correct WHERE expectation > $i and is_correct='true';" -t >> results.tsv
done


for i in "${array[@]}"
do
  psql -d $DBNAME -c "SELECT count(*) FROM permanent_tags_family_parent_precision_is_correct WHERE expectation > $i and is_correct='false';" -t >> results.tsv
done

for i in "${array[@]}"
do
  psql -d $DBNAME -c "SELECT count(*) FROM has_parent_is_true_inference WHERE expectation > $i;" -t >> results.tsv
done

for i in "${array[@]}"
do
  psql -d $DBNAME -c "SELECT count(*) FROM permanent_tags_family_parent_precision_is_correct WHERE expectation > $i and is_correct='true';" -t >> results.tsv
done

psql -d $DBNAME -c "SELECT count(*) FROM permanent_tags_family_parent_precision_is_correct WHERE is_correct='true';" -t >> results.tsv

./calculus.py