#######Dependencies#######

import sys
sys.path.insert(0, 'ProFL-source')
import os
import shlex, subprocess
from prettytable import PrettyTable
from math import sqrt
import re
#import mutations
import time
import click
import argparse
import shutil
import Coverage
import Mutations
import ProFL_s
import ProFL_m


parser = argparse.ArgumentParser()
parser._action_groups.pop()
required = parser.add_argument_group('required arguments')
optional = parser.add_argument_group('optional arguments')
required.add_argument("-p", "--program-path", help="Pass the filename of the faulty Prolog program.", required=True)
required.add_argument("-t", "--test-suite", help="Pass the file name of the plunit test suite.", required=True)
required.add_argument("-f", "--fl-technique", help="Pass the faultlocalization technique to use. The value should be '-spectrum','-mutation', or '-both'.", required=True)
required.add_argument("-v", "--view", help='Pass how much of the ranked  suspicious  list  to  view.  The  value  should  be  "-top1","-top5", "-top10", or "-all".', required=True)
optional.add_argument("-s","--suspicious-formula", help='This argument is optional and is used when the fault localization technique is "-spectrum" or"-both". Pass the suspiciousness formula for ProFLs to use. The value should be "-tarantula", "-ochiai", or "-op2". If specifying more than one, separate with a comma, i.e. "-ochiai,-op2". If not specified, all three are used.')
optional.add_argument("-r","--result-path", help='Pass the path to which you want to save the fault localization results. If not specified, the results are only printed to the terminal.')
optional.add_argument("-c","--coverage-path", help= 'Pass the path to which you want to save the coverage results calculated during ProFLs. If not specified, the coverage informationis not saved.')
args = parser.parse_args()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_testName(testfile, index):
	with open(testfile) as file:
		test_num = 0
		for line in file:
			if "test(" in line:
				if test_num == index:
					result = re.search('test(.*):', line)
					return result.group(1)
				test_num += 1


def getInitialResults(program_file, tests):
	passed_tests = 0
	failed_tests = 0
	initial_test_results = []
	added_statements = ""
	programStr = program_file.replace(".pl", "")
	prog = os.path.basename(programStr)
	folder = os.path.dirname(programStr)
	test_file = open(tests)
	for line in test_file:
		if "test(" in line:
			#put Each test into a test file
			newTestFile = open("runtimeModel.plt", 'w')
			newTestFile.write(":- begin_tests(runtimeModel).\n:- include(runtimeModel).\n")
			newTestFile.write(added_statements)

			newTestFile.write(line)
			
			newTestFile.write("\n:- end_tests(runtimeModel).")

			shutil.copyfile(program_file, "runtimeModel.pl")

			#Run tests and print out results
			command = "swipl -f runtimeModel.pl -s runtimeModel.plt -g run_tests,halt -t 'halt(1)'"
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

GetCoverage = False
SbFl = False
MbFl = False
table = PrettyTable()
table.field_names = ["Statement #", "Passed Tests", "Failed Tests", "Tarantula", "Ochiai", "OP2", "Mutation"]
click.clear()
print(bcolors.HEADER + bcolors.BOLD + "\n *****ProFL*****" + bcolors.ENDC)
program_file = args.program_path
assert os.path.exists(program_file), "I did not find the file, " + str(program_file)
test_file = args.test_suite
assert os.path.exists(test_file), "I did not find the file, "+str(test_file)
print(bcolors.HEADER + bcolors.BOLD + "\n ****Calculating Initial Test Results**** \n" + bcolors.ENDC)
initial_test_results, total_passed_tests, total_failed_tests, added_statements = getInitialResults(program_file, test_file)
click.clear()

report = False
Spectrum_Formula = ""
print(bcolors.HEADER + bcolors.BOLD + "\n ****Creating Mutants**** \n"+ bcolors.ENDC)
mutated_data, number_of_mutants = Mutations.Create_Mutants(program_file)
coverage_info = []

if args.fl_technique == "spectrum":
	GetCoverage = True
	SbFl = True
elif args.fl_technique == "mutation":
	MbFl = True
elif args.fl_technique == "both":
	GetCoverage = True
	SbFl = True
	MbFl = True



table = PrettyTable()
table.field_names = ["Statement #", "Passed Tests", "Failed Tests", "Tarantula", "Ochiai", "OP2"]
	
tarantula = False
ochiai = False
op2 = False
if GetCoverage == True:
	if args.coverage_path != None:
		report = True
if SbFl == True:
	if args.suspicious_formula:
		Spectrum_Formula = args.suspicious_formula
	else:
		tarantula = True
		ochiai = True
		op2 = True

if MbFl == True:
	coverage_info, Mutation_Suspiciousness = ProFL_m.GetSuspiciousness(initial_test_results, mutated_data, program_file, test_file, added_statements, total_passed_tests, total_failed_tests, number_of_mutants)
elif GetCoverage:
	coverage_info = Coverage.GetCoverage(initial_test_results, mutated_data, program_file, test_file, added_statements)

if SbFl == True:
	Spectrum_Suspiciousness = ProFL_s.GetSuspiciousness(table, program_file, initial_test_results, coverage_info, total_failed_tests, total_passed_tests)	
	Spectrum_Formula = Spectrum_Formula.split(",")

topX = 10
if args.view == "top1":
	topX = 1
elif args.view == "top5":
	topX = 5
elif args.view == "top10":
	topX = 10






for formula in Spectrum_Formula:
	if formula == "tarantula":
		tarantula = True
	elif formula == "ochiai":
		ochiai = True
	elif formula == "op2":
		op2 = True

results_string = ""

if tarantula:
	print(int(topX) + 1)
	tarantula_table = Spectrum_Suspiciousness
	tarantula_table.sortby = "Tarantula"
	tarantula_table.reversesort = True
	if args.view == "all":
		print(tarantula_table.get_string(fields=["Statement #", "Passed Tests", "Failed Tests", "Tarantula"], title="Tarantula"))
		results_string += tarantula_table.get_html_string(fields=["Statement #", "Passed Tests", "Failed Tests", "Tarantula"], title="Tarantula")
	else:
		print(tarantula_table.get_string(start=0, end=int(topX), fields=["Statement #", "Passed Tests", "Failed Tests", "Tarantula"], title="Tarantula"))
		results_string += tarantula_table.get_html_string(start=0, end=int(topX), fields=["Statement #", "Passed Tests", "Failed Tests", "Tarantula"], title="Tarantula")

if ochiai:
	ochiai_table = Spectrum_Suspiciousness
	ochiai_table.sortby = "Ochiai"
	ochiai_table.reversesort = True
	if args.view == "all":
		print(ochiai_table.get_string(reversesort = True, sortby="Ochiai", fields=["Statement #", "Passed Tests", "Failed Tests",  "Ochiai"], title="Ochiai"))
		results_string += ochiai_table.get_html_string(reversesort = True, sortby="Ochiai", fields=["Statement #", "Passed Tests", "Failed Tests",  "Ochiai"], title="Ochiai")
	else:
		print(ochiai_table.get_string(reversesort = True, sortby="Ochiai", start=0, end=int(topX), fields=["Statement #", "Passed Tests", "Failed Tests",  "Ochiai"], title="Ochiai"))
		results_string += ochiai_table.get_html_string(reversesort = True, sortby="Ochiai", start=0, end=int(topX), fields=["Statement #", "Passed Tests", "Failed Tests",  "Ochiai"], title="Ochiai")
		
if op2:
	op2_table = Spectrum_Suspiciousness
	if args.view == "all":
		print(op2_table.get_string(reversesort = True, sortby="OP2", start=0, end=int(topX), fields=["Statement #", "Passed Tests", "Failed Tests", "OP2"], title="OP2"))
		results_string += op2_table.get_html_string(reversesort = True, sortby="OP2", start=0, end=int(topX), fields=["Statement #", "Passed Tests", "Failed Tests", "OP2"], title="OP2")
	else:
		print(op2_table.get_string(reversesort = True, sortby="OP2", fields=["Statement #", "Passed Tests", "Failed Tests", "OP2"], title="OP2"))
		results_string += op2_table.get_html_string(reversesort = True, sortby="OP2", fields=["Statement #", "Passed Tests", "Failed Tests", "OP2"], title="OP2")

if MbFl == True:
	Mutation_Suspiciousness.sortby = "Mutation-Based"
	Mutation_Suspiciousness.reversesort = True
	if args.view == "all":
		print(Mutation_Suspiciousness.get_string(reversesort = True, sortby="Mutation-Based", title="ProFl-m"))
		results_string += Mutation_Suspiciousness.get_html_string(reversesort = True, sortby="Mutation-Based", title="ProFl-m")
	else:
		print(Mutation_Suspiciousness.get_string(reversesort = True, sortby="Mutation-Based", start=0, end=int(topX), title="ProFl-m"))
		results_string += Mutation_Suspiciousness.get_html_string(reversesort = True, sortby="Mutation-Based", start=0, end=int(topX), title="ProFl-m")
			
#selection = menu.process_user_input()
#print(selection)



if args.result_path != None:
	path = ""
	if args.result_path.endswith("/"):
		path = args.result_path + "ProFL_Report.html"
	else:
		path = args.result_path + "/ProFL_Report.html"

	with open(path, 'w') as file:
		file.write(results_string)


if args.coverage_path != None:
	coverage_table = PrettyTable()
	coverage_table.field_names = ["Statement", "Covered by passing tests", "Covered by failing tests"]
	passed_Grid = []
	failed_Grid = []
	pf = open(program_file)
	for line in pf:
		failed_Grid.append([])
		passed_Grid.append([])
	for index, test in enumerate(coverage_info):
		for line in test:
			if initial_test_results[index] == "pass":
				passed_Grid[line].append(get_testName(test_file, index))
			else:
				failed_Grid[line].append(get_testName(test_file, index))
	pf.seek(0)
	for index, line in enumerate(pf):
		coverage_table.add_row([line, ''.join(passed_Grid[index]), ''.join(failed_Grid[index])])
		coverage_table.add_row(["", "", ""])
	path = ""
	if args.coverage_path.endswith("/"):
		path = args.coverage_path + "ProFL_Coverage_Report.html"
	else:
		path = args.coverage_path + "/ProFL_Coverage_Report.html"

	with open(path, 'w') as file:
		file.write(coverage_table.get_html_string())

os.remove("runtimeModel.plt")
os.remove("mutated_file.pl")
os.remove("runtimeModel.pl")

