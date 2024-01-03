import time

fileNames = []

outputCode = ""

name = "none"
done = False

print("Type The Name of the Module You Want To Add")
print("EX: News Module -> news")
print("To Confirm the Files, enter \"done\"\n")

while not done:
    name = input("File Name: ").lower()

    if (name == "done"):
        done = True
    elif (name == "reset"):
        fileNames.clear()
    else:
        fileNames.append(name)

outputCode = ""
# First Add Imports
for i in fileNames:
    name = i + "/" + i + "Imports.py"
    with (open(name, "r")) as file:
        for line in file:
            outputCode += line
        outputCode += "\n"

with (open("base/baseImports.py", "r")) as file:
    for line in file:
        outputCode += line

outputCode += "\n\n"

with (open("base/baseFuncs.py", "r")) as file:
    for line in file:
        outputCode += line

outputCode += "\n\n"

# Then Add Classes
for i in fileNames:
    name = i + "/" + i + "Class.py"
    with (open(name, "r")) as file:
        for line in file:
            outputCode += line

outputCode += "\n\n"

# Lastly, Add Append Lines
for i in fileNames:
    name = i + "/" + i + "Add.py"
    with (open(name, "r")) as file:
        for line in file:
            outputCode += line
        outputCode += "\n"

outputCode += "\n\n"

with (open("base/baseMain.py", "r")) as file:
    for line in file:
        outputCode += line

with open("output.py", "w") as file:
    file.write(outputCode)
