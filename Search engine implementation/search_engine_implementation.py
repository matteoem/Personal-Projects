import requests
import json
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import string
import pandas as pd
from pandas import DataFrame
import csv
from collections import defaultdict
import math
import numpy as np
from numpy import linalg
import operator as op
import time
#from tabulate import tabulate

#nltk.download('punkt')

def csv_to_tsv(nameCsv_file,nameTsv_file):
    #the two inputs must be str
    with open(nameCsv_file,'r', encoding='utf-8') as csvin, open(nameTsv_file, 'w', newline='', encoding='utf-8') as tsvout:
        csvin = csv.reader(csvin)
        tsvout = csv.writer(tsvout, delimiter='\t')
 
        for row in csvin:
            tsvout.writerow(row)

def Polish_informations_and_preprocess(result,only_names=False):
    arr_names = []
    arr_prices = []
    arr_prime = []
    arr_stars = []
    arr_url = []
    arr_tokens = []
    for element in result:
        result_names = element.find(class_='a-size-base-plus a-color-base a-text-normal')
        arr_names.append(result_names.text)
        if element.findAll('span', attrs={"class":"a-price-whole"}):
            arr_prices.append(element.find(class_='a-price-whole').text)
            #print(arr_prices)
        if not element.findAll('span', attrs={"class":"a-price-whole"}):
            arr_prices.append("no price available")
        if (len(element.findAll(class_='a-icon a-icon-prime a-icon-medium'))==1 ) :
            arr_prime.append("prime")
        if(len(element.findAll(class_='a-icon a-icon-prime a-icon-medium'))==0):
            arr_prime.append("not prime")
        result_stars = element.findAll(class_='a-row a-size-small')#.findAll(class_='a-row a-size-small')
        if(len(result_stars)!=0):
            arr_stars.append(result_stars[0].find(class_='a-icon-alt').text)
        if(len(result_stars)==0):
            arr_stars.append("no vote available")
        if(element.find('a', {'class': 'a-size-base a-link-normal a-text-normal'}) is None):
            arr_url.append("No url Available")
        if(element.find('a', {'class': 'a-size-base a-link-normal a-text-normal'}) is not None):
            arr_url.append(element.find('a', {'class': 'a-size-base a-link-normal a-text-normal'})['href'])


    df,tokenized_filtered_arr_names = tokenize_and_proprocess_data(arr_names,arr_prices,arr_prime,arr_stars,arr_url,only_names)

    return df,tokenized_filtered_arr_names

def tokenize_query(query):
    symbol_to_remove = "!@#$%^&*()_-+={}[],'\"”;:.-–''xds/|"
    things_to_remove = {"1", "2", "3","4","5","6","7","8","9","0"}
    stop_words = set(stopwords.words('italian'))
    query = query.lower()
    tokenized_query = word_tokenize(query,language='italian') 
    filtered_query = [] 
    for w in tokenized_query: 
        #if (w not in stop_words and w not in symbol_to_remove): 
        if (w not in stop_words and w not in symbol_to_remove and w not in things_to_remove): 
            filtered_query.append(w) 
    return filtered_query

def tokenize_and_proprocess_data(arr_names,arr_prices,arr_prime,arr_stars,arr_url,only_names=False):
    tokenized_filtered_arr_names =[]
    symbol_to_remove = "!@#$%^&*()_-+={}[],'\"”;:.-–''xds/|"
    things_to_remove = {"1", "2", "3","4","5","6","7","8","9","0"}
    stop_words = set(stopwords.words('italian'))

    for element in arr_names:
        element = element.lower()
        tokenized_elements = word_tokenize(element,language='italian') 
        filtered_sentence = [] 
        for w in tokenized_elements:
            #if (w not in stop_words and w not in symbol_to_remove): 
            if (w not in stop_words and w not in symbol_to_remove and w not in things_to_remove): 
                filtered_sentence.append(w) 
        tokenized_filtered_arr_names.append(filtered_sentence)
    if(only_names==False):
        # print("print tokenized_filtered_arr_names:")
        # print(len(tokenized_filtered_arr_names))
        helper_list = list(zip(arr_names,arr_prices,arr_prime,arr_stars,arr_url))
        df = pd.DataFrame(helper_list,columns=["description","price","prime?","rating","url link"])
        print("size of df")
        #print(df.shape)
        return df,tokenized_filtered_arr_names
    elif(only_names==True):
        return tokenized_filtered_arr_names

def hashing_documents(corpus):
    hashed_documents=[]
    i = 0
    for element in corpus:
        hashed_documents.append([])
        for token in element:
            hashed_documents[i].append(hash(token))
        i += 1
    return hashed_documents

def create_inverted_index(hashed_documents):
    dictionary = defaultdict(list)
    idf_dict = dict()
    for i, element in enumerate(hashed_documents):
        max_freq = 0

        for index, token in enumerate(element):
            count = element.count(token)                         # conto quante volte il token compare nel documento
            first_occurence = element.index(token)               # mi salvo la prima volta che compare
            if count > 1 and first_occurence != index : continue # skippo l'append della tupla nel dict se ho un token che appare piu volte per evitare tuple identiche

            freq = count / len(element)                          # la frequenza di un token è il count diviso il #token nel documento
            if freq > max_freq : max_freq = freq                 # salvo la max frequency fra i termini nel doc
            dictionary[token].append((i, freq))                  # appendo al dizionario con key=tokens, una tupla con l'indice del doc e la frequenza
            index += 1                                           # index usato per controllare se il token a cui mi trovo è il primo incontrato(check line 120-121)
        
        for index, token in enumerate(element):
            count = element.count(token)                         #prendo il count del token corrente nel doc
            first_occurence = element.index(token)
            if count > 1 and first_occurence != index : continue

            list_ = dictionary[token]   #accedo alla tupla di valori assegnati al token
            token_index = len(list_) - 1    #
            freq = list_[token_index][1]    #perchè non freq = list_[]
            list_[token_index] = (i, freq / max_freq)   #(id_doc,tf score)

            index += 1

    #qui avro' un dizionario dove ogni key è un token,con assegnate tuple (id_doc,tf_score)
    for key in dictionary:
        count = len(dictionary[key])        #number of doc in which the token appear
        idf = math.log2(len(hashed_documents) / count)
        idf_dict[key] = idf

        for i, tuples in enumerate(dictionary[key]): #lista di tuple
            dictionary[key][i] = (tuples[0], tuples[1] * idf)    #tf*idf

    with open("inverted_index.json", "wb") as f:
        f.write(json.dumps(dictionary).encode("utf-8"))

    return dictionary,idf_dict

def vectorize_documents(dictionary, num_documents):
    documents_vectorized = []
    for index in range(num_documents):
        documents_vectorized.append([])

    for index in range(len(documents_vectorized)):
        for key in dictionary:
            doc_found = False
            for tuples in dictionary[key]:
                if tuples[0] == index:
                    doc_found = True
                    documents_vectorized[index].append(tuples[1])
                    break
            if doc_found == False: documents_vectorized[index].append(0)
    return documents_vectorized

def vectorize_query(query, dictionary,idf_dict):
    Q_vect = [0] * len(dictionary)

    for q in query:
        c = query.count(q)
        for index,key in enumerate(dictionary):
            if key == q : 
                Q_vect[index] = (c/len(query)) *idf_dict[key]
                break 
    return Q_vect  

def compute_cos_sim(query, documents_vectorized):
    # print(" ")
    # print("----first document vectorized:")
    # print(documents_vectorized[4])
    # print(" ")
    val = []
    for doc_id, document in enumerate(documents_vectorized):
        val.append( np.dot(document, query) / ( np.linalg.norm(query) * np.linalg.norm(document) ) )
    return val

def search_results(query, dictionary, documents_vectorized,idf_dictionary):
    vec_q = vectorize_query(query, dictionary,idf_dictionary)
    # print(" ")
    # print("-----printing the vectorized query:")
    # print(vec_q)
    # print(" ")
    results = compute_cos_sim(vec_q, documents_vectorized)
    # print("-----results of cosine similarity:")
    # print(results)

    out = []
    for i, res in enumerate(results):
        out.append((i, res))
    return list(zip(*sorted(out, key=op.itemgetter(1), reverse=True)))
    

if __name__ == "__main__":
    load = True ##########
    if(load == False):
        keyword = 'computer'
        X = 6
        tokens_from_description = []
        final_frames=[]
        for i in range(1,X):
            url = 'https://www.amazon.it/s?k=' + keyword +'&page='+ str(i)
            headers = {'User-Agent': 'Chrome/42.0.2311.90 Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14'}
            r = requests.get(url, headers = headers)
            #print(r.status_code)
            if r.status_code == 200:
                print('Success!')
            elif r.status_code == 404:
                print('Not Found.')
            elif r.status_code == 503:
                print('too much requests perhaps? Adjust the header!')
            text = r.text
            soup = BeautifulSoup(text, 'html.parser')
            result = soup.findAll(class_='celwidget slot=MAIN template=SEARCH_RESULTS widgetId=search-results')
            temp_df,temp_tokens_from_description = Polish_informations_and_preprocess(result)
            #print(temp_df.shape)
            tokens_from_description += temp_tokens_from_description
            print("len(token_from_descrpition):"+" " + str(len(tokens_from_description)))
            final_frames.append(temp_df)
            time.sleep(5)
        if(X>1): df = pd.concat(final_frames)
        elif(X==1):
        # print(final_frames)
            df = final_frames[0]
        #print(df.shape)
        del df["Unnamed: 0"]
        df.to_csv('amazon_results_polished.csv')
        csv_to_tsv("amazon_results_polished.csv","amazon_results_polished.tsv")

    if(load == True):
        df = pd.read_csv("amazon_results_polished.tsv", sep="\t",)
        del df["Unnamed: 0"]
        arr_names = df["description"].tolist()
        arr_prices = df["price"].tolist()
        arr_prime = df["prime?"].tolist()
        arr_stars = df["rating"].tolist()
        arr_url = df["url link"].tolist()
        tokens_from_description = tokenize_and_proprocess_data(arr_names,arr_prices,arr_prime,arr_stars,arr_url,only_names=True)
        print(tokens_from_description[0])
        print(tokens_from_description[8])
        # with open('tokenized_documents.tsv', 'w', newline='') as f_output:
        #     tsv_output = csv.writer(f_output, delimiter='\t')
        #     tsv_output.writerow(tokens_from_description)
        with open("tokenized_documents.csv", "w", newline="", encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(tokens_from_description)
        #print(tokens_from_description)

    inverted_index,idf_dictionary = create_inverted_index(tokens_from_description)
    vectorized_documents = vectorize_documents(inverted_index, len(tokens_from_description))
    # for i in range(10):
    #     print(vectorized_documents[i])
    Q = "chuwi"
    tokenized_query = tokenize_query(Q)
    results, similarities = search_results(tokenized_query, inverted_index, vectorized_documents,idf_dictionary)
    print(" ")
    print("query requested: " + str(Q))
    print(" ")
    print("query tokenized: " + str(tokenized_query))
    for index,elem in enumerate(results):
        print(df.loc[[elem]])
        print(" ")
        if(index ==10): break # print top 10 ranking









