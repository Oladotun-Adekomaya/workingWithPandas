import pandas as pd # type: ignore
import os
from dotenv import load_dotenv # type: ignore

from methods import check_bad_number, check_file_size, is_file_content_empty, log, open_file

load_dotenv()
path=os.getenv('path')
extension = '.csv'

# create a list of all the file paths
files = [file for file in os.listdir(path)]


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
    df = df.fillna(0) #first fill all the nan values in the df
    df[columnHeader]= df[columnHeader].astype(int) #convert the ddf to int to remove .0
    df[columnHeader]= '+' + df[columnHeader].astype(str)

    # Check if the file starts with specific numbers and log the file name and directory to badfiles for proper investigation
    check_bad_number(df,file,columnHeader)
    
    # Append dataframe to the dataframe list
    dfList.append(df)

# join all the dataframe in the dataframe list into one.
df = pd.concat(dfList, ignore_index = True)

#remove duplicates
df.drop_duplicates(subset=[columnHeader],inplace=True,keep='first')

# convert dataframe to csv file 
df.to_csv('whatsappGroupLeadMastersheet.csv',index=False)

print(df)

