The code will not be explained since every line was commented inside the .py file that was delivered.

A brief note on the explanation on how to run the code:

-change the path for the dataset from the starting one to the one where you placed the file ”amazon polished”.
-click run to execute the code, and read the print on the terminal.
-to play with the parameters, at the start of the ”main” are reported all the possible changeble parameters. Here are shown:  
![Alt text](https://i.gyazo.com/10a9808bdec82d3f8eb3928cc093bb5a.png)  

The variable window will change the size of the elements inside the shingles.
The duplicate threshold will change the value required to the jaccard similarity between two documents to be considered duplicates.
The variables b and r are the one mentioned in the theory, needed for the LSH implementation.
The variable called ”load signature mat from csv” is needed to avoid time computation. The min hashing procedure is the most expensive in terms of time,and in order to do different tests is it possible to store it into a csv file and read it .from there in order to avoid the computation everytime

The variable n trials is the number of hash functions used to build the signature matrix(= number of rows in the signature matrix).The higher the value,
the more time expensive will be the computation of the minhashing.Also, changing n trials will require you to change b and r accordingly. As taught during
the lecture, we recall that the higher is n, the more concentrated will be the
binomial distribution, thus the more precise will be the LSH.  

Another memorable fact is how the value of b and r were chosen. As said
in the homework, some tuning was required. The tuning I did was leaded by
the theory discussed in both class and in the book, which is telling us that if we
want to reach a certain duplicate threshold on the ”blind LSH application” we
need to tune b and r accordingly.
Firstly, b and r cannot be chosen arbitrarily but have to be in a relation between
them: their product has to be equal to the number of hash function used to
build the signature matrix.
Secondly, the duplicate threshold simulated with b and r is approximatively
equal to:  

![Alt text](https://i.gyazo.com/7d62c729ee8490b506492354275f2b0a.png)   

The value chosen for the work are b=4 and r=5, that generates a similarity
threshold of approximatively 0.757, close enough.  

Results are reported here:  

![Alt text](https://i.gyazo.com/0d6e0b1da3f315f135615a4d8c5141c9.png)   

