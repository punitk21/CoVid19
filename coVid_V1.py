# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 18:00:28 2020

@author: Punit
"""
#%%
import wget
import os
import urllib.request
# importing all the required modules
import PyPDF2
import tabula
import pandas as pd
import numpy as np
print('Package Imported Now Data Import')
from datetime import datetime, timedelta

#%%
os.chdir(r"E:\Punit\Project\Covid\Data")  ## Folder name where you want to download the PDF report
#%%
current_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d').__str__().replace('-', '')

from datetime import datetime
then = datetime(2020, 3,26)        # Random date in the past
now  = datetime.now()                         # Now
duration = (now - then).days 
i = str(65+duration)
 
 
fixed_url = "https://www.who.int/docs/default-source/coronaviruse/situation-reports/"
dynamic_url = current_date+"-sitrep-"+i+"-covid-19.pdf"
url = fixed_url+ dynamic_url
#url = 'https://www.who.int/docs/default-source/coronaviruse/situation-reports/20200323-sitrep-63-covid-19.pdf'
urllib.request.urlretrieve(url, "filename.pdf")

#%%
# creating an object 
file = open('filename.pdf', 'rb')
# pdf reader object
pdfReader = PyPDF2.PdfFileReader(file)
# number of pages in pdf
print(pdfReader.numPages)
no_of_page = pdfReader.numPages
# readinf the PDF file that contain Table Data
# you can find find the pdf file with complete code in below
# read_pdf will save the pdf table into Pandas Dataframe
actual_page = no_of_page
#%% last Page Indentifier
res= False
while res == False:
    try:
        actual_page = actual_page-1
        print(actual_page)
        chk_pdf = tabula.read_pdf("filename.pdf",pages=actual_page)
        col_nm = chk_pdf.columns
        tmp_result = chk_pdf[col_nm[0]].str.contains("Grand total")
        res = True in tmp_result.unique()
        print(actual_page)
    except AttributeError:
        print("working")
    except TypeError:
        print("working")
#%%
start_page =0
res= False
while res == False:
    try:
        start_page = start_page+1
        print(start_page)
        chk_pdf = tabula.read_pdf("filename.pdf",pages=start_page)
        col_nm = chk_pdf.columns
        tmp_result = chk_pdf[col_nm[0]].str.contains("China")
        res = True in tmp_result.unique()
        print(start_page)
    except AttributeError:
        print("working")
    except TypeError:
        print("working")
#%%
#import camelot
temp_pdf = pd.DataFrame()       
for i in range(start_page,actual_page+1):
    print(i)
    temp  = tabula.read_pdf("filename.pdf",pages=i,multiple_tables=True)
    temp_pdf = temp_pdf.append(temp)
    
temp_pdf = pd.DataFrame(temp_pdf).reset_index()

del temp_pdf['index']
#tabula.read_pdf    
#%% Data Cleaning 
    
#ch = pd.DataFrame(df[0])
initial = temp_pdf[temp_pdf[0].str.startswith('Reporting Country/')== True].index[0]
#last = temp_pdf.loc[temp_pdf[0].str.startswith('IV. MANU')== True].index[0]

base_data = temp_pdf.drop(index = list(range(0,initial-1)))
headers= base_data[base_data.index.isin(list(range(initial-1,initial+4)))]   

base_data = base_data.drop(index = list(range(initial-1,initial+4)))


header_concat = headers.T.fillna('')

header_concat['columns'] = header_concat.apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

header = pd.DataFrame(header_concat['columns']).T
base_data.columns= header.iloc[0]

cols_names= base_data.columns
base_data[cols_names[0]] = np.where(base_data[cols_names[0]].isnull(), base_data[cols_names[1]], base_data[cols_names[0]])


#%% Data Bifurgation
colu = base_data.columns
null_data = base_data[base_data[colu[5]].isnull()].index.tolist()
null_data.insert(0, 0)
subs = []
for i in range(0,len(null_data)-1):
    start = i
    end = i+1
    print(start,end)
    temp = base_data[base_data.index.isin(list(range(null_data[start],null_data[end])))]
    name = temp[cols_names[0]].iloc[0]
    globals()['{}'.format(name)] = temp
    subs.append(globals()['{}'.format(name)])