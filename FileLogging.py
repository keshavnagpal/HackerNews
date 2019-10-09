import logging
logging.basicConfig(filename='ApplicationLogs.log',level=logging.INFO,format='%(asctime)s %(message)s',datefmt='%x %X')

def log(*args):
	logInfo=''
	for i in range(0,len(args)):
		logInfo+=str(args[i])
	logging.debug("%s",logInfo)

def clearLog():
	with open('ApplicationLogs.log', 'w'):
		pass