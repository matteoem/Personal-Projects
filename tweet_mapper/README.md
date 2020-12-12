# TWEET MAPPER USING TWEEPY AND GMAP
![Alt text](https://i.gyazo.com/d289e4e19bbff108dc0921a951492239.png)

Very simple implementation for an homework assigned in the course of Data Mining. In the following code we created,through the tweepy library, a tweet streamer to fetch tweets as they are created. Once they are fetched, we extract informations from them and we map those who have their coordinates available on a google map, opened as an html file.   
 
 # Requirements to run
You must insert your keys inside the python file in order to have access to both twitter and google map API.   
To obtain the authetication keys for twitter AP, [here is reported a step-by-step procedure on how to get them](https://github.com/user/repo/blob/branch/other_file.md) (Go look into the "Creating Twitter API Authentication Credentials"). For the google map API instead, [check this link](https://developers.google.com/maps/documentation/javascript/get-api-key?utm_source=google&utm_medium=cpc&utm_campaign=FY20-Q3-global-demandgen-displayonnetworkhouseads-cs-GMP_maps_contactsal_saf_v2&utm_content=text-ad-none-none-DEV_c-CRE_304552672714-ADGP_Hybrid%20%7C%20AW%20SEM%20%7C%20BKWS%20~%20Google%20Maps%20API-KWID_43700037633546773-kwd-382406281820-userloc_20596&utm_term=KW_%2Bgmap%20%2Bapi-ST_%2Bgmap%20%2Bapi&gclid=Cj0KCQiA8dH-BRD_ARIsAC24umYYDwR747tZTSs1gcopX0lorQxg8xpfqopYz405zDKd2DNzOCMwxJkaAk28EALw_wcB)!

 # General informations
 The positions and the coordinates needed to mark regions or positions on the map requires a specific format(longitude-latitude). [Here I report a very useful online tool I used to obtain the right coordinates.](http://bboxfinder.com/#-16.636192,-69.433594,-1.581830,-51.503906)(refer to the longitude-latitude format,beware!)  
   
 The code is structured to fetch tweets only inside a certain region. It is possible to change such region modifying the variable **tweet_extraction_box**.  
   
 Once have fetched tweets from that region, they will be stored into a json file. After having them saved, you can decide to read the tweets from the file directly modifying the variable **load**.   
   
 It is also possible to mark the user of the program changing the variables **my_pos_lat, my_pos_lon**.  
 
 # Final comments
I'm fully aware that this project is a very simple one, and no "rocket science is involved". Yet, the result is very cool, and also could be used as a first part for a sentiment analyzer using tweets, kind of an hot topic right now.  



For any comments, questions, or code usage, please contact me to matteoemanuele0@gmail.com   
linkedin profile: [Matteo Emanuele](linkedin.com/in/matteo-emanuele-688b121a3)


