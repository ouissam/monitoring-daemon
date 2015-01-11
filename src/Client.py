#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="sakatiamy"
__date__ ="$11 janv. 2015 15:40:53$"

import nmap, os, sys

def getIP_Mask():
    #Permet d'afficher les adresses réseaux et leur masque
    ips = subprocess.call("ip -o -f inet addr show | awk '/scope global/ {print $2, $4}'", "r").readlines()
    print(ips)

if __name__ == "__main__":
    getIP_Mask()
