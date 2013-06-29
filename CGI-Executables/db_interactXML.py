#!/usr/env python

import MySQLdb
import datetime
import log
from xml.dom.minidom import Document
import sys
import pdb
############################################################
def connect_DB():
	db = MySQLdb.connect("localhost","otis","toor","finances2" )
#	db = MySQLdb.connect("localhost","root","toor","finances" )

	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	return db, cursor
#endef

###############################################################################
def isNull( string ):

  if(type(string) is str):
    return string
  elif(type(string) is datetime.datetime):
    return string.strftime("%Y-%m-%d %H:%M:%S")
  elif(type(string) is int) or (type(string) is long):
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
		#get the day of the month they are due
		cursor.execute("SELECT day_of_month, current_month_due, current_status, next_status FROM tbl_Bills WHERE id=%d" %i)
		data = cursor.fetchone()
		#if the day is a single digit add a 0 in front of it to match mysql date format
		if(data[0] < 10):
			day = "0%d" % data[0]
		else:
			day = data[0]
		#take the current months dates and status and put them in last months columns
		updateLastMonth = "UPDATE tbl_Bills SET past_month_due='%s', prev_status='%s' WHERE id=%d" % (data[1], data[2], i)
		#set the new current month columns and take next months status (in case next month is already paid for a bill) and put them as current month
		updateThisMonth = "UPDATE tbl_Bills SET current_month_due='%s-%s-%s', current_status='%s' WHERE id=%d" % (year, month, day, data[3], i)
		#set the next months new due dates and set all status' to due
		updateNextMonth = "UPDATE tbl_Bills SET next_month_due='%s-%s-%s', next_status='Due' WHERE id=%d" % (year, next_month, day, i)
		cursor.execute(updateLastMonth)
		cursor.execute(updateThisMonth)
		cursor.execute(updateNextMonth)
		db.commit()
#endef
############################################################
def get_all_bills():
	db, cursor = connect_DB()
	try:
		query = "SELECT tbl_Bills.id, tbl_Bills.name, tbl_Bills.amount_due, tbl_Bills.current_month_due, tbl_Bills.current_status, tbl_Accounts.name as AccountName, tbl_Bills.next_month_due, tbl_Bills.next_status, tbl_Bills.past_month_due, tbl_Bills.prev_status FROM tbl_Bills INNER JOIN tbl_Accounts ON tbl_Bills.account_index=tbl_Accounts.id WHERE 1"
		cursor.execute(query)
		data = cursor.fetchall()
		count = 0
		#create doc, create root element
		doc = Document()
		base = doc.createElement('Results')
		doc.appendChild(base)

		for result in data:
			row = doc.createElement('Row ' + str(count))
			base.appendChild(row)
			
			#build the record entry
			bill_id = doc.createElement('id')
			bill_id_c = doc.createTextNode(str(result["id"]))
			bill_id.appendChild(bill_id_c)
			
			name = doc.createElement('name')
			name_c = doc.createTextNode(str(result["name"]))
			name.appendChild(name_c)

			amount_due = doc.createElement('amount_due')
			amount_due_c = doc.createTextNode(str(result["amount_due"]))
			amount_due.appendChild(amount_due_c)
			
			this_month_due_date = doc.createElement('current_month_due')
                        this_month_due_date_c = doc.createTextNode(str(result["current_month_due"]))
                        this_month_due_date.appendChild(this_month_due_date_c)
			
			this_month_status = doc.createElement('current_status')
			this_month_status_c = doc.createTextNode(str(result['current_status']))
			this_month_status.appendChild(this_month_status_c)

			account = doc.createElement('account')
			account_c = doc.createTextNode(str(result['AccountName']))
			account.appendChild(account_c)

			next_due_date = doc.createElement('next_month_due')
			next_due_date_c = doc.createTextNode(str(result['next_month_due']))
			next_due_date.appendChild(next_due_date_c)

			next_month_status = doc.createElement('next_month_status')
			next_month_status_c = doc.createTextNode(str(result['next_status']))
			next_month_status.appendChild(next_month_status_c)

			past_month_due = doc.createElement('past_month_due')
			past_month_due_c = doc.createTextNode(str(result['past_month_due']))
			past_month_due.appendChild(past_month_due_c)

			past_month_status = doc.createElement('prev_status')
			past_month_status_c = doc.createTextNode(str(result['prev_status']))
			past_month_status.appendChild(past_month_status_c)
			
			#add the built fields to the row
			row.appendChild(bill_id)
			row.appendChild(name)
			row.appendChild(amount_due)
			row.appendChild(this_month_due_date)
			row.appendChild(this_month_status)
			row.appendChild(account)
			row.appendChild(next_due_date)
			row.appendChild(next_month_status)
			row.appendChild(past_month_due)
			row.appendChild(past_month_status)
			
	except MySQLdb.Error, e:
		log.log_error("MySQL Error [%d]: %s {%s}\n\n" %(e.args[0], e.args[1], query))
    		close_DB(db)
		return 0
	return doc 
#endef

#################
#     MAIN      #
#################

db, cursor = connect_DB()
#change_months()
close_DB(db)
