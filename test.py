# bot.py
import os
from discord.ext import commands
import discord
from dotenv import load_dotenv
from datetime import datetime
import random 
import time
import asyncio
import pyrebase
from collections import OrderedDict 

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = commands.Bot(command_prefix = '.')

config = {
  "apiKey": "AIzaSyAvsq_dvQJqIE22qIlHbrqQ96KHgVS63aY",
  "authDomain": "dailygoals-b747f.firebaseapp.com",
  "databaseURL": "https://dailygoals-b747f-default-rtdb.firebaseio.com",
  "storageBucket": "dailygoals-b747f"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

user_id="321062066544705547"

#display method tests
#user=db.child(user_id).get()
#entries=user.val()
#print(entries)

#entries=db.child(user_id).get().val()
#for entry in entries:
#    if (entry != "Count") and (entry != "Points"):
#       OrderedDict=db.child(user_id).child(entry).get().val()
#       print(entry+": "+OrderedDict[entry])

#leaderboard method tests
#clan=db.get().val()
#print(clan)

#print(ctx.get_user(user_id))

OrderedDict=db.child(user_id).child("Points").get().val()
print(OrderedDict)
points = OrderedDict["Points"]
print(points)
db.child(user_id).child("Points").set({"Points" : int(points) + 1})

client.run(TOKEN)