#! /usr/bin/env bash

psql -d deepdive_founder -c "SELECT count(*) FROM permanent_tags_founder_precision_is_correct WHERE expectation > 0.9 and is_correct='true';" -t >> results.txt