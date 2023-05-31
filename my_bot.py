
# The purpose is simple: reply to a tweet whenever your account is mentioned 
# followed by a trigger phrase (in the TAG variable). In this case, I used 
# a fictional account that responds to mentions followed by the phrase 
# "data de hoje" with the corresponding day of the week, day of the month, month, and year.


import tweepy
import re
from datetime import datetime
import time


# All 4 variables below are generated and provided after the creation of the account and the App at https://developer.twitter.com/
CONSUMER_KEY = 'consumer_key_hash'
CONSUMER_SECRET = 'consumer_secret_hash'
ACCESS_KEY = 'access_key_hash'
ACCESS_SECRET = 'access_secret_hash'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit= True)

FILE_NAME = 'last_seen_id.txt'

TAG = "data de hoje"

#Dictionaries created for translation purposes
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

# Month Translation function
def month_in_pt(dictMonth, month_num):
    month_pt = dictMonth[month_num]
    return month_pt

# Weeks Translation function
def weekday_in_pt(dictWeekday, weekday_en):
    weekday_pt = dictWeekday[weekday_en]
    return weekday_pt

# Function to read the file "last_seen_id.txt" and ignore mentions that have already been replied to.
def read_last_seen(filename):
    f_read = open(filename, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

# function to upload the "last_seen_id.txt" file with the last seen mention Id
def store_last_seen(filename, last_seen_id):
    f_write = open(filename, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

# Main Function
def reply():
    mentions = api.mentions_timeline(read_last_seen(FILE_NAME), tweet_mode = 'extended') #Acessa o feed das menções feitas
    for mention in reversed(mentions): #Inverte a ordem da lista de menções para que publicações mais antigas sejam respondidas primeiro
        if "dia de hoje" in mention.full_text.lower(): #Se existe a frase-gatilho
            
            #Linhas 85 à 90 servem para a formatação do Reply
            now = datetime.now()
            day = now.strftime("%d")
            weekday = weekday_in_pt( weekdays ,now.strftime("%A"))
            month = month_in_pt(months, int(now.strftime("%m")))
            year = now.strftime("%Y")
            data_de_hoje = ("Hoje é "+ weekday +", "+ day + " de " + month +" de "+ year)

            print(str(mention.id) + ' - ' + mention.full_text) # Para fins de análise e verificação dos ID's
            api.update_status("@" + mention.user.screen_name +" "+data_de_hoje, mention.id) #cria o reply
            api.create_favorite(mention.id) #Favorita a menção feita
            api.retweet(mention.id) #Retweet na menção feita
            store_last_seen(FILE_NAME, mention.id) #Finalmente, salva o ID da ultima menção respondida, que será também ignorada

# Infinite Loop to Make a constant verification
while True:
    reply()
    time.sleep(2)

# After that the script was hosted to keep working

# For more information about the lib, please check: http://docs.tweepy.org/en/latest/
