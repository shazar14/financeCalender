#!/usr/env python

import MySQLdb
import datetime, calendar
import log
import sys
import decimal

############################################################
def connect_DB():
#	db = MySQLdb.connect("localhost","otis","toor","finances2" )
#	db = MySQLdb.connect("localhost","root","toor","finances" )
	db = MySQLdb.connect("localhost","root","toor","newFinances" )
	
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
def deleteStatus(bill_id):
	db, cursor = connect_DB()
	tables = ['tbl_January', 'tbl_February', 'tbl_March', 'tbl_April', 'tbl_May', 'tbl_June', 'tbl_July', 'tbl_August', 'tbl_September', 'tbl_October', 'tbl_November', 'tbl_December']
	query = "SELECT * FROM tbl_Bills WHERE id=%d" % int(bill_id)
	jsonResponse = '{ "name":'
	try:
		num_rows = cursor.execute(query)
	except MySQLdb.Error, e:
		print("MySQL Error [%d]: %s {%s}\n\n" %(e.args[0], e.args[1], query))
		close_DB(db)
		sys.exit(1)
	if num_rows > 1:
		return '{ "valid":"false"}'
	else:
		row = cursor.fetchone()
		jsonResponse = jsonResponse + '"' + row['name'] + '", "amount":"' + str(decimal.Decimal(row['amount_due'])) + '"}'
		return jsonResponse
		
			
#endef
############################################################
def delete(bill_id):
	db, cursor = connect_DB()
	tables = ['tbl_January', 'tbl_February', 'tbl_March', 'tbl_April', 'tbl_May', 'tbl_June', 'tbl_July', 'tbl_August', 'tbl_September', 'tbl_October', 'tbl_November', 'tbl_December']
	for table in tables:
		query = "SELECT * FROM %s WHERE bill_id=%d" %(table, int(bill_id))
		try:
			num_rows = cursor.execute( query )
		except MySQLdb.Error, e:
			print("MySQL Error [%d]: %s {%s}\n\n" %(e.args[0], e.args[1], query))
			close_DB(db)
			sys.exit(1)
		if(num_rows == 1):
			query = "DELETE FROM %s WHERE bill_id=%d" %(table, int(bill_id))
			try:
				cursor.execute(query)
				db.commit()
			except MySQLdb.Error, e:
				print("MySQL Error [%d]: %s {%s}\n\n" %(e.args[0], e.args[1], query))
				close_DB(db)
				sys.exit(1)
	query = "DELETE FROM tbl_Bills WHERE id=%d" % int(bill_id)
	try:
		cursor.execute(query)
		db.commit()
	except MySQLdb.Error, e:
		print("MySQL Error [%d]: %s {%s}\n\n" %(e.args[0], e.args[1], query))
		close_DB(db)
		sys.exit(1)

	return '{ "valid" : "true" }'
			
#endef

############################################################
def list_bills():
	db, cursor = connect_DB()
	counter = 0
	jsonResponse = '{'
	try:
		query = "SELECT tbl_Bills.id, tbl_Bills.name, tbl_Bills.amount_due, tbl_Bills.day_of_month, tbl_Bills.payment_type, tbl_Accounts.name AS account FROM tbl_Bills INNER JOIN tbl_Accounts ON tbl_Accounts.id=tbl_Bills.account_index"
		cursor.execute( query )
		rows = cursor.fetchall()
		for row in rows:
			singleRecord = '{ "id" : "' + isNull(row['id']) + '", "account" : "' + row['account'] + '", "name" : "' + row['name'] + '", "amount" : "' + isNull(row['amount_due']) + '", "dayofmonth" : "' + isNull(row['day_of_month']) + '", "paymentType" : "' + row['payment_type'] + '" }' 
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
def add_bill(name, amount, dueDay, pay_type, pay_account, months, repeat_options):
	db, cursor = connect_DB()
	
	if( pay_type == 'Manual'):
		pay_account = 'None'
	try:
		query = "SELECT id FROM tbl_Accounts WHERE name='%s'" % pay_account
		num_rows = cursor.execute( query )
		if( num_rows == 1):
			rows = cursor.fetchall()
			pay_account_id = rows[0]['id']
		else:
			return '{ "valid" : "db error" }'
	except MySQLdb.Error, e:
		print("MySQL Error [%d]: %s {%s}\n\n" %(e.args[0], e.args[1], query))
		close_DB(db)
		sys.exit(1)
		
	try:
		query = "INSERT INTO tbl_Bills(name, amount_due, day_of_month, payment_type, account_index) VALUES('%s', %.02f, %d, '%s', %d )" % (name, decimal.Decimal(amount), int(dueDay), pay_type, pay_account_id) 
		cursor.execute( query )
		db.commit()
	except MySQLdb.Error, e:
		print("MySQL Error [%d]: %s {%s}\n\n" %(e.args[0], e.args[1], query))
		close_DB(db)
		sys.exit(1)

	insertID = cursor.lastrowid
	current_month = datetime.datetime.now().month
	current_day = datetime.datetime.now().day
	#table = "tbl_" + calendar.month_name[int(current_month)]
	tables = ['tbl_January', 'tbl_February', 'tbl_March', 'tbl_April', 'tbl_May', 'tbl_June', 'tbl_July', 'tbl_August', 'tbl_September', 'tbl_October', 'tbl_November', 'tbl_December']
	if( repeat_options == 'monthly' and int(dueDay) >= current_day ):
		for i in range((current_month-1), 12):
			query = "INSERT INTO %s(bill_id, status, day_of_month, amount) VALUES(%d, 'Due', %d, %.02f)" % (tables[i], insertID, int(dueDay), decimal.Decimal(amount)) 	
			try:
				cursor.execute( query )
				db.commit()
			except MySQLdb.Error, e:
				print("MySQL Error [%d]: %s {%s}\n\n" %(e.args[0], e.args[1], query))
				close_DB(db)
				sys.exit(1)
	elif( repeat_options == 'monthly' and int(dueDay) < current_day):
		for i in range(current_month, 12):
			query = "INSERT INTO %s(bill_id, status, day_of_month, amount) VALUES(%d, 'Due', %d, %.02f)" % (tables[i], insertID, int(dueDay), decimal.Decimal(amount)) 	
			try:
				cursor.execute( query )
				db.commit()
			except MySQLdb.Error, e:
				print("MySQL Error [%d]: %s {%s}\n\n" %(e.args[0], e.args[1], query))
				close_DB(db)
				sys.exit(1)
	else:
		for month in months:
			query = "INSERT INTO tbl_%s(bill_id, status, day_of_month, amount) VALUES(%d, 'Due', %d, %.02f)" % (month, insertID, int(dueDay), decimal.Decimal(amount)) 	
			try:
				cursor.execute( query )
				db.commit()
			except MySQLdb.Error, e:
				print("MySQL Error [%d]: %s {%s}\n\n" %(e.args[0], e.args[1], query))
				close_DB(db)
				sys.exit(1)
			
	return '{ "valid" : "true" }'

#endef
############################################################
def change_bill(status, bill, amount, month):
	db, cursor = connect_DB()
	tables = ['tbl_January', 'tbl_February', 'tbl_March', 'tbl_April', 'tbl_May', 'tbl_June', 'tbl_July', 'tbl_August', 'tbl_September', 'tbl_October', 'tbl_November', 'tbl_December']
	
	query = "SELECT * FROM tbl_Bills WHERE name='%s'" % bill 
	cursor.execute(query)
	row = cursor.fetchone()

	query = "UPDATE %s SET status='%s', amount=%.02f WHERE bill_id=%d" % (tables[int(month)-1], status, decimal.Decimal(amount), row['id'])
	cursor.execute(query)
	db.commit()
	return '{ "valid" : "true" }'
	
#endef
############################################################
def change_all_bill(oldBillName, status, pay_type, bill, pay_account, amount, month, day):
	db, cursor = connect_DB()
	tables = ['tbl_January', 'tbl_February', 'tbl_March', 'tbl_April', 'tbl_May', 'tbl_June', 'tbl_July', 'tbl_August', 'tbl_September', 'tbl_October', 'tbl_November', 'tbl_December']

	query = "SELECT * FROM tbl_Bills WHERE name='%s'" % oldBillName
	try:
		cursor.execute(query)
	except MySQLdb.Error, e:
		print("MySQL Error [%d]: %s {%s}\n\n" %(e.args[0], e.args[1], query))
		close_DB(db)
		sys.exit(1)
	row = cursor.fetchone()

	query = "SELECT * FROM tbl_Accounts WHERE name='%s'" % pay_account
	try:
		cursor.execute(query)
	except MySQLdb.Error, e:
		print("MySQL Error [%d]: %s {%s}\n\n" %(e.args[0], e.args[1], query))
		close_DB(db)
		sys.exit(1)
	account = cursor.fetchone()
	account_index = account['id']
		
	query = "UPDATE tbl_Bills SET name='%s', day_of_month=%d, payment_type='%s', account_index=%d, amount_due=%.02f WHERE id=%d" % (bill, int(day), pay_type, account_index, decimal.Decimal(amount), row['id'])
	cursor.execute(query)
	db.commit()

	for i in range(int(month)-1, 12):
		query = "UPDATE %s SET status='%s', amount=%.02f, day_of_month=%d WHERE bill_id=%d" % (tables[i], status, decimal.Decimal(amount), int(day), row['id'])
		try:
			cursor.execute(query)
		except MySQLdb.Error, e:
			print("MySQL Error [%d]: %s {%s}\n\n" %(e.args[0], e.args[1], query))
			close_DB(db)
			sys.exit(1)
	
		db.commit()
	return '{ "valid" : "true" }'
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
			query = "SELECT %s.amount, tbl_Bills.day_of_month, tbl_Bills.payment_type, tbl_Accounts.name, %s.status FROM tbl_Bills INNER JOIN tbl_Accounts ON tbl_Accounts.id=tbl_Bills.account_index INNER JOIN %s ON %s.bill_id=tbl_Bills.id WHERE bill_id=%d" % (table, table, table, table, result['id'])
			cursor.execute( query )
			bills = cursor.fetchall()
			for bill in bills:
				jsonResponse = jsonResponse + '"day" : "' + isNull(bill['day_of_month']) + '", "amount" : "' + isNull(bill['amount']) + '", "pay_type" : "' + bill['payment_type'] + '", "account": "' + bill['name'] + '", "status" : "' + bill['status'] + '"'	 
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

	query = "SELECT name FROM `tbl_Accounts`"
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
def get_months(startMonth):
	db, cursor = connect_DB()
	tables = ['tbl_January', 'tbl_February', 'tbl_March', 'tbl_April', 'tbl_May', 'tbl_June', 'tbl_July', 'tbl_August', 'tbl_September', 'tbl_October', 'tbl_November', 'tbl_December']
	month = 1
	jsonResponse = '{'

	for i in range(int(startMonth), int(startMonth) + 3):
		query = "SELECT SUM(amount) AS sum FROM %s" % tables[i-1]
		cursor.execute( query )
		data = cursor.fetchall()
		jsonResponse = jsonResponse + ' "month' + str(month) + '": "' + calendar.month_name[int(i)] + '", "month' + str(month) + 'Total": "' + str(decimal.Decimal(data[0]['sum'])) + '", '
		month = month + 1

	return(jsonResponse[:-2] + ' }')
		
#endef
############################################################
def weeks(weeks):
	db, cursor = connect_DB()
	tables = ['tbl_January', 'tbl_February', 'tbl_March', 'tbl_April', 'tbl_May', 'tbl_June', 'tbl_July', 'tbl_August', 'tbl_September', 'tbl_October', 'tbl_November', 'tbl_December']
	week=1
	monthCost = 0
	monthDue = 0
	jsonResponse = '{'
	for i in range(0, 24, 4):
		cost = 0
		due = 0
		if weeks[i+2] > weeks[i]:
			query1 = "SELECT SUM(amount) AS sum FROM %s WHERE day_of_month >= %d" % (tables[weeks[i] - 1], weeks[i+1])
			query2 = "SELECT SUM(amount) AS sum  FROM %s WHERE day_of_month <= %d" % (tables[weeks[i+2] - 1], weeks[i+3])
			cursor.execute( query1 )
			data1 = cursor.fetchall()
			if data1[0]['sum'] != None:
				cost += decimal.Decimal(data1[0]['sum'])
				monthCost += decimal.Decimal(data1[0]['sum'])
			cursor.execute( query2 )
			data2 = cursor.fetchall()
			if data2[0]['sum'] != None:
				cost += decimal.Decimal(data2[0]['sum'])
				monthCost += decimal.Decimal(data2[0]['sum'])
		#	jsonResponse = jsonResponse + '"week' + str(week) + '":"' + str(decimal.Decimal(cost)) + '", '
			#print "[%d/%d-%d/%d] Week%s Total: %.02f\t" % (weeks[i], weeks[i+1], weeks[i+2], weeks[i+3], week, decimal.Decimal(cost)),

			cursor.execute( query1 + " AND status!='Paid'" )
			data = cursor.fetchall()
			if data[0]['sum'] != None:
				due += decimal.Decimal(data[0]['sum'])
				monthDue += decimal.Decimal(data[0]['sum'])
			cursor.execute( query2 + " AND status!='Paid'" )
			data = cursor.fetchall()
			if data[0]['sum'] != None:
				due += decimal.Decimal(data[0]['sum'])
				monthDue += decimal.Decimal(data[0]['sum'])
		#	jsonResponse = jsonResponse + '"week' + str(week) + 'Due":"' + str(decimal.Decimal(due)) + '", '
			#print "Remaining Due: %.02f" % decimal.Decimal(due)	
		else:
			query = "SELECT SUM(amount) AS sum FROM %s WHERE day_of_month >= %d and day_of_month <= %d" % (tables[weeks[i] - 1], weeks[i+1], weeks[i+3])
			cursor.execute( query )
			data = cursor.fetchall()
			if data[0]['sum'] != None:
				cost += decimal.Decimal(data[0]['sum'])
				monthCost += decimal.Decimal(data[0]['sum'])
			#jsonResponse = jsonResponse + '"week' + week + '":"' + decimal.Decimal(cost) + '", '
			#print "[%d/%d-%d/%d] Week%s Total: %.02f\t" % (weeks[i], weeks[i+1], weeks[i+2], weeks[i+3], week, decimal.Decimal(cost)),

			cursor.execute( query + " AND status!='Paid'" )
			data = cursor.fetchall()
			if data[0]['sum'] != None:
				due += decimal.Decimal(data[0]['sum'])
				monthDue += decimal.Decimal(data[0]['sum'])
			#jsonResponse = jsonResponse + '"week' + week + 'Due":"' + decimal.Decimal(due) + '", '
			#print "Remaining Due: %.02f" % decimal.Decimal(due)
		jsonResponse = jsonResponse + '"week' + str(week) + 'Due":"' + str(decimal.Decimal(due)) + '", "Date' + str(week) + '":"' + str(weeks[i]) + '/' + str(weeks[i+1]) + '-' + str(weeks[i+2]) + '/' + str(weeks[i+3]) + '", '
		jsonResponse = jsonResponse + '"week' + str(week) + '":"' + str(decimal.Decimal(cost)) + '", '
		week = week + 1
	jsonResponse = jsonResponse + '"calendarCost":"' + str(decimal.Decimal(monthCost)) + '", "calendarDue":"' + str(decimal.Decimal(monthDue)) + '"}'
	return(jsonResponse)
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
					#print name, day, status, payment_type, monthCounter, current_month, current_day, day
					status = 'Paid' 
					query2 = "UPDATE %s SET status='Paid' WHERE bill_id=%s" % (month, bill_id)
					cursor.execute(query2)
					db.commit()				
				#elif( monthCounter == 10 ):
				#	print name, day, status, payment_type, monthCounter, current_day
	
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

