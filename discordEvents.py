from mitsbot_globals import *
from discordHelpers import *

# initialise all commands and services (registering them, starting async tasks etc)
from commands import *
from services import *


@client.event
async def on_message(message):
    # Check if message came from bot
    if (message.author == client.user):
        return

    # Check if message is a bot command
    if (message.content.lower().startswith("m!")):
        command = message.content.lower()[2:]

        for eventName in events:
            # if the command issued matches a defined event name
            if command.startswith(eventName):
                # resolve the callback function (idk if it will work without)
                fn = events[eventName]
                # pass message into callback function
                await fn(message)
                return
        await message.channel.send("That's not a valid command. Try using m!help to find the right command.",
                                   delete_after=10)


# After Discord client is ready, define the channels and start the threads
@client.event
async def on_ready():
    print('Discord Client ready!')

    trashcanChannel = client.get_channel(trashcanChannelID)
    bargainChannel = client.get_channel(bargainChannelID)
    announcementsChannel = client.get_channel(announcementsChannelID)
    motionChannel = client.get_channel(motionChannelID)

    # start ozbargain monitor
    ozbargain.checkForDeals.start()
