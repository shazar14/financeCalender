#!/usr/env python

import MySQLdb
import datetime
import log
import sys
import decimal

############################################################
def connect_DB():
#	db = MySQLdb.connect("localhost","otis","toor","finances2" )
	db = MySQLdb.connect("localhost","root","toor","finances2" )
	
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	#cursor = db.cursor()
	return db, cursor
#endef

###############################################################################
def isNull( string ):

  if(type(string) is str):
    return string
  elif(type(string) is datetime.date):
    return string.strftime("%Y-%m-%d")
  elif(type(string) is int) or (type(string) is long) or (type(string) is decimal.Decimal):
    return str(string)
  else:
    return ''
#endef ISNULL

############################################################
def close_DB(db):
	db.close()
#endef

############################################################
def change_months():
	"""

		should be ran on the first of each month to move the current due dates and status' to past month, move next month due dates and status' to current month
		and set next month status' and due dates

		input:  nothing
		return: nothing
		
	"""
	#get todays date
	now = datetime.datetime.now()

	#store the month in a two digit format
	month = '%02d' % now.month
	next_month = '%02d' % (now.month + 1)
	year = now.year

	#loop through the bills
	for i in range(2, 16):
		try:
			query = "SELECT day_of_month, current_month_due, current_status, next_status FROM tbl_Bills WHERE id=%d" % i
			#get the day of the month they are due
			cursor.execute( query )
			rows = cursor.fetchall()
			#if the day is a single digit add a 0 in front of it to match mysql date format
			for row in rows:
				if(row['day_of_month'] < 10):
					day = "0%d" % row['day_of_month']
				else:
					day = row['day_of_month']
				#take the current months dates and status and put them in last months columns
				updateLastMonth = "UPDATE tbl_Bills SET past_month_due='%s', prev_status='%s' WHERE id=%d" % (row['current_month_due'], row['current_status'], i)
				#set the new current month columns and take next months status (in case next month is already paid for a bill) and put them as current month
				updateThisMonth = "UPDATE tbl_Bills SET current_month_due='%s-%s-%s', current_status='%s' WHERE id=%d" % (year, month, day, row['next_status'], i)
				#set the next months new due dates and set all status' to due
				updateNextMonth = "UPDATE tbl_Bills SET next_month_due='%s-%s-%s', next_status='Due' WHERE id=%d" % (year, next_month, day, i)
				cursor.execute(updateLastMonth)
				cursor.execute(updateThisMonth)
				cursor.execute(updateNextMonth)
				db.commit()
		except MySQLdb.Error, e:
                	print("MySQL Error [%d]: %s {%s}\n\n" %(e.args[0], e.args[1], query))
                	close_DB(db)
			sys.exit(1)
#endef
############################################################
def list_bills():
	db, cursor = connect_DB()
	counter = 0
	jsonResponse = '{'
	try:
		query = "SELECT tbl_Bills.name, tbl_Bills.amount_due, tbl_Bills.day_of_month, tbl_Bills.payment_type, tbl_Accounts.name AS account FROM tbl_Bills INNER JOIN tbl_Accounts ON tbl_Accounts.id=tbl_Bills.account_index"
		cursor.execute( query )
		rows = cursor.fetchall()
		for row in rows:
			singleRecord = '{ "account" : "' + row['account'] + '", "name" : "' + row['name'] + '", "amount" : "' + isNull(row['amount_due']) + '", "dayofmonth" : "' + isNull(row['day_of_month']) + '", "paymentType" : "' + row['payment_type'] + '" }' 
			if(counter == len(rows) - 1):
				jsonResponse = jsonResponse + '"%s" : [ %s ] }' % (counter, singleRecord)
			else:
				jsonResponse = jsonResponse + '"%s" : [ %s ], ' % (counter, singleRecord)
			counter += 1 
	except MySQLdb.Error, e:
		print("MySQL Error [%d]: %s {%s}\n\n" %(e.args[0], e.args[1], query))
		close_DB(db)
		sys.exit(1)
	return jsonResponse
	
#endef
############################################################
def bill_info():
	db, cursor = connect_DB()
	tables = ['tbl_January', 'tbl_February', 'tbl_March', 'tbl_April', 'tbl_May', 'tbl_June', 'tbl_July', 'tbl_August', 'tbl_September', 'tbl_October', 'tbl_November', 'tbl_December']
	try:
		query = "SELECT * FROM tbl_Bills"
		cursor.execute( query ) 
		rows = cursor.fetchall()
		for row in rows:
			for month in tables:
				if(month == 'tbl_August' or month == 'tbl_September' or month == 'tbl_October' or month == 'tbl_November' or month == 'tbl_December'):
					status = 'Due'
				else:
					status = 'Paid'

				query = "UPDATE %s SET day_of_month=%d WHERE bill_id=%d" % (month, row['day_of_month'], row['id'])
				cursor.execute( query )
				db.commit()
	except MySQLdb.Error, e:
		print("MySQL Error [%d]: %s {%s}\n\n" %(e.args[0], e.args[1], query))
		close_DB(db)
		sys.exit(1)
#endef
############################################################
def get_all_bills():
	db, cursor = connect_DB()
	tables = ['tbl_January', 'tbl_February', 'tbl_March', 'tbl_April', 'tbl_May', 'tbl_June', 'tbl_July', 'tbl_August', 'tbl_September', 'tbl_October', 'tbl_November', 'tbl_December']
	monthCounter = 1
	year = datetime.datetime.now().year
	counter = 0
	jsonResponse = '{'
	try:
		for month in tables:
			query = "SELECT tbl_Bills.name, tbl_Bills.amount_due, %s.day_of_month, tbl_Bills.payment_type, tbl_Accounts.name AS account, %s.status FROM tbl_Bills INNER JOIN tbl_Accounts ON tbl_Accounts.id=tbl_Bills.account_index INNER JOIN %s ON %s.bill_id=tbl_Bills.id" % (month, month, month, month)
			cursor.execute( query )
			data = cursor.fetchall()
			numRecords = 0
			for result in data:
				name          	     = result['name']
				amount_due           = result['amount_due']
				day  		     = result['day_of_month']
				status    	     = result['status']
				payment_type	     = result['payment_type']
				pay_account	     = result['account']

				if(monthCounter == 2 and day > 28):
					day = 28
				due_date = datetime.datetime( year, monthCounter, int(day) )
				due_date = datetime.date.strftime( due_date, "%Y-%m-%d" )
			
				singleRecord = '{ "status" : "' + payment_type + '", "account" : "' + pay_account + '", "currentTitle" : "' + name + ': $' + isNull(amount_due) + '", "currentDate" : "' + isNull(due_date) + '", "currentStatus" : "' + status + '" }' 
				if(month == 'tbl_December' and numRecords == len(data) - 1):
					jsonResponse = jsonResponse + '"%s" : [ %s ] }' % (counter, singleRecord)
				else:
					jsonResponse = jsonResponse + '"%s" : [ %s ], ' % (counter, singleRecord)
				counter += 1 
				numRecords += 1
			monthCounter += 1
	except MySQLdb.Error, e:
		log.log_error("MySQL Error [%d]: %s {%s}\n\n" %(e.args[0], e.args[1], query))
    		close_DB(db)
		return 0
	return jsonResponse
#endef

#################
#     MAIN      #
#################

#db, cursor = connect_DB()
#change_months()
#result = get_all_bills()
#print result
#close_DB(dbl)
list_bills()
