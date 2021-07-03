import os
import json
import discord

# Only the best color ;)
MITS_COLOR = 0xbe2a36

# globals, should be passed around eventually
# client = None
# bingAPIKey = None
# animals = None
# animalFilter = None
# haroldImages = None
# javaFacts = None
# motionChannelID = None
# trashcanChannelID = None
# bargainChannelID = None
# announcementsChannelID = None
# mitsServerID = None
# moderatorRoleID = None
# helpEmbed = None
# resourcesEmbed = None
# trashcanChannel = None
# bargainChannel = None
# announcementsChannel = None
# motionChannel = None
global client
global config
global bingAPIKey
global animals
global animalFilter
global haroldImages; haroldImages = None
global javaFacts
global motionChannelID
global trashcanChannelID
global bargainChannelID
global announcementsChannelID
global mitsServerID
global moderatorRoleID
global helpEmbed; helpEmbed = None
global resourcesEmbed; resourcesEmbed = None
global trashcanChannel; trashcanChannel = None
global bargainChannel
global announcementsChannel; announcementsChannel = None
global motionChannel; motionChannel = None

# a dict of command names, and callback functions to what they should be process when called
# callbacks should take a parameter "message", the matching discord message sent
global events; events = {}

client = discord.Client()

# Set working directory to directory of Python script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open('config.json', encoding='utf-8') as configFile:
    config = json.load(configFile)

token = config['token']

bingAPIKey = config['bingKey']
animals = config['animals']
animalFilter = config['animalsFilter']

javaFacts = config['javaFacts']

motionChannelID = config['Channels']['motionChannel']
trashcanChannelID = config['Channels']['trashcanChannel']
bargainChannelID = config['Channels']['bargainChannel']
announcementsChannelID = config['Channels']['announcementsChannel']
mitsServerID = config['serverID']
moderatorRoleID = config['Roles']['moderatorRole']


def addEventListener(command_name, callback):
    events.update({command_name: callback})
