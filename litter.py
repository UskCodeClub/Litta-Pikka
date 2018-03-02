# User Interface
from guizero import *
from datetime import datetime
import RPi.GPIO as GPIO
import time
import sys
from hx711 import HX711

def cleanAndExit():
    print ("Cleaning...")
    GPIO.cleanup()
    print ("Bye!")
    sys.exit()

hx = HX711(9, 10)

#hx.set_reference_unit(380)

hx.reset()
hx.tare()


def litter_collected():
    for i in range(5):
        try:
            val = max(0, int(hx.get_weight(5)))
            print (val)
            hx.power_down()
            hx.power_up()
            time.sleep(2)
            
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()


#Database
import sqlite3
dbfile = sqlite3.connect('litter.db')
db = dbfile.cursor()
db.execute('''CREATE TABLE IF NOT EXISTS litter (date text, house text, weight real)''')

# Twitter
#App keys need to be added for Twitter to function
from twython import Twython
app_key = "xxxxxxxxxxKyZaJ4jWaFQw9vW"
app_secret = "xxxxxxxxxxgsOS9vQKd7yK2AZNO9o2wJHVKNfsWhSw8nEAX8Az"
oauth_token = "xxxxxxxxxx84710400-hD2xP20nilT2oFDU00oieLfrNU7mZ2J"
oauth_token_secret = "xxxxxxxxxxTQfniyuIpG1qmO6hQ8MQZgPyVIFf65xmaES"
twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)

thetime = datetime.now().strftime('%-I:%M%P on %d-%m-%Y')
val = max(0, int(hx.get_weight(5)))

# Global Variables
house = ''
weight = str(val)

def enter_litter():
    global house
    global weight
    
    if weight == '':
       print ("You haven't added a weight")
    if house == '':
       print ("You haven't tapped a house icon")
    else :
       print ("Well done " +house)
       twitter.update_status(status=house +" have added more litter. That's 5 Dojos for " + house + " " + thetime)
       print ("Adding "+weight + "g of litter to " +house)
       q = "INSERT INTO litter (date, weight, house) VALUES (date('now'),'"
       q += weight
       q += "', '"
       q += house
       q += "')"
       db.execute(q)
       dbfile.commit()
       cleanAndExit()
        

# Button Commands

def add_wentwood():
        global house
        house = 'Wentwood'

def add_snowdon():
        global house
        house = 'Snowdon'

def add_elan():
        global house
        house = 'Elan'

def add_gower():
        global house
        house = 'Gower'

#Build User Interface
app = App(title="LittaPikka", height=600, width=800)
t01 = Text(app, text="Please select a house icon, then enter the weight of litter", font="20", grid=[0,5,5,1])
box = Box(app, layout="grid")

t02 = Text(box, text="Wentwood Wolves", font="20", grid=[1,1])
t03 = Text(box, text="Snowdon Eagles", font="20", grid=[4,1])

b1 = PushButton (box, command=add_wentwood, icon="Wentwood.gif", grid=[1,2])
b2 = PushButton (box, command=add_snowdon, icon="Snowdon.gif", grid=[4,2])
b3 = PushButton (box, command=add_elan, icon="Elan.gif", grid=[1,3])
b4 = PushButton (box, command=add_gower, icon="Gower.gif", grid=[4,3])

t05 = Text(box, text="Elan Kites", font="20", grid=[1,4])
t06 = Text(box, text="Gower Dragons", font="20", grid=[4,4])
t07 = Text(app, text="Enter weight of litter in grams", grid=[5,1,5,1])

button = PushButton(app, litter_collected, text="Press to activate scale")
button = PushButton(app, enter_litter, text="Enter litter")

app.display()

