# HackerNews
Client Application for [Hacker News API](https://hackernews.api-docs.io/)

## How to Run
- Install Dependencies from requirements.txt using the following command **python -m pip install -r requirements.txt**
- Run the application using application.py file
- To view api docs go to **./docs** endpoint
- Add your Aylien APP_ID and ACCESS_KEY in HackerNews.py for the Scheduled Job to fetch story sentiments


## Implementation

There are two parts of the implementation
1. Application to serve web pages and handle api calls
2. Scheduled job to update and store hacker news stories along with their sentiment in **stories.json**

This Way improve the load time and latency of searching hacker news story.<br>
Due to the nature of Hacker News API, we have to make one api call per story which is not scalable. So we separate out the job to download the stories and fetch their sentiment which runs in every 12 hour interval (so we don't run out of 1000/day free calls from [Aylien API](https://docs.aylien.com/textapi/endpoints/#api-endpoints))
