#!/usr/env python

import MySQLdb
import datetime, calendar
import log
import sys
import decimal

############################################################
def connect_DB():
#	db = MySQLdb.connect("localhost","otis","toor","finances2" )
	db = MySQLdb.connect("localhost","root","toor","finances" )
	
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
def add_bill(name, amount, dueDay, pay_type, pay_account):
	db, cursor = connect_DB()



	return '{ "valid" : "true" }'

#endef
############################################################
def change_bill(status, pay_type, bill, pay_account, amount, month):
	db, cursor = connect_DB()
	table = "tbl_" + calendar.month_name[int(month)]
	
	query = "SELECT id FROM tbl_Bills WHERE name='%s'" % bill 
	records = cursor.execute(query)
	if(records == 0 or records > 1):
		return '{ "valid" : "false"}'
	else:
		results = cursor.fetchall()
		for result in results:
			query = "UPDATE %s SET status='%s', amount=%.02f WHERE bill_id=%d" % (table, status, decimal.Decimal(amount), result['id'])
			cursor.execute(query)
			db.commit()
	

#endef
############################################################
def change_day(dayToChange, title, monthToChange):
	db, cursor = connect_DB()
	#get the title of the bill
	bill_name = title.split(":")[0]
	#build the tbl name from the monthToChange
	table = "tbl_" + calendar.month_name[int(monthToChange)]
	
	query = "SELECT id FROM tbl_Bills WHERE name='%s'" % bill_name
	records = cursor.execute( query )
	if(records == 0 or records > 1):
		return
	else:
		results = cursor.fetchall()	
		for result in results:
			query = "UPDATE %s SET day_of_month=%d WHERE bill_id=%d" % (table, int(dayToChange), result['id'])
			cursor.execute( query )
			db.commit()

#endef
############################################################
def get_bill(bill, billMonth):
	db, cursor = connect_DB()
	jsonResponse = '{'
	
	table = "tbl_" + calendar.month_name[int(billMonth)]
	query = "SELECT id FROM tbl_Bills WHERE name='%s'" % bill
	records = cursor.execute( query )
	if(records == 0 or records > 1):
		return
	else:
		results = cursor.fetchall()
		for result in results:
			query = "SELECT %s.amount, tbl_Bills.payment_type, tbl_Accounts.name, %s.status FROM tbl_Bills INNER JOIN tbl_Accounts ON tbl_Accounts.id=tbl_Bills.account_index INNER JOIN %s ON %s.bill_id=tbl_Bills.id WHERE bill_id=%d" % (table, table, table, table, result['id'])
			cursor.execute( query )
			bills = cursor.fetchall()
			for bill in bills:
				jsonResponse = jsonResponse + '"amount" : "' + isNull(bill['amount']) + '", "pay_type" : "' + bill['payment_type'] + '", "account": "' + bill['name'] + '", "status" : "' + bill['status'] + '"'	 
			return jsonResponse + ' }'
#endef
############################################################
def add_account(account):
	db, cursor = connect_DB()

	query = "INSERT INTO tbl_Accounts(name) VALUES('%s')" % MySQLdb.escape_string(account)
	cursor.execute( query )
	db.commit()
	return '{ "valid" : "true"}'

#endef
############################################################
def get_accounts():
	db, cursor = connect_DB()
	jsonResponse = '{'
	counter = 0

	query = "SELECT name FROM `tbl_Accounts` WHERE name!='None'"
	cursor.execute( query )
	results = cursor.fetchall()
	for result in results:
		if( counter == len(results) - 1):
			jsonResponse = jsonResponse + ' "' + str(counter) + '" : "' + result['name'] + '" }'
		else:
			jsonResponse = jsonResponse + ' "' + str(counter) + '" : "' + result['name'] + '", '
		counter = counter + 1
	return jsonResponse
			

#endef
############################################################
def get_all_bills():
	db, cursor = connect_DB()
	tables = ['tbl_January', 'tbl_February', 'tbl_March', 'tbl_April', 'tbl_May', 'tbl_June', 'tbl_July', 'tbl_August', 'tbl_September', 'tbl_October', 'tbl_November', 'tbl_December']
	monthCounter = 1
	year = datetime.datetime.now().year
	current_day = datetime.datetime.now().day
	current_month = datetime.datetime.now().month
	counter = 0
	jsonResponse = '{'
	try:
		for month in tables:
			query = "SELECT %s.bill_id, tbl_Bills.name, %s.amount, %s.day_of_month, tbl_Bills.payment_type, tbl_Accounts.name AS account, %s.status FROM tbl_Bills INNER JOIN tbl_Accounts ON tbl_Accounts.id=tbl_Bills.account_index INNER JOIN %s ON %s.bill_id=tbl_Bills.id" % (month, month, month, month, month, month)
			cursor.execute( query )
			data = cursor.fetchall()
			numRecords = 0
			for result in data:
				bill_id		     = result['bill_id']
				name          	     = result['name']
				amount_due           = result['amount']
				day  		     = result['day_of_month']
				status    	     = result['status']
				payment_type	     = result['payment_type']
				pay_account	     = result['account']

				if(monthCounter == 2 and day > 28):
					day = 28
				due_date = datetime.datetime( year, monthCounter, int(day) )
				due_date = datetime.date.strftime( due_date, "%Y-%m-%d" )
				#blue out the automatically paid bills
				if( monthCounter == current_month and current_day > int(day) and payment_type == 'Automatic'):
					status = 'Paid' 
					query2 = "UPDATE %s SET status='Paid' WHERE bill_id=%s" % (month, bill_id)
					cursor.execute(query2)
					db.commit()				
	
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
#list_bills()
