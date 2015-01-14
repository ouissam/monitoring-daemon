#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="sakatiamy"
__date__ ="$11 janv. 2015 15:40:53$"

import pymongo, time
from Ping import *
from Networks import *


def displayNetwork_Test(networks_dictionary):
    test = networks_dictionary["lxcbr0"]
    nm = nmap.PortScanner()
    nm.scan(hosts=test, arguments='-sP')
    print(nm.command_line())
    hosts = nm.all_hosts()
    print(hosts)
    print("------------------")

def displayNetwork(networks_dictionary):
    nm = nmap.PortScanner()
    for network_name, network_ip in networks_dictionary.items():
        nm.scan(hosts=network_ip, arguments='-sP')
        print(nm.command_line())
        hosts = nm.all_hosts()
        print(hosts)
        print("------------------")
           
    '''
    for k, v in networks_dictionary.items():
        print("****** Scan du reseau " + v + " ****** ")
        result = subprocess.Popen(["nmap", "-sP", v], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = result.communicate()
        stri = out.decode('utf8')
        print(stri)
        print("------------------")
        sio = StringIO(stri)
        for sline in sio.readlines():
            print(sline)
        print("****** FIN Scan du reseau " + v + " ****** ")

        #status = ping(v, "1")
        
    #for n in networks
    #print(ip_format.stdout)
    #print(ip.stdout)
    '''
    
if __name__ == "__main__":
    networks = Networks()
    dictionary = networks.getNetworksDictionary()
    #displayNetwork_Test(dictionary)
    #displayNetwork(dictionary)
    hosts_active = networks.getActiveHosts(dictionary)
    print(hosts_active)
