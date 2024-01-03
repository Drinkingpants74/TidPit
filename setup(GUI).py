import tkinter as tk

window = tk.Tk()
window.title("TidPit GUI Setup")
screenHeight = window.winfo_screenheight()
screenWidth = window.winfo_screenwidth()
window.configure(height=screenHeight/2, width=screenWidth/2)

fileNames = []

name = "none"
done = False

fileName = tk.StringVar()

def confirmClicked():
    fileNames.append(str(fileName.get()).lower())
    fileTB.delete(0, tk.END)
    refreshFileList()

def resetClicked():
    fileTB.delete(0, tk.END)
    fileNames.clear()
    fileNames.append("base")
    refreshFileList()

def listFinished():
    fileTB.destroy()
    confButt.destroy()
    resetButt.destroy()
    writeButt.destroy()
    instMess.destroy()
    fileLBL.configure(text="Writing To Output.py...")
    fileLBL.grid(row=0, column=0, sticky="nw")
    listLBL.grid(row=1, column=0, sticky="nw")
    fileList.grid(row=2, column=0)

def refreshFileList():
    fileListContents = ""
    for i in fileNames:
        fileListContents += i.capitalize() + "\n"
    fileList.configure(text=fileListContents)

def write_to_file():
    listFinished()
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
            outputCode += "\n"

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

    fileLBL.configure(text="Output.py Written.")

instructions = "To Add Modules, type the name of the Folder.\n"
instructions += "EX: News Module -> news\n"

instMess = tk.Message(window, text=instructions)
instMess.grid(row=0, column=0, sticky="nw", columnspan=4)
instMess.configure(justify="left", width=500)

fileLBL = tk.Label(window, text="File Name:")
fileLBL.grid(row=1, column=0, sticky="nw")

fileTB = tk.Entry(window, textvariable=fileName)
fileTB.grid(row=1, column=1)

confButt = tk.Button(window, text="Add Module", command=confirmClicked)
confButt.grid(row=2, column=0)

resetButt = tk.Button(window, text="Reset List", command=resetClicked)
resetButt.grid(row=2, column=1)

writeButt = tk.Button(window, text="Create", command=write_to_file)
writeButt.grid(row=2, column=2)

listLBL = tk.Label(window, text="Functions To Add:")
listLBL.grid(row=3, column=1, sticky="s")

fileListContents = ""
for i in fileNames:
    fileListContents += i.capitalize() + "\n"

fileList = tk.Label(window, text=fileListContents)
fileList.grid(row=4, column=1)

tk.mainloop()