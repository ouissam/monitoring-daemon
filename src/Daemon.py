import sys, time, pymongo
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
        while True:
            #distinct permet de recuperer uniquement les valeurs (sans les cles)
            ips = computers.distinct('ip')    
            for ip in ips:
                active_ip = computers.find({"ip" : ip}).distinct('active')
                status = ping(ip, "1")
                if(status == 0):
                    if(active_ip == False):
                        computers.update({"ip" : ip}, {"$set" : {"active": True}})                
                        os.system("echo " + str(i) + " : " + ip + " = true + modif >> /tmp/log")
                    else:
                        os.system("echo " + str(i) + " : " + ip + " = true + non modif >> /tmp/log")
                else:
                    if(active_ip == True):
                        computers.update({"ip" : ip}, {"$set" : {"active": False}})    
                        os.system("echo " + str(i) + " : " + ip + " = false + modif >> /tmp/log")
                    else:
                        os.system("echo " + str(i) + " : " + ip + " = false + non modif >> /tmp/log")
            i += 1
            time.sleep(5)
            
if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon_project.pid')
    if len(sys.argv) == 2:
            if 'start' == sys.argv[1]:
                    daemon.start()
            elif 'stop' == sys.argv[1]:
                    daemon.stop()
            elif 'restart' == sys.argv[1]:
                    daemon.restart()
            else:
                    print("Unknown command")
                    sys.exit(2)
            sys.exit(0)
    else:
            print("usage: %s start|stop|restart" % sys.argv[0])
            sys.exit(2)