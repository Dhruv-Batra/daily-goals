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


@client.event
async def on_ready():
    print('Bot is ready.')

@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)}ms')#sends ping

responses = ['\"You only live once, but if you do it right, once is enough.\" -- Mae West',
                 '\"Opportunities don\'t happen. You create them.\" -- Chris Grosser',
                 '\"Try not to become a person of success, but rather try to become a person of value.\" -- Albert Einstein',
                 '\"If you can\'t explain it simply, you don\'t understand it well enough.\"-- Albert Einstein',
                 '\"You can\'t please everyone, and you can\'t make everyone like you.\" -- Katie Couric',
                  '\"Keep your face to the sunshine and you can never see the shadow.\" -- Helen Keller'
                 ]


@client.command(aliases = ['encourage'])
async def motivate(ctx):#sends out responses with motivational quotes
    responses = ['\"I avoid looking forward or backward, and try to keep looking upward.\"-- Charlotte Bronte',
                 '\"Everything you can imagine is real.\" -- Pablo Picasso',
                 '\"Try not to become a person of success, but rather try to become a person of value.\" -- Albert Einstein ',
                 '\"If you can\'t explain it simply, you don\'t understand it well enough.\"-- Albert Einstein',
                 '\"You can\'t please everyone, and you can\'t make everyone like you.\" -- Katie Couric',
                  '\"Keep your face to the sunshine and you can never see the shadow.\" -- Helen Keller'
                 ]
    await ctx.send(random.choice(responses))#sends encouragement



@client.command(aliases = ['create', 'add']) #put "" around task to have spaces
async def createtask(ctx, task):#creates a new task and adds to to do list and sends todolist
    user_id=ctx.message.author.id
    user=db.child(user_id).get()
    dic=user.val()
    try:
        OrderedDict=db.child(user_id).child("Count").get().val()
        count = OrderedDict["Count"]
        data={("Task "+str(count+1)):task}
        title="Task "+str(count+1)
        db.child(user_id).child("Count").set({"Count" : int(count) + 1})
    except:
        data={"Task 1": task}
        points={"Points": 0}
        count={"Count": 1}
        title = "Task 1"
        db.child(str(user_id)).child("Points").set(points)
        db.child(str(user_id)).child("Count").set(count)
    db.child(str(user_id)).child(title).set(data)
    await ctx.send('Task created. Good luck~~ ')
    await ctx.send('https://images.theconversation.com/files/302306/original/file-20191118-169393-r78x4o.jpg?ixlib=rb-1.1.0&q=45&auto=format&w=1200&h=675.0&fit=crop')


@client.command(aliases = ['tasks', 'show'])
async def display(ctx): #displays tasks
    user_id=ctx.message.author.id
    entries=db.child(user_id).get().val()
    OrderedDict=db.child(user_id).child("Count").get().val()
    count = OrderedDict["Count"]
    try:
        await ctx.send('Outstanding Tasks:')
        for entry in entries:
            if (entry != "Count") and (entry != "Points"):
                OrderedDict=db.child(user_id).child(entry).get().val()
                await ctx.send(entry+": "+OrderedDict[entry])
    except:
        await ctx.send('No Outstanding Tasks')

    #await ctx.send(json.dumps(user.val(), indent=4))

@client.command(aliases = ['fin', 'finish'])
async def finished(ctx, task): #Removes finished task (#) from list
    user_id=ctx.message.author.id
    OrderedDict=db.child(user_id).child("Points").get().val()
    points = OrderedDict["Points"]
    try:
        db.child(user_id).child("Task " + str(task)).remove()
        await ctx.send('https://cdn.discordapp.com/attachments/762018357774909465/792624068095901707/unknown.png')
        await ctx.send('Yay! Congratulations! Now on to the next task!')
        db.child(user_id).child("Points").set({"Points" : int(points) + 1})
        OrderedDict=db.child(user_id).child("Points").get().val()
        points = OrderedDict["Points"]
        await ctx.send("You have "+str(points)+" points")
        await ctx.send('Task ' + task + ' completed.')
    except:
        await ctx.send("Task not found. Please make sure you are using a numerical value")
    

 
@client.command(aliases = ['lead', 'all'])
async def leaderboard(ctx): #displays leaderboard with people with most points on top and people with least on bottom
    user_id=ctx.message.author.id
    #await ctx.send(name+"san")
    await ctx.send('Here are the standings so far:')
    clan=db.shallow().get().val()
    
    #for usernum in clan:
        #points = db.child(usernum).child("Points").get().val()
        
    #await ctx.send(ctx.get_all_members())
    for usernum in clan:
       a = db.child(usernum).child("Points").get().val()
       b = str(ctx.bot.get_user(int(usernum)))
       points = a["Points"]
       if b == "None": b = "Someone in your server owo"
       await ctx.send( str(b) + ": " + str(points) + " Points")
    await ctx.send('Keep it up!')
    await ctx.send('https://api.duniagames.co.id/api/content/upload/file/8934703071608706089.jpg')

@client.command(aliases = ['total', 'points'])
async def balance(ctx):
    user_id=ctx.message.author.id
    OrderedDict=db.child(user_id).child("Points").get().val()
    points = OrderedDict["Points"]
    await ctx.send("You have "+str(points)+" points")
    await ctx.send('https://i.imgur.com/Oqli8Hc.jpg')

@client.command(pass_context=True)
@commands.cooldown(1, 60*60*12, commands.BucketType.user)
async def daily(ctx):
    user_id=ctx.message.author.id
    OrderedDict=db.child(user_id).child("Points").get().val()
    points = OrderedDict["Points"]
    db.child(user_id).child("Points").set({"Points" : int(points) + 3})
    await ctx.send('Here is a gift from me: +3 points! pika!')
    await ctx.send(random.choice(responses))
    await ctx.send('https://resizeimage.net/mypic/WcMZRgv5XpABTrW0/6dRA5/unknown.png')
    #except:
    #    OrderedDict=db.child(user_id).child("Points").get().val()
    #    points = OrderedDict["Points"]
    #    await ctx.send('Did you just try and get extra points? >:c Try again later.')
    #    await ctx.send('https://cdn.bulbagarden.net/upload/thumb/b/b9/Holiday_Hi-Jynx.png/200px-Holiday_Hi-Jynx.png')
        
@daily.error
async def daily_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send('Did you just try and get extra points? >:c')
        await ctx.send('https://cdn.bulbagarden.net/upload/thumb/b/b9/Holiday_Hi-Jynx.png/200px-Holiday_Hi-Jynx.png')
        msg = 'This command is ratelimited, please try again in {:.2f}s'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error
    

#@client.command()
#async def setDaily(ctx, task):
    #user_id=ctx.message.author.id
    #data = {"Daily" : task}
    #db.child(str(user_id)).child("Daily").set(data)
    #await ctx.send("Task " + task + " is now a daily task!")

    
#@client.command()
#async def leaderboard(ctx, member = discord.Member): #discord.Member refers to @user argument

#@client.event
#async def on_message():
#    await client.process_commands(message)
#    if message.author == client.user:
#        return

#    if 'kys' in message.content.lower():
#        response = "That is not appropriate to say to anyone. Please watch your language."
#        await message.channel.send(response)
        
client.run(TOKEN)
