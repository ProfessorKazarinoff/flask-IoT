# myproject.py
from flask import Flask, render_template, request
import requests
import datetime
import os
import sqlite3
from dbtools import createdb
import dateutil.parser
from config import API_KEY, MAC_ADDRESS
import pytz

app = Flask(__name__)

createdb('data.db')


@app.route("/")
def index():
    # r = requests.get('https://api.thingspeak.com/channels/254616/fields/1/last.txt')
    # temp_c = r.text
    # temp = str(round(((9.0 / 5.0) * float(temp_c) + 32), 1)) + ' F'
    # temp = '90'
    # r_in = requests.get('https://api.thingspeak.com/channels/254616/fields/2/last.txt')
    # temp_c_in = r_in.text
    # temp_in = str(round(((9.0 / 5.0) * float(temp_c_in) + 32), 1)) + ' F'
    # return render_template("index.html", temp_out=temp, temp_in=temp_in)
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT data, date_time, MAX(rowid) FROM data WHERE field=?", ('1',))
    row1 = c.fetchone()
    c.execute("SELECT data, date_time, MAX(rowid) FROM data WHERE field=?", ('2',))
    row2 = c.fetchone()
    c.close()
    conn.close()
    data1 = str(round((float(row1[0]) * 1.8) + 32))
    data2 = str(round((float(row2[0]) * 1.8) + 32))
    time_str1 = row1[1]
    t1 = dateutil.parser.parse(time_str1)
    t_pst1 = t1.astimezone(pytz.timezone('US/Pacific'))
    time_stamp1 = t_pst1.strftime('%I:%M:%S %p   %b %d, %Y')
    time_str2 = row2[1]
    t2 = dateutil.parser.parse(time_str2)
    t_pst2 = t2.astimezone(pytz.timezone('US/Pacific'))
    time_stamp2 = t_pst2.strftime('%I:%M:%S %p   %b %d, %Y')
    return render_template("showdoubletemp.html", data1=data1, time_stamp1=time_stamp1, data2=data2,time_stamp2=time_stamp2)


@app.route("/showrecent")
def show_recent():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM data WHERE ID = (SELECT MAX(ID) FROM data);')
    row = c.fetchone()
    c.close()
    conn.close()
    data = str(round(row[5], 1))
    time_str = row[2]
    t = dateutil.parser.parse(time_str)
    t_pst = t.astimezone(pytz.timezone('US/Pacific'))
    time_stamp = t_pst.strftime('%I:%M:%S %p Time Zone: %Z   %b %d, %Y')
    return render_template("showrecent.html", data=data, time_stamp=time_stamp)


@app.route("/showdoubletemp")
def show_double_temp():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT data, date_time, MAX(rowid) FROM data WHERE field=?", ('1',))
    row1 = c.fetchone()
    c.execute("SELECT data, date_time, MAX(rowid) FROM data WHERE field=?", ('2',))
    row2 = c.fetchone()
    c.close()
    conn.close()
    data1 = str(round((float(row1[0]) * 1.8) + 32))
    data2 = str(round((float(row2[0]) * 1.8) + 32))
    time_str1 = row1[1]
    t1 = dateutil.parser.parse(time_str1)
    t_pst1 = t1.astimezone(pytz.timezone('US/Pacific'))
    time_stamp1 = t_pst1.strftime('%I:%M:%S %p   %b %d, %Y')
    time_str2 = row2[1]
    t2 = dateutil.parser.parse(time_str2)
    t_pst2 = t2.astimezone(pytz.timezone('US/Pacific'))
    time_stamp2 = t_pst2.strftime('%I:%M:%S %p   %b %d, %Y')
    return render_template("showdoubletemp.html", data1=data1, time_stamp1=time_stamp1, data2=data2,
                           time_stamp2=time_stamp2)


@app.route("/showtemp")
def show_temp():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM data WHERE ID = (SELECT MAX(ID) FROM data);')
    row = c.fetchone()
    c.close()
    conn.close()
    data = str(round((float(row[5]) * 1.8) + 32))
    time_str = row[2]
    t = dateutil.parser.parse(time_str)
    t_pst = t.astimezone(pytz.timezone('US/Pacific'))
    time_stamp = t_pst.strftime('%I:%M:%S %p   %b %d, %Y')
    return render_template("showlocaltemp.html", data=data, time_stamp=time_stamp)


@app.route("/update/API_key=<api_key>/mac=<mac>/field=<int:field>/data=<data>", methods=['GET'])
def write_data_point(api_key, mac, field, data):
    if (api_key == API_KEY and mac == MAC_ADDRESS):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        t = datetime.datetime.now(tz=pytz.utc)
        date_time_str = t.isoformat()
        c.execute("INSERT INTO data VALUES(:Id, :API_key, :date_time, :mac, :field, :data)",
                  {'Id': None, 'API_key': api_key, 'date_time': date_time_str, 'mac': mac, 'field': int(field),
                   'data': round(float(data), 4)})
        conn.commit()
        c.close()
        conn.close()

        return render_template("showrecent.html", data=data, time_stamp=date_time_str)

    else:
        return render_template("403.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
