#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="sakatiamy"
__date__ ="$11 janv. 2015 15:40:53$"

import nmap, subprocess, re, pymongo
from MongoDB import *

def scanProcess(ip_address):
    scan = subprocess.check_output(["nmap", "-sS", ip_address])
    resultat = scan.decode('utf-8')
    res = resultat.splitlines()
    return res

def scanProcess(ip_address, ports):
    scan = subprocess.check_output(["nmap", "-sS", ip_address, "-p", ports])
    resultat = scan.decode('utf-8')
    res = resultat.splitlines()
    return res

def parseResultat(resultat):
    ports = {}
    for line in resultat:
        line = re.sub("[ ]{2,}", " ", line)
        if "open" in line or "filtered" in line or "closed" in line:
            print(line)
            port = line.split("/")[0]
            status = line.split(" ")[1]
            name = line.split(" ")[2]
            ports[port] = name
    return ports

def getServices():
    mongo = MongoDB()
    mongo.setDatabas,e('test')
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
        for k, v in ports.items():
            #ervice = {"name" : v, "port" : k, "active" : True}
            #computers.update({"ip" : ip, "services.name": v}, {"$set" : {"services.$.name": v, "services.$.port": k, "services.$.active": True}}, uspert=True)                
            #exist = computers.find({"ip" : ip, "services.name" : v}).distinct('services')
            exist = computers.find({"ip" : ip, "services.name" : v, "services.port" : k}).count()
            #print("Le service " + v + " existe : " + str(exist))
            if(exist == 0):
                #print("oui")
                computers.update({"ip" : ip}, {"$addToSet" : {"services": {"name": v, "port": k, "active": True}}})                
            else:
                #print("non")
                computers.update({"ip" : ip, "services.name" : v}, {"$set" : {"services.$.active" : False}})                                
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
    '''
    ip = "192.168.1.1"
    ip = "10.10.115.91"
    ports = "1024, 6000"
    r = scanProcess(ip, ports)
    ports = parseResultat(r)
    print("---------")
    print(ports)
    #getServices()

    