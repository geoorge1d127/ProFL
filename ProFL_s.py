from prettytable import PrettyTable
from math import sqrt


def divide(x,y):
    try:
        return x/y
    except ZeroDivisionError:
        return 0


#Apply Tarantula equation to each statement
def Tarantula(totalFailed, totalPassed, passed, failed):
	#suspiciousness = float((float(passed / totalPassed) / float(float(passed / totalPassed) + float(failed / totalFailed))))
	suspiciousness = divide(divide(passed, totalPassed), divide(passed , totalPassed) + divide(failed, totalFailed))
	return suspiciousness

#Apply Ochiai equation to each statement
def Ochiai(totalFailed, totalPassed, passed, failed):
	a11 = failed
	a1 = totalFailed - failed
	a10 = passed
	suspiciousness = divide(a11, sqrt(totalFailed * (failed + passed)))
	return suspiciousness

def Op2(totalFailed, totalPassed, passed, failed):
	suspiciousness = failed - (divide(passed , totalPassed + 1))
	return suspiciousness



def GetSuspiciousness(table, program, initial_test_results, coverage_info, totalFailed, totalPassed):
	spnpassed_Grid = []
	spnfailed_Grid = []
	program_file = open("models/" + program)
	for line in program_file:
		spnfailed_Grid.append(0)
		spnpassed_Grid.append(0)
	for index, test in enumerate(coverage_info):
		for line in test:
			if initial_test_results[index] == "pass":
				spnpassed_Grid[line] += 1
			else:
				spnfailed_Grid[line] += 1
	program_file.seek(0)
	for index,line in enumerate(program_file):
		if spnfailed_Grid[index] == 0 and spnpassed_Grid[index] == 0:
			tarantula = None
			ochiai = None
			op2 = None
			table.add_row([index + 1, spnpassed_Grid[index], spnfailed_Grid[index], tarantula, ochiai, op2])
		else:
			tarantula = Tarantula(float(totalFailed), float(totalPassed), float(spnpassed_Grid[index]), float(spnfailed_Grid[index]))
			ochiai = Ochiai(float(totalFailed), float(totalPassed), float(spnpassed_Grid[index]), float(spnfailed_Grid[index]))
			op2 = Op2(float(totalFailed), float(totalPassed), float(spnpassed_Grid[index]), float(spnfailed_Grid[index]))
			table.add_row([index + 1, spnpassed_Grid[index], spnfailed_Grid[index], tarantula, ochiai, op2])
	return table







