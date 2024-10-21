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
    # num = df[columnHeader].str.startswith('0').sum()
    # if num > 10:
    #     st = f'{file}\n\n'
    #     file1 = open("badfiles.txt", "a")
    #     file1.write(st)
    #     file1.close()

    check_bad_number(df,file,columnHeader)

    
    # Append dataframe to the dataframe list
    dfList.append(df)

print('Finished creating list of dataframes.')

print(dfList)

# join all the dataframe in the dataframe list into one.
newdf = pd.concat(dfList, ignore_index = True)
print('\n\nFinished creating new Dataframe from list of dataFrame')
print(newdf)

#remove duplicates
newdf.drop_duplicates(subset=[columnHeader],inplace=True,keep='first')
print("\n\nFinish removing duplicates")
print(newdf)

# mastersheet = pd.read_csv(mastersheetPath)
mastersheet = pd.read_csv(mastersheetPath)
print("\n\nFinish creating mastersheet dataframe")
print(mastersheet)

# convert mastersheet phone column to string
mastersheet[columnHeader]= mastersheet[columnHeader].astype(str)
print("\n\nConverted mastersheet phone column to string")
print(mastersheet)

# Get unique Phone number - numbers present in newdf but not in mastersheet
df_diff = newdf[~newdf.Phone.isin(mastersheet.Phone)]

print(df_diff)

newMastersheet = pd.concat([mastersheet, df_diff], ignore_index=True)

print(newMastersheet)

newMastersheet.to_csv('whatsappGroupLeadMastersheet.csv',index=False)

newMastersheet.to_csv(mastersheetPath,index=False)