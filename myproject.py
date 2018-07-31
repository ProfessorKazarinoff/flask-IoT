from flask import Flask, render_template, request
import requests
import datetime
import os
import sqlite3
from dbtools import createdb
import dateutil.parser

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
    c.execute('SELECT * FROM data WHERE ID = (SELECT MAX(ID) FROM data);')
    row = c.fetchone()
    conn.close()
    data = str(round(row[5],1))
    time_str = row[2]
    t = dateutil.parser.parse(time_str)
    time_stamp = t.strftime('%I:%M %p +%S sec %b %d, %Y')
    return render_template("showrecent.html", data=data, time_stamp=time_stamp)


@app.route("/update/API_key=<api_key>/mac=<mac>/field=<int:field>/data=<data>", methods=['GET'])
def write_data_point(api_key, mac, field, data):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    t = datetime.datetime.now()
    date_time_str = t.isoformat()
    c.execute("INSERT INTO data VALUES(:Id, :API_key, :date_time, :mac, :field, :data)",
              {'Id':None,'API_key': api_key, 'date_time': date_time_str, 'mac': mac, 'field': int(field), 'data': round(float(data),4)})
    conn.commit()
    conn.close()

    return render_template("showrecent.html", data = data, time_stamp=date_time_str)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
