# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="sakatiamy"
__date__ ="$14 janv. 2015 18:41:54$"

import subprocess, nmap, time
from Scan_Port_2 import *
 
class Networks:
    
    networks_dictionary = {}
    networks_dictionary_Bis = {}
    
    def __init__(self, nm):
        self.nm = nm
           
    def getNetworksDictionary(self):
        ip = subprocess.Popen(["ip", "-o", "-f", "inet", "addr", "show"], stdout=subprocess.PIPE)
        ip_format = subprocess.Popen(["awk", "/scope global/ {print $2, $4}"], stdin=ip.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, error = ip_format.communicate()
        resultat = out.decode('utf8')
        ips = []
        networks = resultat.splitlines()
        for n in networks:
            name, ip = n.split(" ", 1)
            Networks.networks_dictionary[name] = ip
        return Networks.networks_dictionary    
    
    def getNetworksDictionary_Bis(self):
        ip = subprocess.Popen(["ip", "-o", "-f", "inet", "addr", "show"], stdout=subprocess.PIPE)
        ip_format = subprocess.Popen(["awk", "/scope global/ {print $2, $4}"], stdin=ip.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, error = ip_format.communicate()
        resultat = str(out)
        ips = []
        networks = resultat.split("b'")
        del networks[0]
        networks = networks[0].split("\\n")
        size = len(networks) 
        del networks[size-1]
        for n in networks:
            name, ip = n.split(" ", 1)
            Networks.networks_dictionary_Bis[name] = ip
        return Networks.networks_dictionary_Bis

    def getHosts(self, networks_dictionary):
        hosts = []
        for network_name, network_ip in networks_dictionary.items():
            self.nm.scan(hosts=network_ip, arguments='-sL')
            hosts += self.nm.all_hosts()
        return hosts

    def getActiveHosts(self, networks_dictionary):
        hosts_active = []
        for network_name, network_ip in networks_dictionary.items():
            self.nm.scan(hosts=network_ip, arguments='-sP')
            hosts_active += self.nm.all_hosts()
        return hosts_active

    def setNetworksDictionary(self, networks_dictionary):
        Networks.networks_dictionary = networks_dictionary
        
    def scanTCP(self, ip_address):
        #ports_ouverts = portscan(ip_address, ports)
        #return ports_ouverts
        res = scanProcess(ip_address)
        ports = parseResultat(res)
        return ports
    
    
    def scanTCP_NMAP(self, ip_address):
        print()
        self.nm.scan(hosts=ip_address, arguments='-sS')
        print(self.nm.all_hosts())
        for host in self.nm.all_hosts():
            print('----------------------------------------------------')
            print('State : ' + self.nm[host].state())
            print('----------')
            print('Protocol : ' + 'tcp')
            lport = self.nm[host]['tcp'].keys()
            lport.sort()
            for port in lport:
                print('port : ' + port + '\tstate : ' + self.nm[host]['tcp'][port]['state'])
        
'''
if __name__ == "__main__":
    networks = Networks()
    debut2 = time.time()
    dictionary_Bis = networks.getNetworksDictionary_Bis()
    fin2 = time.time()
    print(dictionary_Bis)
    t2 = fin2-debut2
    print("Tps 2 : " + str(t2))
    debut = time.time()
    dictionary = networks.getNetworksDictionary()
    fin = time.time()
    print(dictionary)
    t = fin-debut
    print("Tps 1 : " + str(t) + "\n") 
    hosts_active = getActiveHosts(dictionary)
    print(hosts_active)
'''        
