import json
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
        except Exception as e:
            print("Error during authentication")
            print(e)

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

    def purifyMarkdown(self, text):
        symbols = r"()'*_.+-#{}[]\!"
        for s in symbols:
            if s in text:
                text = text.replace(s, f"\\{s}")
        return text

    def getTweets(self) -> list:
        tweets = []

        # get home timeline
        users = {
            "PokemonGoApp": "public",
            "NianticLabs": "private",
            "pvpoke": "private",
            "PokemonGOHubNet": "private",
            "captgoldfish": "private",
            "poke_miners": "private",
            "NianticHelp": "private",
            "LeekDuck": "private"
        }

        if self.twid == 0:
            tl = self.api.home_timeline(tweet_mode="extended")
        else:
            tl = self.api.home_timeline(since_id=self.twid, tweet_mode="extended")

        # for debuging purpose
        with open(f"tweets_{int(datetime.now().timestamp())}.json", "w") as fh:
            fh.write(json.dumps(tl))
        ###

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
                    text = f'{tweet["user"]["name"]} tweeted:\n'
                    text += f"{tweet.get('full_text')}\n{urlToTweet}\n"
                    tweets.append([text, post_status, user])
        self.save_twid(self.twid)
        return tweets


if __name__ == "__main__":
    from datetime import datetime
    twitor = Twitor()
    tw = twitor.getTweets()

    for t in tw:
        print(t)
