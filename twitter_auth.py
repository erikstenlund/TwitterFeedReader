import http.client
from rauth import OAuth1Service
from secret import key, secret
class TwitterObj():
    def __init__(self):
        self.twitter_auth = OAuth1Service(
            name='PythonFeedReader',
            consumer_key=key,
            consumer_secret=secret,
            request_token_url='https://api.twitter.com/oauth/request_token',
            access_token_url='https://api.twitter.com/oauth/access_token',
            authorize_url='https://api.twitter.com/oauth/authorize',
            base_url='https://api.twitter.com/1.1/'
        )

    def get_auth_url(self):
        self.req_token, self.req_token_secret = self.twitter_auth.get_request_token()
        return self.twitter_auth.get_authorize_url(self.req_token)

    def get_tweets(self,pin):
        session = self.twitter_auth.get_auth_session(self.req_token, self.req_token_secret, 
                    method='POST', data={ 'oauth_verifier':pin })

        rawTweets = session.get('statuses/home_timeline.json', 
                    params={'count':100}).json()
        tweets = list()
        profilePictures = dict()
        for rawTweet in rawTweets:
            tweet = dict()
            tweet["name"] = rawTweet["user"]["name"]
            tweet["text"] = rawTweet["text"]
            if tweet["name"] in profilePictures:
                tweet["imgFilePath"] = profilePictures["name"]
            else:
                profilePictureUrl = rawTweet["user"]["profile_image_url"]
                domain = profilePictureUrl.split("/", 3)[2]
                route = "/" + profilePictureUrl.split("/", 3)[3]
                conn = http.client.HTTPConnection(domain)
                conn.request("GET", route)
                rawImg = conn.getresponse()
                imgFilePath = "images/" + tweet["name"] + "_profile.jpg"
                profilePictures["name"] = imgFilePath
                with open(imgFilePath, "wb") as imgFile:
                    imgFile.write(rawImg.read())

                tweet["imgFilePath"] = imgFilePath
            tweets.append(tweet)
        return tweets

        
