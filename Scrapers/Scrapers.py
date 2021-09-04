from tkinter.ttk import * # place before import tkinter
import tkinter as tk
from tkinter import simpledialog # pop-up window for user input

import os
import requests
from bs4 import BeautifulSoup
import re


Scrapers = tk.Tk()
Scrapers.title("Scrapper")
Scrapers.geometry("100x100")

def downloadpath(topic,type):
    folder_path = r'C:\\Users\WEIYA\Downloads\\'+topic+" ( "+type+" )" # download folder
    if not os.path.exists(folder_path): # if folder doesn't exist, create it
        os.mkdir(folder_path)
    return folder_path

def titlecleaner(title):
    title = title.replace("\n","").strip() # remove line breaks and empty heads and tails
    return re.sub('\W+'," ",title) # remove special characters

#############################################################################################
def scraper_arxiv():
    inquiry = simpledialog.askstring(title = "Arxiv Scrapper", 
                                        prompt = "What do you want to scrape ? ")
    
    if inquiry != None:
        folder_path = downloadpath(inquiry,"arxiv")

        url = "https://arxiv.org/search/?query="+"+".join(inquiry.split())+"&searchtype=all&abstracts=show&order=-announced_date_first&size=25"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        for result in soup.find_all("li", class_="arxiv-result"):
            title = titlecleaner(result.find("p", class_="title is-5 mathjax").text) # get a valid file name
            link = result.find("a", href = lambda href: href and "pdf" in href)['href']
            filename = os.path.join(folder_path,title)+".pdf"
            with open(filename, 'wb') as f:
                f.write(requests.get(link).content)
 

tk.Button(Scrapers,text="Arxiv Scraper~",command=lambda:scraper_arxiv()).grid(row=0,column=0)
#############################################################################################

def scraper_google():
    inquiry = simpledialog.askstring(title = "Arxiv Scrapper", 
                                        prompt = "What do you want to scrape ? ")
    if inquiry != None:
        folder_path = downloadpath(inquiry,"Google")
    
    url = "https://www.google.com/search?q="+"+".join(inquiry.split())+"+filetype%3Apdf&num=10"
    response = requests.get(url)
    soup= BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all("a", href = lambda href: href and ".pdf" in href):
        link = link['href']
        
        if 'https' in link:
            link = link[link.index('https'):link.index('.pdf')+4]
            title = titlecleaner(link[:-4].split('/')[-1].split('%')[-1]) # get a valid file name
            filename = os.path.join(folder_path,title)+".pdf"
            with open(filename, 'wb') as f:
                f.write(requests.get(link).content)

tk.Button(Scrapers,text="Google Scraper~",command=lambda:scraper_google()).grid(row=1,column=0)
##################################################################################################



Scrapers.mainloop()
