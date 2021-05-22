import asyncio
import datetime
import requests
import random
from discord.ext import tasks

# import local modules
from birthdays import addBday, delBday, viewBday, getTodaysBirthdays
from ozbargain import checkURL
from discordHelpers import sendTextEmbed, sendImageEmbed
from mitsbot_globals import *

# --- Events ---


# Check birthdays file each day, and post if any are on the current date
@tasks.loop(hours=24)
async def dailyBirthdays():
    todaysBirthdays = getTodaysBirthdays(MITS_COLOR)
    if (todaysBirthdays != 0):
        await trashcanChannel.send(embed=todaysBirthdays)


# task is scheduled on import
@tasks.loop(minutes=2)
async def checkForDeals():
    dealEmbeds = checkURL('https://www.ozbargain.com.au/cat/computing', 'computing.txt', 'electronics.txt')
    print("Checked for new computing deals.")
    for embedVar in dealEmbeds:
        await bargainChannel.send(embed=embedVar)
    # await asyncio.sleep(60)

    dealEmbeds = checkURL('https://www.ozbargain.com.au/cat/electrical-electronics', 'electronics.txt', 'computing.txt')
    print("Checked for new electronics deals.")
    for embedVar in dealEmbeds:
        await bargainChannel.send(embed=embedVar)


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
        elif (command.startswith("help") or command.startswith("h ") or command.startswith("commands")):
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
        elif (command.startswith("mm ") or command.startswith("lfg ")):
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


# --- Helper Funcs ---


async def sendDog(message):
    data = requests.get('https://api.thedogapi.com/v1/images/search').json()
    try:
        title = 'Here is a ' + data[0]['breeds'][0]['name'] + '.'
    except:
        title = 'Here is a dog.'
    dogEmbed = discord.Embed(
        title = title,
        colour = discord.Colour(MITS_COLOR)
    )
    dogEmbed.set_image(url=data[0]['url'])
    print("Waiting to send dog")
    await message.channel.send(embed=dogEmbed)
    print("Dog sent")


async def sendCat(message):
    data = requests.get('https://api.thecatapi.com/v1/images/search').json()
    try:
        title = 'Here is a ' + data[0]['breeds'][0]['name'] + '.'
    except:
        title = 'Here is a cat.'
    catEmbed = discord.Embed(
        title = title,
        colour = discord.Colour(MITS_COLOR)
    )
    catEmbed.set_image(url=data[0]['url'])
    print("Waiting to send cat")
    await message.channel.send(embed=catEmbed)
    print("Cat sent")


async def sendCatFact(message):
    title = 'Here is a cat fact!'
    desc = ""
    try:
        data = requests.get('https://catfact.ninja/fact').json()
        desc = data['fact']
    except:
        desc = "Could not get a cat fact!"

    print("Waiting to send cat fact")
    await sendTextEmbed(message, title, desc)
    print("Sent cat fact")


async def sendJavaFact(message):
    title = 'Here is a fact about Java!'
    desc = javaFacts[random.randint(0,len(javaFacts)-1)]
    print("Waiting to send java fact")
    await sendTextEmbed(message, title, desc)
    print("Sent java fact")


async def getImage(searchTerm, imageType):
    randomPage = random.randint(0, 200)
    searchURL = "https://api.bing.microsoft.com/v7.0/images/search"
    headers = {"Ocp-Apim-Subscription-Key" : bingAPIKey}
    params  = {"q": searchTerm, "safeSearch": "Strict", "imageType": imageType, "count": "1", "offset": str(randomPage)}
    try:
        response = requests.get(searchURL, headers=headers, params=params)
        data = response.json()
        url = data["value"][0]["contentUrl"]
        return url
    except:
        return


async def createAnnouncementPropEmbed(description, author, announcement):
    announcementPropEmbed = discord.Embed(
        title = "Announcement Proposal",
        description = description,
        colour = discord.Colour(MITS_COLOR)
    )
    announcementPropEmbed.add_field(name='Announcement Author', value=author)
    announcementPropEmbed.add_field(name='Announcement Message ID', value=announcement)
    return announcementPropEmbed


async def createLFGPost(message):
    print(message)


async def countAnnouncementReactions(reaction, user):
    # Test if the message being reacted to is an announcement proposal, and check if the reacting user is this bot
    embed = ""
    try:
        embed = reaction.message.embeds[0].to_dict()
        if (embed["title"] != "Announcement Proposal" or embed["description"].endswith("has passed.\n\n_ _") or embed["description"].endswith("has failed.\n\n_ _") or user == client.user):
            return
    except:
        return
    
    # Test if the reacting user is the announcement proposer, and delete the reaction if so
    proposer = client.get_user(int(embed["fields"][0]["value"][2:-1])) # Get user object for user that proposed announcement
    if (user == proposer):
        await reaction.message.remove_reaction(reaction.emoji, user)
        return
    
    originalDescription = "The above announcement has been proposed. Please react to this message with a <:thumbsup:825609718181265490> to approve it, or a <:thumbsdown:825609718181265490> to deny it.\n\n"
    moderatorCount = len(client.get_guild(mitsServerID).get_role(role_id=moderatorRoleID).members) - 1
    requiredVote = int(round((moderatorCount) * 0.3))
    approvalRating = 0
    forVotes = []
    againstVotes = []

    for reaction in reaction.message.reactions:
        if (reaction.emoji == "👍"):
            approvalRating = approvalRating + reaction.count - 1
            async for user in reaction.users():
                forVotes.append(user)
        if (reaction.emoji == "👎"):
            approvalRating = approvalRating - reaction.count + 1
            async for user in reaction.users():
                againstVotes.append(user)
    
    # Calculate the total number of voters, minus the bot (duplicates are removed from the list of voter users)
    numberOfVoters = len(list(set(forVotes + againstVotes))) - 1

    if (approvalRating == requiredVote):
        try:
            announcement = await motionChannel.fetch_message(int(embed["fields"][1]["value"]))
            announcement = announcement.content[11:]
            await announcementsChannel.send(announcement)
            description = originalDescription + "The proposed announcement has passed.\n\n_ _"
            announcementPropEmbed = await createAnnouncementPropEmbed(description, "<@" + str(proposer.id) + ">", embed["fields"][1]["value"])
            await reaction.message.edit(embed = announcementPropEmbed)
        except:
            description = originalDescription + "The original announcement cannot be found. The proposed announcement has failed.\n\n_ _"
            announcementPropEmbed = await createAnnouncementPropEmbed(description, "<@" + str(proposer.id) + ">", embed["fields"][1]["value"])
            await reaction.message.edit(embed = announcementPropEmbed)
    elif ((moderatorCount - numberOfVoters) + approvalRating < requiredVote):
        description = originalDescription + "The required approval rating can no longer be reached. The proposed announcement has failed.\n\n_ _"
        announcementPropEmbed = await createAnnouncementPropEmbed(description, "<@" + str(proposer.id) + ">", embed["fields"][1]["value"])
        await reaction.message.edit(embed = announcementPropEmbed)
    # The following elif can't be an else, because if someone upvotes immediately after the proposal passes (but before Discord has time to update the message),
    # the function would reach this point again. So this elif prevents the message from being updated again once the vote has already passed.
    elif ((moderatorCount - numberOfVoters) + approvalRating >= requiredVote):
        description = originalDescription + "The approval rating is currently " + str(approvalRating) + ". It must reach " + str(requiredVote) + " for the proposed announcement to pass.\n\n_ _"
        announcementPropEmbed = await createAnnouncementPropEmbed(description, "<@" + str(proposer.id) + ">", embed["fields"][1]["value"])
        await reaction.message.edit(embed = announcementPropEmbed)
    else:
        return


# --- Main ----

def main():
    client.run(token)


# if only run if main script
if __name__ == "__main__":
    main()
