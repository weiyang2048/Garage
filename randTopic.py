import time
import os
from colorama import Fore
from colorama import Back
from colorama import Style
from datetime import datetime
import numpy as np
from tkinter import Tk, Label, Button, Entry, LabelFrame


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

        # * Random Topic Generator
        self.topics_out = Label(self.topics, text="Random Topic")
        self.topics_out.grid(column=1, row=1)
        self.topics_out.configure(
            bg="black", fg="white", font=("Arial", 12, "bold"))

        self.topics_button = Button(
            self.topics, text="Generate", command=self.topics_clicked)
        self.topics_button.grid(column=0, row=1)

        self.topics_dict = {
            "Mathematics": {"color": ["lightblue"], "list": ["Complex Analysis", "Measure Theory", "Function Analysis", "Calculus", "Linear Algebra"]},
            "Probability": {"color": ["lightgreen"], "list": ["Random Matrix", "Probability"]},
            "Machine Learning": {"color": ["yellow"], "list": ["Deep Learning", "Machine Learning", "Finance"]},
            "Programming": {"color": ["red"], "list": ["Review", "Web", "Data", "Programming"]},
            "Language": {"color": ["cyan"], "list": ["Duolingo", "Spanish", "French"]},
            "Others": {"color": ["pink"], "list": ["todo list"]},
        }

        self.topics = list()
        self.appeared_topics = dict()

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

# # read topicslist.txt into a array separtate by line
# topics_dict = {
#     "Mathematics": {"color": [Fore.LIGHTBLUE_EX], "list": ["Complex Analysis", "Measure Theory", "Function Analysis", "Calculus", "Linear Algebra"]},
#     "Probability": {"color": [Fore.LIGHTGREEN_EX], "list": ["Random Matrix", "Probability"]},
#     "Machine Learning": {"color": [Fore.LIGHTYELLOW_EX], "list": ["Deep Learning", "Machine Learning", "Finance"]},
#     "Programming": {"color": [Fore.LIGHTMAGENTA_EX], "list": ["Review", "Web", "Data", "Programming"]},
#     "Language": {"color": [Fore.LIGHTCYAN_EX], "list": ["Duolingo", "Spanish", "French"]},
#     "Others": {"color": [Fore.LIGHTRED_EX], "list": ["todo list"]},
# }

# # combine topic lists into one list
# topics = []
# for topic in topics_dict.keys():
#     topics.extend(topics_dict[topic]["list"])

# for topic in topics_dict.keys():
#     print(
#         f" {Fore.GREEN} {topic} : {topics_dict[topic]['color'][0]} {topics_dict[topic]['list']} {Style.RESET_ALL}\n")

# # create a dictionary between color and their dark version
# color_dict = {
#     Fore.LIGHTBLUE_EX: Fore.BLUE,
#     Fore.LIGHTGREEN_EX: Fore.GREEN,
#     Fore.LIGHTYELLOW_EX: Fore.YELLOW,
#     Fore.LIGHTMAGENTA_EX: Fore.MAGENTA,
#     Fore.LIGHTCYAN_EX: Fore.CYAN,
#     Fore.LIGHTRED_EX: Fore.RED,
# }

# # press enter to exist, other to generate another topic
# user_input = ""
# print("Press enter to generate another topic, other to exit\n")
# appeared_topics = dict()


# user_input = ""

# while user_input == "":
#     ok = False
#     while not ok:
#         random_topic = np.random.choice(topics)
#         if random_topic in appeared_topics.keys():
#             appeared_topics[random_topic] += 1

#             if np.random.uniform(0, 1) < 1/(appeared_topics[random_topic]+1):
#                 ok = True
#             else:
#                 random_topic = np.random.choice(topics)
#         else:
#             appeared_topics[random_topic] = 1
#             ok = True
#     for topic in topics_dict.keys():
#         if random_topic in topics_dict[topic]["list"]:
#             random_color = topics_dict[topic]["color"][0]
#             # Replace light color with dark color
#             random_color = color_dict[random_color]

#     print(f"{Fore.GREEN}random topic : {Back.WHITE}{random_color} {random_topic} {Style.RESET_ALL}", end="\r")
user_input = input()
