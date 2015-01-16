#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="sakatiamy"
__date__ ="$11 janv. 2015 15:40:53$"

import pymongo, time, urllib.request, nmap
from Ping import *
from Networks import *
from Scan_Port_4 import *


def scanNetwork_Test(networks_dictionary):
    test = networks_dictionary["lxcbr0"]
    nm = nmap.PortScanner()
    nm.scan(hosts=test, arguments='-sP')
    print(nm.command_line())
    hosts = nm.all_hosts()
    print(hosts)
    print("------------------")

def scanNetwork(networks_dictionary):
    nm = nmap.PortScanner()
    for network_name, network_ip in networks_dictionary.items():
        nm.scan(hosts=network_ip, arguments='-sP')
        print(nm.command_line())
        hosts = nm.all_hosts()
        print(hosts)
        print("------------------")
           
              
def restAPI_Computer(params_computer, username, password):
    url = "http://localhost:3000/api/computer"
    params = urllib.parse.urlencode(params_computer)
    params = params.encode('utf-8')
    request = urllib.request.Request(url, params)
    # Récuperation de la réponse du serveur
    response = urllib.request.urlopen(request)
    data = response.read   
    
def restAPI_Service(params_computer, params_service, username, password):
    rawip = params_computer["ip"].replace(".", "")
    url = "http://localhost:3000/api/computer/service/"+rawip
    params = urllib.parse.urlencode(params_service)
    params = params.encode('utf-8')
    request = urllib.request.Request(url, params)
    # Récuperation de la réponse du serveur
    response = urllib.request.urlopen(request)
    data = response.read   
    
    
def scanComputer(ip, username, password):
    name = "machine_" + ip.replace(".", "")
    print(name + ":" + ip)
    params_computer = {"name" : name, "ip" : ip}
    restAPI_Computer(params_computer, username, password)

def scanService(port, ip, username, password):
    rawip = ip.replace(".", "")
    timeNow = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
    params_service = { "name" : "service_"+str(port), "port" : port, "active" : True, "testResult" : "open", "testDate" : timeNow} 
    params_computer = {"name" : rawip, "ip" : ip}
    restAPI_Service(params_computer, params_service, username, password)
    
def test_Computer():   
    ip = ["86.6.6.6"]
    ip += ["96.6.6.6"]
    ip += ["106.6.6.6"]
    print(ip)
    for i in ip:
        name = "machine_" + i.replace(".", "")
        print(name + ":" + i)
        params = {"name" : name, "ip" : i}
        restAPI_Computer(params, "southpark", "southpark")    
    
    
def test_ServiceScan():
    nm = nmap.PortScanner()
    networks = Networks(nm)
    list = []
    #list.append("10.10.120.216")
    #list.append("10.10.120.216")
    list.append("10.10.113.71")
    list.append("10.10.114.198")
    print(list)
    for ip in list:
        scanComputer(ip, "southpark", "southpark")
        ports = networks.scanTCP("10.10.113.71")
        print("ip " + ip + " <=> ports " + str(ports))
        for p in ports:
            scanService(p, ip, "southpark", "southpark")

        
def test_Scan():
    nm = nmap.PortScanner()
    networks = Networks(nm)
    dictionary = networks.getNetworksDictionary()
    print(dictionary)
    #scanNetwork_Test(dictionary)
    scanNetwork(dictionary)
    hosts_active = networks.getActiveHosts(dictionary)
    print(hosts_active)
    for ip in hosts_active:
        scanComputer(ip, "southpark", "southpark")
        ports = networks.scanTCP(ip)
        for p in ports:
            print("ip " + ip + " <=> ports " + str(ports))
            scanService(p, ip, "southpark", "southpark")
        
    
        
def scanNMAP(ip_address):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_address, arguments='-sS')
    print(nm.all_hosts())
    for host in nm.all_hosts():
        print('----------------------------------------------------')
        print('State : ' + nm[host].state())
        print('----------')
        print('Protocol : ' + str(nm[ip_address].all_tcp()))
        lport = nm[ip_address].tcp()
        lport.sort()
        for port in lport:
            print('port : ' + port + '\tstate : ' + nm[host]['tcp'][port]['state'])
        
        
        
def scanProcess(ip_address):
    scan = subprocess.check_output(["nmap", "-sS", ip_address])
    #out, error = scan.communicate()
    resultat = scan.decode('utf-8')
    #print(scan.stdout)
    print(resultat)
    #print(resultat)

if __name__ == "__main__":
    test_Scan()
    #nm = nmap.PortScanner()
    #networks = Networks(nm)
    #ip = "10.0.3.1"
    #ports = networks.scanTCP(ip)
    #ports = portscan(ip)
    #print("ip " + ip + " <=> ports " + str(ports))
    #scanNMAP(ip)
    #scanProcess(ip)