import json
import pandas as pd
import matplotlib.pyplot as plt
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient
from pprint import pprint
from flask import Flask, jsonify
from flask import make_response
from flask import request

app = Flask(__name__)
 
access_token = "943540635277058048-kb88GYQ5aRKKJ6EBmwBvM1q6ZEAn8TC"
access_token_secret = "SykYf9TizBbTMl1nTVjiJE1ULPIfi3m5HS4U3gt2tEoCG"
consumer_key = "JEwy3iwGumWLPRmEKhCZo1gR4"
consumer_secret = "y4RlODi7Rw1KHitqDapb3bo1vY8SUYvwZHkoj85LYv6RAqJUPa"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
    
client = MongoClient()
db=client.sampledb

@app.route('/',methods=['GET'])
def hello():
	return jsonify({'hello':'world'})

@app.route('/triggertweets',methods=['POST'])
def triggertweets():
	#key = request.json['keyword']
	#max_tweets = request.json.get('max_tweets','20')
	#print(key)
	l = StdOutListener()
	stream = Stream(auth, l)
	stream.filter(track=['modi', 'AbkiBarModiSarkar', 'ModiForPM'],async=True)
	return jsonify({"trigger":"started"})

@app.route('/gettweets', methods=['POST'])
def getTweets():
	#key = request.json['keyword']
	s = []
	for tweet in db.mycollection.find():
		s.append(tweet['text'])
	return jsonify(s)

class StdOutListener(StreamListener):
    count=0
    
    def __init__(self):
		self.count = 0
        
    def on_data(self, data):
        #print data
        #file = open('testfile1', 'a')
        #file.write(data)
        #file.close()
        obj= json.loads(data)
        db.mycollection.insert_one(obj)
        print "sucess"
        self.count+=1
        if self.count == 20:
            #del self
            return False
        return True

    def on_error(self, status):
        print "failed"+status


if __name__ == '__main__':
    app.run(port=5000,use_reloader=True)
    
    
    