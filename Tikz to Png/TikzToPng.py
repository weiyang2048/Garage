import os
from pdf2image import convert_from_path
from tkinter.ttk import *  # note: place before importing tkinter
import tkinter as tk
from tkinter.filedialog import askopenfilename
# use to ask the user to open an file and record its location/name

Tikz = tk.Tk()
Tikz.title("Tikz Pictures")
Tikz.geometry("800x400")
Display = tk.Label(Tikz, bg='blue', fg='white',
                   text='Choose a Tikz Picture from : ')
Display.grid(row=0, column=0)


def GetPic(name):
    with open('Template.tex', "w") as myfile:
        myfile.writelines(lines[0:7])
        myfile.write("\\usepackage[pdftex,active,tightpage]{preview}\n")
        myfile.write("\\begin{document} \n \\begin{preview}\n")
    
        myfile.writelines(lines[NameDic[name][0]:NameDic[name][1]+1])
        myfile.write("\\end{preview}\\end{document}")
    # compile tex file
    os.system(
        "pdflatex -synctex=1 -interaction=nonstopmode --shell-escape Template.tex")

    # convert pdf into png
    pages = convert_from_path('Template.pdf', 500)


    for page in pages:
        page.save('{}.png'.format(name), 'PNG')

# change directory
os.chdir(r"C:\Users\WEIYA\Downloads")

f = open("Tikz.tex", "r")
lines = f.readlines()
Names = []
temp = 0
NameDic = dict()
for x in filter(lambda x: "%Name: " in x or "\end{tikz" in x, lines):
    temp += 1
    if temp % 2 == 1:
        Names.append([x[x.index("%Name: ")+7:-1], lines.index(x)])
    else:
        NameDic[Names[-1][0]] = (Names[-1][1], Names[-1]
                                 [1]+lines[Names[-1][1]:].index(x))
f.close()
COLUMN = 0
ROW = 1
for name in NameDic.keys():
    tk.Button(Tikz, text=name, bg='ivory3',
              command=lambda j=name: GetPic(j))\
        .grid(row=ROW, column=COLUMN, padx=6, pady=1)
    ROW += 1


Tikz.mainloop()
