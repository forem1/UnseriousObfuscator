import random
import argparse
import shutil
import sys
import minify

keywords = [
    "int ", "uint8_t ", "uint16_t ", "uint32_t ", "uint64_t ", "int8_t ", "int16_t ", "int32_t ", "int64_t ",
    "float ", "long ", "double ",
    "string ", "char ",
    "const ", "void ", "return ",
    "+=", "-=", "*=", "/=", "%=", "==", "!=", "|", "!", "^", "<<", ">>",
    "+", "-", "*", "/", "%", "++", "--",
    "bool ", "boolean ", "true", "false", "<=", ">=", "&&", "||",
    "switch(", "switch (", "for(", "for (", "while(", "while (", "if(", "if (", "else "
]

def argParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', default='input.cpp', help="Path to input cpp file")
    parser.add_argument('-o', '--output', default='output.cpp', help="Path to output cpp file")
    parser.add_argument('-a', '--header', default='obfuscate.h', help="Path to output header file")
    return parser

def replaceTextInFile(fileName, search_text, replace_text):
    with open(fileName, 'r') as file:
        data = file.read()
        data = data.replace(search_text, replace_text)

    with open(fileName, 'w') as file:
        file.write(data)
        file.close()

#just for easy
def concatTwoFiles():
    filenames = ['obfuscate.h', 'output.cpp']
    with open('output.txt', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
        outfile.close()


def main():
    parser = argParser()
    argNamespace = parser.parse_args(sys.argv[1:])

    shutil.copy2(argNamespace.input, argNamespace.output)

    minify.minifyFile(argNamespace.output)

    scramblePointer = random.randrange(0, 9999999999)
    scramblePointerList = []

    sourceFile = open(argNamespace.output, "r")
    headerFile = open(argNamespace.header, "a")

    # Strips the newline character
    for sourceFileLine in sourceFile.readlines():
        line = sourceFileLine.strip()
        #line = re.sub(r"(?<=[\s|(|=|-|+|/])(\d+(0[xX])?[A-Fa-f0-9])", lambda m: str(hex(int(m.group(1), 10))), line)
        #print(line)
        for changingKey in keywords:
            if (line.lower().find(changingKey) > -1):
                replaceTextInFile(argNamespace.output, changingKey, " C_" + str(scramblePointer) + " ")
                headerFile.write("#define C_" + str(scramblePointer) + " " + changingKey + "\r")

                scramblePointerList.append(scramblePointer)
                scramblePointer = random.randrange(0, 9999999999)
                while (scramblePointer in scramblePointerList):
                    scramblePointer = random.randrange(0, 9999999999)

    headerFile.close()
    sourceFile.close()

    concatTwoFiles()
    headerFile.close()
    sourceFile.close()



if __name__ == "__main__":
    main()