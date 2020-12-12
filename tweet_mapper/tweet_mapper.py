from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pandas as pd
import gmplot
import re
import math

APP_KEY = 'VUT9Jv4qHSUiT8yHbVB2YYPq9'
APP_SECRET = 'Q7trUFUJFyys8mHsM3OTPsazTXU2mGUNPYnsqFSJVdhwLlBLJ4'
ACC_TOKEN = '3329067400-jjRzSOAi5EHBRHlXzlVHAwspupR5ehXdTpG6jKq'
ACC_TOKEN_SECRET = 'qhsoFBeVTUIx2Q9eXJ75Sp77XWhWAcEHvvggAdXqcJxa2'
apikey = 'AIzaSyBceQIdyyKtoBJhUpbMeUGmUT15ARyqvy4'


# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        pass

    def stream_tweets(self, fetched_tweets_filename, positions,load):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = StdOutListener(fetched_tweets_filename)
        auth = OAuthHandler(APP_KEY, APP_SECRET)
        auth.set_access_token(ACC_TOKEN, ACC_TOKEN_SECRET)

        if(load == False):
            stream = Stream(auth, listener)
            # This line filter Twitter Streams to capture data by the keywords: 
            stream.filter(locations=positions)
            return stream
        if(load == True):
            tweets = []
            for line in open('tweets.json'):
                try:
                    tweets.append(json.loads(line))
                except:
                    continue
            return tweets

def polishing_important_tweets_into_df(tweets):
    tweet_polished = dict()
    list_tweet_polished = []
    for tweet in tweets:
        if(tweet['coordinates'] is not None):
            tweet_polished['screen_name'] = tweet['user']['screen_name']
            tweet_polished['text'] = tweet['text']
            tweet_polished['coord'] = tweet['coordinates']['coordinates']
            list_tweet_polished.append(tweet_polished.copy())
    df = pd.DataFrame(list_tweet_polished)
    return df


class StdOutListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:

            js_dict = json.loads(data)
            if(js_dict["coordinates"] is not None):
                print("new tweet saved!")
                with open(self.fetched_tweets_filename, 'a') as tf:
                    tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
    

    def on_error(self, status):
        print(status)
        if status == 420: 
            return False
        pass
    
    # mark yourself with a red marker on the map
    my_pos_lat = 42.075578
    my_pos_lon = 12.289143

    # choose the vertices of a square for a bounding box
    # to highlight on the map.
    Rome_bounding_box_vertex1 = (41.3994, 12.140)
    Rome_bounding_box_vertex2 = (41.3994, 13.0334)
    Rome_bounding_box_vertex3 = (42.1546, 13.0334)
    Rome_bounding_box_vertex4 = (42.1546,12.140)

if __name__ == '__main__':
    fetched_tweets_filename = "tweets.json"
    twitter_streamer = TwitterStreamer()

    #bounding box around Rome. Pure flavour. U can change it
    tweets = twitter_streamer.stream_tweets(fetched_tweets_filename, [12.142,41.3994,13.0334,42.1546],load=True) 

    # after fetching the tweets, preprocess them and store them into a pandas df  
    df = polishing_important_tweets_into_df(tweets)

    # initialize the map with the center of where will display in the world
    gmap = gmplot.GoogleMapPlotter(41.9109, 12.4818, 14, apikey=apikey)


    #I extract in arrays the informations I need to place in the gmap from the df
    
    for index, row in df.iterrows():
        coord = row['coord']
        text = row['text']
        screename = row['screen_name']

        str_clean = text.encode('ascii', 'ignore').decode('unicode-escape')  #remove special characters
        str_clean = str_clean.replace("\n", " ").replace("\"", "'")                        #remove \n and replace "" with ''
        gmap.marker(coord[1], coord[0], color='cornflowerblue',title= "@"+ screename + " : " + str_clean) #each position fetched from the tweet stream

    gmap.marker(my_pos_lat,my_pos_lon, title = "I'm here")   # my position
    
        
    # Highlight some attractions:
    attractions_lats, attractions_lngs = zip(*[
        (41.3994, 12.142),
        (41.3994, 13.0334),
        (42.1546, 12.142),
        (42.1546,13.0334),  
    ])

    gmap.scatter(attractions_lats, attractions_lngs, color='#3B0B39', size=40, marker=False)

    # Draw the bounding box. For the sake of the exercise, I choose it to place it around Rome.
    Rome_bounding_box = zip(*[
        Rome_bounding_box_vertex1,
        Rome_bounding_box_vertex2,
        Rome_bounding_box_vertex3,
        Rome_bounding_box_vertex4,
    ])

    gmap.polygon(*Rome_bounding_box, color='cornflowerblue', edge_width=5)

    # Draw the map to an HTML file:
    gmap.draw('map.html')



