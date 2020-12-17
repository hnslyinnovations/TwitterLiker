# TwitterLiker
Goes through and likes tweets from specific hashtags. 
If 429 response is made, waits 15 minutes and retries. 
If 429 reponse happens 3x in a row, sleeps for 24 hours.

This was made in Python 3.9
User will need to install tweepy to use script
pip install tweepy
