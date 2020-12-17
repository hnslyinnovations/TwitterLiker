import tweepy
import datetime
import time,sys

listOfHashTags = ["#Addlistofhashtags"]
testList = ["#test"]
global tweetFavCount
global counter

def apiConfig():
    #Twitter keys used to access the twitter api. twiter used oauth authentication
    CONSUMER_KEY = "Add twitter api"
    CONSUMER_SECRET = ""
    ACCESS_KEY = "Add bearer key"
    ACCESS_SECRET = ""
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
    
    try:
        api.verify_credentials()
        print("Authentication OK")
        return api
    except:
        print("Error during authentication")

def processFavorites(api):
    tweetFavCount = 0
    counter = 0
    results = True
    #while(results):
    for tags in listOfHashTags:
        searchTweetList = findTweets(tags,api)
        print (tags)
        for search in searchTweetList:
            results,counter = favoriteTweets(search,api,tweetFavCount, counter)
            tweetFavCount = results
            counter = counter

def findTweets(searchTags,api):
    query = searchTags
    tweetLimit  = 50
    fromDate = datetime.datetime.now() - datetime.timedelta(days=30)
    searchedTweets = tweepy.Cursor(api.search,q=query,lang="en",sincedate=fromDate,result_type='mixed').items(tweetLimit)
    #print(searchedTweets)
    searchedTweetsList = [tweet for tweet in searchedTweets]
    return searchedTweetsList

def favoriteTweets(searchTweet,api,tweetFavCount,counter):
    statusFav = searchTweet.favorited
    print("Is tweet favorited: " + str(statusFav), end="\n")
    if counter == 3:
        print("Sleeping 24 hrs")
        time.sleep(60 * 1440)
        counter = 0
    if statusFav == False:
        try:
            searchTweet.favorite()
            tweetFavCount = tweetFavCount + 1
            print(searchTweet.text)
            print("Favorited count = " + str(tweetFavCount), end="\n")
        except Exception as ex:
            if str(ex) == """[{'code': 139, 'message': 'You have already favorited this status.'}]""":
                print("Already Favorited.. Continuing..", end="\n")
            if str(ex) == "Twitter error response: status code = 429":
                print("Sleeping...", end="\n")
                waitTime = (15)
                counter = counter + 1
                for remaining in range(waitTime, 0, -1):
                    sys.stdout.write("\r")
                    sys.stdout.write("{:2F} minutes remaining.".format((remaining*60/60)))
                    sys.stdout.flush()
                    time.sleep(60)
                    sys.stdout.write("\rComplete!            \n")
            else:
                print(ex)
    if statusFav == True:
        print("Already Favorited.. Continuing..", end="\n")
    return tweetFavCount,counter

if __name__ == '__main__':
    api = apiConfig()
    processFavorites(api)
