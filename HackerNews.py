import requests
from aylienapiclient import textapi
import time
from FileLogging import log

def getTopStoryIds(hn_url):
	endpoint = hn_url+"topstories.json"
	response = requests.request("GET", endpoint)
	id_list = response.text[1:-1].split(',')
	return id_list

def get_stories_with_sentiment_by_idlist(hn_url,id_list):
	endpoint = hn_url+"item/{item}.json"
	stories=[]
	for story_id in id_list:
		item = requests.request("GET", endpoint.format(item=story_id))
		item = item.json()
		
		# Coupling - Performance trade-off | Decoupling this will add one more loop for adding sentiment
		item['sentiment'] = getSentimentPolarity(item['title'])
		
		stories.append(item)
		log(len(stories)," stories downloaded")
		time.sleep(0.7) # To Avoid rate limit 60/minute from aylien api
	return stories

def getUser(hn_url,userid):
	endpoint = hn_url+"user/{userid}.json"
	response = requests.request("GET", endpoint.format(userid=userid))
	return response.json()

def getSentimentPolarity(text):
	c = textapi.Client("YOUR_APP_ID", "YOUR_ACCESS_KEY")
	try:
		s = c.Sentiment({'text': text})
	except Exception as ex:
		log("Exception in Aylien Api ",str(ex))
		return ""
	return s['polarity']	