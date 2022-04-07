import re
import codes

instructions = ["INP", "STA", "ADD", "SUB", "LDA", "OUT", "BRP", "BRZ", "BRA"]

def preparse(code):
    code = re.sub(r'  +', '\t', code)
    return re.sub(r'\t+', '\t', code)

def parse(code):
    RAM = [0 for i in range(100)]
    ACC = 0
    variables = {}
    function_indexes = {}
    unused_index = 0
    raw = code.split("\n")
    for i, line in enumerate(raw):
        if line.startswith("//"):
            continue
        # create variables
        if "DAT" in line:
            white_space = "\t" if "\t" in line else " "
            parts = line.lower().split(white_space)
            variable = parts[0].replace("DAT", "").replace(" ", "")
            variables[variable] = unused_index
            try:
                # if there is a value after the DAT
                value = int(parts[1].split(" ")[1])
                RAM[unused_index] = value
            except:
                pass
            unused_index += 1
        # indexes of line of jump locations
        white_space = "\t" if "\t" in line else " "
        parts = line.lower().split(white_space)
        if parts[0] in instructions or len(parts) == 1:
            continue
        if parts[1] in instructions:
            function_indexes[line.split(white_space)[0]] = i
        elif parts[1].split(" ")[0].upper() in instructions:
            function_indexes[line.split(white_space)[0]] = i
    index = 0
    while index >= 0 and index < len(raw):
        line = raw[index]
        # empty lines
        if line == "\n" or line == "" or line == "\t" or line.startswith("///") or line.startswith("#"):
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
        data = line[4:]
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
                ACC += RAM[variables[location.lower()]]
        if cmd == "SUB":
            location = line.split(" ")[1]
            if location.isdigit():
                ACC -= RAM[int(location)]
            else:
                ACC -= RAM[variables[location.lower()]]
        if cmd == "LDA":
            location = line.split(" ")[1]
            if location.isdigit():
                ACC = RAM[int(location)]
            else:
                ACC = RAM[variables[location.lower()]]
        if cmd == "BRP":
            if ACC >= 0:
                func = data
                index = function_indexes[func] - 1
        if cmd == "BRA":
            func = data
            index = function_indexes[func] - 1
        if cmd == "BRZ":
            if ACC == 0:
                func = data
                index = function_indexes[func] - 1
        if cmd == "OUT":
            print(ACC)
        if cmd == "HLT":
            return
        index += 1



parse(preparse(codes.counter_code))