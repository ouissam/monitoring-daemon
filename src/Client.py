#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="sakatiamy"
__date__ ="$11 janv. 2015 15:40:53$"

import os, sys, subprocess, nmap
from Ping import *



def getIP_Mask():
    #Permet d'afficher les adresses réseaux et leur masque
    ip = subprocess.Popen(["ip", "-o", "-f", "inet", "addr", "show"], stdout=subprocess.PIPE)
    ip_format = subprocess.Popen(["awk", "/scope global/ {print $2, $4}"], stdin=ip.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out_final, error = ip_format.communicate()
    out = out_final.decode('utf8')
    print(out)
    out = str(out_final)
    print(out)
    
    ips = []
    networks = out.split("b'")
    print(networks)
    del networks[0]
    print(networks)
    networks = networks[0].split("\\n")
    print(networks)
    print(len(networks))
    size = len(networks) 
    del networks[size-1]
    print(networks)
    
    networks_dictionary = {}
    for n in networks:
        name, ip = n.split(" ", 1)
        networks_dictionary[name] = ip
        
    print(networks_dictionary)    

    print("------------------")

    test = networks_dictionary["lxcbr0"]
    nm = nmap.PortScanner()
    nm.scan(hosts=test, arguments='-sL')
    print(nm.command_line())
    hosts = nm.all_hosts()
    print(hosts)
    print("------------------")
    #hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
    #for host, status in hosts_list:
    #    print('{0}:{1}'.host)
    
    
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
    getIP_Mask()
