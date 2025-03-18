import os 
import random


# turn this into a function
def open_random_folder():
    folders = [x[0]  for x in os.walk(r"C:\Users\WEIYA\Google Drive") 
            if os.path.isdir(x[0])==True 
                # and all(t not in x[0] for t in [".git",])
                ] 

    # compute the size of each folder not including subfolders
    folder_size = dict()
    for folder in folders:
        folder_size[folder] = sum([os.path.getsize(os.path.join(folder, f)) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))])
        # round up to the nearest MB
        folder_size[folder] = round(folder_size[folder]/1024/1024, 2) + 1   

    # randomly choose a folder based on the size of the folder
    # the larger the size, the higher the probability of being chosen
    # print size

    randomfolder = random.choices(list(folder_size.keys()), weights=list(folder_size.values()))[0]
    size = folder_size[randomfolder]
    # print size in MB
    print(size-1, "MB :", randomfolder )
    os.startfile(randomfolder)