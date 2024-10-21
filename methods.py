import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
path=os.getenv('path')

def log(name):
    file1 = open("log.txt", "a")
    file1.write(f'Working on {name}...\n\n')
    file1.close()
   
def check_file_size(fpath, file):
    if os.stat(os.path.join(fpath,file)).st_size == 0:
        fh = open("badfiles.txt", "a")
        fh.write(file)
        fh.close()

def open_file(fpath,file):
    return pd.read_csv(os.path.join(fpath,file))

def is_file_content_empty(df,file):
   if df.empty:
      st = f'{file}\n\n'
      file1 = open("badfiles.txt", "a")
      file1.write(st)
      file1.close()

def check_bad_number(df,file,columnHeader):
   badNumberList = ['0','1','3','4','5','6','7','8','9']
   for n in badNumberList:
       
        num = df[columnHeader].str.startswith(n).sum()

        if num > 10:
            st = f'{file}\nStarts with {n}\n\n'
            file1 = open("badfiles.txt", "a")
            file1.write(st)
            file1.close()



def append_df(df1, df2, columnTitle):
    for value in df2[columnTitle]:
        if not df1[columnTitle].isin([value]).any():
            row_number = df2.index.get_loc(df2[df2[columnTitle] == value ].index[0])
            row = df2.loc[row_number]
            df1.loc[len(df1.index)] = row
    return df1
