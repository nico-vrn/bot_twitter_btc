import requests
import json
import tweepy
import time
from datetime import date
from tkinter import *
from tkinter.messagebox import *

consumer_key=''
consumer_secret=''
access_token=''
access_token_secret=''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
print("connecté a Twitter")

#api.update_status(status = 'coucou')

def recup_btc():
    global valeur_btc
    url="https://api.coindesk.com/v1/bpi/currentprice.json"
    content=requests.get(url)
    data=content.json()
    valeur_btc=data['bpi']['EUR']['rate_float']

'''with open('variable.json','r+') as f:
    data2=json.load(f)
    data2.update(fait2)
    f.seek(0)
    json.dump(data2,fichier)
    v=data2['fait']
    print(v)'''

quitter=False

def depart():
    global nombre_depart
    nombre_depart=input('entre le nombre:')
    if not nombre_depart.isdigit():
        print('il faut rentrer un nombre')
        depart()
    else:
        nombre_depart=float(nombre_depart)

today=date.today()
print(today)
declencheur=date(today.year,6,23)
print(declencheur)
depart()
fait=0

while quitter!=True:
    if fait!=1:
        recup_btc()
        nombre_btc=nombre_depart/valeur_btc
        cumul_nombre=nombre_btc*valeur_btc
        cumul_btc=nombre_btc
        fait=1
        fichier={'nombre_depart_depart':nombre_depart, 'valeur_btc':nombre_btc, 'fait':fait}
        with open('variable.json','w') as f:
            json.dump(fichier,f)
        '''tweet='BTC is worth: €{:0.3f}, in day of {}.\n {}€ will get you {:0.5f}btc.'.format(valeur_btc,today,nombre_depart,nombre_btc)
        api.update_status(status=tweet)'''
    else:
        if declencheur==today:
            print('on tweet')
            declencheur=declencheur.replace(month=today.month+1)
            print(declencheur)
            recup_btc()
            nombre_btc=nombre_depart/valeur_btc
            cumul_nombre+=nombre_btc*valeur_btc
            cumul_btc+=nombre_btc
            '''tweet='BTC is worth: €{:0.3f}, in day of {}.\n €{} will get you {:0.5f}btc. \n Which brings the total to \
{:0.5f}btc.\n Which is €{:0.2f}.'.format(valeur_btc,today,nombre_depart,nombre_btc,cumul_btc,cumul_nombre)
            api.update_status(status=tweet)'''
        else:
            temps_restant=abs(declencheur-today)
            print(temps_restant)
            break
