# DISASTER DETECTION USING TWEET TEXTS WITH LSTM & BERT
![Alt text](https://static.ffx.io/images/$width_768%2C$height_432/t_crop_fill/q_86%2Cf_auto/be24cc4d8bb7910cd0d03e4386339e46d167b0b5)
 # Introduction
 This exercise was a task I was asked to complete in my Data Mining course, as a small homework. The implementation is a bit rusty, since I preferred to have it a little bit more clear and explicit with a lot of comments.
 Consider that half the notebook is in my motherlanguage(italian), since no constraint was put on the language. I was too bored to translate all the comments, but I think the code is self explanatory! :)
 I report here the homework's instruction given:
 ![Alt text](https://i.gyazo.com/60b3aa3dae1ae3e919b4c6a0ef53a418.png)
 
 # Dataset 
 You can find the dataset on the kaggle site on this link: [Disaster detection dataset](https://www.kaggle.com/vstepanenko/disaster-tweets)!
 
 # Bert implementation 
 The link used to implement BERT is the following:  [BERT implementation]( https://github.com/nlptown/nlp-notebooks/blob/master/Text%20classification%20with%20BERT%20in%20PyTorch.ipynb).  
 As you can imagine, I had to work onto the implementation in order to make it work on this dataset, but fear not,my friend! Everything is in the python notebook I uploded ;)
 
 # General notes
 I suggest to run the code on Colab, since it is implemented to work on it. The only issue is that, working on colab, you will have to load the dataset on your Google Drive.
 
 # Final Performances with my LSTM model:
 ![Alt text](https://i.gyazo.com/3c5c9ea85bd1394fc695213c667cdc3f.png)
 
  # Final Performances with my BERT:
   ![Alt text](https://i.gyazo.com/30aa213b0842e561bf75f788f91fa2dd.png)
   ![Alt text](https://i.gyazo.com/9a793961af97d4ab2115e30ae496fb7f.png)

# Conclusions
No wonder BERT performed better. Transformers are currently taking over the NLP field since they appear to be extremely powerful and better performative than recurrent neural network.  
Yet, the difference in the performance was very little and I consider myself satisfied, having been able to build a model that could hold his own against BERT, the state-of-the-art solution for this kind of tasks.
