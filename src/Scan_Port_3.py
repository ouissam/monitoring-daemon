# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="sakatiamy"
__date__ ="$3 janv. 2015 18:41:34$"

import socket
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description='Scan_port.py - Replicates limited Scan_port functionality in python')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable this for full output')
    parser.add_argument('-sS', '--tcpscan', action='store_true', help='Enable this for TCP scans')
    parser.add_argument('-sU', '--udpscan', action='store_true', help='Enable this for UDP scans')
    parser.add_argument('-p', '--ports', default='1-1024', help='The ports you want to scan (21,22,80,135-139,443,445)')
    parser.add_argument('-t', '--targets', help='The target(s) you want to scan (192.168.0.1)')
    if len(sys.argv)==1: parser.print_help(); sys.exit(0)
    args = parser.parse_args()

    # Set target (and convert for FQDN)
    targets=[]
    if args.targets:
            try: targets.append(socket.gethostbyname(args.targets)) # get IP from FQDN
            except: errormsg("Failed to translate hostname to IP address")
    else: parser.print_help(); errormsg("You need to set a hostname")

    # Set ports
    if args.ports == '-': args.ports = '1-65535'
    ranges = (x.split("-") for x in args.ports.split(","))
    ports = [i for r in ranges for i in range(int(r[0]), int(r[-1]) + 1)]

    # Output command line args to screen
    if args.verbose: printmsg("Arguments used:"); print args ;

    # Start Scanning
    for target in targets:
        tcpports, udpports = portscan(target,ports,args.tcpscan,args.udpscan,args.verbose)

def portscan(target,ports,tcp,udp,verbose):
    #target=IPaddr,ports=list of ports,tcp=true/false,udp=true/false,verbose=true/false
    printmsg(("Now scanning %s" % (target)))
    tcpports=[]
    udpports=[]
    if tcp:
        for portnum in ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.01)
                s.connect((target, portnum))
            except Exception:
                failvar = 0
                if verbose: print "%d/tcp \tclosed" % (portnum)
            else:
                print "%d/tcp \topen"% (portnum)
                tcpports.append(portnum)
            s.close()
    if udp:
        for portnum in ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.settimeout(0.1)
                s.sendto("--TEST LINE--", (target, portnum))
                recv, svr = s.recvfrom(255)
            except Exception, e:
                try: errno, errtxt = e
                except ValueError:
                    print "%d/udp \topen"% (portnum)
                    udpports.append(portnum)
                else:
                    if verbose: print "%d/udp \tclosed" % (portnum)
            s.close()
    printmsg(("%i open TCP ports, %i open UDP ports of %i ports scanned" % (len(tcpports),len(udpports),len(ports))))
    return tcpports, udpports


if __name__ == "__main__":
    main()