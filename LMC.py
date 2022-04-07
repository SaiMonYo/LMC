instructions = ["INP", "STA", "ADD", "SUB", "LDA", "OUT", "BRP", "BRZ", "BRA"]

def parse(code):
    RAM = [0 for i in range(100)]
    ACC = 0
    variables = {}
    function_indexes = {}
    unused_index = 0
    raw = code.split("\n")
    for i, line in enumerate(raw):
        # create variables
        if "DAT" in line:
            parts = line.lower().split("\t")
            variables[parts[0]] = unused_index
            try:
                # if there is a value after the DAT
                value = int(parts[1].split(" ")[1])
                RAM[unused_index] = value
            except:
                pass
            unused_index += 1
        parts = line.split("\t")
        # indexes of line of jump locations
        try:
            if parts[1].split(" ")[0] in instructions and parts[0] != "":
                function_indexes[parts[0]] = i
        except:
            pass
    index = 0
    while index >= 0 and index < len(raw):
        line = raw[index]
        # empty lines
        if line == "\n" or line == "" or line == "\t":
            i+=1
            continue
        # removing tabs
        line = line.replace("\t", "")
        # starts with a function, ignore that start
        for func in function_indexes.keys():
            if line.startswith(func):
                line = line.replace(func, "")
        # all commands are length 3 in this case
        cmd = line[:3]
        if cmd == "INP":
            ACC = int(input())
        if cmd == "STA":
            variable_name = line.split(" ")[1].lower()
            RAM[variables[variable_name]] = ACC
        if cmd == "ADD":
            location = line.split(" ")[1]
            if location.isdigit():
                ACC += RAM[int(location)]
            else:
                ACC += RAM[variables[location]]
        if cmd == "SUB":
            location = line.split(" ")[1]
            if location.isdigit():
                ACC -= RAM[int(location)]
            else:
                ACC -= RAM[variables[location]]
        if cmd == "LDA":
            location = line.split(" ")[1]
            if location.isdigit():
                ACC = RAM[int(location)]
            else:
                ACC = RAM[variables[location]]
        if cmd == "BRP":
            if ACC >= 0:
                func = line.split(" ")[1]
                index = function_indexes[func] - 1
        if cmd == "BRA":
            func = line.split(" ")[1]
            index = function_indexes[func] - 1
        if cmd == "BRZ":
            if ACC == 0:
                func = line.split(" ")[1]
                index = function_indexes[func] - 1
        if cmd == "OUT":
            print(ACC)
        if cmd == "HLT":
            return
        index += 1



# Code is easily breakable
# needs to use single tab for indenting
# needs to use single space between instructions and variables
# needs to use single tab between jump locations like outit and LDA y
# needs to use single tab between variable names and DAT
code = '''	INP
	STA x
	INP
	STA y
	SUB x
	BRP outit
	LDA x
	OUT
	HLT
	


outit	LDA y
	OUT
	HLT


x	DAT
y	DAT   
'''


# TODO:
# add a preparser to convert malformed code to parseable code
parse(code)
