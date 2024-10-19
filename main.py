import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
path=os.getenv('path')
extension = '.csv'

files = [file for file in os.listdir(path)]


dfs = []

def log(name):
    file1 = open("log.txt", "a")
    file1.write(f'Working on {name}...\n\n')
    file1.close()
   

for file in files:
    if os.stat(os.path.join(path,file)).st_size == 0:
        file1 = open("badfiles.txt", "a")
        file1.write(file)
        file1.close()
        continue
    
    log(file) 

    df = pd.read_csv(os.path.join(path,file))

    if df.empty:
        st = f'{file}\n\n'
        file1 = open("badfiles.txt", "a")
        file1.write(st)
        file1.close()
        continue

    df['Phone']= df['Phone'].astype(str)

    num = df['Phone'].str.startswith('0').sum()

    if num > 10:
        st = f'{file}\n\n'
        file1 = open("badfiles.txt", "a")
        file1.write(st)
        file1.close()
        continue 

    dfs.append(df)
    


# print(dfs)

# df = pd.read_csv(os.path.join(path,files[0]))
# print(df)



# dd = pd.concat(dfs, ignore_index = True)

