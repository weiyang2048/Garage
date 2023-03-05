import time
import os
from colorama import Fore
from colorama import Style
from datetime import datetime
import numpy as np

apps = ["C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Drive.lnk",
        r"C:\Users\WEIYA\Google Drive\z. Documents\z. Apps\0 TidyTabs\TidyTabs.Daemon.exe"]

#        print(f"At {datetime.now().strftime('%H:%M:%S')} UTC, {Fore.GREEN} approximately {np.round(proportion_completed*100,4)}% completed.\
# {Fore.RED} Expecting to be completed in about {np.round(time_lapsed/proportion_completed - time_lapsed,0)} minuites.\
# {Fore.BLUE}  Start quering {query_name} for period : [\
# {datetime.strptime(start_date,'%Y%m%d').strftime('%Y-%m-%d')}T00:00,\
# {datetime.strptime(end_date,'%Y%m%d').strftime('%Y-%m-%d')}T00:00){Style.RESET_ALL}", end="\r")

for app in apps:
    print(
        f" {Fore.GREEN} oppening app : {Fore.BLUE} {app}"
    )
    os.startfile(app)
print("\n")

# close the Google Drive app after 3 minutes
close_delay = 180
for i in np.arange(1, close_delay+1):
    time.sleep(1)
    print(f" {Fore.LIGHTRED_EX} Closing Google Drive app after {close_delay-i} seconds. {Style.RESET_ALL}", end="\r")

tasks = ["taskkill /f /im GoogleDriveFS.exe"]
for task in tasks:
    print(
        f" {Fore.RED} closing task : {Fore.BLUE} {task}\n"
    )
    os.system(task)
print("\n")

delay = 120
for i in np.arange(1, delay+1):
    time.sleep(1)
    print((
        f" {Fore.RED} terminal will close in {delay-i}  sections."
    ), end="\r")

# time.sleep(delay)
# user_input = input("Press any key to exit")
