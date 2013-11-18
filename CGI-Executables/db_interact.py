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

	db = MySQLdb.connect("localhost","root","toor","testFinances" )
	
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
		query = "SELECT *, tbl_Accounts.name as account FROM tbl_Bills INNER JOIN tbl_Accounts ON tbl_Accounts.id=tbl_Bills.account_index"
		#query = "SELECT tbl_Bills.id, tbl_Bills.name, tbl_Bills.amount_due, tbl_Bills.day_of_month, tbl_Bills.payment_type, tbl_Accounts.name AS account FROM tbl_Bills INNER JOIN tbl_Accounts ON tbl_Accounts.id=tbl_Bills.account_index"
		cursor.execute( query )
		rows = cursor.fetchall()
		for row in rows:
			singleRecord = '{ "id" : "' + isNull(row['id']) + '", "account" : "' + row['account'] + '", "name" : "' + row['name'] + '", "amount" : "' + isNull(row['amount']) + '", "dayofmonth" : "' + isNull(row['date']) + '", "paymentType" : "' + row['pay_type'] + '" }' 
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
	currentYear = datetime.datetime.now().year
	currentMonth = datetime.datetime.now().month
	currentDay = datetime.datetime.now().day

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
		
	if repeat_options == 'monthly':
		#calculate if the bill should start this month
		if( dueDay >= currentDay):
			date = datetime.date(currentYear, currentMonth, int(dueDay)) 
		else:
			if(currentMonth == 12):
				date = datetime.date(currentYear + 1, 1, int(dueDay))
			else:
				date = datetime.date(currentYear, currentMonth + 1, int(dueDay)) 
		for i in range(0, 24):
			try:
				query = "INSERT INTO tbl_Bills(status, name, amount, date, pay_type, account_index) VALUES('Due', '%s', %.02f, '%s', '%s', %d )" % (name, decimal.Decimal(amount), date, pay_type, pay_account_id) 
				cursor.execute( query )
				db.commit()
			except MySQLdb.Error, e:
				print("MySQL Error [%d]: %s {%s}\n\n" %(e.args[0], e.args[1], query))
				close_DB(db)
				sys.exit(1)
			#calculate date for the next month
			if date.month == 12:
				date = datetime.date(date.year + 1, 1, int(dueDay))
			else:
				if int(dueDay) > calendar.monthrange(date.year, date.month + 1)[1]:
					date = datetime.date(date.year, date.month + 1, calendar.monthrange(date.year, date.month + 1)[1])
				else:
					date = datetime.date(date.year, date.month + 1, int(dueDay))

	else:
		for month in months:
			if int(month) < currenMonth and int(dueDay) < currentDay: 	
				if int(dueDay) > calendar.monthrange(currentYear + 1, int(month))[1]:
					date = datetime.date(currentYear + 1, int(month), calendar.monthrange(currentYear + 1, int(month))[1])
				else:
					date = datetime.date(currentYear + 1, int(month), int(dueDay))
			else:
				if int(dueDay) > calendar.monthrange(currentYear, int(month))[1]:
					date = datetime.date(currentYear, int(month), calendar.monthrange(currentYear, int(month))[1])
				else:
					date = datetime.date(currentYear, int(month), int(dueDay))
			
			query = "INSERT INTO tbl_Bills(name, pay_type, account_index, status, date, amount) VALUES('%s', '%s', %d, 'Due', %s, %.02f)" % (name, pay_type, pay_account_id, date, decimal.Decimal(amount)) 	
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
def get_months(startMonth, year):
	db, cursor = connect_DB()
	monthCnt = 1
	jsonResponse = '{'

	for i in range(0, 3):
		yr = int(year)
		sm = int(startMonth)
		if(sm > 10):
			if sm + i > 12:
				month = sm + i - 12
				yr = yr + 1
			else:
				month = sm + i
		else:
			month = int(startMonth) + i

		query = "SELECT SUM(amount) AS sum FROM tbl_Bills WHERE date BETWEEN '%s' AND '%s'" %(datetime.date(int(yr), month, 1), datetime.date(int(yr), month, calendar.monthrange(int(yr), month)[1]))
		cursor.execute( query )
		data = cursor.fetchall()

		if(data[0]['sum'] == None):
			tot = 0
		else:
			tot = data[0]['sum']
		jsonResponse = jsonResponse + ' "month' + str(monthCnt) + '": "' + calendar.month_name[month] + '", "month' + str(monthCnt) + 'Total": "' + str(tot) + '", '
		monthCnt = monthCnt + 1

	return(jsonResponse[:-2] + ' }')
		
#endef
############################################################
def weeks(weeks):
	db, cursor = connect_DB()
	week=1
	monthCost = 0
	monthDue = 0
	jsonResponse = '{'
	for i in range(0, 35, 6):
		cost = 0
		due = 0

		#calculate total for the week
		query = "SELECT SUM(amount) AS sum FROM tbl_Bills WHERE date BETWEEN '%s' AND '%s'" % (datetime.date(int(weeks[i+2]), weeks[i], weeks[i+1]), datetime.date(int(weeks[i+5]), weeks[i+3], weeks[i+4]))
		cursor.execute( query )
		data = cursor.fetchall()
		if data[0]['sum'] != None:
			cost = data[0]['sum']
			monthCost += decimal.Decimal(data[0]['sum'])
		else:
			cost = 0
			monthCost += 0

		#calculate the total remaining amount due for the month
		query = query + " AND status != 'Paid'"
		cursor.execute( query )
		
		data1 = cursor.fetchall()
		if data1[0]['sum'] != None:
			monthDue += decimal.Decimal(data1[0]['sum'])
			due = decimal.Decimal(data1[0]['sum'])

		jsonResponse = jsonResponse + '"week' + str(week) + 'Due":"' + str(decimal.Decimal(due)) + '", "Date' + str(week) + '":"' + str(weeks[i]) + '/' + str(weeks[i+1]) + '-' + str(weeks[i+3]) + '/' + str(weeks[i+4]) + '", '
		jsonResponse = jsonResponse + '"week' + str(week) + '":"' + str(decimal.Decimal(cost)) + '", '
		week = week + 1
	jsonResponse = jsonResponse + '"calendarCost":"' + str(decimal.Decimal(monthCost)) + '", "calendarDue":"' + str(decimal.Decimal(monthDue)) + '"}'
	return(jsonResponse)
#endef

############################################################
def get_all_bills():
	db, cursor = connect_DB()
	year = datetime.datetime.now().year
	current_day = datetime.datetime.now().day
	current_month = datetime.datetime.now().month
	counter = 0
	jsonResponse = '{'
	try:
		query = "SELECT *, tbl_Accounts.name AS account FROM tbl_Bills INNER JOIN tbl_Accounts ON tbl_Accounts.id=tbl_Bills.account_index"
		numrecords = cursor.execute( query )
		data = cursor.fetchall()
		if numrecords == 0:
			return jsonResponse + ' }'
		for result in data:
			bill_id		     = result['id']
			name          	     = result['name']
			amount_due           = result['amount']
			date  		     = result['date']
			status    	     = result['status']
			payment_type	     = result['pay_type']
			pay_account	     = result['account']

			#blue out the automatically paid bills
			if( date.year == year and date.month == current_month and current_day > int(date.day) and payment_type == 'Automatic'):
					status = 'Paid' 
					query2 = "UPDATE tbl_Bills SET status='Paid' WHERE id=%s" % bill_id
					cursor.execute(query2)
					db.commit()				
	
			singleRecord = '{ "status" : "' + payment_type + '", "account" : "' + pay_account + '", "currentTitle" : "' + name + ': $' + isNull(amount_due) + '", "currentDate" : "' + isNull(date) + '", "currentStatus" : "' + status + '" }' 
			jsonResponse = jsonResponse + '"%s" : [ %s ], ' % (counter, singleRecord)
			counter += 1 
		jsonResponse = jsonResponse[:-2] + ' }'
	except MySQLdb.Error, e:
		log.log_error("MySQL Error [%d]: %s {%s}\n\n" %(e.args[0], e.args[1], query))
    		close_DB(db)
		return 0
	return jsonResponse
#endef

