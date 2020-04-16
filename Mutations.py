def removal(s, index):
	global mutated_data
	temp_map = ("", index)
	mutated_data.append(temp_map)
	number_of_mutants[index] += 1
	##print("Remove")

def disToCon(s, index):
	global mutated_data
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

def conToDis(s, index):
	global mutated_data
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

def varToAnom(s, index):
	global mutated_data
	##print("")

def AO(s, index):
	global mutated_data
	if '*' in s:
		##print("FOUND")
		s = s.replace("*", "-")
	elif '+' in s:
		s = s.replace("+", "*")
	elif '-' in s:
		s = s.replace("-", "+")
	temp_map = (s, index)
	mutated_data.append(temp_map)
	number_of_mutants[index] += 1
	##print("Arithmetic")

def RO(s, index):
	global mutated_data
	if '<' in s:
		s = s.replace("<", ">")
	elif '>' in s:
		s = s.replace(">", "<")
	temp_map = (s, index)
	mutated_data.append(temp_map)
	number_of_mutants[index] += 1
	##print("Relational")

def Negation(s, index):
	global mutated_data
	s = s.replace("\+", "")
	temp_map = (s, index)
	mutated_data.append(temp_map)
	number_of_mutants[index] += 1