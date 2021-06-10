import asyncio
import datetime
import random

from mitsbot_globals import *
from discordHelpers import *
from birthdays import *
from ozbargain import checkForDeals
from commands.javafact import *
from commands.dog import *
from commands.cat import *
from commands.catfact import *
from commands.announcement import *
from commands.image import *
from commands.lfg import *


@client.event
async def on_message(message):
    # Check if message came from bot
    if (message.author == client.user):
        return

    # Check if message is a bot command
    if (message.content.lower().startswith("m!")):
        command = message.content.lower()[2:]

        # Check what the command is, and respond accordingly
        if (command.startswith("addbday") or command.startswith("addbirthday") or command.startswith(
                "newbday") or command.startswith("newbirthday")):
            await addBday(message)
        elif (command.startswith("delbday") or command.startswith("deletebday") or command.startswith(
                "delbirthday") or command.startswith("deletebirthday")):
            await delBday(message)
        elif (command.startswith("help") or command.startswith("h") or command.startswith("commands")):
            await message.channel.send(embed=helpEmbed)
        elif (command.startswith("viewbday") or command.startswith("todaysbdays") or command.startswith(
                "viewbirthdays") or command.startswith("todaysbirthdays")):
            await viewBday(message)
        elif (command.startswith("resources") or command.startswith("links") or command.startswith("resource")):
            await message.channel.send(embed=resourcesEmbed)
        elif (command.startswith("javafact") or command.startswith("jfact")):
            await sendJavaFact(message)
        elif (command.startswith("dog") or command.startswith("doggo") or command.startswith(
                "pupper") or command.startswith("pup") or command.startswith("woof")):
            await sendDog(message)
        elif (command.startswith("catfact") or command.startswith("felinefact") or command.startswith("kittyfact")):
            await sendCatFact(message)
        elif (command.startswith("cat") or command.startswith("feline") or command.startswith(
                "kitty") or command.startswith("puss")):
            await sendCat(message)
        elif (command.startswith("announce ")):
            if (message.channel.id != motionChannelID):
                await message.channel.send("That's the wrong channel for proposing announcements. Please use #motions.",
                                           delete_after=10)
            else:
                description = "@everyone The above announcement has been proposed. Please react to this message with a <:thumbsup:825609718181265490> to approve it, or a <:thumbsdown:825609718181265490> to deny it.\n\n_ _"
                announcementPropEmbed = await createAnnouncementPropEmbed(description,
                                                                          "<@" + str(message.author.id) + ">",
                                                                          str(message.id))
                proposal = await message.channel.send(embed=announcementPropEmbed)
                await proposal.add_reaction("👍")
                await proposal.add_reaction("👎")
        elif (command.startswith("an")):
            try:
                if (command == "an" or command == "animal" or command == "ang" or command == "animalgif"):
                    animal = animals[random.randint(0, len(animals) - 1)]
                    imageURL = ""
                    if (command == "an" or command == "animal"):
                        imageURL = await getImage(animal + animalFilter, "Photo")
                    else:
                        imageURL = await getImage(animal + animalFilter, "AnimatedGif")
                    await sendImageEmbed(message, "Here is a " + animal + ".", imageURL)
                else:
                    for i in animals:
                        if (i.startswith(command[command.find(" ") + 1:])):
                            imageURL = ""
                            if (command.startswith("ang") or command.startswith("animalgif")):
                                imageURL = await getImage(i + animalFilter, "AnimatedGif")
                            else:
                                imageURL = await getImage(i + animalFilter, "Photo")
                            await sendImageEmbed(message, "Here is a " + i + ".", imageURL)
                            return
                    await message.channel.send("Sorry, that animal cannot be found.", delete_after=10)
            except Exception as e:
                print(e)
                await message.channel.send("Sorry, the image retrieval failed.", delete_after=10)
        elif (command.startswith("harold")):
            randomHarold = random.randint(0, len(haroldImages) - 1)
            haroldEmbed = discord.Embed(
                title="Here's Harold",
                colour=discord.Colour(MITS_COLOR)
            )
            haroldEmbed.set_image(url="attachment://" + haroldImages[randomHarold])
            await message.channel.send(file=discord.File("Harold/" + haroldImages[randomHarold]), embed=haroldEmbed)
        elif (command.startswith("mm") or command.startswith("lfg")):
            await createLFGPost(message)
        else:
            await message.channel.send("That's not a valid command. Try using m!help to find the right command.",
                                       delete_after=10)


@client.event
async def on_reaction_add(reaction, user):
    await countAnnouncementReactions(reaction, user)


@client.event
async def on_reaction_remove(reaction, user):
    await countAnnouncementReactions(reaction, user)


# After Discord client is ready, define the channels and start the threads
@client.event
async def on_ready():
    print('Discord Client ready!')

    trashcanChannel = client.get_channel(trashcanChannelID)
    bargainChannel = client.get_channel(bargainChannelID)
    announcementsChannel = client.get_channel(announcementsChannelID)
    motionChannel = client.get_channel(motionChannelID)

    # start ozbargain monitor
    checkForDeals.start()

    # Wait until 8AM to post the first birthday(s)
    now = datetime.datetime.now()
    if (int(now.hour) < 8):
        future = now.replace(hour=8, minute=0, second=0, microsecond=0)
    else:
        future = now.replace(hour=8, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
    secondsLeft = int(future.strftime('%s')) - int(now.strftime('%s'))
    await asyncio.sleep(secondsLeft)

    dailyBirthdays.start()

