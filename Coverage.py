import os
import shlex, subprocess
from prettytable import PrettyTable
from math import sqrt
import re
#import mutations
import time




def compile(data):
	with open('models/mutated_file.pl', 'w') as f:
	    for item in data:
	        print >> f, item


def GetCoverage(initial_test_results, mutated_data, program, tests, added_statements):
	data = ""
	with open("models/" + program, 'r') as file:
	    data = file.read().replace("", "")
	file.close()
	data = data.split("\n")
	original = list(data)
	coverage_info = []
	test_file = open("models/" + tests)
	for (mutant, i) in mutated_data:
		#print mutation + "    " + str(i)
		##print mutation + "GG"
		data[i] = mutant
		print("MUTANT: " + str(mutant) + str(i))
		compile(data)
		getResults(i, initial_test_results, test_file, coverage_info, added_statements)
		data = list(original)
	return coverage_info


def divide(x,y):
    try:
        return float(x / y)
    except ZeroDivisionError:
        return 0


def getResults(index, initial_test_results, test_file, coverage_info, added_statements):
	test_number = 0
	for (i, line) in enumerate(test_file):
		if "test(" in line:
			if len(coverage_info) - 1 < test_number:
				coverage_info.append([])
			#put Each test into a test file
			newTestFile = open("models/runtimeModel.plt", 'w')
			newTestFile.write(":- begin_tests(mutated_file).\n:- include(mutated_file).\n")
			newTestFile.write(added_statements)
			newTestFile.write(line)
			newTestFile.write("\n:- end_tests(mutated_file).")

			#Run tests and ##print out results
			command = "swipl -f models/mutated_file.pl -s models/runtimeModel.plt -g run_tests,halt -t 'halt(1)'"


			#Close files
			newTestFile.close()

			
			#*************PASSED TEST********#####
			try:
				output = subprocess.check_call(command.split())
				
				if initial_test_results[test_number] == "fail":
					coverage_info[test_number].append(index)

			##***********FAILED TEST************#####
			except subprocess.CalledProcessError:
				if initial_test_results[test_number] == "pass":
					#print(test_number)
					coverage_info[test_number].append(index)

			test_number = test_number + 1
	##print initial_test_results
	test_file.seek(0)




def cleanup(s):
	global mutated_data
	s.remove("")
	for (i, index) in enumerate(s):
		s[i] = s[i] + "."

def replace_str_index(text,index=0,replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])


