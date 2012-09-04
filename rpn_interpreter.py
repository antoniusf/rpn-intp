import itertools

stack = [0,0,0,0,0]
variables = []
values = []

def enter(number):
    global stack
    number = float(number)
    stack = list(itertools.chain([number],stack[0:4]))

def compute(operator):
    global stack
    res = eval("("+str(stack[1])+")"+operator+"("+str(stack[0])+")")
    stack = list(itertools.chain([res],stack[2:5],[0]))
    print "["+str(stack[0])+"]"

def analyze(inp):
    pre_tokens = inp.split(" ")
    tokens = []
    t_contents = []
    for pt in pre_tokens:
        t_content = ""
        token_type = None
        for pt_elem in pt:
            if pt_elem in ["1","2","3","4","5","6","7","8","9","0","."]:
                if token_type == None or token_type == 0:
                    token_type = 0#0 := number
                    if pt_elem == ".":
                        if "." in t_content:
                            pt_elem = ""
                        elif t_content == "":
                            pt_elem = "0."
                    t_content += pt_elem
                elif token_type == 1:#1 := identifier
                    t_content += pt_elem
            elif pt_elem in ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","_"]:
                if token_type == None or token_type == 1:
                    token_type = 1
                    t_content += pt_elem
                elif token_type == 2:#2 := string
                    t_content += pt_elem
            elif pt_elem == '"':
                if token_type == None:
                    token_type = 2
                elif token_type == 2:
                    break
            elif pt_elem == "=":
                if token_type == None:
                    token_type = 3#3 := assignment
                    t_content += pt_elem
                elif token_type == 4:
                    t_content += pt_elem
                elif token_type == 3:
                    token_type = 4
                    t_content += pt_elem
                else:
                    print "Syntax Error"
                    return 0
            elif pt_elem in ["+","-","*","/","%","&","|","^","~","<",">","#","!"]:
                if token_type == None or token_type == 4:#4 := (binary) operator
                    token_type = 4
                    t_content += pt_elem
                else:
                    print "Syntax Error"
                    return 0
            elif pt_elem in ['\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', '\x08', '\t', '\n', '\x0b', '\x0c', '\r', '\x0e', '\x0f', '\x10', '\x11', '\x12', '\x13', '\x14', '\x15', '\x16', '\x17', '\x18', '\x19', '\x1a', '\x1b', '\x1c', '\x1d', '\x1e', '\x1f', ' ', '!', '#', '$', '%', '&', '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~']:
                if token_type == 2:
                    t_content += pt_elem
                else:
                    print "Syntax Error"
                    return 0#means here error
            else:
                print "Syntax Error"
                return 0
        tokens.append(token_type)
        t_contents.append(t_content)
    return tokens, t_contents

def parse(inp):
    token_stream = analyze(inp)
    if token_stream != 0:
        tokens, contents = token_stream
        l = len(tokens)
        for i in range(0,l):
            token = tokens[i]
            content = contents[i]
            if token == 0:
                enter(float(content))
            elif token == 1:
                if i < (l-1) and tokens[i+1] == 3:
                    if content in variables:
                        values[variables.index(content)]=stack[0]
                    else:
                        variables.append(content)
                        values.append(stack[0])
                else:
                    if content in variables:
                        enter(values[variables.index(content)])
                        print "["+str(values[variables.index(content)])+"]"
                    else:
                        print "Name Error: "+content+" is not defined"
                        return 0
            elif token == 2:
                return content
            elif token == 4:
                if content in ["+","-","*","/","%","&","|","^","~","<",">","**","//","<=",">=","==","!="]:
                    compute(content)
                elif content == "#":
                    stack[0] = 1/stack[0]
                    compute("**")
                else:
                    print "Operation Error: operator "+content+" is not existing"
                    return 0
##def str_eval(inp):
##    inp += " "
##    num = None
##    op = None
##    chartype = None
##    for char in inp:
##        if char in ["0","1","2","3","4","5","6","7","8","9","."]:
##            if chartype == 0:#chartype 0 := number
##                if char == ".":
##                    if char in num:
##                        char = ""
##                num += char
##            elif chartype == 1:#chartype 1 := operator
##                if char == ".":
##                    char = "0."
##                num = char
##                chartype = 0
##                compute(op)
##                op = None
##            elif chartype == None:
##                if char == ".":
##                    char = "0."
##                num = char
##                chartype = 0
##        elif char in ["+","-","*","/","//","%","**"]:
##            if chartype == 1:
##                op += char
##            elif chartype == 0:
##                op = char
##                chartype = 1
##                if num[-1] == ".":
##                    num += 0
##                enter(float(num))
##                num = None
##            elif chartype == None:
##                op = char
##                chartype = 1
##        elif char in [" "]:
##            if chartype == 0:
##                enter(float(num))
##                num = None
##            elif chartype == 1:
##                compute(op)
##                op = None
##            chartype = None
##        elif char == "q":
##            return 1

if __name__ == "__main__":
    while True:
        inp = raw_input(":>")
        a = parse(inp)
