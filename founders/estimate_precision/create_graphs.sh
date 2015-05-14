#! /usr/bin/env bash

rm results.tsv

array=(0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95)
for i in "${array[@]}"
do
  psql -d deepdive_founder -c "SELECT count(*) FROM permanent_tags_founder_precision_is_correct WHERE expectation > $i and is_correct='true';" -t >> results.tsv
done


for i in "${array[@]}"
do
  psql -d deepdive_founder -c "SELECT count(*) FROM permanent_tags_founder_precision_is_correct WHERE expectation > $i and is_correct='false';" -t >> results.tsv
done

for i in "${array[@]}"
do
  psql -d deepdive_founder -c "SELECT count(*) FROM is_founder_is_true_inference WHERE expectation > $i;" -t >> results.tsv
done

./calculus.py