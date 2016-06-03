import datetime
import json
import random
import re
import sqlite3

import markovify
import tweepy

import config
import utils

class SimulatorText(markovify.Text):
    def sentence_split(self, text):
        return text.split('<...>')

def get_recent_tweets():
    pass

def generate_random_tweet():
    db_connection = sqlite3.connect(config.SQLITE_DB)
    db_cursor = db_connection.cursor()
    db_cursor.execute('SELECT * FROM tweets')

    dataset = ''

    for tweet in db_cursor.fetchall():
        dataset += tweet[1]
        dataset += '<...>' # delimiter
    #print(dataset)
    db_connection.close()

    model = SimulatorText(dataset, state_size=random.randrange(2,4))
    tweet = model.make_short_sentence(140, tries=100)
    tweet = re.sub(r'&amp;', '&', tweet)
    tweet = re.sub(r'&lt;', '<', tweet)
    tweet = re.sub(r'&gt;', '>', tweet)

    return tweet

def send_random_tweet():
    tweet = generate_random_tweet()
    with open(config.RECENT_DB) as f:
        recent = json.load(f)
    #if len(recent) > 30:
    #    recent.pop(0)
    while tweet in recent:
        tweet = generate_random_tweet()

    api = utils.get_api()
    try:
        api.update_status(status=tweet)
    except:
        pass

    recent.append(tweet)
    with open(config.RECENT_DB, 'w') as f:
        json.dump(recent, f)
    return tweet

if __name__ == '__main__':
    t = send_random_tweet()
    print(len(t), t)
    #print(get_recent_tweets())