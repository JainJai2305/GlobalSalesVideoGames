from re import L, LOCALE
from flask import Flask
from flask import render_template, request, redirect, url_for
import db
from bson.objectid import ObjectId
import json
from pymongo.collation import Collation 

app = Flask(__name__)
collection_name = "gamez"

@app.route('/')
def home():
    #data = db.exports.find()
    #data = db.exports.aggregate([{"$sort":{"Rank":1}}])c.Collation(LOCALE:"en_US", numericOrdering:True)
    data = db.exports.find().sort("Rank").collation(Collation(locale="en_US",numericOrdering=True))
    return render_template('main.html', data=data)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/add', methods = ['POST'])
def addExport():
    document = {}
    document['Rank'] = request.form["Rank"]
    document['Name'] = request.form["Name"]
    document['Genre'] = request.form["Genre"]
    document['Global_Sales'] = request.form["Global_Sales"]
    document['Year'] = request.form["Year"]
    db.exports.insert_one(document)
    data = db.exports.find()
    return render_template('main.html', message="Succesfully added new record", data=data)

@app.route('/update')
def update():
  id = request.args.get("id")
  data = db.exports.find_one({ '_id': ObjectId(id) })
  return render_template('update.html', data=data)

@app.route('/updateExport', methods = ['POST'])
def updateExport():
  id = request.form["id"]
  present_data= db.exports.find_one({ '_id': ObjectId(id) })
  document = {}
  document['Rank'] = request.form["Rank"]
  document['Name'] = request.form["Name"]
  document['Genre'] = request.form["Genre"]
  document['Global_Sales'] = request.form["Global_Sales"]
  document['Year'] = request.form["Year"]
  db.exports.update_one(present_data, { '$set': document })
  return redirect(url_for('home'))

@app.route('/delete', methods = ['POST'])
def delete():
  id = request.form["id"]
  db.exports.delete_one({'_id': ObjectId(id)})
  return redirect(url_for('home'))

@app.route('/visualize')
def visualize():
  data = db.exports.aggregate([
    {
      "$group" :
        {
          "_id" : "$Name",
          "totalExports" : { "$sum": 5 }
        }
     },
    #  {
    #    "$skip": 50
    #  },
    #  {
    #    "$limit": 30
    #  }
  ])
  countries = []
  exports = []
  for record in data:
    countries.append(record['_id'])
    exports.append(record['totalExports'])
  return render_template('visualize.html', countries=json.dumps(countries), exports=json.dumps(exports))

if __name__ == '__main__':
    app.run(port=8000)