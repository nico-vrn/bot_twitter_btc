import requests
import json
import tweepy
import time
from datetime import date
from tkinter import *
from tkinter.messagebox import *

Fenetre = Tk()

today=date.today()
print(today)
declencheur=date(today.year,6,23)
print(declencheur)

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

stop = True
antistart=0
def start():
    stop = False
    boutonStart.config(text = "Stop", fg = "red", command = stopBoucle)
    if antistart == 0:          #Lance la boucle la première fois
        bouclePrincipale()      #Les autres fois, change juste stop à False et aspect du bouton


def stopBoucle():
    stop = True
    boutonStart.config(text = "Start", fg = "chartreuse", command = start)

boutonStart = Button(Fenetre, text = "Start", fg = "chartreuse", command = start)
boutonStart.grid(row = 0, column = 0)

def bouclePrincipale():
    global antistart
    if antistart == 1 and stop == False:
        coucou=Label(Fenetre, text='coucou') #fonction qui fait le programme
        coucou.grid()
    else:
        hey=Label(Fenetre, text='hey')
        hey.grid()
    antistart = 1
    Fenetre.after(0, bouclePrincipale)

bouclePrincipale()
Fenetre.mainloop()
