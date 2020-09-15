import sys
import os, time

database = {}

def parse_input(input_file):
	with open(input_file) as f:
		initial_values = f.readline()
		initial_values = initial_values.strip().split()
		for vname, vval in zip(*[iter(initial_values)]*2):
			database[vname] = int(vval)
	with open(input_file) as f:
		input_lines = f.readlines()
	return list(reversed(input_lines[1:]))

def iterate(input_lines):
	end_ckpt = False
	start_ckpt = False
	incomplete = []
	counter = 0
	for line in input_lines:
		if "END" in line:
			end_ckpt = True
		elif "START CKPT" in line and not end_ckpt:
			counter += 1
			new_additions = line.replace(" ","").split("(")[1].split(")")[0].split(",")
			for new_addition in new_additions:
				if new_addition not in incomplete:
					incomplete.append(new_addition)
			start_ckpt = True
		elif "START CKPT" in line and end_ckpt:
			break
		elif "START" in line and start_ckpt:
			if line.split()[1].strip().split('>')[0] in incomplete:
				counter += 1
			if counter == len(incomplete):
				break
		elif "COMMIT" in line:
			committed = line.split()[1].strip().split('>')[0]
			try:
				incomplete.remove(committed)
			except:
				incomplete = incomplete
		elif len(line.split(',')) == 3:
			transaction , var, val = line[1:-2].replace(' ','').split(',')
			val = int(val)
			if transaction in incomplete:
				database[var] = val

if(len(sys.argv)) != 2:
	sys.exit("Error: python 20171133_2.py inp")
dummy, input_file = sys.argv
input_lines = parse_input(input_file)
iterate(input_lines)
print(database)
