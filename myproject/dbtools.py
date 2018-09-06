# dbtools.py

import os
import sqlite3

def createdb(dbfilename='data.db'):
    if not os.path.isfile('data.db'):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE data (
            Id INTEGER PRIMARY KEY AUTOINCREMENT, 
            API_key text,
            date_time text,
            mac text,
            field integer,
            data real
            )""")
        conn.commit()
        conn.close()

def writedata(API_key, channel, field, data, datetime):
    pass
    """
	writes a new line to the database. Completes the database transaction, no return value
    """

def readlast(channel, field):
    pass
    """
	reads the most recent entry of a particular channel and field, returns the data and datetime of that entry.
    """
	# return(data, datetime)

def write_data(d, dbname='data.db'):
    pass
   # conn = sqlite3.connect(dbname)

    #c = conn.cursor()
    #with conn:
    #    c.execute("INSERT INTO data VALUES (:API_key, :date_time, :channel, :field, :data), d.data_point_dict()")