from flask import Flask
from flask_pymongo import pymongo

CONNECTION_STRING = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('games')
exports = pymongo.collection.Collection(db, 'gamez')