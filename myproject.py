from flask import Flask, render_template, request
import requests

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(host='0.0.0.0')
