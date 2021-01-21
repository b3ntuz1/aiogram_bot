import tweepy
import json
import os.path
from os import getenv


class Twitor:
    def __init__(self):
        self.twid = 0
        self.tw_url = "https://twitter.com/twitter/statuses/"
        # Auth
        auth = tweepy.OAuthHandler(getenv("TWITOR_API_KEY"), getenv("TWITOR_API_KEY_S"))
        auth.set_access_token(getenv("TWITOR_AT"), getenv("TWITOR_ATS"))

        self.api = tweepy.API(auth)

        try:
            self.api.verify_credentials()
            # print("Authentication OK")
        except:
            print("Error during authentication")

    def getTweets(self) -> list:
        tweets = []
        if os.path.exists("twid.txt"):
            with open("twid.txt", "r") as fh:
                self.twid = int(fh.readline())

        # get home timeline
        users = ["Pokémon GO", "Niantic", "PokeMiners"]
        tl = self.api.home_timeline() if self.twid == 0 else self.api.home_timeline(since_id=self.twid) 

        for tweet in tl:
            if self.twid < tweet.id:
                self.twid = tweet.id
            if (tweet.user.name in users):
                tweets.append(self.tw_url + tweet.id_str)

        # save max tweet id
        with open("twid.txt", "w") as fh:
            fh.write(str(self.twid))
        return tweets

if __name__ == "__main__":
    twitor = Twitor()
    print(twitor.getTweets())






# # Auth
# auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
# auth.set_access_token(access_token, access_token_secret)

# api = tweepy.API(auth)

# try:
#     api.verify_credentials()
#     print("Authentication OK")
# except:
#     print("Error during authentication")

# if os.path.exists("twid.txt"):
#     with open("twid.txt", "r") as fh:
#         twid = int(fh.readline())

# # get home timeline
# users = ["Pokémon GO", "Niantic Lab.", "PokeMiners", "Habr"]
# tl = api.home_timeline(since_id=twid) 

# for tweet in tl:

#     if twid < tweet.id:
#         twid = tweet.id

#     if (tweet.user.name in users):
#         url = tw_url + tweet.id_str
#         print(url)

# # save max tweet id
# with open("twid.txt", "w") as fh:
#     fh.write(str(twid))