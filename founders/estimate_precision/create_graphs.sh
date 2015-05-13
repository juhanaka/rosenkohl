#! /usr/bin/env bash

array=(0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95)
for i in "${array[@]}"
do
  psql -d deepdive_founder -c "SELECT count(*) FROM permanent_tags_founder_precision_is_correct WHERE expectation > $i and is_correct='true';" -t >> results.txt
done


for i in "${array[@]}"
do
  psql -d deepdive_founder -c "SELECT count(*) FROM permanent_tags_founder_precision_is_correct WHERE expectation > $i and is_correct='false';" -t >> results.txt
done
