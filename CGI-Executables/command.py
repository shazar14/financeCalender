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
elif(jsonData['request'] == 'billInfo'):
	jsonResults = db_interact.list_bills()
elif(jsonData['request'] == 'changeDay'):
	jsonResults = db_interact.change_day(jsonData['dayToChange'], jsonData['title'], jsonData['month'])
elif(jsonData['request'] == 'getBill'):
	jsonResults = db_interact.get_bill(jsonData['bill'], jsonData['date'])
elif(jsonData['request'] == 'getAccounts'):
	jsonResults = db_interact.get_accounts()
elif(jsonData['request'] == 'changeBill'):
	jsonResults = db_interact.change_bill(jsonData['stat'], jsonData['pay_type'], jsonData['bill'], jsonData['pay_method'], jsonData['amount'], jsonData['month'])

try:
  result = jsonResults
except ValueError:
  log.log_error("Error converting jsonResults: '%s' to jsonData\n\n" %jsonResults)
  sys.exit()

print "Content-Type: application/json"
print
print result
