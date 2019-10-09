from flask import Flask, render_template, url_for, send_from_directory
from flask_restplus import Api, Resource
from apscheduler.scheduler import Scheduler
import os
from FileLogging import log
import HackerNews as HN
import Helpers as HL

app = Flask(__name__)

story_download_interval_in_hours = 12
story_file_name = "stories.json"
application_logs_file = "ApplicationLogs.log"
favico_icon_path = 'icons/favicon.ico'
hn_url = "https://hacker-news.firebaseio.com/v0/"

@app.route("/")
def index():
	"""
	Renders a list of top stories
	"""
	return render_template("index.html")

@app.route("/user/<string:userid>")
def user(userid):
	"""
	Renders a list of top stories
	"""
	return render_template("user.html",userid=userid)

@app.route('/favicon.ico')
def favicon():
	"""
	Serves the favicon icon
	"""
	return send_from_directory(os.path.join(app.root_path, 'static'), favico_icon_path, mimetype='image/vnd.microsoft.icon')

# Because of an open issue https://github.com/noirbizarre/flask-restplus/issues/247
# I'm initialising the API after registering app.route, we can also make use of blueprints to put the apis in a separate module

api = Api(app=app, doc='/docs', title="Custom Hacker News API", description="Fetches stories and users from hacker news api")
stories = api.namespace('stories', description='Stories from HackerNews')
userdata = api.namespace('userdata', description='Users from HackerNews')

@stories.route("/top")
class TopStories(Resource):
	def get(self):
		"""
        returns a list of top stories
        """
		stories = HL.readStories(story_file_name)
		return stories

@userdata.route("/<string:userid>")
class Profile(Resource):
	def get(self,userid):
		"""
        returns the user profile by userid
        """
		user = HN.getUser(hn_url, userid)
		return user

logs = api.namespace('logs', description='Application Logs')
@logs.route("/")
class Log(Resource):
	def get(self):
		"""
		Returns application logs
		"""
		return send_from_directory(app.root_path, application_logs_file, mimetype='text')


# Schedule Job to download and update top stories from hackernews along with the sentiment from aylien
cron = Scheduler(daemon=True)
cron.start() # Explicitly kick off the background thread for downloading stories from HN

@cron.interval_schedule(hours=story_download_interval_in_hours)
def download_top_stories():
	log("downloading ids")
	story_ids = HN.getTopStoryIds(hn_url)
	try:
		log("downloading stories")
		stories = HN.get_stories_with_sentiment_by_idlist(hn_url,story_ids)
	except Exception as ex:
		log("Exception while downloading stories: ",str(ex))
		return False
	
	log("Download finished")
	response = HL.saveStories(stories,story_file_name)
	
	if(response):
		log("Stories Saved")
		return True
	else:
		log("Failed: Saving Stories")
		return False

if __name__ == '__main__':
	app.run(host='0.0.0.0',port='80',use_reloader=False,debug=False)