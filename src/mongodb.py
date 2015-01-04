import pymongo, time, sys
import datetime
#installation de pymongo via le git, l'utilisation de pip n'est pas recommandé
from pymongo import MongoClient
from MongoDB import *
from Ping import *

'''
client = MongoClient()
db = client.test

users = db.users
'''
'''
mongo = MongoDB()
mongo.setDatabase('test')
'''
'''mongo.setCollection()
users, computers = mongo.getCollection()
print(users.count())
print(computers.count())
print(users.find_one({"name": "toto"}))
'''
'''
mongo.findCollections()
collections = mongo.getCollections()
print(collections)

users = mongo.getCollection('users')
print(users.count())


#user = {"name" : "Kyle"}
#users.insert(user)
print(users.count())
print(users.find_one({"name": "Kenny"}))
print(users.find({}, {"_id": 0, "name": 1}))

computers = mongo.getCollection('computers')
print(computers.count())

computer = {"name" : "CartmanPC",
    "ip" : "192.168.1.66",
    "rawip": "192168166",
    "creation_date" : datetime.datetime.utcnow(),
    "successfull_ping_date" : datetime.datetime.utcnow(),
    "last_ping_date" : datetime.datetime.utcnow(),
    "active" : "true"}
#computers.insert(computer)
print(computers.count())

#Nécessite de faire une iteration car on récupere un curseur
ips_cursor = computers.find({}, {"_id" : 0, "ip" : 1})
for ip in ips_cursor:
    print(ip)

#distinct permet de récuperer uniquement les valeurs (sans les cles)
fichier = open("/tmp/log", 'a')
i = 0
while i < 5:
    #distinct permet de recuperer uniquement les valeurs (sans les cles)
    ips = computers.distinct('ip')    
    for ip in ips:
        active_ip = computers.find({"ip" : ip}).distinct('active')
        status = ping(ip, "1")
        if(status == 0):
            if(active_ip == False):
                computers.update({"ip" : ip}, {"$set" : {"active": True}})                
                fichier.write(str(i) + " : " + ip + " ====> true + modif\n")
            else:
                fichier.write(str(i) + " : " + ip + " ====> true + non modif\n")
        else:
            if(active_ip == True):
                computers.update({"ip" : ip}, {"$set" : {"active": False}})    
                fichier.write(str(i) + " : " + ip + " ====> false + modif\n")
            else:
                fichier.write(str(i) + " : " + ip + " ====> false + non modif\n")
    time.sleep(1)
    i += 1

fichier.close()
        
#Permet de mettre à jour le boolean active
#computers.update({"rawip": "19216866"}, {"$set" : {"active" : "true"}})

#permet de faire un projection sur le resultat de la requete
#db.users.find({}, {_id: 0, name:1})

'''

ip = "192.168.1.1"
i = 666
os.system("echo pipi >> /tmp/test_daemon") 
os.system("echo " + str(i) + " : " + ip + " = false + modif >> /tmp/log")


