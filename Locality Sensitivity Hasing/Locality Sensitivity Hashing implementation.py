import pandas as pd
import hashlib
import numpy as np
from random import randint
import collections
import time

def createCharacteristicMatrix(listOfShingles):
    aux_dict = dict()
    column_names = []
    for index,shingled_doc in enumerate(listOfShingles):
        column_names.append("shingled_doc n°"+str(index+1))
        for elem in shingled_doc:
            aux_dict[elem] = [0]*len(listOfShingles)    #I build a dict to have the number of rows needed for the char_matrix

    for index,shingled_doc in enumerate(listOfShingles):
        for elem in shingled_doc:
            aux_dict[elem][index] = 1   #0 if the element is in the set,zero otherwise

    characteristic_matrix = pd.DataFrame.from_dict(aux_dict, orient='index',columns = column_names)
    return characteristic_matrix

def hashFamily(i):
    # Implement a family of hash functions. It hashes strings and takes an
    # integer to define the member of the family.
    # Return a hash function parametrized by i
    resultSize = 8 # how many bytes we want back
    maxLen = 20 # how long can our i be (in decimal)
    salt = str(i).zfill(maxLen)[-maxLen:]   #zfill fill the string "i" with zeros on the left up to maxlen
    def hashMember(x):
        #return hashlib.sha1((x + salt).encode()).hexdigest()[-resultSize:] #return the hexadecimal format
        #return int(hashlib.sha1((x + salt).encode()).hexdigest()[-resultSize:],32 ) #return the int format of the value
        return hashlib.sha1((x + salt).encode()).digest()[-resultSize:] #return the byte format

    return hashMember

def Jaccard_Similarity_with_sets(set1,set2):
    return len(set1.intersection(set2))/len(set1.union(set2))

def Jaccard_Similarity_with_signatures(vec1,vec2):
    count = 0
    for i in range(len(vec1)):
        if(vec1[i]==vec2[i]): count +=1
    return count/len(vec1)

def testJaccardSim(signature_matrix,listOfShingled_doc,num_doc_1,num_doc_2):
    vec_docTest1 = list(signature_matrix['sig_vec_doc n°'+str(num_doc_1)])
    vec_docTest2 = list(signature_matrix['sig_vec_doc n°'+str(num_doc_2)])
    setTest1 = listOfShingled_doc[num_doc_1]
    setTest2 = listOfShingled_doc[num_doc_2]


    jaccard_sim = Jaccard_Similarity_with_signatures(vec_docTest1,vec_docTest2)
    eff_jaccard_sim = Jaccard_Similarity_with_sets(setTest1,setTest2)
    print("jaccard sim computed through the signature vectors:")
    print(str(jaccard_sim*100)+"%")
    print("jaccard sim computed through the starting sets of shingles:")
    print(str(eff_jaccard_sim*100)+"%")

def compute_real_jaccard_similarity_matrix(characteristic_matrix,listOfShingled_doc):
    effective_jaccard_sim_mat = dict()
    for i in range(len(characteristic_matrix.columns)):
        for j in range(len(characteristic_matrix.columns)):
            tup = (i,j)
            if tup in effective_jaccard_sim_mat or tup[::-1] in effective_jaccard_sim_mat or i==j:
                continue
            set1 = listOfShingled_doc[i]
            set2 = listOfShingled_doc[j]
            eff_jaccard_sim = Jaccard_Similarity_with_sets(set1,set2)
            effective_jaccard_sim_mat[tup] = eff_jaccard_sim
    return effective_jaccard_sim_mat

def create_estimated_jaccard_similarity_matrix(signature_matrix):
    estimated_jaccard_sim_mat = dict()
    for i in range(len(signature_matrix.columns)):
        for j in range(len(signature_matrix.columns)):
            tup = (i,j)
            if tup in estimated_jaccard_sim_mat or tup[::-1] in estimated_jaccard_sim_mat or i==j:
                continue
            estimated_jaccard_sim_mat[tup] = 0
    return estimated_jaccard_sim_mat

def intersection(lst1, lst2):
    b = set(lst1)
    c = set(lst2)
    a = b.intersection(c)
    return a

def difference(lst1, lst2):
    b = set(lst1)
    c = set(lst2)
    a = b.difference(c)
    return a

class Make_Shingling:
    def __init__(self, document, window,want_hash):
        self.document = document
        self.window = window
        self.want_hash = want_hash
        #for hashing we will use the basic function of python. 
        #The largest value it can represent is (2^31) - 1.
        #The smallest value it can represent is -(2^31).
        #Thus each element of the set will be mapped to a bucket of value that ranges from -(2^31) to (2^31) - 1.

    def createShingleFromDoc(self):
        shingles = set()
        for i in range(len(self.document)-self.window+1 ):  #creerò un elmento nello shingle per ogni character nella stringa
          if (self.want_hash):                              #se voglio hasharlo
            element = self.document[i:self.window+i]        #con questo taglio della substring interna prendo un numero pari a "window"..
            shingles.add(hash(element))                     #..di caratteri e li conidero un elemento. Dopodichè grazie al for,la finestra scorre
          else:
            element = self.document[i:self.window+i]
            shingles.add(element)
        return shingles
    

class Make_Signature_Matrix:
    def __init__(self,characteristic_matrix,n_trials,load_sign_mat):
        self.characteristic_matrix = characteristic_matrix
        self.n_trials = n_trials
        self.load_sign_mat = load_sign_mat

    def load_signature_matrix(self):
        #signature_matrix = pd.read_csv('C:/Users/rikuh/Desktop/Data Mining/homeworks/DM_Homework_3_1912588_Matteo_Emanuele/signature_matrix_10k_hash.csv',index_col=0)
        signature_matrix = pd.read_csv('C:/Users/rikuh/Desktop/Data Mining/homeworks/DM_Homework_3_1912588_Matteo_Emanuele/signature_matrix.csv',index_col=0)   #100 hash functions
        return signature_matrix

    def compute_signature_matrix(self):
        n_trials = self.n_trials
        characteristic_matrix = self.characteristic_matrix
        hash_function_list = []
        signature_matrix = []
        for i in range(n_trials):
            #hash_function_list.append(hashFamily(randint(-1000000,1000000))) #creo un array di hashfunctions parametrizzate da un valore int random
            hash_function_list.append(hashFamily(i)) #creo un array di hashfunctions random
        sig_vectors =[]
        for j,col in enumerate(characteristic_matrix):                           #per ogni colonna...
            sig_vectors.append("sig_vec_doc n°"+str(j))
            column = list(characteristic_matrix[col])               # converto in lista,poi..
            aux_list = []                                           #inizializzo gli array
            sig_vec = []                                            #//
            for index,elem in enumerate(column):                    #per ogni elemento nella colonna..
                aux_list = []
                if elem==1:                                         #se ci trovo un 1 significa che quell'elemento è nello shingled_document,dunque..
                    for hashf in (hash_function_list):              #computo l'hash value dell'indice della riga di quel valore per ogni hashfunction creata...
                        aux_list.append(hashf(str(characteristic_matrix.iloc[index].name))) # e li storo dentro un array ausiliario.
                    if(len(sig_vec)==0): sig_vec = aux_list         #se il mio signature vector è vuoto,il mio vettore ausiliario diventa il mio signature vector,
                    else:                                           #..altrimenti
                        for i,element in enumerate(aux_list):       #per ogni elemento nell'array ausiliario controllo..
                            if(element < sig_vec[i]):               #se l'elemento in posizione i è minore del valore in posizione i del signature vector,se lo è...
                                sig_vec[i] = element                #lo sostituisco
            signature_matrix.append(sig_vec)                        #finito questo ciclo sulla colonna, ho un vettore signature che storo nella mia signature_matrix


        signature_matrix = pd.DataFrame(signature_matrix,index=sig_vectors)
        signature_matrix = signature_matrix.transpose() 
        print(signature_matrix)
        signature_matrix.to_csv('signature_matrix.csv')
        return signature_matrix

    def get_signature_matrix(self):
        if self.load_sign_mat: signature_matrix = self.load_signature_matrix();
        else: signature_matrix = self.compute_signature_matrix();
        return signature_matrix

class locality_Sensitive_Hashing:
    def __init__(self,signature_matrix,b,r,duplicate_threshold):
        self.signature_matrix = signature_matrix
        self.b = b
        self.r = r
        self.duplicate_threshold = duplicate_threshold
        
    def find_candidates_duplicates(self):
        arr_buckets = []                                         #creo un array di dizionari
        for i in range(b):
            arr_buckets.append(collections.defaultdict(list))    # riempio l'array con i rispettivi dizionari,che rappresentano i bucket
        print("-----------------------------")
        hh = hashFamily(42)               #creo un hash function che userò per mappare le singole sottocolonne in una banda dentro un bucket
    
        for i,col in enumerate(self.signature_matrix):
            bucket_index = 0                                        
            for j in range(b):                                   # il range [r*j:(j+1)*r] rappresenta le varie finestre ampie r righe in ogni colonna
                element = hh(str(list(self.signature_matrix[col][r*j:(j+1)*r]))) # ed individuo tante finestre quante è il numero di bande che ho scelto
                arr_buckets[bucket_index][element].append(i)     # per ogni elemento trasformato a str e hashato, creo una key nel suo 
                                                                 # rispettivo bucket a cui appendo l'indice del documento
                bucket_index +=1

        list_of_duplicate_candidates = []                        #una volta che i bucket sono pieni,inizio ad individuare i vari duplicati
        for bucket in arr_buckets:                               #in ogni bucket...
            for key in bucket:                                   #controllo per ogni key...
                if len(bucket[key]) > 1:                         #..se quella key ha piu di un documento appuntato,se Sì...
                    list_of_duplicate_candidates.append(bucket[key])   #salvo quella lista come "lista di documenti potenzialmente duplicati"
        return list_of_duplicate_candidates

    def refine_duplicates(self,list_of_duplicate_candidates):      #funzione per eliminare le tuple ripetute 
        refined_duplicates = []
        for element in list_of_duplicate_candidates:
            if len(element)<=2: refined_duplicates.append((element[0],element[1]))
            if len(element)>2:
                for elem1 in element:
                    for elem2 in element:
                        if elem1==elem2 or (elem2,elem1) in refined_duplicates: continue
                        else: refined_duplicates.append((elem1,elem2))   #costruisco una lista composta da tutte le tuple di elementi non uguali,e...
        return refined_duplicates

    def fill_estimated_jaccard_similarity_matrix(self,list_of_duplicate_candidates,estimated_jaccard_similarity_matrix):
        #print(list_of_duplicate_candidates)
        for element in list_of_duplicate_candidates:                                          #per le liste di potenziali duplicati...
            if len(element)<=2:                                                               #se ne conto solo due...
                vec_docTest1 = list(self.signature_matrix['sig_vec_doc n°'+str(element[0])])
                vec_docTest2 = list(self.signature_matrix['sig_vec_doc n°'+str(element[1])])
                jaccard =  Jaccard_Similarity_with_signatures(vec_docTest1,vec_docTest2)      #calcolo la loro jaccard similarity e me la salvo...
                estimated_jaccard_similarity_matrix[(element[0],element[1])] = jaccard        #nella matrice che contiene tutte le jaccard stimata fra tutti i documenti

            if len(element)>2:                            #Se ho invece piu' di due elemnti candidati ad essere duplicati fra loro...
                list1 = []                                #significa che dovro' considerare tutte le varie coppie! Dunque..
                for elem1 in element:
                    for elem2 in element:
                        if elem1==elem2 or (elem2,elem1) in list1: continue
                    #    if elem1==elem2 : continue
                        else: list1.append((elem1,elem2))   #costruisco una lista composta da tutte le tuple di elementi non uguali,e...
                   
                #print(list1)
                for couples in list1:                                                             #una volta che tutte le coppie sono pronte...
                    vec_docTest1 = list(self.signature_matrix['sig_vec_doc n°'+str(couples[0])])
                    vec_docTest2 = list(self.signature_matrix['sig_vec_doc n°'+str(couples[1])])
                    jaccard =  Jaccard_Similarity_with_signatures(vec_docTest1,vec_docTest2)    # computo la jaccard e la salvo nella rispettiva key della tupla--
                    estimated_jaccard_similarity_matrix[couples] = jaccard                       #--dell'estimated jaccard matrix
        return estimated_jaccard_similarity_matrix   

    def compute_stats_and_print_blind_LSH(self,real_duplicates,list_of_refined_duplicate_candidates):
        tp = len(intersection(real_duplicates, list_of_refined_duplicate_candidates))
        fp = len(difference(list_of_refined_duplicate_candidates,real_duplicates))
        fn = len(difference(real_duplicates,list_of_refined_duplicate_candidates))
        tn = len(estimated_jaccard_similarity_matrix) - tp - fp - fn

        precision_ = tp/(tp+fp)  #true positives / total estimated positives
        recall_ = tp/(tp+fn)     #true positives / total actual positives

        print("-----------------------------")
        print("Performance of the duplicate search after blindly applying LSH:")
        print("TP:" +" "+ str(tp))
        print("TN:" +" "+ str(tn))
        print("FP:" +" "+ str(fp))
        print("FN:" +" "+ str(fn))
        print("accuracy:"+" "+ str( ((tp+tn)/(tp+tn+fp+fn))*100.0  )+ "%" )
        print("precision:" + " " + str(precision_*100)+ "%")
        print("recall:" + " " + str(recall_*100)+ "%")
        print("F1-score:" + " " + str( 2*(precision_*recall_)/(precision_+recall_)*100 )+ "%" )

    def compute_stats_and_print(self,estimated_jaccard_similarity_matrix,real_jaccard_similarity_matrix):
        true_positives = 0
        true_negatives = 0
        false_positive = 0
        false_negative = 0
        for key in estimated_jaccard_similarity_matrix:
            if(estimated_jaccard_similarity_matrix[key]>=self.duplicate_threshold and real_jaccard_similarity_matrix[key] >= self.duplicate_threshold): true_positives +=1
            elif(estimated_jaccard_similarity_matrix[key]>=self.duplicate_threshold and real_jaccard_similarity_matrix[key] < self.duplicate_threshold): false_positive +=1
            elif(estimated_jaccard_similarity_matrix[key]<self.duplicate_threshold and real_jaccard_similarity_matrix[key] >= self.duplicate_threshold): false_negative += 1
            elif(estimated_jaccard_similarity_matrix[key]<self.duplicate_threshold and real_jaccard_similarity_matrix[key] < self.duplicate_threshold): true_negatives +=1
        
        precision = true_positives/(true_positives+false_positive)  #true positives / total estimated positives
        recall = true_positives/(true_positives+false_negative)     #true positives / total actual positives

        print("from the estimated duplicates,we check for the duplicates through the jaccard.") 
        print("After checking,these are the results:")
        print("TP:" +" "+ str(true_positives))
        print("TN:" +" "+ str(true_negatives))
        print("FP:" +" "+ str(false_positive))
        print("FN:" +" "+ str(false_negative))
        print("accuracy:"+" "+ str( ((true_positives+true_negatives)/(true_positives+true_negatives+false_positive+false_negative))*100.0  )+ "%" )
        print("precision:" + " " + str(precision*100)+ "%")
        print("recall:" + " " + str(recall*100)+ "%")
        print("F1-score:" + " " + str( 2*(precision*recall)/(precision+recall)*100 )+ "%" )
         

if __name__ == "__main__":

    df = pd.read_csv("C:/Users/rikuh/Desktop/Data Mining/homeworks/DM_Homework_3_1912588_Matteo_Emanuele/amazon_results_polished.tsv", sep="\t")
    del df["Unnamed: 0"]
    corpus = df["description"].tolist()
    for i,element in enumerate(corpus):
        if len(element)<20: corpus.remove(element)  #rimuovo gli elementi che hanno una descrizione troppo breve. Sono elementi
                                                    #erroneamente ottenuti durante lo scraping nel secondo esercizio che vanno eliminati.


    #inizializzo le variabili chiave del problema. 
    #MODIFICARE QUESTE PER PARAMETRIZZARE L'INTERO ALGORITMO

    window = 10
    duplicate_threshold = 0.8
    load_signature_mat_from_csv = False
    b=4
    r=5
    # similarity threshold ≃ (1/b)^(1/r)
    n_trials = 20
    print_time_ex = True
    #b*r = n_trials!!

    listOfShingled_doc = []

    #creo per ogni documento nel corpus, lo shingle corrispondente e lo storo in una lista
    for doc in corpus:
        doc = doc.lower()
        shingling = Make_Shingling(doc,window,True)
        shingle = shingling.createShingleFromDoc()
        listOfShingled_doc.append(shingle)
        #listOfShingles has length l - k + 1 
    

    #creo la characteristic matrix dalla lista di shingles
    characteristic_matrix = createCharacteristicMatrix(listOfShingled_doc)
    print(characteristic_matrix)

    #inizializzo il builder per la signature matrix
    builder_signature_matrix = Make_Signature_Matrix(characteristic_matrix, n_trials, load_signature_mat_from_csv)  #with True I load the signature mat from the csv
    
    #computo la signature matrix
    signature_matrix = builder_signature_matrix.get_signature_matrix()

    #computo la real jaccard similarity matrix tramite i set di shingles
    if(print_time_ex): 
        start = time.time()
    real_jaccard_similarity_matrix = compute_real_jaccard_similarity_matrix(characteristic_matrix,listOfShingled_doc)
    

    real_duplicates = []
    for key in real_jaccard_similarity_matrix:
        if real_jaccard_similarity_matrix[key]>=duplicate_threshold : real_duplicates.append(key)
    print("number of duplicates found with the comparison of each set using the shingles:")
    print(len(real_duplicates))
    print("-----------------------------")
    if(print_time_ex):
        end = time.time()
        print("time required to compute the jaccard similarity between all the documents from the set:")
        print(end-start)


    #inizializzo la estimated jaccard similarity matrix. Ogni coppia di documenti avrà J=0,inizialmente
    estimated_jaccard_similarity_matrix = create_estimated_jaccard_similarity_matrix(signature_matrix)

    #inizializzo LSH
    Lsh = locality_Sensitive_Hashing(signature_matrix, b, r, duplicate_threshold)

    #trovo la lista di duplicati candidati tramite LSH
    if(print_time_ex): start = time.time()
    list_of_duplicate_candidates = Lsh.find_candidates_duplicates()
    list_of_refined_duplicate_candidates = Lsh.refine_duplicates(list_of_duplicate_candidates)
    if(print_time_ex): 
        end = time.time()
        print("time required to compute possible duplicates through LSH:")
        print(end-start)
    
    Lsh.compute_stats_and_print_blind_LSH(real_duplicates,list_of_refined_duplicate_candidates)


    #riempio la estimated jaccard similarity matrix creata precedentemente
    estimated_jaccard_similarity_matrix = Lsh.fill_estimated_jaccard_similarity_matrix(list_of_duplicate_candidates,estimated_jaccard_similarity_matrix)


    #piccola funzione di print di TP,TN,FP,FN e dell'accuracy
    print("-----------------------------")
    Lsh.compute_stats_and_print(estimated_jaccard_similarity_matrix,real_jaccard_similarity_matrix) 
    print("-----------------------------")



