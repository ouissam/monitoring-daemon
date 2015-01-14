# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="sakatiamy"
__date__ ="$14 janv. 2015 18:41:54$"

import subprocess, nmap, time
 
class Networks:
    
    networks_dictionary = {}
    networks_dictionary_Bis = {}
           
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
        nm = nmap.PortScanner()
        hosts = []
        for network_name, network_ip in networks_dictionary.items():
            nm.scan(hosts=network_ip, arguments='-sL')
            hosts += nm.all_hosts()
        return hosts

    def getActiveHosts(self, networks_dictionary):
        nm = nmap.PortScanner()
        hosts_active = []
        for network_name, network_ip in networks_dictionary.items():
            nm.scan(hosts=network_ip, arguments='-sP')
            hosts_active += nm.all_hosts()
        return hosts_active

    def setNetworksDictionary(self, networks_dictionary):
        Networks.networks_dictionary = networks_dictionary
        
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
