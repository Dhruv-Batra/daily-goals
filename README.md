# daily-goals
Contributors/Owners (Listed in Alphabetical Order): Dhruv Batra, Justin Chen, Kevin Chen

Detailed Instructions: https://realpython.com/how-to-make-a-discord-bot-python/
This bot is not like other bots where you can just click and add it to your server. Those bots are being hosted on a vps. I am not currently hosting this bot so it will not work like that (requires money). What you would have to do (this is described in detail in the link above) is create your own discord bot using the code provided. Thats how it is currently, once I get some more time probs late may, ill host the bot on a ras pi so all u have to do is click a link to add the bot to your server

Download the repository and unzip it

Edit the .env file by replacing the DISCORD_TOKEN variable's value with your own token obtained through the Discord Developer Portal  

Edit the .env file by replacing the DISCORD_GUILD variable's value with the server id of the server you are trying to add this bot to. This can be obtained by going to your server in discord server settings -> Widget -> and the server id should be visible there

![image](https://user-images.githubusercontent.com/47730411/116829279-76570280-ab71-11eb-8f7e-0e0c69e4bb63.png)

Navigate to the downloaded directory within your terminal

Run the commmands pip install -U discord.py and pip install pyrebase

Run commands.py ex) py commands.py or python3 commands.py

Have fun!

Project details can be viewed at: https://devpost.com/software/productivity-discord-bot
