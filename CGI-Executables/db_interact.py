#!/usr/env python

import MySQLdb
import datetime

def connect_DB():
	db = MySQLdb.connect("localhost","root","toor","finances" )
	cursor = db.cursor()
	return db, cursor
#endef

def close_DB(db):
	db.close()
#endef

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

#################
#     MAIN      #
#################

db, cursor = connect_DB()
#change_months()
close_DB(db)
