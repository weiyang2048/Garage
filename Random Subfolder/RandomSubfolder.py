import os 
import random
folders = [x[0]  for x in os.walk(r"C:\Users\WEIYA\Google Drive") 
            if os.path.isdir(x[0])==True 
                and all(t not in x[0] for t in [".git",".tmp", "ipynb"])] 

os.startfile(random.choice(folders))