import json
from FileLogging import log
import datetime as dt

def readStories(filename):
	try:		
		with open(filename, 'r') as f:
			stories = json.loads(f.read())
	except Exception as ex:
		return str(ex)
	
	return stories

def saveStories(stories,filename):
	sort_by_score = sorted(stories, key=lambda i: i['score'],reverse=True)
	log("saving stories started")
	today = dt.datetime.today()
	stories[0]['FileDate'] = today.strftime('%d %b %Y')
	try:
		with open(filename, 'w') as f:
			json.dump(sort_by_score, f)
	except Exception as ex:
		log("Exception: ",str(ex))
		return False
	return True