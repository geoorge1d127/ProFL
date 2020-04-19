#######Dependencies#######

import os
import shlex, subprocess
from prettytable import PrettyTable
from math import sqrt
import re
#import mutations
import time
import click
import Coverage
import Mutations
import ProFL_s
import ProFL_m
import sys


topX = sys.argv[1]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def getInitialResults(program_file, tests):
	passed_tests = 0
	failed_tests = 0
	initial_test_results = []
	added_statements = ""
	programStr = program_file.replace(".pl", "")
	test_file = open("models/" + tests)
	for line in test_file:
		if "test(" in line:
			#put Each test into a test file
			newTestFile = open("models/runtimeModel.plt", 'w')
			newTestFile.write(":- begin_tests(" + programStr + ").\n:- include(" + programStr + ").\n")
			newTestFile.write(added_statements)

			newTestFile.write(line)
			
			newTestFile.write("\n:- end_tests(" + programStr + ").")

			#Run tests and print out results
			command = "swipl -f models/" + programStr + ".pl -s models/runtimeModel.plt -g run_tests,halt -t 'halt(1)'"
			print(line)

			#Close files
			newTestFile.close()

			
			#*************PASSED TEST********#####
			try:
				output = subprocess.check_call(command.split())
				initial_test_results.append("pass")
				passed_tests += 1


			##***********FAILED TEST************#####
			except subprocess.CalledProcessError:
				initial_test_results.append("fail")
				failed_tests += 1
	#print initial_test_results
		elif line[0] != ":":
			added_statements = added_statements + line + "\n"
	return (initial_test_results, passed_tests, failed_tests, added_statements)
	test_file.close()

Coverage = False
SbFl = False
MbFl = False
table = PrettyTable()
table.field_names = ["Statement #", "Passed Tests", "Failed Tests", "Tarantula", "Ochiai", "OP2", "Mutation"]
click.clear()
print(bcolors.HEADER + bcolors.BOLD + "\n *****ProFL*****" + bcolors.ENDC)
program_file = raw_input("\n Enter the name of your prolog model (ending with '.pl')")
assert os.path.exists("models/" + program_file), "I did not find the file, "+str(program_file) + " in the 'models' folder"
test_file = raw_input("\n Enter the name of the test suite file (ending with 'plt'")
assert os.path.exists("models/" + test_file), "I did not find the file, "+str(test_file) + " in the 'models' folder"

print(bcolors.HEADER + bcolors.BOLD + "\n ****Calculating Initial Test Results**** \n" + bcolors.ENDC)
initial_test_results, total_passed_tests, total_failed_tests, added_statements = getInitialResults(program_file, test_file)
click.clear()
decision = raw_input("  What would you like to do?\n(For multiple selections, separate each entry by a comma) \n 1.) Determine Coverage \n 2.) Spectrum-based Fault Localization \n 3.) Mutation-based Fault Localization \n")

decisions = decision.split(",")
report = False
Spectrum_Formula = ""
print(bcolors.HEADER + bcolors.BOLD + "\n ****Creating Mutants**** \n"+ bcolors.ENDC)
mutated_data, number_of_mutants = Mutations.Create_Mutants(program_file)
coverage_info = []
for opt in decisions:
	if opt.replace(" ", "") == '1':
		Coverage = True
	elif opt.replace(" ", "") == '2':
		Coverage = True
		SbFl = True
	elif opt.replace(" ", "") == '3':
		MbFl = True

table = PrettyTable()
table.field_names = ["Statement #", "Passed Tests", "Failed Tests", "Tarantula", "Ochiai", "OP2"]
	

if Coverage == True:
	rep = raw_input("Would you like to store a report of the coverage information? y or n \n")
	if rep == 'y' or rep == 'Y':
		report = True
if SbFl == True:
	Spectrum_Formula = raw_input("Which Spectrum-based formula(s) would you like to use\n(For multiple selections, separate each entry by a comma)\n 1.) Tarantula \n 2.) Ochiai \n 3.) OP2 \n")


if MbFl == True:
	coverage_info, Mutation_Suspiciousness = ProFL_m.GetSuspiciousness(initial_test_results, mutated_data, program_file, test_file, added_statements, total_passed_tests, total_failed_tests, number_of_mutants)
elif Coverage:
	coverage_info = Coverage.GetCoverage(initial_test_results, mutated_data, program_file, test_file, added_statements)

if SbFl == True:
	Spectrum_Suspiciousness = ProFL_s.GetSuspiciousness(table, program_file, initial_test_results, coverage_info, total_failed_tests, total_passed_tests)	
	Spectrum_Formula = Spectrum_Formula.split(",")
for formula in Spectrum_Formula:
	if formula.replace(" ", "") == '1':
		print(int(topX) + 1)
		tarantula_table = Spectrum_Suspiciousness
		tarantula_table.sortby = "Tarantula"
		tarantula_table.reversesort = True
		print(tarantula_table.get_string(start=0, end=int(topX) + 1, fields=["Statement #", "Passed Tests", "Failed Tests", "Tarantula"], title="Tarantula"))
	elif formula.replace(" ", "") == '2':
		ochiai_table = Spectrum_Suspiciousness
		ochiai_table.sortby = "Ochiai"
		ochiai_table.reversesort = True
		print(ochiai_table.get_string(reversesort = True, sortby="Ochiai", start=0, end=int(topX) + 1, fields=["Statement #", "Passed Tests", "Failed Tests",  "Ochiai"], title="Ochiai"))
	elif formula.replace(" ", "") == '3':
		op2_table = Spectrum_Suspiciousness
		print(op2_table.get_string(reversesort = True, sortby="OP2", start=0, end=int(topX) + 1, fields=["Statement #", "Passed Tests", "Failed Tests", "OP2"], title="OP2"))
		
if MbFl == True:
	Mutation_Suspiciousness.sortby = "Mutation-Based"
	Mutation_Suspiciousness.reversesort = True
	print(Mutation_Suspiciousness.get_string(reversesort = True, sortby="Mutation-Based", start=0, end=int(topX) + 1, title="ProFl-m"))
		
#selection = menu.process_user_input()
#print(selection)








