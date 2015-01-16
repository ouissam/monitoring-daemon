import sys, datetime, time, pymongo, re, subprocess
from Daemon_Generic import *
from Ping import *
from pymongo import *
from MongoDB import *
from Scan_Port_2 import *

class MyDaemon(daemon):
    def run(self):
        mongo = MongoDB()
        mongo.setDatabase('test')
        mongo.findCollections()
        collections = mongo.getCollections()
        users = mongo.getCollection('users')
        computers = mongo.getCollection('computers')
        
        #le fichier de log ne se met à jour qu'une fois le travail terminé, or si on a une boucle infini ???
        #Vaudrait mieux utiliser les redirections comme en bash
        i = 0
        dateNow = time.localtime()
        dateNow = str(dateNow.tm_year) + "-" + str(dateNow.tm_mon) + "-" + str(dateNow.tm_mday) + "_"+ str(dateNow.tm_hour) + "-" + str(dateNow.tm_min) + "-" + str(dateNow.tm_sec)
        log = "/tmp/log_" + str(dateNow)           
        while True:
            #distinct permet de recuperer uniquement les valeurs (sans les cles)
            ips = computers.distinct('ip')  
            periode = self.periode
            for ip in ips:
                active_ip = computers.find({"ip" : ip}).distinct('active')
                if(active_ip[0] == True):
                    status = ping(ip, "1")
                    timeNow = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
                    if(status == 0): 
                        computers.update({"ip" : ip}, {"$set" : {"last_ping_date": timeNow, "successfull_ping_date": timeNow}})                
                    else:
                        computers.update({"ip" : ip}, {"$set" : {"last_ping_date": timeNow}})                
                    services = computers.find({"ip" : ip}).distinct('services.port')
                    print(services)
                    for service in services:
                        res = scanProcessPort(ip, str(service))
                        timeNow = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
                        ports, status = parseResultatStatus(res)
                        for k, v in ports.items():
                            monitoring = computers.find({"ip" : ip, "services.name" : v, "services.port" : int(k)}).distinct("services.active")
                            if(monitoring[0] == True):
                                computers.update({"ip" : ip, "services.port" : int(k)}, {"$set" : {"services.$.name" : str(v), "services.$.testResult" : status[k], "services.$.testDate" : timeNow}})     
            i += 1
            time.sleep(float(periode))

            
            
def test(periode):
    mongo = MongoDB()
    mongo.setDatabase('test')
    mongo.findCollections()
    collections = mongo.getCollections()
    users = mongo.getCollection('users')
    computers = mongo.getCollection('computers')

    #le fichier de log ne se met à jour qu'une fois le travail terminé, or si on a une boucle infini ???
    #Vaudrait mieux utiliser les redirections comme en bash
    i = 0
    dateNow = time.localtime()
    dateNow = str(dateNow.tm_year) + "-" + str(dateNow.tm_mon) + "-" + str(dateNow.tm_mday) + "_"+ str(dateNow.tm_hour) + "-" + str(dateNow.tm_min) + "-" + str(dateNow.tm_sec)
    log = "/tmp/log_" + str(dateNow)
    while True:
        #distinct permet de recuperer uniquement les valeurs (sans les cles)
        ips = computers.distinct('ip')    
        print("****************Debut " + str(i) + " : Periode = " + periode + "**************** >> ")
        for ip in ips:
            active_ip = computers.find({"ip" : ip}).distinct('active')
            print(active_ip)
            print(type(active_ip))
            status = ping(ip, "1")
            if(status == 0):
                if(active_ip[0] == False):
                    computers.update({"ip" : ip}, {"$set" : {"active": True}}) 
                    print(str(i) + " : " + ip + " false -> true et update")
                else:
                    print(str(i) + " : " + ip + " true -> true ")
            else:
                if(active_ip[0] == True):
                    computers.update({"ip" : ip}, {"$set" : {"active": False}}) 
                    print(str(i) + " : " + ip + " true -> false et update")
                else:
                    print(str(i) + " : " + ip + " false -> false")
        print("****************Fin" + str(i) + " : Periode = " + periode + "**************** >> ")
        i += 1
        time.sleep(float(periode))
        
def test2(periode):
    mongo = MongoDB()
    mongo.setDatabase('test')
    mongo.findCollections()
    collections = mongo.getCollections()
    users = mongo.getCollection('users')
    computers = mongo.getCollection('computers')

    #le fichier de log ne se met à jour qu'une fois le travail terminé, or si on a une boucle infini ???
    #Vaudrait mieux utiliser les redirections comme en bash
    i = 0
    dateNow = time.localtime()
    dateNow = str(dateNow.tm_year) + "-" + str(dateNow.tm_mon) + "-" + str(dateNow.tm_mday) + "_"+ str(dateNow.tm_hour) + "-" + str(dateNow.tm_min) + "-" + str(dateNow.tm_sec)
    log = "/tmp/log_" + str(dateNow)
    while True:
        #distinct permet de recuperer uniquement les valeurs (sans les cles)
        ips = computers.distinct('ip')    
        print("****************Debut " + str(i) + " : Periode = " + periode + "**************** >> ")
        for ip in ips:
            active_ip = computers.find({"ip" : ip}).distinct('active')
            if(active_ip[0] == True):
                print(active_ip)
                status = ping(ip, "1")
                timeNow = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
                if(status == 0):
                    #if(active_ip == False):
                    #computers.update({"ip" : ip}, {"$set" : {"active": True, ""}})    
                    computers.update({"ip" : ip}, {"$set" : {"last_ping_date": timeNow, "successfull_ping_date": timeNow}})                
                    print(str(i) + " : " + ip + " = Actif")
                else:
                    computers.update({"ip" : ip}, {"$set" : {"last_ping_date": timeNow}})                
                    print(str(i) + " : " + ip + " : Eteint")
        print("****************Fin " + str(i) + " : Periode = " + periode + "**************** >> ")

        i += 1
        time.sleep(float(periode))

            
if __name__ == "__main__":  
    periode = '5'
    daemon = MyDaemon('/tmp/daemon_project.pid', periode)
    if len(sys.argv) == 3:
        validePeriode = "^[0-9]+(\.[0-9]{1,2})?$" #regex nombre decimal avec precision 2
        if not (re.match(validePeriode, sys.argv[2])):
            print("Invalid period format !")
            sys.exit(1)         
        periode = sys.argv[2]    
        daemon = MyDaemon('/tmp/daemon_project.pid', periode) #periode en seconde par defaut periode = 5s

    if (len(sys.argv) == 2 or len(sys.argv) == 3):
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(0)
    else:
        print("usage: %s <start|stop|restart> [periode]" % sys.argv[0])
        sys.exit(2)
    #est2("5")
            