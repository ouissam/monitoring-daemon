'''
Created on 13 janv. 2015

@author: Rym_r
'''

import socket
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description='Scan_port.py')
    parser.add_argument('-sS', '--tcpscan', action='store_true', help='Enable this for TCP scans')
    parser.add_argument('-p', '--ports', default='1-1024', help='The port you want to scan')
    parser.add_argument('-t', '--targets', help='The IP address you want to scan (x.x.x.)')
    
    if len(sys.argv)==1:
            parser.print_help()
            sys.exit(0)
    
    args = parser.parse_args()

    targets=[]
    if args.targets:
            try: targets.append(socket.gethostbyname(args.targets)) # get IP
            except: errormsg("Failed to translate hostname to IP address")
    else: parser.print_help(); errormsg("Set a hostname")

    # Set ports
    if args.ports == '-': args.ports = '1-65535'
    ranges = (x.split("-") for x in args.ports.split(","))
    ports = [i for r in ranges for i in range(int(r[0]), int(r[-1]) + 1)]

    # Scan
    for target in targets:
        tcpports = portscan(target,ports,args.tcpscan)

def portscan(target,ports,tcp):
    printmsg(("Now scanning %s" % (target)))
    tcpports=[]
    
    if tcp:
        for portnum in ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.01)
                s.connect((target, portnum))
            except Exception:
                failvar = 0
            else:
                print("%d/tcp \topen") % (portnum)
                tcpports.append(portnum)
            s.close()
            printmsg(("%i open TCP ports of %i ports scanned" % (len(tcpports),len(ports))))
    return tcpports

def errormsg(msg): 
    print("Error: %s") % (msg) ; sys.exit(1)
def printmsg(msg): 
    print("Scan_port.py: %s") % (msg)

if __name__ == "__main__":
    main()