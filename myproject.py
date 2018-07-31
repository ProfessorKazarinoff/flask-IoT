from flask import Flask, render_template, request
import requests
import datetime
import os
import sqlite3
from datatools import DataPoint
from dbtools import createdb

app = Flask(__name__)

createdb('data.db')


@app.route("/")
def index():
    r = requests.get('https://api.thingspeak.com/channels/254616/fields/1/last.txt')
    temp_c = r.text
    temp = str(round(((9.0 / 5.0 ) * float(temp_c) + 32),1) ) + ' F'
    #temp = '90'
    r_in = requests.get('https://api.thingspeak.com/channels/254616/fields/2/last.txt')
    temp_c_in = r_in.text
    temp_in = str(round(((9.0 / 5.0) * float(temp_c_in) + 32),1) ) + ' F'
    return render_template("index.html", temp_out=temp, temp_in=temp_in)

@app.route("/showrecent")
def showrecent():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    lid = c.lastrowid
    c.execute("SELECT * FROM data WHERE field=?", (2,))
    row = c.fetchall()
    conn.close()
    print(row)
    return render_template("showrecent.html", data='12', time_stamp='45')


@app.route("/update/API_key=<api_key>/channel=<int:channel>/field=<int:field>/data=<data>", methods=['GET'])
def write_data_point(api_key, channel, field, data):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    t = datetime.datetime.now()
    date_time_str = t.isoformat()
    d = DataPoint(api_key, date_time_str, channel, field, data)
    c.execute("INSERT INTO data VALUES(:Id, :API_key, :date_time, :channel, :field, :data)",
              {'Id':None,'API_key': d.API_key, 'date_time': date_time_str, 'channel': int(d.channel), 'field': int(d.field), 'data': round(float(d.data),4)})
    conn.commit()
    conn.close()

    return render_template("showrecent.html", data = d.data, time_stamp=d.date_time)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
