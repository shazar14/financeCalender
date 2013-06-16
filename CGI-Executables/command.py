#!/usr/bin/env python

import json
import log
import db_interact

try:
	data = sys.stdin.readline()
except:
	log.log_error("Error reading '%s' from stdin\n\n" % data[:-1])
	sys.exit()

#turn the string into json
try:
  jsonData = json.loads(data)
except ValueError:
  log.log_error("Error converting stdin: '%s' to jsonData\n\n" % data[:-1])
  sys.exit()

if(jsonData['request'] == 'queryAll'):
	jsonResults = db_interact.get_all_bills()
