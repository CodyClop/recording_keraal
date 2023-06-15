import os

with open('rename_files.txt', 'r') as f:
    lines = f.readlines()
    lines.reverse() # reverse to rename latest version of each file
    for line in lines:
        source, target = line.split(',')
        try:
            os.rename(source, target[:-1]) # :-1 to remove '\n'
        except:
            pass
