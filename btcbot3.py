import requests
import json
import tweepy
import time
from datetime import date
from tkinter import *
from tkinter.messagebox import *

fenetre = Tk()

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

def lire(donnes):
    with open('variable.json','r+') as f:
        data2=json.load(f)
        v=data2[donnes]
        print(v)

'''fichier={'nombre_depart_depart':nombre_depart, 'valeur_btc':nombre_btc, 'fait':fait}
    with open('variable.json','w') as f:
    json.dump(fichier,f)'''

def tweet1():
    global champ_tweet1
    global tweeter
    global c_fait
    champ_tweet1.destroy()
    tweeter.destroy()
    c_fait.destroy()

quitter=False
def demarrage_boucle():
    global nombre_depart
    global declencheur
    global nombre_depart1
    global champ_tweet1
    global tweeter
    global c_fait
    global nombredepart
    global recommencerbt
    global champ_temps
    global textebt
    global message
    nombre_depart=nombre_depart1.get()
    if not nombre_depart.isdigit():
        print('il faut rentrer un nombre')
        depart()
    else:
        nombre_depart=float(nombre_depart)
    print(nombre_depart)
    fait=0
    nombre_depart1.destroy()
    nombredepart.destroy()
    recommencerbt=Button(fenetre, text='recommencer', command=lambda:recommencer())
    recommencerbt.grid(row=5)
    message='BTC is worth: €{:0.3f}, in day of {}.\n €{} will get you {:0.5f}btc. \n Which brings the total to \
{:0.5f}btc.\n Which is €{:0.2f}.'
    while quitter!=True:
        if fait!=1:
            recup_btc()
            nombre_btc=nombre_depart/valeur_btc
            cumul_nombre=nombre_btc*valeur_btc
            cumul_btc=nombre_btc
            fait=1
            tweet='BTC is worth: €{:0.3f}, in day of {}.\n {}€ will get you {:0.5f}btc.'.format(valeur_btc,today,nombre_depart,nombre_btc)
            champ_tweet1=Label(fenetre, text='le tweet est: {}'.format(tweet))
            champ_tweet1.grid(row=1)
            tweeter=Button(fenetre,text='OK', command=lambda:tweet1())
            tweeter.grid(row=3)
            api.update_status(status=tweet)
            c_fait=Label(fenetre, text='bien tweeter')
            c_fait.grid(row=2)
        else:
            if declencheur==today:
                print('on tweet')
                declencheur=declencheur.replace(month=today.month+1)
                print(declencheur)
                recup_btc()
                nombre_btc=nombre_depart/valeur_btc
                cumul_nombre+=nombre_btc*valeur_btc
                cumul_btc+=nombre_btc
                tweet=message.format(valeur_btc,today,nombre_depart,nombre_btc,cumul_btc,cumul_nombre)
                champ_tweet1=Label(fenetre, text=tweet)
                champ_tweet1.grid(row=1)
                tweeter=Button(fenetre,text='ok', command=lambda:tweet1())
                tweeter.grid(row=3)
                api.update_status(status=tweet)
                c_fait=Label(fenetre, text='bien tweeter')
                c_fait.grid(row=2)
            else:
                temps_restant=abs(declencheur-today)
                champ_temps=Label(fenetre,text='il reste:{} avant prochain tweet'.format(temps_restant))
                champ_temps.grid(row=4)
            fenetre.update()


def depart():
    global nombre_depart1
    global nombredepart
    variable=DoubleVar()
    nombre_depart1=Entry(fenetre, textvariable=variable, width=30)
    nombre_depart1.grid(row=1)
    nombredepart=Button(fenetre, text='execut', command=lambda:demarrage_boucle())
    nombredepart.grid(row=2)

def recommencer():
    global recommencerbt
    global champ_temps
    tweet1()
    champ_temps.destroy()
    recommencerbt.destroy()
    fait=0
    depart()


depart()



fenetre.mainloop()
