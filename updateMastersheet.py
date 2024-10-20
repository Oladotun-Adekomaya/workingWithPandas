import pandas as pd
import os
from dotenv import load_dotenv

from methods import append_df, check_bad_number, check_file_size, is_file_content_empty, log, open_file


path=os.getenv('path')
mastersheetPath=os.getenv('mastersheet')

# create a list of all the file paths
files = [file for file in os.listdir(path)]
print(files)


dfList = []
columnHeader = 'Phone'



for file in files:
    check_file_size(path,file)  
    
    log(file) 
    
    # open the file
    df = open_file(path,file)

    # Check if file content is empty
    is_file_content_empty(df,file)

    # Turn the phone column which contains numbers to text
    df[columnHeader]= df[columnHeader].astype(str)

    # Check if the file starts with specific numbers and log the file name and directory to badfiles for proper investigation
    check_bad_number(file,columnHeader)
    
    # Append dataframe to the dataframe list
    dfList.append(df)

# join all the dataframe in the dataframe list into one.
newdf = pd.concat(dfList, ignore_index = True)

#remove duplicates
newdf.drop_duplicates(subset=[columnHeader],inplace=True,keep='first')

mastersheet = pd.read_csv(mastersheetPath)

append_df(mastersheet,newdf,columnHeader)

# convert dataframe to csv file 

print(mastersheet)



