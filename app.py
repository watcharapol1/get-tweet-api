from flask import Flask
import pandas as pd
# import pyodbc 
import tweepy as tw
import json


#############################################################################################
################################  DB SETUP  #################################################

# server = '192.168.75.126' 
# database = 'DB_OpenData' 
# username = 'sa' 
# password = 'Bj4free' 
# conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
# cursor = conn.cursor()

#############################################################################################
################################  TWEEPY SETUP  #############################################

consumer_key = 'KNY4Zvfpg3ZJw9HEXgYZgpEsV'
consumer_secret = 'omlOAjdQViBKm1IKVWQfa0xuPakw6qs8G3YgnVM796KuaEabVz'
access_token = '60773330-kwmBd0SRPws1b0xl9EqF6hqOGuzXp0gxU9dX1HKZi'
access_token_secret = 'Lxl9jZJIcS2QresKsaRaSEcxcCly5JVuA6gVBtrveY9Eh'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth)

app = Flask(__name__)

def search_tweets(keyword):

    # Define the search term and the date_since date as variables
    search_words = keyword

    new_search = search_words + "-filter:retweets" # Do not get retweet of tweets
    
    #collect tweets
    tweets = tw.Cursor(api.search_tweets, q = new_search,  lang = 'th' ).items(10)
    
    users_locs = [[ tweet.created_at, tweet.text, tweet.user.followers_count,tweet.retweet_count, tweet.favorite_count] for tweet in tweets]
    
    # To dateframe
    tweet_df = pd.DataFrame(data=users_locs, columns=['time_stamp', 'text', 'followers_count', 'retweet_count','favorite_count'])

#   for index, row in tweet_df.iterrows():
        #     cursor.execute("INSERT INTO dbo.data_tweet (date_time,tweet_text,retweet) values(?,?,?)", row.time_stamp, row.text, row.retweet_count)
        #     conn.commit()

    # To Json  
    result = tweet_df['text'].to_json(orient="index")
    parsed = json.loads(result)

    return parsed


@app.route('/', methods=['GET'])
def home():
    return 'Hello World'

@app.route('/get-tweet/<string:keyword>', methods=['GET'])
def get_api(keyword):
    return search_tweets(keyword)

if __name__ == "__main__":
    app.run(debug=True)