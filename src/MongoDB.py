# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="sakatiamy"
__date__ ="$4 janv. 2015 16:00:13$"

import pymongo
import datetime
#installation de pymongo via le git, l'utilisation de pip n'est pas recommande
from pymongo import MongoClient

class MongoDB:
     
    database = None
    collections = []
     
    def __init__(self, host='localhost', port=27017):
        self.host = host
        self.port = port        
        self.connection = MongoClient(host, port, j=True)
        
    def setDatabase(self, db_name):
        MongoDB.database = self.connection[db_name]

    def findCollections(self):
        collection = MongoDB.database.collection_names(False)
        for c in collection:
            MongoDB.collections.append(c)
            
    def getDatabase(self):
        return MongoDB.database
    
    def getCollections(self):
        return MongoDB.collections
    
    def getCollection(self, name):
        collection_index = MongoDB.collections.index(name)
        collection = MongoDB.database[MongoDB.collections[collection_index]]
        return collection