"""
Created on Tue Aug 22 14:53:35 2020

@author: Pradyumna.M
"""

import nltk
nltk.download('stopwords')

import numpy as np
import pandas as pd
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import nltk 
import re
import os
import shutil
from os.path import join
import time
import requests
from os import makedirs
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import xlrd 
import datetime

########################################

def renamed_latest_data_downloading(data_folder_loc,xl_file_loc):
    # to fetch current date
    current_date = datetime.datetime.today()
    d1 = current_date.strftime("%Y%m%d")
    Current_Date = str(d1) 


    # to fetch previous date
    previous_date = datetime.datetime.today() - datetime.timedelta(days=1)
    d2 = previous_date.strftime("%Y%m%d")
    Previous_Date = str(d2) 


    # Create a folder to store the result
    #drive_location = r'/content/drive/My Drive/ML Project/demo'
    drive_location = data_folder_loc
    if not os.path.exists(drive_location):os.mkdir(drive_location)

    folder_location = join(drive_location,Current_Date)
    if not os.path.exists(folder_location):os.mkdir(folder_location)


    # to fetch xl file
    loc = (xl_file_loc) 


    # To open Workbook 
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0) 
    n=len(sheet.col_values(1))

    for i in range (5,50):
      url = sheet.cell_value(i, 1)
      response = requests.get(url)
      soup= BeautifulSoup(response.text, "html.parser")
      for link in soup.select("a[href$='.pdf']"):
        cn1 = str(sheet.cell_value(i,0))
        # Create a file with company name (available in excel file) + "..." + pdf name from link
        # Spacing between company name and pdf name i.e. "..." is used later for string split 
        pdfname = join(cn1+"..."+link['href'].split('/')[-1])
        filename = join(folder_location,pdfname)
        print(filename)
        with open(filename, 'wb') as f:
            f.write(requests.get(urljoin(url,link['href'])).content)

    pfl = join(drive_location,Previous_Date)
    cfl = join(drive_location,Current_Date)


    # List of pdf available in folders 
    
    arr = [f for f in os.listdir(pfl) if f.endswith('.pdf')]
    arr1 = [g for g in os.listdir(cfl) if g.endswith('.pdf')]
    arr2=arr1


    # Create new folder to store only new files
    nfl = join(folder_location,"new")
    if not os.path.exists(nfl):os.mkdir(nfl)


    # delete duplicate files
    k=0
    for i in range(len(arr1)):
        for j in range(len(arr)):
            if arr1[i] == arr[j] :
                arr2=np.delete(arr2,i-k)
                k=k+1

    # store only new files in new folder
    for m in range(len(arr2)):
        pdf1 = join(cfl,arr2[m])
        shutil.copy(pdf1, nfl)

    # array of newely founded pdf documents only
    arr3 = [h for h in os.listdir(nfl) if h.endswith('.pdf')]

    #rename the documents
    for count, srcf in enumerate(arr3): 
        # array split 
        srcfc=srcf.split("...")
        src = join(nfl,srcf)
        dst = join(nfl,(srcfc[0]+"_"+ Current_Date + "_" +str(count)+ ".pdf"))
        os.rename(src,dst)
    
    return (data_folder_loc+Current_Date+"/new")

########################################
def oil_classification(pdf_loc,top_number=None):
    def pdf_to_text(path):
        manager = PDFResourceManager()
        retstr = StringIO()
        layout = LAParams(all_texts=True)
        device = TextConverter(manager, retstr, laparams=layout)
        filepath = open(path, 'rb')
        interpreter = PDFPageInterpreter(manager, device)
        for page in PDFPage.get_pages(filepath, check_extractable=True):
            interpreter.process_page(page)
        text = retstr.getvalue()
        filepath.close()
        device.close()
        retstr.close()
        return text

    if __name__ == "__main__":
        text_data = pdf_to_text(pdf_loc)
    
    dataset =nltk.regexp_tokenize(text_data, "[\w']+") 
    dataset.append("hgnismavihs")
    for i in range(len(dataset)): 
        dataset[i] = dataset[i].lower()
        dataset[i] = re.sub(r'\W', ' ', dataset[i]) 
        dataset[i] = re.sub(r'\s+', ' ', dataset[i]) 
        dataset[i] = re.sub(r'\d+', ' ', dataset[i])
    
    
    from nltk.corpus import stopwords
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    dataset = [w for w in dataset if not w in stop_words]
 
    from sklearn.feature_extraction.text import CountVectorizer


    def get_top_n_words(corpus, n=None):
        vec = CountVectorizer().fit(corpus)
        bag_of_words = vec.transform(corpus)
        sum_words = bag_of_words.sum(axis=0) 
        words_freq = [(word, sum_words[0, idx]) for word, idx in      
                      vec.vocabulary_.items()]
        words_freq =sorted(words_freq, key = lambda x: x[1], 
                           reverse=True)
        return words_freq[:n]

    dataset=(np.array(get_top_n_words(dataset,top_number)))[:,0]

    check_keywords=['oil','gas','petroleum','upstream','midstream','downstream','crude','pipeline','wells','rigs','wti','brent','frac']

    x=0;
    if(len(dataset)==1):
            x=-10  
    for i in check_keywords:
        for j in dataset:
            if(i==j):
                x=10
        
    if (x>0) :
        output="oil_file" 
    elif (x<0):output="foreign_language_file"
    else:output="non_oil_file"
    
    return output



################################

def categorising_as_csv_and_folder(pdf_folder_loc,priority_number=None):
    
    pdf_list = [h for h in os.listdir(pdf_folder_loc) if h.endswith('.pdf')]
    dict={"pdf_list":pdf_list}
    output=pd.DataFrame(dict)
    output.set_index("pdf_list",inplace=True)
    output.to_csv(pdf_folder_loc+'/result_file.csv')


    csv_file_location= pdf_folder_loc +'/result_file.csv'
    pdf_files=pd.read_csv(csv_file_location)

    categories=[]
    pdf_file_list=[]
    pdf_files["pdf_list"]
    for pdf_file in pdf_files["pdf_list"]:
        file_path_list=[pdf_folder_loc,pdf_file]
        pdf_file_list.append(pdf_file)
        pdf_location="/".join(file_path_list)
        category=oil_classification(pdf_location,priority_number)
        if (category=="oil_file"):
            oil_folder = join(pdf_folder_loc,"oil_files")
            if not os.path.exists(oil_folder):os.mkdir(oil_folder)
            shutil.copy(pdf_location, oil_folder)
        if (category=="non_oil_file"):
            non_oil_folder = join(pdf_folder_loc,"non_oil_files")
            if not os.path.exists(non_oil_folder):os.mkdir(non_oil_folder)
            shutil.copy(pdf_location, non_oil_folder)
        if (category=="foreign_language_file"):
            foreign_language_file = join(pdf_folder_loc,"foreign_language_file")
            if not os.path.exists(foreign_language_file):os.mkdir(foreign_language_file)
            shutil.copy(pdf_location, foreign_language_file)


        categories.append(category)
        print(pdf_file)
        print(category)

    dict={"pdf_file_list":pdf_file_list,"categories":categories}
    result=pd.DataFrame(dict)
    result.set_index("pdf_file_list",inplace=True)
    print(result)
    result.to_csv(csv_file_location)

########################################

#follow the given below instruction to get the downloading of files

##Change the data_folder_loc(where you want to download the file) and xl_file_loc (which contains the links)




data_folder_loc = './mr_project/'
xl_file_loc = "./mr_project/Radar Links_Europe & CIS.xlsx"

#below command will start the downloading of files and copying the non duplicte file in "new" folder inside the folder "CurrentDate" in data_folder_loc
pdf_folder_loc=renamed_latest_data_downloading(data_folder_loc,xl_file_loc)

############################################
#follow the given below instruction to get the classification of files
##change the number 100 to your priority number for list of words which has high frequency or remove it to get all words



#Below command will separate the files in "new" folder and copying them into "oil_files", "non_oil_files" and "foreign_language_files"folder
#It will aslo generate the corresponding csv file regarding classification
categorising_as_csv_and_folder(pdf_folder_loc)

