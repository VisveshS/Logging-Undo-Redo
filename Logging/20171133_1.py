import sys
import os, time

class memory_mgr():
	def __init__(self):
		self.memory = {}
	def print(self):
		out = sorted (self.memory.keys())
		for i in range(len(out)):
			print(out[i]+' '+str(self.memory[out[i]])+(' ' if i!=len(out)-1 else ''),end = "")
		print('')
	def update(self,variable,val):
		self.memory[variable]=val

transactions = {}
readhead = {}
ram = memory_mgr()
temp = memory_mgr()
disk = memory_mgr()

def execute(command,transaction):
	if "READ" in command:
		var1, var2 = command.split('(')[1].split(')')[0].strip().split(',')
		if var1 not in ram.memory:
			ram.update(var1,disk.memory[var1])
		temp.update(var2,ram.memory[var1])
	elif "WRITE" in command:
		var1, var2 = command.split('(')[1].split(')')[0].strip().split(',')
		ram.memory[var1] = ram.memory[var1] if var1 in ram.memory else disk.memory[var1]
		print('<%s, %s, %d>'%(transaction,var1,ram.memory[var1]))
		ram.update(var1,temp.memory[var2])
	elif "OUTPUT" in command:
		var1 = command.split('(')[1].split(')')[0].strip()
		disk.update(var1,ram.memory[var1])
	else:
		lhs, rhs = command.replace(' ','').split(":=")
		operator = None
		for op in ['*','+','-','/']:
			if op in rhs:
				operator = op
		v1, v2 = rhs.split(operator)
		v1 = int(v1) if v1.isdigit() else temp.memory[v1]
		v2 = int(v2) if v2.isdigit() else temp.memory[v2]
		if operator == '/':
			try:
				v = v1/v2
			except:
				print("Division by 0 not allowed")
				sys.exit(0)
		elif operator == '*':
			v = v1*v2
		elif operator == '+':
			v = v1+v2
		elif operator == '-':
			v = v1-v2
		else:
			print("operator not present in expression",command)
			sys.exit(0)
		temp.update(lhs,v)
	if "WRITE" in command:
		ram.print()
		disk.print()

def iterate(round_robin):
	n_complete = 0
	while n_complete < len(transactions):
		for transaction in sorted (transactions.keys()):
			if readhead[transaction] != -1:
				for i in range(round_robin):
					if readhead[transaction] == 0:
						print("<START %s>"%transaction)
						ram.print()
						disk.print()
					execute(transactions[transaction][readhead[transaction]],transaction)
					readhead[transaction] += 1
					if readhead[transaction] == len(transactions[transaction]):
						print("<COMMIT %s>"%transaction)
						ram.print()
						disk.print()
						readhead[transaction] = -1
						n_complete += 1
						break

def parse_input(input_file):
	with open(input_file) as f:
		initial_values = f.readline()
		initial_values = initial_values.strip().split()
		for vname, vval in zip(*[iter(initial_values)]*2):
			disk.update(vname,int(vval))
		current_transaction = None
		for lines in f:
			if lines.strip() is "":
				current_transaction = f.readline().strip().split()[0]
				readhead[current_transaction] = 0
				transactions[current_transaction] = []
			else:
				transactions[current_transaction].append(lines.strip())

if len(sys.argv)!=3:
	sys.exit("Error: python 20171133_1.py <input_file> <x>")
dummy,input_file,round_robin = sys.argv
round_robin = int(round_robin)
parse_input(input_file)
iterate(round_robin)
