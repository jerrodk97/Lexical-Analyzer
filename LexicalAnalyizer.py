keyword = ['class', 'constructor', 'function', 'method', 'static', 'field', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'this', 'null', 'let', 'do', 'if', 'else', 'while', 'return', 'null', 'true', 'false', 'this']

symbols = ['{', '}', '[', ']', '(', ')', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~', '\'']

#clean function to remove comments from recievd file
def clean(file):
    original = open(file + ".jack", "r")
    cleaned = open('c' + file +".jack", "w")
    for line in original:
        if line.strip().startswith('*') or line.strip().startswith("/*") or line.strip().startswith("*/") or line.strip().startswith("//"):
            pass
        else:
            if "//" in line.strip():
                line = line.split("//")[0]
                line += "\n"
            cleaned.write(line)
    
    cleaned.close()


#opens the file now cleaned of comments
#opens a new file to output in xml format
def tokenize(file):
    cleaned = open('c' + file + ".jack")
    xmlfile = open("c"+file + "T.xml", "w")
    xmlfile.write("<tokens>\n")
    for line in cleaned:
        line = line.strip() #removes leading/trailing whitespace from each line
        while len(line) > 0:
            if line[0].isalpha() or line[0] == '_': #if current value of the line is a letter or underscore
                token = ''
                while line[0].isalpha() or line[0].isdigit() or line[0] == '_': #while the current value is a letter or number or underscore
                    token += line[0]
                    line = line[1:]
                if token in keyword:
                    xmlfile.write('<keyword> ' + token + ' </keyword>\n')
                else:
                    xmlfile.write('<identifier> ' + token + ' </identifier>\n')
            elif line[0].isdigit(): #if current value of the line is a number
                number = ''
                while line and line[0].isdigit(): #while the current value is a number
                    number += line[0]
                    line = line[1:]
                xmlfile.write('<integerConstant> ' + number + ' </integerConstant>\n')
            elif line[0] in symbols: #if the current value is in the symbol list
                if line[0] == '>':
                    xmlfile.write('<symbol> ' + "&gt;" + ' </symbol>\n')
                elif line[0]  == '<':
                    xmlfile.write('<symbol> ' + "&lt;" + ' </symbol>\n')
                elif line[0] == '"':
                    xmlfile.write('<symbol> ' + "&quot;" + ' </symbol>\n')
                elif line[0] == '&':
                    xmlfile.write('<symbol> ' + "&amp;" + ' </symbol>\n')
                else:
                    xmlfile.write('<symbol> ' + line[0] + ' </symbol>\n')
                line = line[1:].strip()
            elif line.startswith('"'): # if line starts with a " 
                try: #try is used here in case there is only a single quote within a line
                    string_constant = line[1:line.index('"', 1)].strip() #if there is a second " in the line, return the index of the last character before
                    xmlfile.write('<stringConstant> ' + string_constant + ' </stringConstant>\n')
                    line = line[line.index('"', 1) + 1:].strip() 
                except ValueError: # except is used in the instance that a second " was not found in the string and writes &quot to the xml file
                    string_constant = "&quot;"
                    xmlfile.write('<symbol> ' + string_constant + ' </symbol\n')
                    break

            else:
                line = line[1:]
    xmlfile.write("</tokens>")

    cleaned.close()
    xmlfile.close()

# set file name and call functions
file= "SquareGame"
clean(file)
tokenize(file)
#file_name = "Main"
#clean(file_name)
