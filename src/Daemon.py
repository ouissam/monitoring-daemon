import sys, time
from Daemon_Generic import *
from Ping import *

class MyDaemon(daemon):
    def run(self):
        while True:
                ping("127.0.0.1", "1")
                time.sleep(5)

if __name__ == "__main__":
	daemon = MyDaemon('/tmp/daemon_project.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)