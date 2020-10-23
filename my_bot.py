import tweepy
import re
from datetime import datetime
import time

#Todas as 4 variáveis abaixo são geradas e fornecidas após a criação da conta e do App em developer.twitter.com
CONSUMER_KEY = 'consumer_key_hash'
CONSUMER_SECRET = 'consumer_secret_hash'
ACCESS_KEY = 'access_key_hash'
ACCESS_SECRET = 'access_secret_hash'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit= True)

FILE_NAME = 'last_seen_id.txt'

TAG = "#adatadehoje"

months = {
    1: 'janeiro',
    2: 'fevereiro',
    3: 'março',
    4: 'abril',
    5: 'maio',
    6: 'junho', 
    7: 'julho',
    8: 'agosto',
    9: 'setembro',
    10: 'outubro',
    11: 'novembro',
    12: 'dezembro',
}

weekdays = {
    'Monday':'segunda-feira',
    'Tuesday':'terça-feira',
    'Wednesday':'quarta-feira',
    'Thursday':'quinta-feira',
    'Friday':'sexta-feira',
    'Saturday':'sábado',
    'Sunday':'domingo'
}

def month_in_pt(dictMonth, month_num):
    month_pt = dictMonth[month_num]
    return month_pt

def weekday_in_pt(dictWeekday, weekday_en):
    weekday_pt = dictWeekday[weekday_en]
    return weekday_pt

def read_last_seen(filename):
    f_read = open(filename, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen(filename, last_seen_id):
    f_write = open(filename, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply():
    mentions = api.mentions_timeline(read_last_seen(FILE_NAME), tweet_mode = 'extended')
    for mention in reversed(mentions):
        if "dia de hoje" in mention.full_text.lower():
            now = datetime.now()
            day = now.strftime("%d")
            weekday = weekday_in_pt( weekdays ,now.strftime("%A"))
            month = month_in_pt(months, int(now.strftime("%m")))
            year = now.strftime("%Y")
            data_de_hoje = ("Hoje é "+ weekday +", "+ day + " de " + month +" de "+ year)

            print(str(mention.id) + ' - ' + mention.full_text)
            api.update_status("@" + mention.user.screen_name +" "+data_de_hoje, mention.id)
            api.create_favorite(mention.id)
            api.retweet(mention.id)
            store_last_seen(FILE_NAME, mention.id)

while True:
    reply()
    time.sleep(2)
