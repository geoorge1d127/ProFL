import os
import shlex, subprocess
from prettytable import PrettyTable
from math import sqrt
import re
#import mutations
import time




def compile(data):
	with open('mutated_file.pl', 'w') as f:
	    for item in data:
	        print(item, file=f)


def GetSuspiciousness(initial_test_results, mutated_data, program, tests, added_statements, total_passed, total_failed, number_of_mutants):
	total_pass_to_fail = 0
	total_fail_to_pass = 0
	data = ""
	with open(program, 'r') as file:
	    data = file.read().replace("", "")
	file.close()
	data = data.split("\n")

	spnpassed_Grid = [0] * len(data)
	spnfailed_Grid = [0] * len(data)
	fail_to_pass = [0] * len(data)
	pass_to_fail = [0] * len(data)
	original = list(data)
	coverage_info = []
	test_file = open(tests)
	for (mutant, i) in mutated_data:
		#print mutation + "    " + str(i)
		##print mutation + "GG"
		data[i] = mutant
		print("MUTANT: " + str(mutant) + str(i))
		compile(data)
		getResults(i, initial_test_results, test_file, coverage_info, added_statements, fail_to_pass, pass_to_fail, total_fail_to_pass, total_pass_to_fail, spnfailed_Grid, spnpassed_Grid)
		data = list(original)

	indexes_covered = []
	table = PrettyTable()
	table.field_names = ["Statement #", "Passed Tests", "Failed Tests", "Mutation-Based"]
	f2p = float(total_fail_to_pass)
	mutP = float(len(mutated_data))
	fp = float(total_failed)
	pp = float(total_passed)
	p2f = float(total_pass_to_fail)
	failed_tests = total_failed
	passed_tests = total_passed
	#print("GGGG" + str(p2f))
	weight = float(divide(f2p, mutP * fp) * divide(mutP * pp, p2f))
	#print(weight)
	Ms = float(0)
	previous_index = 0
	#print(f2p + mutP + fp + pp + p2f)
	for mutant, index in mutated_data:
		if index != previous_index:
			if spnpassed_Grid[previous_index] == 0 and spnfailed_Grid[previous_index] == 0:
				table.add_row([index, spnpassed_Grid[previous_index], spnfailed_Grid[previous_index], None])
			else:
				table.add_row([index, spnpassed_Grid[previous_index], spnfailed_Grid[previous_index], Ms])
		else:
			if index in indexes_covered:
				Ms += float((divide(float(fail_to_pass[index]), float(failed_tests)) - weight) * (divide(float(pass_to_fail[index]), float(passed_tests))))
			else:
				Ms += float(divide(1.0, float(number_of_mutants[index])) * ((divide(float(fail_to_pass[index]), float(failed_tests)) - weight) * (divide(float(pass_to_fail[index]), float(passed_tests)))))
				indexes_covered.append(index)
		previous_index = index
	#table.add_row([index + 1, spnpassed_Grid[index], spnfailed_Grid[index], Ms])
			#print(float((divide(float(fail_to_pass[index]), float(failed_tests)) - weight) * (divide(float(pass_to_fail[index]), float(passed_tests)))))
	

	return coverage_info, table


def divide(x,y):
    try:
        return float(x / y)
    except ZeroDivisionError:
        return 0


def getResults(index, initial_test_results, test_file, coverage_info, added_statements, fail_to_pass, pass_to_fail, total_fail_to_pass, total_pass_to_fail, spnfailed_Grid, spnpassed_Grid):
	test_number = 0
	for (i, line) in enumerate(test_file):
		if "test(" in line:
			if len(coverage_info) - 1 < test_number:
				coverage_info.append([])
			#put Each test into a test file
			
			newTestFile = open("runtimeModel.plt", 'w')
			newTestFile.write(":- begin_tests(mutated_file).\n:- include(mutated_file).\n")
			newTestFile.write(added_statements)
			newTestFile.write(line)
			newTestFile.write("\n:- end_tests(mutated_file).")

			#Run tests and ##print out results
			command = "swipl -f mutated_file.pl -s runtimeModel.plt -g run_tests,halt -t 'halt(1)'"


			#Close files
			newTestFile.close()

			
			#*************PASSED TEST********#####
			try:
				output = subprocess.check_call(command.split())
				
				if initial_test_results[test_number] == "fail":

					if index not in coverage_info[test_number]:
						coverage_info[test_number].append(index)
						spnfailed_Grid[index] += 1
					fail_to_pass[index] += 1
					total_fail_to_pass += 1


			##***********FAILED TEST************#####
			except subprocess.CalledProcessError:
				if initial_test_results[test_number] == "pass":
					#print(test_number)
					if index not in coverage_info[test_number]:
						coverage_info[test_number].append(index)
						spnpassed_Grid[index] += 1
					pass_to_fail[index] += 1
					total_pass_to_fail += 1

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


def mutate(programStr, initial_test_results, passed_tests, failed_tests):
	global original
	global mutated_data
	global coverage_info
	global suspiciousness
	global number_of_mutants
	global fail_to_pass 
	global pass_to_fail 
	global total_pass_to_fail 
	global total_fail_to_pass

	start_time = time.time()
	test_file = open(programStr + ".plt")
	data = ""
	with open(programStr + '.pl', 'r') as file:
	    data = file.read().replace("", "")

	data = data.split("\n")
	#for line in test_file:
	#	if "test(" in line:
	#		coverage_info.append([])
	print(data)
	test_file.seek(0)
	open_count = 0
	closed_count = 0
	#cleanup(data)
	original = list(data)
	s = list(original)
	for (i, index) in enumerate(s):
		number_of_mutants.append(0)
		fail_to_pass.append(0)
		pass_to_fail.append(0)
		suspiciousness.append(0.0)
		removal(s[i], i)
		##print(s[i])
		statement = s[i]
		for a, j in enumerate(statement):
			try:
			    p_char = statement[a - 1]
			except IndexError:
			    print('index out of bounds with p_char')  
			if statement[a] == "(":
				open_count = open_count + 1
			elif statement[a] == ")":
				closed_count = closed_count + 1
			elif statement[a] == "," and open_count == closed_count:
				#print("removed")
				conToDis(s[i], i)
			elif statement[a] == ";" and open_count == closed_count:
				disToCon(s[i], i)
			elif statement[a] == "*":
				AO(s[i], i)
			elif statement[a] == "+" and p_char != '\\':
				AO(s[i], i)
			elif statement[a] == "-" and p_char != ':':
				AO(s[i], i)
			elif statement[a] == "*":
				AO(s[i], i)
			elif statement[a] == ">":
				RO(s[i], i)
			elif statement[a] == "<":
				RO(s[i], i)
			elif statement[a] == "+" and p_char == '\\':
				Negation(s[i], i)
	print(mutated_data)
	for (mutant, i) in mutated_data:
		#print mutation + "    " + str(i)
		##print mutation + "GG"
		data[i] = mutant
		print("MUTANT: " + str(mutant))
		compile(data)
		#print()
		getResults(i, initial_test_results, test_file)
		coverage_time = time.time() - start_time
		data = list(original)

	test_file.seek(0)
	#file.seek(0)
	test_file.close()
	file.close()
	calculate(failed_tests, passed_tests)
	mutation_time = time.time() - start_time
	return suspiciousness, coverage_info, coverage_time, mutation_time

def calculate(failed_tests, passed_tests):
	global mutated_data 
	global number_of_mutants
	global fail_to_pass 
	global pass_to_fail 
	global total_pass_to_fail 
	global total_fail_to_pass 
	global suspiciousness
	indexes_covered = []


	f2p = float(total_fail_to_pass)
	mutP = float(len(mutated_data))
	fp = float(failed_tests)
	pp = float(passed_tests)
	p2f = float(total_pass_to_fail)
	#print("GGGG" + str(p2f))
	weight = float(divide(f2p, mutP * fp) * divide(mutP * pp, p2f))
	#print(weight)

	#print(f2p + mutP + fp + pp + p2f)
	for mutant, index in mutated_data:
		if fail_to_pass[index] == 0 and pass_to_fail[index] == 0:
			suspiciousness[index] = None
		else:
			if index in indexes_covered:
				suspiciousness[index] += float((divide(float(fail_to_pass[index]), float(failed_tests)) - weight) * (divide(float(pass_to_fail[index]), float(passed_tests))))
			else:
				suspiciousness[index] += float(divide(1.0, float(number_of_mutants[index])) * ((divide(float(fail_to_pass[index]), float(failed_tests)) - weight) * (divide(float(pass_to_fail[index]), float(passed_tests)))))
				indexes_covered.append(index)
			#print(float((divide(float(fail_to_pass[index]), float(failed_tests)) - weight) * (divide(float(pass_to_fail[index]), float(passed_tests)))))
	return suspiciousness





#getInitialResults()
def mm(filename, init_results, passed_tests, failed_tests):
	MutationFl, coverage_info, coverage_time, mutation_time = mutate(filename, init_results, passed_tests, failed_tests)
	return MutationFl, coverage_info, coverage_time, mutation_time
#print(coverage_info)
	#calculate()
#print(initial_test_results)
#print(mutated_data)
#print(total_pass_to_fail)
#print(total_fail_to_pass)
#print(pass_to_fail)
#print(fail_to_pass)
#print(suspiciousness)



