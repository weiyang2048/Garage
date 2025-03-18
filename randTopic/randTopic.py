import time
import os
from colorama import Fore
from colorama import Back
from colorama import Style
from datetime import datetime
import numpy as np
from tkinter import Tk, Label, Button, Entry, LabelFrame
# *  import modules 
from data.data import topics_dict
from modules.RandomSubfolder import open_random_folder

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Random Things")
        self.minsize(640, 400)

        # * Main Grid Layout
        self.topics = LabelFrame(self, text="Random Topic Generator")
        self.topics.grid(column=0, row=1, padx=20, pady=20)
        self.topics.configure(
            font=("Arial", 12, "bold"))

        self.auto = LabelFrame(self, text="Auto")
        self.auto.grid(column=1, row=1, padx=20, pady=20)
        self.auto.configure(
            font=("Arial", 12, "bold"))

        # * Auto
        self.auto_button = Button(
            self.auto, text="Start", command=self.auto_clicked)

        self.auto_button.grid(column=0, row=0)

        self.apps = {
            "Google Drive": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Drive.lnk",
            "TidyTabs": r"C:\Users\WEIYA\Google Drive\z. Documents\z. Apps\0 TidyTabs\TidyTabs.Daemon.exe",
        }

        self.google_button = Button(
            self.auto, text="open Drive", command=self.open_drive)
        self.google_button.grid(column=0, row=1)

        self.google_button = Button(
            self.auto, text="close Drive", command=self.close_drive)
        self.google_button.grid(column=0, row=2)

        self.tidy_button = Button(
            self.auto, text="open Tidy", command=self.open_tidy)
        self.tidy_button.grid(column=0, row=3)

        # * Random Topic Generator
        self.topics_out = Label(self.topics, text="Random Topic")
        self.topics_out.grid(column=1, row=1)
        self.topics_out.configure(
            bg="black", fg="white", font=("Arial", 12, "bold"))

        self.topics_button = Button(
            self.topics, text="Generate", command=self.topics_clicked)
        self.topics_button.grid(column=0, row=1)

        self.topics_dict = topics_dict

        self.topics = list()
        self.appeared_topics = dict()

        # * Small tools
        self.tools = LabelFrame(self, text="Small Tools")
        self.tools.grid(column=0, row=2, padx=20, pady=20)
        self.tools.configure(
            font=("Arial", 12, "bold"))
        
        self.folder_button = Button(
            self.tools, text="Open Random Folder", command=open_random_folder)
        self.folder_button.grid(column=0, row=0)
        

    def open_drive(self):
        os.startfile(self.apps["Google Drive"])

    def close_drive(self):
        os.system("taskkill /f /im GoogleDriveFS.exe")

    def open_tidy(self):
        os.startfile(self.apps["TidyTabs"])

    def auto_clicked(self):

        os.system("py auto.py")

    def topics_clicked(self):
        if self.topics == list():
            for topic in self.topics_dict.keys():
                self.topics.extend(self.topics_dict[topic]["list"])

        out = self.generateTopic()
        # bold the text
        self.topics_out.configure(
            text=out[0], fg=out[1])

    def generateTopic(self):

        ok = False
        while not ok:
            random_topic = np.random.choice(self.topics)
            if random_topic in self.appeared_topics.keys():
                self.appeared_topics[random_topic] += 1

                if np.random.uniform(0, 1) < 1/(self.appeared_topics[random_topic]+1):
                    ok = True
                else:
                    random_topic = np.random.choice(self.topics)
            else:
                self.appeared_topics[random_topic] = 1
                ok = True
        for topic in self.topics_dict.keys():
            if random_topic in self.topics_dict[topic]["list"]:
                random_color = self.topics_dict[topic]["color"][0]

        random_topic = random_topic.ljust(20)

        return (f"{random_topic}", f"{random_color}")


root = Root()
root.mainloop()
