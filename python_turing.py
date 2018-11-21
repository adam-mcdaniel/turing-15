import parsley, sys, os, pyparsing


listOfVariablesAndTypes = {}

listOfFunctions = []

lastClassName = ""

pwd = os.path.dirname(sys.argv[2])
print(pwd)

scope = ""
parser = None

indentation_level = 0

class_vars = []

pwd = os.path.dirname(sys.argv[1])
print(pwd)

def assign(op):
	# if op == "<-":
	# 	return "="
	return op

def returnPrint(op):
	# if op == "<-":
	# 	return "="
	print(op)
	return op

def setLastClass(className):
	global lastClassName
	lastClassName = className
	print("set class: " + lastClassName)
	# print(listOfFunctions)
	return className

def returnLastClass():
	global lastClassName
	print("get class: " + lastClassName)
	return lastClassName

def markList(name):
	global listOfVariablesAndTypes, scope
	listOfVariablesAndTypes[str(name)+":"+str(scope)] = "auto "
	return name

def returnAutoReserved(left, op, right):
	global listOfVariablesAndTypes, scope

	if "." in left:
		left = str(left[:left.index(".")])

	if "[" in left:
		print(str(left)+":"+str(scope))
		left = left.replace(left[left.index("["):left.index("]")+1],"")
		print("changed to: " + str(left)+":"+str(scope))

	if str(left)+":"+str(scope) in listOfVariablesAndTypes:
		return str(left) + str(op) + str(right)
	else:
		listOfVariablesAndTypes[str(left)+":"+str(scope)] = ""
	 	return '__auto_reserved__(' + str(left) + ', ' + str(right) + ')'

def checkVarInList(left, right, Type=""):
	global listOfVariablesAndTypes, scope
	# print(listOfVariablesAndTypes)
	# print(left)

	print(str(left)+":"+str(scope) + " received")

	if "." in left:
		left = str(left[:left.index(".")])

	if "[" in left:
		print(str(left)+":"+str(scope))
		left =  left.replace(left[left.index('['):left[::-1].index(']')-1]+']', "")
		print("changed to: " + str(left)+":"+str(scope))


	if str(left)+":"+str(scope) in listOfVariablesAndTypes:
		return ""
		# pass
	else:
		if Type == "var":
			# print("2:identifier")
			listOfVariablesAndTypes[str(left)+":"+str(scope)] = listOfVariablesAndTypes[str(right)]
		else:

			if Type == "intlist":
				listOfVariablesAndTypes[str(left)+":"+str(scope)] = "vector <int> "
				# print("2:intlist")

			elif Type == "int":
				listOfVariablesAndTypes[str(left)+":"+str(scope)] = "int "
				# print("2:number")

			elif Type == "math":
				listOfVariablesAndTypes[str(left)+":"+str(scope)] = "int "
				# print("2:math")

			elif Type == "strlist":
				listOfVariablesAndTypes[str(left)+":"+str(scope)] = "vector <string> "
				# print("2:intlist")

			elif Type == "str":
				listOfVariablesAndTypes[str(left)+":"+str(scope)] = "string "
				# print("2:string")

			elif Type == "bool":
				listOfVariablesAndTypes[str(left)+":"+str(scope)] = "bool "
				# print("2:bool")

			elif Type == "functioncall":
				listOfVariablesAndTypes[str(left)+":"+str(scope)] = "auto "

			elif Type == "auto":
				listOfVariablesAndTypes[str(left)+":"+str(scope)] = "auto "
				# print("2:bool")

		# # print("type: " + listOfVariablesAndTypes[str(left)])
		if str(left)+":"+str(scope) in listOfVariablesAndTypes:
			return str(listOfVariablesAndTypes[str(left)+":"+str(scope)])
		else:
			return "auto "
		# return "auto "

def setScope(newScope):
	global scope
	print("set scope: "+newScope)
	scope = newScope
	return newScope


def returnTemplate(listOfParameters):
	# print(listOfParameters)
	changedList = []
	if len(listOfParameters) > 0:
		i = 0
		for j in listOfParameters[:-1]:
			changedList.append("typename type"+str(i)+", ")
			i += 1
		changedList.append("typename type"+str(i)+" ")
		return 'template<'+''.join(changedList)+'>'
	else:
		return ''

def returnTypedParameters(listOfParameters):
	# print(listOfParameters)
	changedList = []
	if len(listOfParameters) > 0:
		i = 0
		for j in listOfParameters[:-1]:
			changedList.append("type"+str(i)+" "+listOfParameters[i]+", ")
			i += 1
		changedList.append("type"+str(i)+" "+listOfParameters[i]+" ")
		return ''.join(changedList)
	else:
		return ''



def g_or_l(var):
	global class_vars
	if "." in var:
		if var[:var.index('.')] in class_vars:
			return "this."+var
	if var in class_vars:
		return "this."+var

	return var

def g_or_l_args(list_vars):
	global class_vars
	list_vars_new = []
	for var in list_vars:
		if "." in var:
			if var[:var.index('.')] in class_vars:
				list_vars_new.append("this."+var)
			else:
				list_vars_new.append(var)
		else:
			if var in class_vars:
				list_vars_new.append("this."+var)
			else:
				list_vars_new.append(var)

	return list_vars_new

def empty_locals():
	global class_vars
	class_vars = []
	return ''

def append_local_var(var):
	global class_vars
	class_vars.append(var)
	return var

def indent(contents):
	global indentation_level
	indentation_level += 1
	content_lines = contents.split('\n')
	return_contents = '\n'+ '\t'*indentation_level +('\n'+'\t'*indentation_level).join(content_lines)
	return return_contents

def unindent():
	global indentation_level
	indentation_level -= 1
	return ''

def require(name):
	global parser, pwd
	name = name.replace('"','')
	with open(os.path.join(pwd, name), "r") as f:
		contents = f.read()
		f.close()

	print(contents)
	return parser(contents).req()


def assign(op):
	# if op == "<-":
	# 	return "="
	return op

def returnPrint(op):
	# if op == "<-":
	# 	return "="
	print(op)
	return op

def moveFunction(func):
	global listOfFunctions
	listOfFunctions.append(func)
	# print(listOfFunctions)
	return ''

def returnParameters(listOfParameters):
	# print(listOfParameters)
	changedList = []
	if len(listOfParameters) > 0:
		i = 0
		for j in listOfParameters[:-1]:
			changedList.append(listOfParameters[i]+", ")
			i += 1
		changedList.append(listOfParameters[i]+" ")
		# changedList = [','] + changedList
		return ''.join(changedList)
	else:
		return ''

def returnClassParameters(listOfParameters):
	# print(listOfParameters)
	changedList = []
	if len(listOfParameters) > 0:
		i = 0
		for j in listOfParameters[:-1]:
			changedList.append(listOfParameters[i]+", ")
			i += 1
		changedList.append(listOfParameters[i]+" ")
		# changedList = [','] + changedList
		if len(changedList) > 0:
			changedList = [','] + changedList
		return ''.join(changedList)
	else:
		return ''



if sys.argv[1] == '-p':
	print("Python it is!")

	keywords = ['for', 'while', 'if', 'elif', 'else']
	arg_keywords = ['read', 'print', 'println', 'system', 'pass']

	parser = parsley.makeGrammar("""

allw = w endl w

w = <(' ' | '\\t')*>
endl = <('\\n')*>
mw = <('\\n')+>

digit = anything:x ?(x in '0123456789.')
char = anything:x ?(x in '0123456789_.')
number = (<digit+>:ds -> str(ds)
			| '-' <digit+>:ds -> '-' + str(ds)
			)

letter = anything:x ?(x in 'abcdefghijklmnopqrstuvwxyz' or x in 'abcdefghijklmnopqrstuvwxyz'.upper())

indice = <'['+>:a <( (letter|char)
				| w (number|identifier) w
			)*>:b <']'+>:c -> str(a) + str(b) + str(c)

identifier = w <(letter|char|indice)+>:ds -> str(ds)
string = (multi_line_string | string)
single_line_string = '"' (~'"' anything)*:c '"' -> '"' + ''.join(c) + '"'
multi_line_string = '\\"\\"\\"' (~'\\"\\"\\"' anything)*:c '\\"\\"\\"' -> '\\"\\"\\"' + ''.join(c) + '\\"\\"\\"'

# assign = ('=' | '+=' | '-='):a -> a
assign = '<-' -> '='

operator = anything:x ?(x in '*/+-()') -> str(x)


bool = ('True' | 'False'):a -> str(a)


# functioncall_object = functioncall | past_assignment | number | bool | string | identifier
functioncall_object = functioncall | number | bool | string | identifier
object = number | bool | string | identifier

whileloop = '(' allw 'while' w functioncall_object:a mw statement*:b allw ')' allw -> 'while (' + g_or_l(str(a)) + '):\\n' + indent(''.join(b)) + '\\n' + unindent()

forloop = '(' allw 'for' w identifier:a w 'in' w (functioncall|identifier):b mw statement*:c allw ')' allw -> 'for ' + str(a) + ' in ' + g_or_l(str(b)) + ':\\n' + indent(''.join(c)) + '\\n' + unindent()


if = '(' allw 'if' w functioncall_object:a mw statement*:b allw ')' allw -> 'if (' + g_or_l(str(a)) + '):\\n' + indent(''.join(b)) + '\\n' + unindent()

elif = '(' allw 'elif' w functioncall_object:a mw statement*:b allw ')' allw -> 'elif (' + g_or_l(str(a)) + '):\\n' + indent(''.join(b)) + '\\n' + unindent()
else = '(' allw 'else' mw statement*:a allw ')' allw -> 'else:\\n' + indent(''.join(a)) + '\\n' + unindent()


comment = allw ';' <(~'\\n' anything)*> -> ''


past_assignment = allw identifier:left w assign:op w ( bool:right -> 				str(left) + assign(str(op)) + str(right)
										| number:right -> 							str(left) + assign(str(op)) + str(right)
										| string:right 	-> 							str(left) + assign(str(op)) + str(right)
										| identifier:right -> 						str(left) + assign(str(op)) + str(right)
										| functioncall:right -> 					str(left) + assign(str(op)) + str(right)
										)

method_assignment = allw identifier:left w assign:op w ( bool:right -> 				g_or_l(str(left)) + assign(str(op)) + g_or_l(str(right))
										| number:right -> 							g_or_l(str(left)) + assign(str(op)) + g_or_l(str(right))
										| string:right 	-> 							g_or_l(str(left)) + assign(str(op)) + g_or_l(str(right))
										| identifier:right -> 						g_or_l(str(left)) + assign(str(op)) + g_or_l(str(right))
										| functioncall:right -> 					g_or_l(str(left)) + assign(str(op)) + g_or_l(str(right))
										)

functioncall = allw '(' identifier:func ?(func not in keywords) allw (allw functioncall_object)*:args allw ')' w -> g_or_l(str(func)) + '(' + str(','.join(g_or_l_args(args))) + ')'
local_functioncall = allw '(' identifier:func ?(func not in keywords) allw (allw functioncall_object)*:args allw ')' w -> g_or_l(str(func)) + '(' + str(','.join(args)) + ')'




function_begin = '(' allw 'func' w identifier:a -> 'def ' + str(a)
functiondef = function_begin:a w (w object)*:b allw statement*:c allw ')' allw -> a + '(' + str(returnParameters(b) + '):\\n' + indent(''.join(c)) + '\\n\\n') + unindent()


require =  '(' allw 'require' w string:a w ')' -> require(a+'.tr')
cpp_require =  '(' allw '!require' w (string|identifier):a w ')' -> moveFunction('from '+str(a).replace('"', '')+' import *\\n\\n')
imported_require =  '(' allw 'require' w string:a w ')' -> ''

return = (
		allw '(' w 'return' w functioncall_object:a w ')' w -> 'return ' + str(a)
		)
pass = (
		allw '(' w 'pass':a w ')' w -> 'pass'
		)

class_begin = '(' allw 'class' w identifier:a -> 'class ' + str(a)
classdef = (
			class_begin:a allw class_statement*:b allw ')' allw -> moveFunction( str(a) + ':\\n' + indent(''.join(b)) + '\\n\\n') + unindent() + empty_locals()
			| class_begin:a w identifier:b allw class_statement*:c allw ')' allw -> moveFunction( str(a) + '(' + str(b) + '):\\n' + indent(''.join(c)) + '\\n\\n') + unindent() + empty_locals()
			)

constructor = '(' allw 'init' w (w object)*:a allw method_statement*:b allw ')' allw -> '\\n' + 'def __init__(this' + str(returnClassParameters(a)) + '):\\n' + indent(''.join(b)) + '\\n' + unindent()
methoddef = '(' allw 'func' w identifier:a w (w object)*:b allw method_statement*:c allw ')' allw -> 'def ' + append_local_var(a) + '(this' + str(returnClassParameters(b)) + '):\\n' + indent(''.join(c)) + '\\n' + unindent()


set = allw identifier:a w assign w object:b allw -> append_local_var(a) + ' = ' + str(b) + '\\n'

# list = allw identifier:a w assign w '(' w 'list' w '[' '['*:q w (identifier|w):b w ']' ']'*:u w ')' w -> append_local_var(a) + ' = [' + len(q)*'[' + len(u)*']' + ']'
list = allw identifier:a w assign w '(' w 'list' w '[' '['*:q w (identifier|w):b w ']' ']'*:u w ')' w -> (a) + ' = [' + ']'
set_list = allw identifier:a w assign w '(' w 'list' w '[' '['*:q w (identifier|w):b w ']' ']'*:u w ')' w -> append_local_var(a) + ' = [' + ']'

set_function_call = allw identifier:a w assign w local_functioncall:b allw -> append_local_var(a) + ' = ' + str(b) + '\\n'

setmethod = '(' allw 'set' allw (allw set|set_list|set_function_call|comment)*:a allw ')' allw -> '\\n'.join(a)+'\\n'


class_statement = ( allw comment
			| allw list:a endl allw -> a + "\\n"
			# | allw print:a endl allw  -> a + "\\n"
			# | allw read:a endl allw  -> a + "\\n"
			# | allw system:a endl allw  -> a + "\\n"
			| allw return:a endl allw  -> a + "\\n"
			| allw pass:a endl allw  -> a + "\\n"
			| allw whileloop:a -> a + "\\n"
			| allw forloop:a -> a + "\\n"
			| allw if:a -> a + "\\n"
			| allw elif:a -> a + "\\n"
			| allw else:a -> a + "\\n"
			| allw setmethod:a -> a + "\\n"
			| allw constructor:a -> a + "\\n"
			| allw methoddef:a -> a + "\\n"
			| allw functioncall:a endl allw  -> a + "\\n"
			)

statement = ( allw comment
			| allw list:a endl allw -> a + "\\n"
			# | allw set:a endl allw -> a + "\\n"
			| allw past_assignment:a endl allw  -> a + "\\n"
			# | allw print:a endl allw  -> a + "\\n"
			# | allw read:a endl allw  -> a + "\\n"
			# | allw system:a endl allw  -> a + "\\n"
			| allw return:a endl allw  -> a + "\\n"
			| allw pass:a endl allw  -> a + "\\n"
			| allw whileloop:a -> a + "\\n"
			| allw forloop:a -> a + "\\n"
			| allw if:a -> a + "\\n"
			| allw elif:a -> a + "\\n"
			| allw else:a -> a + "\\n"
			| allw classdef:a endl allw -> a
			| allw functiondef:a -> a + "\\n"
			| allw cpp_require:a endl allw  -> a
			| allw require:a endl allw  -> a
			| allw functioncall:a endl allw  -> a + "\\n"
			)

method_statement = ( allw comment
			| allw list:a endl allw -> a + "\\n"
			# | allw set:a endl allw -> a + "\\n"
			| allw method_assignment:a endl allw  -> a + "\\n"
			# | allw print:a endl allw  -> a + "\\n"
			# | allw read:a endl allw  -> a + "\\n"
			# | allw system:a endl allw  -> a + "\\n"
			| allw return:a endl allw  -> a + "\\n"
			| allw pass:a endl allw  -> a + "\\n"
			| allw whileloop:a -> a + "\\n"
			| allw forloop:a -> a + "\\n"
			| allw if:a -> a + "\\n"
			| allw elif:a -> a + "\\n"
			| allw else:a -> a + "\\n"
			| allw classdef:a endl allw -> a
			| allw functiondef:a -> a + "\\n"
			| allw cpp_require:a endl allw  -> a
			| allw require:a endl allw  -> a
			| allw functioncall:a endl allw  -> a + "\\n"
			)

imported = ( allw comment
			| allw list:a endl allw -> a + "\\n"
			# | allw set:a endl allw -> a + "\\n"
			| allw past_assignment:a endl allw  -> a + "\\n"
			# | allw print:a endl allw  -> a + "\\n"
			# | allw read:a endl allw  -> a + "\\n"
			# | allw system:a endl allw  -> a + "\\n"
			| allw return:a endl allw  -> a + "\\n"
			| allw pass:a endl allw  -> a + "\\n"
			| allw whileloop:a -> a + "\\n"
			| allw forloop:a -> a + "\\n"
			| allw if:a -> a + "\\n"
			| allw elif:a -> a + "\\n"
			| allw else:a -> a + "\\n"
			| allw classdef:a endl allw -> a
			| allw functiondef:a -> a + "\\n"
			| allw cpp_require:a endl allw  -> a
			| allw imported_require:a endl allw  -> a
			| allw functioncall:a endl allw  -> a + " \\n"
			)


req = (
		imported+:a -> ''.join(a)
		)

expr = (
		statement+:a -> returnPrint(''.join(a))
		)

# expr = (
# 		math:a -> a
# 		)

""", {
		"require" : require,
		"assign" : assign,
		"returnPrint" : returnPrint,
		"returnParameters" : returnParameters,
		"returnClassParameters" : returnClassParameters,
		"keywords" : keywords,
		"moveFunction" : moveFunction,
		"indent" : indent,
		"unindent" : unindent,
		"g_or_l" : g_or_l,
		"g_or_l_args" : g_or_l_args,
		"empty_locals" : empty_locals,
		"append_local_var" : append_local_var,
		"arg_keywords" : arg_keywords
	})


	# while True:
	# 	print (parser(raw_input(">")).expr())


	with open(sys.argv[2], "r") as f:
	    script = f.read()
	    f.close()
	    script = "".join([s for s in script.splitlines(True) if s.strip("\r\n")])


	# comment = pyparsing.nestedExpr(";", "!").suppress()
	# script = comment.transformString(script)

	translated = (parser(script).expr())

	with open(os.path.join(pwd, "turing.py"), "w+") as f:
		f.write("""

import os

def inStr(s1, s2):
	return (s1 in s2)

def read():
	return input()

def write(a):
	print(a, end='')

def writeln(a):
	print(a)

def get_char():
	return input()[0]

def Add(a, b):
	return a+b

def Sub(a, b):
	return a-b

def Negative(a):
	return -a

def Mul(a, b):
	return a*b

def Div(a, b):
	return a/b

def Int(a):
	return int(a)

def String(a):
	return str(a)

def Is(a, b):
	return (a==b)

def Not(a):
	return (not a)

def And(a, b):
	return (a and b)

def Or(a, b):
	return (a or b)

def append(a, b):
	c = a
	c.append(b)
	return c

def console(a):
	os.system(a)


	""")
		for func in listOfFunctions:
			# print(func)
			f.write(func)
		f.write(translated)
		f.close()

	# os.system("cd " + pwd + "\ng++ -std=c++14 " + os.path.join(pwd, "main.cpp") + "\nrm " + os.path.join(pwd, "main.cpp") + "\nmv a.out main\nclear\n./main")
	# print("cd " + pwd + "\ng++ -std=c++14 " + os.path.join(pwd, "main.cpp") + "\nmv a.out main\nclear\n./main")
	os.system("cd " + pwd + "\nclear\npython3 " + os.path.join(pwd, "turing.py"))


if sys.argv[1] == '-cpp':
	print("C++ it is!")

	keywords = ['for', 'while', 'if', 'elif', 'else']
	arg_keywords = ['read', 'print', 'println', 'system']

	parser = parsley.makeGrammar("""

allw = w endl w

w = <(' ' | '\\t')*>
endl = <('\\n')*>
mw = <('\\n')+>

digit = anything:x ?(x in '0123456789.')
char = anything:x ?(x in '0123456789_.')
number = (<digit+>:ds -> str(ds)
			| '-' <digit+>:ds -> '-' + str(ds)
			)

letter = anything:x ?(x in 'abcdefghijklmnopqrstuvwxyz' or x in 'abcdefghijklmnopqrstuvwxyz'.upper())

indice = <'['+>:a <( (letter|char)
				| w (number|identifier) w
			)*>:b <']'+>:c -> str(a) + str(b) + str(c)

identifier = w <(letter|char|indice)+>:ds -> str(ds)

string = '"' (~'"' anything)*:c '"' -> '"' + ''.join(c) + '"'

# assign = ('=' | '+=' | '-='):a -> a
assign = '<-' -> '='

operator = anything:x ?(x in '*/+-()') -> str(x)


bool = ('True' | 'False'):a -> str(a).lower()


functioncall_object = functioncall | number | bool | string | identifier
object = number | bool | string | identifier

whileloop = '(' allw 'while' w functioncall_object:a mw statement*:b allw ')' allw -> 'while (' + str(a) + ') {\\n' + indent(''.join(b)) + '\\n}' + unindent()

forloop = '(' allw 'for' w identifier:a w 'in' w (functioncall|identifier):b mw statement*:c allw ')' allw -> 'for (auto ' + str(a) + ':' + str(b) + ') {\\n' + indent(''.join(c)) + '\\n}' + unindent()


if = '(' allw 'if' w functioncall_object:a mw statement*:b allw ')' allw -> 'if (' + str(a) + ') {\\n' + indent(''.join(b)) + '\\n}' + unindent()

elif = '(' allw 'elif' w functioncall_object:a mw statement*:b allw ')' allw -> 'else if (' + str(a) + ') {\\n' + indent(''.join(b)) + '\\n}' + unindent()
else = '(' allw 'else' mw statement*:a allw ')' allw -> 'else {\\n' + indent(''.join(a)) + '\\n}' + unindent()


comment = ';' <(~'\\n' anything)*> -> ''


past_assignment = allw identifier:left w assign:op w ( bool:right -> 				checkVarInList(left, right, "bool") + str(left) + 			assign(str(op)) + str(right)
										| number:right -> 						checkVarInList(left, right, "int") + str(left) +            assign(str(op)) + str(right)
										| string:right 	-> 						checkVarInList(left, right, "str") + str(left) +            assign(str(op)) + str(right)
										| identifier:right -> 					checkVarInList(left, right, "auto") + str(left) +           assign(str(op)) + str(right)
										| functioncall:right -> 				checkVarInList(left, right, "functioncall") + str(left) +   assign(str(op)) + str(right)
										)

functioncall = allw '(' identifier:func ?(func not in keywords) allw (allw functioncall_object)*:args allw ')' w -> str(func) + '(' + str(','.join(args)) + ')'




function_begin = '(' allw 'func' w identifier:a -> 'auto ' + setScope(str(a))
functiondef = function_begin:a w (w object)*:b allw statement*:c allw ')' allw -> setScope('') + moveFunction(str(returnTemplate(b)) + a + '(' + str(returnTypedParameters(b)) + ') {\\n' + indent(''.join(c)) + '\\n}\\n\\n') + unindent()


require =  '(' allw 'require' w string:a w ')' -> require(a+'.tr')
cpp_require =  '(' allw '!require' w (string|identifier):a w ')' -> moveFunction('#include '+str(a)+'\\n\\n')
imported_require =  '(' allw 'require' w string:a w ')' -> ''

return = (
		allw '(' w 'return' w functioncall_object:a w ')' w -> 'return ' + str(a)
		)

class_begin = '(' allw 'class' w identifier:a -> 'class ' + setScope(setLastClass(str(a)))
classdef = (
			class_begin:a allw class_statement*:b allw ')' allw -> setScope('') + moveFunction( str(a) + ' {\\npublic:\\n' + indent(''.join(b)) + '\\n};\\n\\n') + unindent()
			| class_begin:a w identifier:b allw class_statement*:c allw ')' allw -> setScope('') + moveFunction( str(a) + ': public ' + str(b) + ' {\\npublic:\\n' + indent(''.join(c)) + '\\n};\\n\\n') + unindent()
			)

constructor = '(' allw 'init' w (w object)*:a allw statement*:b allw ')' allw -> str(returnTemplate(a)) + '\\n' + returnLastClass() + ' (' + str(returnTypedParameters(a)) + ') {\\n' + indent(''.join(b)) + '\\n}' + unindent()
methoddef = '(' allw 'func' w identifier:a w (w object)*:b allw statement*:c allw ')' allw -> str(returnTemplate(b)) + 'auto ' + str(a) + '(' + str(returnTypedParameters(b)) + ') {\\n' + indent(''.join(c)) + '\\n}' + unindent()


pass =  (
		allw '(' w 'pass' w ')' w -> ''
		)

# x = (list [Dog])

set = allw identifier:a w assign w ( string:b allw -> returnPrint('string ' + markList(str(a)) + '=' + str(b))
								| object:b allw -> returnPrint('__auto_reserved__(' + markList(str(a)) + ', ' + str(b) + ')')
								)

list = allw identifier:a w assign w '(' w 'list' w '[' <'['*>:q w identifier:b w ']' <']'*>:u w ')' w -> '__auto_reserved__(' + markList(str(a)) + ', __List__<' + q.replace('[', 'vector<') + str(b) + u.replace(']', '>') + '>())'

set_function_call = allw identifier:a w assign w functioncall:b allw -> returnPrint('__auto_reserved__(' + markList(str(a)) + ', ' + str(b) + ')')

setmethod = '(' allw 'set' allw (allw set|list|set_function_call|comment)*:a allw ')' allw -> ';\\n'.join(a)+';\\n'


class_statement = ( allw comment
			| allw list:a endl allw -> a + ";\\n"
			# | allw print:a endl allw  -> a + ";\\n"
			# | allw read:a endl allw  -> a + ";\\n"
			# | allw system:a endl allw  -> a + ";\\n"
			| allw return:a endl allw  -> a + ";\\n"
			| allw pass:a endl allw  -> ''
			| allw whileloop:a -> a + "\\n"
			| allw forloop:a -> a + "\\n"
			| allw if:a -> a + "\\n"
			| allw elif:a -> a + "\\n"
			| allw else:a -> a + "\\n"
			| allw setmethod:a -> a + "\\n"
			| allw constructor:a -> a + "\\n"
			| allw methoddef:a -> a + "\\n"
			| allw functioncall:a endl allw  -> a + ";\\n"
			)

statement = ( allw comment
			| allw list:a endl allw -> a + ";\\n"
			# | allw set:a endl allw -> a + ";\\n"
			| allw past_assignment:a endl allw  -> a + ";\\n"
			# | allw print:a endl allw  -> a + ";\\n"
			# | allw read:a endl allw  -> a + ";\\n"
			# | allw system:a endl allw  -> a + ";\\n"
			| allw return:a endl allw  -> a + ";\\n"
			| allw pass:a endl allw  -> ''
			| allw whileloop:a -> a + "\\n"
			| allw forloop:a -> a + "\\n"
			| allw if:a -> a + "\\n"
			| allw elif:a -> a + "\\n"
			| allw else:a -> a + "\\n"
			| allw classdef:a endl allw -> a
			| allw functiondef:a -> a + "\\n"
			| allw cpp_require:a endl allw  -> a
			| allw require:a endl allw  -> a
			| allw functioncall:a endl allw  -> a + ";\\n"
			)

imported = ( allw comment
			| allw list:a endl allw -> a + ";\\n"
			# | allw set:a endl allw -> a + ";\\n"
			| allw past_assignment:a endl allw  -> a + ";\\n"
			# | allw print:a endl allw  -> a + ";\\n"
			# | allw read:a endl allw  -> a + ";\\n"
			# | allw system:a endl allw  -> a + ";\\n"
			| allw return:a endl allw  -> a + ";\\n"
			| allw pass:a endl allw  -> ''
			| allw whileloop:a -> a + "\\n"
			| allw forloop:a -> a + "\\n"
			| allw if:a -> a + "\\n"
			| allw elif:a -> a + "\\n"
			| allw else:a -> a + "\\n"
			| allw classdef:a endl allw -> a
			| allw functiondef:a -> a + "\\n"
			| allw cpp_require:a endl allw  -> a
			| allw imported_require:a endl allw  -> a
			| allw functioncall:a endl allw  -> a + ";\\n"
			)


req = (
		imported+:a -> ''.join(a)
		)

expr = (
		statement+:a -> returnPrint(''.join(a))
		)

# expr = (
# 		math:a -> a
# 		)

""", {"checkVarInList": checkVarInList,
		"returnAutoReserved": returnAutoReserved,
		"returnTemplate": returnTemplate,
		"returnTypedParameters": returnTypedParameters,
		"moveFunction": moveFunction,
		"returnLastClass" : returnLastClass,
		"setLastClass" : setLastClass,
		"setScope" : setScope,
		"require" : require,
		"assign" : assign,
		"returnPrint" : returnPrint,
		"markList" : markList,
		"keywords" : keywords,
		"indent" : indent,
		"unindent" : unindent,
		"arg_keywords" : arg_keywords
	})


# while True:
# 	print (parser(raw_input(">")).expr())


	with open(sys.argv[2], "r") as f:
	    script = f.read()
	    f.close()
	    script = "".join([s for s in script.splitlines(True) if s.strip("\r\n")])


# comment = pyparsing.nestedExpr(";", "!").suppress()
# script = comment.transformString(script)

	translated = (parser(script).expr())

	with open(os.path.join(pwd, "main.cpp"), "w+") as f:
		f.write("""
#include <iostream>
#include <vector>
#include <sstream>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
using namespace std;

#define __auto_reserved__(variable, value) std::decay<decltype(value)>::type variable = value

bool inStr(string s1, string s2)
{
    if (s1.find(s2) != string::npos)
    {
        return true;
    }
    else
    {
        return false;
    }
}

template<typename T>
auto __List__()
{
	vector <T> list;
	return list;
}

template<typename T>
auto __Type__()
{
	T a;
	return a;
}

auto range(int begin, int end)
{
	vector <int> r;
	for (int i = begin; i < end; i++)
	{
		r.push_back(i);
	}
	return r;
}


string read()
{
	string a;
	getline(cin, a);
	return a;
}


template<typename T>
void print(T a)
{
	cout<<a;
}

template<typename T>
void println(T a)
{
	cout<<a<<endl;
}

string get_char()
{
	string s;
 	stringstream ss;

	getline(cin, s);

	if (s.size() > 0)
	{
	 	ss << s.at(0);
	 	ss >> s;
	} else {
		s = " ";
	}

	return s;
}

template<typename T, typename T2>
auto Add(T a, T2 b)
{
	/*
	if (typeid(a) == typeid(const char *()))
	{
		return strcat(a, b);
	}
	else if (typeid(a) == typeid(int()))
	{
		return a+b;
	}
	else if (typeid(a) == typeid(string()))
	{
		return a+b;
	}
	*/
	return a+b;
}

int Sub(int a, int b)
{
	return a-b;
}

int Negative(int a)
{
	return -a;
}

template<typename T, typename T2>
auto Mul(T a, T2 b)
{
	return a*b;
}

int Div(int a, int b)
{
	return a/b;
}


template<typename T>
auto Int(T a)
{
	int c = 0;
	stringstream b(a);
	b >> c;
	return c;
}

template<typename T>
auto String(T a)
{
	stringstream b;
	b << a;
	string c = b.str();
	return c;
}

template<typename T, typename T2>
auto Is(T a, T2 b)
{
	return (a==b);
}

template<typename T>
auto Not(T a)
{
	return (!a);
}

template<typename T, typename T2>
auto And(T a, T2 b)
{
	return (a&&b);
}

template<typename T, typename T2>
auto Or(T a, T2 b)
{
	return (a||b);
}

auto console(string a)
{
	system(a.c_str());
}

template<typename T, typename T2>
auto append(T a, T2 b)
{
	auto c = a;
	c.push_back(b);
	return c;
}

template<typename T>
auto len(T a)
{
	return a.size();
}


""")
		for func in listOfFunctions:
			# print(func)
			f.write(func)
		f.write("\n\nint main(int argc,char* __char_argv__[])\n{\n\n\tstring __file__ = *__char_argv__;\n")
		f.write(translated)
		f.write("\n\treturn 0;\n\n}\n\n")
		f.close()

	# os.system("cd " + pwd + "\ng++ -std=c++14 " + os.path.join(pwd, "main.cpp") + "\nrm " + os.path.join(pwd, "main.cpp") + "\nmv a.out main\nclear\n./main")
	print("cd " + pwd + "\ng++ -std=c++14 " + os.path.join(pwd, "main.cpp") + "\nmv a.out main\nclear\n./main")
	os.system("cd " + pwd + "\ng++ -std=c++14 " + os.path.join(pwd, "main.cpp") + "\nmv a.out main\nclear\n./main")
