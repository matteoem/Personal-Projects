import pandas as pd
import numpy as np
import operator as op

data = dict()

def ExtractReview(line):
    index = len(line) - 2
    while True:
        if line[index - 1].isnumeric() == False : break
        else: index-=1

    name = line[0 : index-1]
    score = int(line[index : len(line) - 1])

    return [name, score]

for line in open('beers.txt','r'):
    result = ExtractReview(line)

    name = result[0]
    score = result[1]
    count = 1

    if name in data: 
        score = data[name][0] + score
        count = data[name][1] + 1

    data[name] = [score, count, score/count]         #sostituisco l'elemento nel dizionario oppure lo aggiungo

significant_data = []
helper = []
j=0

for elem in data:                                 #controllo ogni elemento del dizionario
    if(data[elem][1]>=100):                       #se ho almeno 100 counts...
        helper.append(list(data.keys())[j])       #appendo il nome...
        helper.append(data[elem][2])              #appendo l'avg
        significant_data.append(helper)           #appendo l'elemento ad un array per creare una matrice
        helper = []                               #svuoto l'helper array
    j+=1

sorted_significant_data = sorted(significant_data, key=op.itemgetter(1), reverse=True)

df = pd.DataFrame(sorted_significant_data,columns=["beer_Name","avg_score"])
print(df.head(n=10))
print("finished!")
#print(len(significant_data))