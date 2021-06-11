import json
import os.path
from os import getenv

import tweepy

from setup_db import KVStorage


class Twitor:
    def __init__(self):
        self.twid = 0
        self.tw_url = "https://twitter.com/twitter/statuses/"
        # Auth
        auth = tweepy.OAuthHandler(
            getenv("TWITOR_API_KEY"), getenv("TWITOR_API_KEY_S"))
        auth.set_access_token(getenv("TWITOR_AT"), getenv("TWITOR_ATS"))

        self.api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

        try:
            self.api.verify_credentials()
            print("Authentication OK")
        except:
            print("Error during authentication")

        # get tweet id
        try:
            self.kvs = KVStorage.select().where(KVStorage.key == "twitor").get()
        except KVStorage.DoesNotExist:
            self.kvs = KVStorage(key="twitor", value="0")
        self.twid = int(self.kvs.value)

    def save_twid(self, twid):
        # save latests tweet id
        self.kvs.value = str(self.twid)
        self.kvs.save()

    # REFACTOR:
    # - схлопнути шматок try;except та оновлення twid (передостанні рядки) до окремого методу
    # - повертати масив словарів у форматі {text: текст відформатований у markdown, img: url до картинки}
    # - формат одного твіту:
    #   : [userName](link_to_tweet) tweeted:
    #   : text or/and image
    #   : \n

    def getTweets(self) -> list:
        tweets = []

        # get home timeline
        users = {
            "PokemonGoApp": "public", "NianticLabs": "private", "pvpoke": "private",
            "PokemonGOHubNet": "private", "captgoldfish": "private", "poke_miners": "private",
            "NianticHelp": "private", "LeekDuck": "private"
        }
        tl = self.api.home_timeline() if self.twid == 0 else self.api.home_timeline(
            since_id=self.twid)

        for tweet in tl:
            # check tweet id and update if needed
            if self.twid < tweet["id"]:
                self.twid = tweet["id"]

            # перевірити у списку користувачів
            user = tweet["user"]["screen_name"]
            if user in users.keys():
                if "retweeted_status" not in tweet.keys():
                    post_status = users[user]
                    urlToTweet = str(self.tw_url + tweet["id_str"])
                    text = f'[{tweet["user"]["name"]}]({urlToTweet}) tweeted:\n'
                    text += tweet.get('text') + "\n"
                    tweets.append([text, post_status, user])
        self.save_twid(self.twid)
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
