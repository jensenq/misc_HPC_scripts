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
		print "Rank\tThread\tCore"
		self.socket0.printThreads()
		self.socket1.printThreads()	

	def sort(self):
		self.socket0.sort()
		self.socket1.sort()


def parseNode(line):
	match = re.compile('on (nid.....)').search(line)
	if match:
		nid = match.group(1)
		return nid
	

def parseLine(line):

	if line[0]=='S':
		print line
		return

	rank = -1
	thread = -1
	cores = []

	match = re.compile('rank (.)').search(line)
	if match:
		rank = match.group(1)
	match = re.compile('thread (\d[^,]|\d)').search(line)
	if match:
		thread = match.group(1)
	match = re.compile('affinity = (.*\d)').search(line)
	if match:
		rawCores = match.group(1)
		for s in rawCores.split(','):
			cores.append(s)

	return (int(rank),int(thread), cores)	
	

def parse(file):
	with open(file) as f:
		nid = parseNode(f.readline())
		n = myNode(nid)

		for line in f:
			info = parseLine(line)
			if info:
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
	
