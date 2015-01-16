#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="sakatiamy"
__date__ ="$11 janv. 2015 15:40:53$"

import nmap, subprocess, re, pymongo, time
from MongoDB import *

def scanProcess(ip_address):
    scan = subprocess.check_output(["nmap", "-sS", ip_address])
    resultat = scan.decode('utf-8')
    res = resultat.splitlines()
    return res

def scanProcessPort(ip_address, ports):
    scan = subprocess.check_output(["nmap", "-sS", ip_address, "-p", ports])
    resultat = scan.decode('utf-8')
    res = resultat.splitlines()
    return res

def parseResultat(resultat):
    ports = {}
    for line in resultat:
        line = re.sub("[ ]{2,}", " ", line)
        if "open" in line:
            print(line)
            port = line.split("/")[0]
            name = line.split(" ")[1]
            ports[port] = name
    return ports

def parseResultatStatus(resultat):
    ports = {}
    ports_status = {}
    for line in resultat:
        line = re.sub("[ ]{2,}", " ", line)
        if "open" in line or "filtered" in line or "closed" in line:
            print(line)
            port = line.split("/")[0]
            status = line.split(" ")[1]
            name = line.split(" ")[2]
            ports[port] = name
            ports_status[port] = status
    return ports, ports_status

def getServicesIP():
    mongo = MongoDB()
    mongo.setDatabase('test')
    mongo.findCollections()
    collections = mongo.getCollections()
    users = mongo.getCollection('users')
    computers = mongo.getCollection('computers')
    ips = computers.distinct('ip')
    print("ips : " + str(ips))
    for ip in ips:
        print("-----------AVANT-----------")
        print(ip)
        services = computers.find({"ip" : ip}).distinct('services.port')
        print(services)
        for service in services:
            res = scanProcessPort(ip, str(service))
            timeNow = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
            ports, status = parseResultatStatus(res)
            #print(ports)
            #print(status)
            for k, v in ports.items():
                #computers.update({"ip" : ip, "services.name" : str(v), "services.port" : int(k)}, {"$set" : {"services.$.testResult" : status[k], "services.$.testDate" : timeNow}})     
                #computers.update({"ip" : ip, "services.port" : int(k)}, {"$set" : {"services.$.testResult" : status[k], "services.$.testDate" : timeNow}})     
                #computers.update({"ip" : ip, "services" : {"$elemMatch" : {"name": v, "port" : int(k)}}, {"$set" : {"services.$.testResult" : status[k], "services.$.testDate" : timeNow}}})     
                #print(k + " " + v + " = "+ status[k])
                monitoring = computers.find({"ip" : ip, "services.port" : int(k)}).distinct("services.active")
                print(monitoring)
                #computers.update({"ip" : ip, "services.port" : int(k)}, {"$set" : {"services.$.name" : str(v), "services.$.active" : True, "services.$.testResult" : status[k], "services.$.testDate" : timeNow}})     
                if(monitoring[0] == True):
                    computers.update({"ip" : ip, "services.port" : int(k)}, {"$set" : {"services.$.name" : str(v), "services.$.testResult" : status[k], "services.$.testDate" : timeNow}})     
                

            
            



def getServices():
    mongo = MongoDB()
    mongo.setDatabase('test')
    mongo.findCollections()
    collections = mongo.getCollections()
    users = mongo.getCollection('users')
    computers = mongo.getCollection('computers')
    ips = computers.distinct('ip')
    print("ips : " + str(ips))
    for ip in ips:
        print("-----------AVANT-----------")
        print(ip)
        services_ip = computers.find({"ip" : ip}).distinct('services')
        print(services_ip)
        res = scanProcess(ip)
        ports = parseResultat(res)
        timeNow = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
        for k, v in ports.items():
            exist = computers.find({"ip" : ip, "services.name" : v, "services.port" : k}).count()
            if(exist == 0):
                computers.update({"ip" : ip}, {"$addToSet" : {"services": {"name": v, "port": int(k), "testResult": "open", "testDate" : timeNow}}})                
            else:
                monitoring = computers.find({"ip" : ip, "services.name" : v, "services.port" : int(k)}).distinct("services.active")
                print(monitoring)
                if(monitoring[0] == True):
                    print("Monitoring")
                    computers.update({"ip" : ip, "services.name" : v, "services.port" : int(k)}, {"$set" : {"services.$.testResult" : "open", "service.$.testDate" : timeNow}})                                
        print("-----------APRES-----------")
        services_ip = computers.find({"ip" : ip}).distinct('services')
        print(services_ip)
        print("----------------------")

if __name__ == '__main__':
    '''
    ip = "192.168.1.1"
    r = scanProcess(ip)
    ports = parseResultat(r)
    print("---------")
    print(ports)
    ip = "192.168.1.1"
    ip = "10.10.115.91"
    ports = "1024, 6000"
    r = scanProcess(ip, ports)
    ports = parseResultat(r)
    print("---------")
    print(ports)
    '''

    getServicesIP()

    