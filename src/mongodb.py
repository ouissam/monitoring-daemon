import pymongo
import datetime
#installation de pymongo via le git, l'utilisation de pip n'est pas recommandé
from pymongo import MongoClient

client = MongoClient()
db = client.test

users = db.users
users.count()
users.find_one({"name": "Katia"})
computers = db.computers
computer = {"name" : "Butters",
    "ip" : "192.168.1.1",
    "rawip": "19216811",
    "creation_date" : datetime.datetime.utcnow(),
    "successfull_ping_date" : datetime.datetime.utcnow(),
    "last_ping_date" : datetime.datetime.utcnow(),
    "active" : "true"}
computers.insert(computer)

computers.find_one({"rawip": "19216811"})


#Permet de mettre à jour le boolean active
computers.update({"rawip": "19216811"}, {"$set" : {"active" : "true"}})



