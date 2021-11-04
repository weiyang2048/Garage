import os 

folders = [x[0]  for x in os.walk(r"C:\Users\WEIYA\Google Drive") if os.path.isdir(x[0])==True and ".tmp" not in x[0]] 
os.startfile(folders[1])