from tkinter.ttk import * # note: place before importing tkinter
import tkinter as tk
from tkinter.filedialog import askopenfilename
# use to ask the user to open an file and record its location/name

import PyPDF2
import random
import os


Random_Pages = tk.Tk()
Random_Pages.title("Random Pages")
Random_Pages.geometry("400x500")


Display = tk.Label(Random_Pages, bg='blue',fg='white', text='Random Pages from : ')
Display.grid(row=0,column=0)

def Random_Notes(filelocation):
    if filelocation!='':
        
        pdfFileObj = open(filelocation, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        N = pdfReader.numPages
        Branch = tk.Tk()
        Branch.title("Random pages from PDF")
        Branch.geometry("300x300")
        Display = tk.Label(Branch, fg='black',
                            text="There are "+str(N)+" pages in the file."
                            +"\n How many pages do you want ?")
        Display.pack( side=tk.TOP)
        textExample=tk.Entry(Branch, width=30)
        textExample.pack( side=tk.TOP)

     
        def proceed():
            pdfFileObj = open(filelocation, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            x = textExample.get()
            if x!='':
                n = int(x)
                A = sorted(random.sample(range(1,N+1),n))
                Display = tk.Label(Branch,fg='black',
                                    text="The following pages are randomly selected and printed: \n"+f"{A}")
                Display.pack()
                pdfWriter = PyPDF2.PdfFileWriter()
                for a in A:
                      pageObj = pdfReader.getPage(a-1)
                      pdfWriter.addPage(pageObj)
                temp=random.randrange(10000)

                newFile = open(r"C:\Users\WEIYA\Downloads\r RandomBookSections"+str(temp)+".pdf", 'wb')
                pdfWriter.write(newFile)
                pdfFileObj.close()
                newFile.close()
                os.startfile(r"C:\Users\WEIYA\Downloads\r RandomBookSections"+str(temp)+".pdf")
        
        btn = tk.Button(Branch,text="Generate!",command=lambda:proceed())
        btn.pack()

#file = open('filenames.txt', 'r')
file = open(r'C:\Users\WEIYA\Google Drive\y. Garage\Garage\Random PDF pages\filenames.txt', 'r')
Lines = file.readlines()

for i,j in enumerate(Lines):
    Lines[i]=j.replace("\n","")
    

for i in range(len(Lines)//2):
    tk.Button(Random_Pages,text=Lines[2*i],bg='ivory3',
        command=lambda j=Lines[2*i+1]:Random_Notes(j)).grid(row=1+i,column=1)
    


btn=tk.Button(Random_Pages,text="Selected File",bg='ivory3',
        command=lambda:Random_Notes(askopenfilename(title = "Select file",
                                        filetypes =[('pdf files', '*.pdf')])))
btn.grid(row=1,column=10)


Random_Pages.mainloop()




