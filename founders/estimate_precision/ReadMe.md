{\rtf1\ansi\ansicpg1252\cocoartf1347\cocoasubrtf570
{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural

\f0\fs24 \cf0 To add a new file from Mindtag:\
	- pull form git\
	- export from Mintag	\
	- add the tags description, sentences_id, relation_id and is_correct\
	- choose the format insert.sql\
	- put the table name: tags_founder_precision_with_features_is_correct\
		(not needed if you don\'92t have any other tags)\
	- rename the file tags.sql and put it in this folder\
	- run estimate_precision.sh\
	- push to git}