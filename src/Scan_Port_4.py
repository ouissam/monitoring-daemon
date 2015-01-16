'''
Created on 13 janv. 2015

@author: Rym_r
'''

import socket
import argparse
import sys

def test_ligneCommande():
    parser = argparse.ArgumentParser(description='Scan_port.py')
    parser.add_argument('-p', '--ports', default='1-1024', help='The port you want to scan')
    parser.add_argument('-t', '--hostnames', help='The IP address you want to scan (x.x.x.)')
    
    if len(sys.argv)==1:
            parser.print_help()
            sys.exit(0)
    
    args = parser.parse_args()

    hostnames=[]
    if args.hostnames:
            try: hostnames.append(socket.gethostbyname(args.hostnames)) # get IP
            except: errormsg("Failed to translate hostname to IP address")
    else: parser.print_help(); errormsg("Set a hostname")

    # Scan
    for hostname in args.hostnames:
        tcp_ports = portscan(hostname,args.ports)


def main():
    '''
    ports_ouvertsV = portscanVerbose("127.0.0.1")
    print(ports_ouvertsV)
    ports_ouverts = portscan("10.10.113.71")
    print(ports_ouverts)
    '''
    test_ligneCommande()
    
def portscanVerbose(hostname, ports="1-65535"):
    # Set ports
    if ports == '-': ports = "1-65535"
    ranges = (x.split("-") for x in ports.split(","))
    ports = [i for r in ranges for i in range(int(r[0]), int(r[-1]) + 1)]
    
    print("Now scanning " + hostname)
    tcp_ports=[]    
    for portnum in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.01)
            s.connect((hostname, portnum))
        except Exception:
            failvar = 0
        else:
            print(str(portnum) + "/tcp \topen")
            tcp_ports.append(portnum)
        s.close()
        
    printmsg(("%i open TCP ports of %i ports scanned" % (len(tcp_ports),len(ports))))
    return tcp_ports

def portscan(hostname, ports="1-65535"):
    # Set ports
    if ports == '-': ports = "1-65535"
    ranges = (x.split("-") for x in ports.split(","))
    ports = [i for r in ranges for i in range(int(r[0]), int(r[-1]) + 1)]    
    tcp_ports=[]    
    for portnum in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.01)
            s.connect((hostname, portnum))
        except Exception:
            failvar = 0
        else:
            tcp_ports.append(portnum)
        s.close()        
    return tcp_ports

def errormsg(msg): 
    print("Error: " + msg) ; sys.exit(1)
def printmsg(msg): 
    print("Scan_port.py: " + msg)

if __name__ == "__main__":
    main()