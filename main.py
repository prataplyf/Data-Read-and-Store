from flask import Flask, render_template, request, url_for, redirect
from flask_table import Table, Col
import pymongo # for connect with database
import datetime
import time
import pytz
import tzlocal
import sys

########### datetime
current = datetime.datetime.now()
utc= datetime.datetime.utcnow()
local_timezone = tzlocal.get_localzone()
tt = utc.replace(tzinfo=pytz.utc).astimezone(local_timezone)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Employee"]
mycol = mydb["data"]

app = Flask(__name__)

@app.route('/',methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        cnum = int(request.form.get('cnum'))
        TimeStamp = tt
        mycol.insert_one({ "Email": email, "Name":name, "Contact Number":cnum, "TimeStamp": TimeStamp })
        message = "Successfully saved data"
        return render_template('index.html', message=message)
    
    return render_template('index.html')

  
@app.route('/search', methods=['POST', 'GET'])
def search():
    count = 0
    if request.method == 'POST':
        data = request.form.get('search')
        # checking for Name
        #result = mydb.mycol.find({'Name': {'$regex': data}})
        if data in (temp['Name'] for temp in mycol.find({'Name':{'$regex': data}})):
            namelist = []
            for entry in mycol.find({'Name':{'$regex': data}},{"Name":1, "Email":1, "Contact Number":1, "_id":0, "TimeStamp":1}):
                count += 1
                namelist.append({"name": entry['Name'], "email": entry["Email"], "contact": entry['Contact Number'], "time": entry['TimeStamp']})
            
            msg = data
            return render_template('search.html', data = namelist, count = count, message=msg)


        # checking for Email
        elif data in [temp['Email'] for temp in mycol.find({'Email':{'$regex': data}})]:
            emaillist = []
            for entry in mycol.find({'Email':{'$regex': data}},{"Name":1, "Email":1, "Contact Number":1, "_id":0, "TimeStamp":1}):
                count += 1
                emaillist.append({"name": entry['Name'], "email": entry["Email"], "contact": entry['Contact Number'], "time": entry['TimeStamp']})
            msg = data
            return render_template('search.html', data = emaillist, count = count, message=msg)
        
        else: # if search data didn't found
            count = 0
            msg = data
            return render_template('search.html', message = msg, count = count)


    return render_template('search.html')


if __name__== "__main__":
    app.run(debug=True)