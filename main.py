import discord
import os
import requests
import json
import random
from keep_running import keep_alive
from replit import db

client = discord.Client()
sad_words = ["sad", "depressed", "cry", "angry", "angry"]
starter_encouragements = ["Cheer up", "Don't be sad", "You are the best"]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  data = json.loads(response.text)
  quote = data[0]['q'] + " -" + data[0]['a']
  return quote

def update_encouragements(enc_msg):
  if "encouragements" in db.keys(): 
    encouragements = db["encouragements"]
    encouragements.append(enc_msg)
    db["encouragements"] = encouragements

  else:
    db["encouragements"] =[enc_msg]

def delete_encouragements(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if db["responding"]:
    option = starter_encouragements

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(starter_encouragements))

    if "encouragements" in db.keys():
      option = option + db["encouragements"]

    if msg.startswith('$hello'):
      await message.channel.send('Hello!')

  if msg.startswith('$motivate'):
    await message.channel.send(get_quote())
  
  if msg.startswith('$new'):
    encouraging_msg = msg.split("$new ", 1)[1]
    update_encouragements(encouraging_msg)
    await message.channel.send("New encouragement added!")

  if msg.startswith('$del'):
    encouragements = []

    if "encouragements" in db.keys():
      index = int(msg.split("$del ", 1)[1])
      delete_encouragements(index)
      encouragements = db["encouragements"]

    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []

    if "encouragements" in db.keys():
      encouragements = db["encouragements"]

    await message.channel.send(encouragements)
  
  if msg.startswith("$responding"):
    value = msg.split("$responding", 1)[1]

    if value.lower() == "true":
      db["responding"] == True
      await message.channel.send("Responding is on.")
    
    else:
      db["responding"] == False
      await message.channel.send("Responding is off.")

keep_alive()
client.run(os.getenv('TOKEN'))


