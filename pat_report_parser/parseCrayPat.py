import sys
import csv
import pandas as pdlib
import os


def mergeTables():
#https://www.techbeamers.com/pandas-merge-csv-files/
	with open("table2.csv", 'r') as t2:
		with open("table3.csv", 'r') as t3:
			df2 = pdlib.read_csv(t2).set_axis(["Level","Samp%","Samp","Imb..Samp","Imb..Samp%","Function_Name"], axis=1, inplace=False)
			df3 = pdlib.read_csv(t3).set_axis(["Level","Samp%","Samp","Imb..Samp","Imb..Samp%","Function_Name"], axis=1, inplace=False)

			concatenation = pdlib.concat([df2, df3])
			#concatenation.to_csv("craypat_important_functions.csv", index=False, encoding="utf-8", columns=["Level","Samp%","Samp","Imb..Samp","Imb..Samp%","Function_Name"])
			concatenation.to_csv("craypat_important_functions.csv", index=False, encoding="utf-8", columns=["Function_Name"])
	

def extractTable3(f):
	#seek to table 3
	line = f.readline()
	while(line):
		if "Table 3:" in line:
			break
		else:
			line = f.readline()

	#seek to start of csv table
	line = f.readline()
	line = f.readline()

	#extract rows 
	rows = []
	while(line):
		if "Notes for table 4:" in line:
			break
		else:
			rows.append(line)
			line = f.readline()

	#write to csv file because it's easier
	with open('table3.csv', 'a') as fout:
		for row in rows:
			fout.write(row)
	


def extractTable2(f):
	#seek to table 2
	line = f.readline()
	while(line):
		if "Table 2:" in line:
			break
		else:
			line = f.readline()

	#seek to start of csv table
	line = f.readline()
	line = f.readline()

	#extract rows 
	rows = []
	while(line):
		if "====" in line:
			break
		else:
			rows.append(line)
			line = f.readline()

	#write to csv file because it's easier
	with open('table2.csv', 'a') as fout:
		for row in rows:
			fout.write(row)



if __name__ == "__main__":
	filename = sys.argv[1]
	with open(filename) as f:
		extractTable2(f)
		extractTable3(f)
	
	mergeTables()

	with open("craypat_important_functions.csv",'r') as f:
		with open("important_functions.txt",'w') as f1:
			next(f) # skip header line
			for line in f:
				f1.write(line)
		

	os.remove("table2.csv")
	os.remove("table3.csv")
	os.remove("craypat_important_functions.csv")

	
	
