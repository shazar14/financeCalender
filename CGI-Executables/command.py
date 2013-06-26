#!/usr/bin/env python

import sys
import json
import log
import db_interact
data=''

try:
	data = sys.stdin.readline()
except:
	log.log_error("Error reading '%s' from stdin\n\n" % data)
	sys.exit()

#turn the string into json
try:
  jsonData = json.loads(data)
except ValueError:
  log.log_error("Error converting stdin: '%s' to jsonData\n\n" % data[:-1])
  sys.exit()

if(jsonData['request'] == 'queryAll'):
	jsonResults = db_interact.get_all_bills()

try:
  result = json.loads(jsonResults)
except ValueError:
  log.log_error("Error converting jsonResults: '%s' to jsonData\n\n" %jsonResults)
  sys.exit()

print str(result)
