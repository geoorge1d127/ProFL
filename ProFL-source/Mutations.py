def replace_str_index(text,index=0,replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])

def Create_Mutants(program):
	data = ""
	with open(program, 'r') as file:
	    data = file.read().replace("", "")
	mutated_data = []
	data = data.split("\n")
	open_count = 0
	closed_count = 0
	#cleanup(data)
	original = list(data)
	s = list(original)
	number_of_mutants = []
	for (i, index) in enumerate(s):
		number_of_mutants.append(0)
		#fail_to_pass.append(0)
		#pass_to_fail.append(0)
		#suspiciousness.append(0.0)
		removal(s[i], i, mutated_data, number_of_mutants)
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
				conToDis(s[i], i, mutated_data, number_of_mutants)
			elif statement[a] == ";" and open_count == closed_count:
				disToCon(s[i], i, mutated_data, number_of_mutants)
			elif statement[a] == "*":
				AO(s[i], i, mutated_data, number_of_mutants)
			elif statement[a] == "+" and p_char != '\\':
				AO(s[i], i, mutated_data, number_of_mutants)
			elif statement[a] == "-" and p_char != ':':
				AO(s[i], i, mutated_data, number_of_mutants)
			elif statement[a] == "*":
				AO(s[i], i, mutated_data, number_of_mutants)
			elif statement[a] == ">" and p_char != '-':
				RO(s[i], i, mutated_data, number_of_mutants)
			elif statement[a] == "<":
				RO(s[i], i, mutated_data, number_of_mutants)
			elif statement[a] == "+" and p_char == '\\':
				Negation(s[i], i, mutated_data, number_of_mutants)
	return mutated_data, number_of_mutants


def removal(s, index, mutated_data, number_of_mutants):
	temp_map = ("", index)
	mutated_data.append(temp_map)
	number_of_mutants[index] += 1
	##print("Remove")

def disToCon(s, index, mutated_data, number_of_mutants):
	open_count = 0
	closed_count = 0
	for a, j in enumerate(s):  
		if s[a] == "(":
			open_count = open_count + 1
		elif s[a] == ")":
			closed_count = closed_count + 1
		elif s[a] == ";" and open_count == closed_count:
			s = replace_str_index(s, a, ",")

	temp_map = (s, index)
	mutated_data.append(temp_map)

	number_of_mutants[index] += 1
	##print("Disjunct")

def conToDis(s, index, mutated_data, number_of_mutants):
	open_count = 0
	closed_count = 0
	for a, j in enumerate(s): 
		if s[a] == "(":
			open_count = open_count + 1
		elif s[a] == ")":
			closed_count = closed_count + 1
		elif s[a] == "," and open_count == closed_count:
			s = replace_str_index(s, a, ";")
	s = replace_str_index(s, len(s) - 1, ", !.")
	temp_map = (s, index)
	mutated_data.append(temp_map)
	number_of_mutants[index] += 1
	##print("Conjunct")

def varToAnom(s, index, mutated_data, number_of_mutants):
	print("")

def AO(s, index, mutated_data, number_of_mutants):
	if '*' in s:
		##print("FOUND")
		s = s.replace("*", "-")
	elif '+' in s:
		s = s.replace(" + ", "*")
	elif '-' in s:
		s = s.replace(" - ", "+")
	temp_map = (s, index)
	mutated_data.append(temp_map)
	number_of_mutants[index] += 1
	##print("Arithmetic")

def RO(s, index, mutated_data, number_of_mutants):
	if '<' in s:
		s = s.replace("<", ">")
	elif '>' in s:
		s = s.replace(">", "<")
	temp_map = (s, index)
	mutated_data.append(temp_map)
	number_of_mutants[index] += 1
	##print("Relational")

def Negation(s, index, mutated_data, number_of_mutants):
	s = s.replace("\+", "")
	temp_map = (s, index)
	mutated_data.append(temp_map)
	number_of_mutants[index] += 1