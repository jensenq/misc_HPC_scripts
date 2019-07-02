#warning: assumes 1 node being used
import sys
import re

class thread:
	def __init__(self, num, cores):
		self.num = num
		self.cores = cores

class socket:
	def __init__(self, rank):
		self.rank = rank
		self.threads = []

	def addThread(self, num, cores):
		self.threads.append(thread(num,cores))

	def printThreads(self):
		for t in self.threads:
			sys.stdout.write(str(self.rank) + "\t" + str(t.num) + "\t")
			for c in t.cores:
				sys.stdout.write(c + ",")
			print ""

	def sort(self):
		self.threads.sort(key=lambda t: t.num)

class myNode:
	def __init__(self, name):
		self.name = name
		self.socket0 = socket(0)
		self.socket1 = socket(1)

	def printN(self):
		print "Socket\tThread\tCore"
		self.socket0.printThreads()
		self.socket1.printThreads()	

	def sort(self):
		self.socket0.sort()
		self.socket1.sort()


def parseNode(line):
	nid = re.compile('on (nid.....)').search(line).group(1)
	return nid
	

def parseLine(line):
	rank = re.compile('rank (.)').search(line).group(1)
	thread = re.compile('thread (\d[^,]|\d)').search(line).group(1)
	rawCores = re.compile('affinity = (.*\d)').search(line).group(1)
	cores = []
	for s in rawCores.split(','):
		cores.append(s)

	return (int(rank),int(thread), cores)	
	

def parse(file):
	with open(file) as f:
		nid = parseNode(f.readline())
		n = myNode(nid)

		for line in f:
			info = parseLine(line)
			if(info[0] == 0):
				n.socket0.addThread(info[1], info[2])
			else:
				print info[0]
				n.socket1.addThread(info[1], info[2])

		return n

	
if __name__ == "__main__":
	n = parse("test.txt")
	n.sort()
	n.printN()
	
