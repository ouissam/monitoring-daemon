import sys, time, pymongo, re, subprocess
from Daemon_Generic import *
from Ping import *
from pymongo import *
from MongoDB import *

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
            subprocess.call("echo ****************Debut " + str(i) + " : Periode = " + periode + "**************** >> " + log, shell=True)
            for ip in ips:
                active_ip = computers.find({"ip" : ip}).distinct('active')
                status = ping(ip, "1")
                if(status == 0):
                    if(active_ip == False):
                        computers.update({"ip" : ip}, {"$set" : {"active": True}})                
                        subprocess.call("echo " + str(i) + " : " + ip + " = true + modif >> " + log, shell=True)
                    else:
                        subprocess.call("echo " + str(i) + " : " + ip + " = true + non modif >> " + log, shell=True)
                else:
                    if(active_ip == True):
                        computers.update({"ip" : ip}, {"$set" : {"active": False}})    
                        subprocess.call("echo " + str(i) + " : " + ip + " = false + modif >> " + log, shell=True)
                    else:
                        subprocess.call("echo " + str(i) + " : " + ip + " = false + non modif >> " + log, shell=True)                
            subprocess.call("echo ****************Fin " + str(i) + " : Periode = " + periode + "**************** >> " + log, shell=True)        
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
            