#######Dependencies#######

import os
import shlex, subprocess
from prettytable import PrettyTable
from math import sqrt
import re
#import mutations
import time
import click


def Coverage(file):
	print("Coverage")
	decision = input("Would you like to generate a report")

def SbFL(file):
	print("Spectrum-based Technique")

def MbFL(file):
	print("Mutation-based Technique")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def getInitialResults():
	global passed_tests
	global failed_tests
	global initial_test_results
	for line in test_file:
		test_number = 0
		if "test(" in line:
			coverage_info.append([])
			#put Each test into a test file
			newTestFile = open("runtimeModel.plt", 'w')
			newTestFile.write(":- begin_tests(" + programStr + ").\n:- include(" + programStr + ").\n")
			newTestFile.write("float_eq(Real, Expected) :- Expected is round(Real * 100). \n")		
			newTestFile.write("factorial_test_case_generator(0,1).\n")
			newTestFile.write("factorial_test_case_generator(1,1).\n")
			newTestFile.write("factorial_test_case_generator(2,2).\n")
			newTestFile.write("factorial_test_case_generator(3,6).\n")
			newTestFile.write("factorial_test_case_generator(5,120).\n")
			newTestFile.write("factorial_test_case_generator(6,720).\n")
			newTestFile.write("factorial_test_case_generator(7,5040).\n")
			newTestFile.write("factorial_test_case_generator(8,40320).\n")
			newTestFile.write("factorial_test_case_generator(20,2432902008176640000).\n")


			newTestFile.write(line)
			
			newTestFile.write("\n:- end_tests(" + programStr + ").")

			#Run tests and print out results
			command = "swipl -f " + programStr + ".pl -s runtimeModel.plt -g run_tests,halt -t 'halt(1)'"
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
		test_number += 1


click.clear()
print(bcolors.HEADER + bcolors.BOLD + "\n *****ProFL*****" + bcolors.ENDC)
program_file = raw_input("\n Enter the name of your prolog model (ending with '.pl')")

test_file = raw_input("\n Enter the name of the test suite file (ending with 'plt'")

decision = raw_input("  What would you like to do?\n(For multiple selections, separate each entry by a comma) \n 1.) Determine Coverage \n 2.) Spectrum-based Fault Localization \n 3.) Mutation-based Fault Localization \n")

decisions = decision.split(",")
report = False
Spectrum = ""
for opt in decisions:
	if opt.replace(" ", "") == '1':
		rep = raw_input("Would you like to print out a report of the coverage information? y or n \n")
		if rep == 'y' or rep == 'Y':
			report = True

	elif opt.replace(" ", "") == '2':
		Spectrum = raw_input("Which Spectrum-based formula(s) would you like to use\n(For multiple selections, separate each entry by a comma)\n 1.) Tarantula \n 2.) Ochiai \n 3.) OP2 \n")



#selection = menu.process_user_input()
#print(selection)
