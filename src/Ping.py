import os, sys, re, socket, platform

ValidIpAddressRegex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$";

def ping(hostname, count):
    systeme = platform.system();
    option = 'c'
    if systeme == 'Windows':
        option = 'n'

    if not (re.match(ValidIpAddressRegex, hostname)):
            print("Invalid IP Address !")
            exit(1)
    else:
        status_Ping = os.system('ping ' + hostname + ' -' + option + ' ' + count + "| grep time= | cut -d'=' -f4 >> /tmp/test_daemon") 


def Main():
    try:
        hostname = socket.gethostbyname(sys.argv[1])
        count = "1"
        if len(sys.argv) == 3:
            count = sys.argv[2]

        ping(hostname, count)

    except: 
        socket.error
        print("Hostname not resolved : " + hostname)        


if __name__ == '__main__':
    Main()



