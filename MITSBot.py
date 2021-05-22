import asyncio
import os
import datetime
import discord
import requests
import json
import random
from discord.ext import commands, tasks
from bs4 import BeautifulSoup

#import local modules
from birthdays import getTodaysBirthdays, addBday, delBday, viewBday
from fileio import getFileLines

# Only the best color ;)
MITS_COLOR = 0xbe2a36

# globals
client = None
bingAPIKey = None
animals = None
animalFilter = None
haroldImages = None
javaFacts = None
motionChannelID = None
trashcanChannelID = None
bargainChannelID = None
announcementsChannelID = None
mitsServerID = None
moderatorRoleID = None
helpEmbed = None
resourcesEmbed = None

def main():
    # Set working directory to directory of Python script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    config = ""
    with open('config.json', encoding='utf-8') as configFile:
        config = json.load(configFile)

    token = config['token']
    client = discord.Client()

    bingAPIKey = config['bingKey']
    animals = config['animals']
    animalFilter = config['animalsFilter']

    haroldImages = os.listdir(config['Directories']['ImagesDir'])
    javaFacts = config['javaFacts']

    motionChannelID = config['Channels']['motionChannel']
    trashcanChannelID = config['Channels']['trashcanChannel']
    bargainChannelID = config['Channels']['bargainChannel']
    announcementsChannelID = config['Channels']['announcementsChannel']
    mitsServerID = config['serverID']
    moderatorRoleID = config['Roles']['moderatorRole']

    # Create MITS Bot help embed
    helpEmbed = discord.Embed(
                    description = '_ _\n_ _\n',
                    colour = discord.Colour(MITS_COLOR)
                )
    helpEmbed.set_author(name="MITSBot Commands", icon_url="https://cdn.discordapp.com/emojis/756060351854018610.png")
    helpEmbed.add_field(name='<:student:780271578608828437> __**Student Commands**__', value='\
        `m!resources` Get study and support resources. ', inline=False)
        
    helpEmbed.add_field(name='_ _', value='_ _', inline=True) # Gap between command sections
    helpEmbed.add_field(name='<:birthday:779924273950490646> __**Birthday Commands**__', value=' \
        `m!addbday [Month] [Day]` Register a birthday. E.g. m!addbday January 1\n\
        `m!delbday` Remove a birthday.\n\
        `m!viewbday` View today\'s birthdays. ', inline=False)

    helpEmbed.add_field(name='_ _', value='_ _', inline=True) # Gap between command sections
    helpEmbed.add_field(name=':book: __**Fact Commands**__', value=' \
        `m!catfact` Get a cool cat fact!\n\
        `m!javafact` Get a cool fact about Java! ', inline=False)

    helpEmbed.add_field(name='_ _', value='_ _', inline=True) # Gap between command sections
    helpEmbed.add_field(name='<:dog:810097516409257984> __**Image Commands**__', value=' \
        `m!animal [animal]` Any animal you want (almost).\n\
        `m!animalgif [animal]` Same as the above. But a GIF!.\n\
        `m!dog` Pupper.\n\
        `m!cat` Cat.\n\
        `m!harold` Harold. ', inline=False)
        
        
    # Create Murdoch resources embed
    resourcesEmbed = discord.Embed(
                    title = '<:student:780271578608828437><:student:780271578608828437> Murdoch Resources <:student:780271578608828437><:student:780271578608828437>',
                    description = '_ _\n_ _\n',
                    colour = discord.Colour(MITS_COLOR)
                )
    resourcesEmbed.add_field(name='<:book:780285717124743168> Studying', value=' \
        [myMurdoch Learning](https://moodleprod.murdoch.edu.au/my/)\n\
        [Murdoch Library](https://www.murdoch.edu.au/library)\n\
        [Murdoch Referencing](https://www.murdoch.edu.au/library/help-support/support-for-students/referencing)\n\
        [Study Resources](https://moodleprod.murdoch.edu.au/course/view.php?id=9416#section-6)\n\
        [Murdoch Bookshop](https://our.murdoch.edu.au/Bookshop/)\n\
        [Student Hub Booking](https://studenthub.libcal.com/)')
    resourcesEmbed.add_field(name='_ _', value='_ _', inline=True) # Limits embed to two columns
    resourcesEmbed.add_field(name='<:question:780285635021897729> Course Help', value=' \
        [Murdoch Handbook](https://handbook.murdoch.edu.au/)\n\
        [Dates and Timetables](https://timetables.murdoch.edu.au/)\n\
        [Course Plans](https://www.murdoch.edu.au/mymurdoch/support-advice/student-admin/enrolment/how-to-enrol/course-plans/)\n\
        [myMurdoch Advice](https://www.murdoch.edu.au/mymurdoch/support-advice/mymurdoch-advice)\n\
        [Academic Contacts](https://www.murdoch.edu.au/contacts/academic/)')
    resourcesEmbed.add_field(name='_ _', value='_ _', inline=False) # Gap between resources sections
    resourcesEmbed.add_field(name='<:computer:780285373959634984> Student Software', value=' \
        [Azure Dev Tools](https://azureforeducation.microsoft.com/devtools)\n\
        [GitHub Developer Pack](https://education.github.com/pack)\n\
        [VMware Academy](https://e5.onthehub.com/WebStore/ProductsByMajorVersionList.aspx?ws=ef64204f-8ec4-de11-886d-0030487d8897&vsro=8)')
    resourcesEmbed.add_field(name='_ _', value='_ _', inline=True) # Limits embed to two columns
    resourcesEmbed.add_field(name='<:briefcase:780285263585738815> Jobs and Internships', value=' \
        [GradConnection](https://au.gradconnection.com/graduate-jobs/information-technology/)\n\
        [GradAustralia](https://gradaustralia.com.au/)')
    resourcesEmbed.add_field(name='_ _', value='_ _', inline=False) # Gap between resources sections
    resourcesEmbed.add_field(name='<:person_raising_hand:780285082228228116> Support', value=' \
        [Murdoch Support Services](https://www.murdoch.edu.au/life-at-murdoch/support-services)\n\
        [Murdoch Counselling](https://www.murdoch.edu.au/counselling)\n\
        [Murdoch Doctor](http://www.murdoch.edu.au/Medical/Making-an-appointment/)\n\
        [Mental Health Helplines](https://www.healthdirect.gov.au/mental-health-helplines)\n\
        [Headspace](https://headspace.org.au/)')

    client.run(token)

# if only run if main script
if __name__ == "__main__": 
    main()

# Filter deals that contain a blacklisted keyword
def filterDeal(deal):
    filterList = ["Alienware", "Vacuum", "Blender", "Coffee", "Washer", "Washing Machine", "Fryer", "Battery", "Batteries", "Lamp", "Mower", "Barista", "Shaver", "Purifier", "Camera"] 
    for filter in filterList:
        if  (filter.lower() in deal.lower()):
            return True
    return False

# Create deal embed
def newDealEmbed(titleVar, imageLink, store, couponCode, dealLink, externalLink):
    embed = discord.Embed(
        title = titleVar,
        description = '_ _\n_ _\n',
        colour = discord.Colour(MITS_COLOR)
    )
    embed.set_thumbnail(url=imageLink)
    embed.add_field(name='Store', value=store)
    embed.add_field(name='Coupon Code', value=couponCode)
    embed.add_field(name='_ _', value='_ _', inline=False)
    embed.add_field(name='OzBargain Link', value='[Here]('+dealLink+')')
    embed.add_field(name='Deal Link', value='[Here]('+externalLink+')')
    return embed

# Scrape url for new deals
def checkURL(url, file, otherFile):

    # Fetch deals from first history file
    dealHistory = getFileLines(file)

    # Reduce size of first deals history file (if over 60 lines)
    if (len(dealHistory) > 60):
        f = open(file, "w")
        newHistory = dealHistory[10:]
        for line in newHistory:
            f.write(line)
        f.close()
 
    # Fetch deals from second history file
    dealHistory = dealHistory + getFileLines(otherFile)

    newDeals = []

    # Retrieve new deals and extract their information
    try:
        data = requests.get(url)
    except:
        print ("\nAn error occured.")
        return newDeals
    html = BeautifulSoup(data.text, 'html.parser')
    rawPosts = html.select('div[class^="node node-ozbdeal node-teaser"]')
    rawTitles = html.select('h2.title')
    dealEmbeds = []
    
    # Iterate through deals
    for i in range(len(rawTitles)):
        aElement = rawTitles[i].find('a', href=True)
        dealLink = aElement['href']
        refinedDealLink = '<https://www.ozbargain.com.au' + dealLink + '>'

        # Check if deal has already been posted, or contains a restricted keyword
        if (str(dealLink + '\n') in dealHistory):
            continue
        elif (filterDeal(aElement.text) is True):
            continue

        else:
            titleVar = aElement.text
            if ('@' in titleVar):
               atLocation = titleVar.find('@')
               titleVar = titleVar[:atLocation]
            store = rawPosts[i].find('span', {'class': 'via'}).find('a', href=True).text
            foxshot = rawPosts[i].find('div', {'class': 'foxshot-container'})
            imageLink = foxshot.find('img')['src']
            couponCode = rawPosts[i].find('div', {'class': 'couponcode'})
            if (couponCode is None):
                couponCode = 'N/A'
            else:
                couponCode = couponCode.text
            externalLink = '<https://www.ozbargain.com.au' + foxshot.find('a', href=True)['href'] + '>'
            
            # Create new Discord embed message, and add it to the new deals list
            embed = newDealEmbed(titleVar, imageLink, store, couponCode, refinedDealLink, externalLink)
            newDeals.append(dealLink)
            dealEmbeds.append(embed)
            
            print ("Found new deal: " + str(dealLink))
    
    # Append new deals to the relevant deals history file
    f = open(file, "a")
    for newDeal in newDeals:
        f.write(newDeal + '\n')
    f.close()
    return dealEmbeds
      
@tasks.loop(minutes=2)
async def checkForDeals():
    dealEmbeds = checkURL('https://www.ozbargain.com.au/cat/computing', 'computing.txt', 'electronics.txt')
    print ("Checked for new computing deals.")
    for embedVar in dealEmbeds:
        await bargainChannel.send(embed=embedVar)
    await asyncio.sleep(60)

    dealEmbeds = checkURL('https://www.ozbargain.com.au/cat/electrical-electronics', 'electronics.txt', 'computing.txt')
    print ("Checked for new electronics deals.")
    for embedVar in dealEmbeds:
        await bargainChannel.send(embed=embedVar)

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
    await message.channel.send(embed=dogEmbed)
        
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
    await message.channel.send(embed=catEmbed)

async def sendTextEmbed(message, title, description):
    textEmbed = discord.Embed(
        title = title,
        colour = discord.Colour(MITS_COLOR),
        description = description
    )
    await message.channel.send(embed=textEmbed)

async def sendCatFact(message):
    title = 'Here is a cat fact!'
    desc = ""
    try:
        data = requests.get('https://catfact.ninja/fact').json()
        desc = data['fact']
    except:
        desc = "Could not get a cat fact!"
    
    await sendTextEmbed(message, title, desc)
    
async def sendJavaFact(message):
    title = 'Here is a fact about Java!'
    desc = javaFacts[random.randint(0,len(javaFacts)-1)]
    await sendTextEmbed(message, title, desc)

async def getImage(searchTerm, imageType, count):
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
            
async def sendImageEmbed(message, title, imageURL):
    embed = discord.Embed(
        title = title,
        colour = discord.Colour(MITS_COLOR)
    )
    embed.set_image(url=imageURL)
    await message.channel.send(embed=embed)
    
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
    print("yo")

# --- Events ---

@client.event
async def on_message(message):
    # Check if message came from bot
    if (message.author == client.user):
        return
    
    # Check if message is a bot command
    if (message.content.lower().startswith("m!")):
        command = message.content.lower()[2:]
        
        # Check what the command is, and respond accordingly
        if (command.startswith("addbday") or command.startswith("addbirthday") or command.startswith("newbday") or command.startswith("newbirthday")):
            await addBday(message)
        elif (command.startswith("delbday") or command.startswith("deletebday") or command.startswith("delbirthday") or command.startswith("deletebirthday")):
            await delBday(message)
        elif (command.startswith("help") or command.startswith("h ") or command.startswith("commands")):
            await message.channel.send(embed=helpEmbed)
        elif (command.startswith("viewbday") or command.startswith("todaysbdays") or command.startswith("viewbirthdays") or command.startswith("todaysbirthdays")):
            await viewBday(message)
        elif (command.startswith("resources") or command.startswith("links") or command.startswith("resource")):
            await message.channel.send(embed=resourcesEmbed)
        elif (command.startswith("javafact") or command.startswith("jfact")):
            await sendJavaFact(message)
        elif (command.startswith("dog") or command.startswith("doggo") or command.startswith("pupper") or command.startswith("pup") or command.startswith("woof")):
            await sendDog(message)
        elif (command.startswith("catfact") or command.startswith("felinefact") or command.startswith("kittyfact")):
            await sendCatFact(message)
        elif (command.startswith("cat") or command.startswith("feline") or command.startswith("kitty") or command.startswith("puss")):
            await sendCat(message)
        elif (command.startswith("announce ")):
            if (message.channel.id != motionChannelID):
                await message.channel.send("That's the wrong channel for proposing announcements. Please use #motions.", delete_after=10)
            else:
                description = "@everyone The above announcement has been proposed. Please react to this message with a <:thumbsup:825609718181265490> to approve it, or a <:thumbsdown:825609718181265490> to deny it.\n\n_ _"
                announcementPropEmbed = await createAnnouncementPropEmbed(description, "<@" + str(message.author.id) + ">", str(message.id))
                proposal = await message.channel.send(embed=announcementPropEmbed)
                await proposal.add_reaction("👍")
                await proposal.add_reaction("👎")
        elif (command.startswith("an")):
            try:
                if (command == "an" or command == "animal" or command == "ang" or command == "animalgif"):
                    animal = animals[random.randint(0,len(animals)-1)]
                    imageURL = ""
                    if (command == "an" or command == "animal"):
                        imageURL = await getImage(animal + animalFilter, "Photo")
                    else:
                        imageURL = await getImage(animal + animalFilter, "AnimatedGif")
                    await sendImageEmbed(message, "Here is a " + animal + ".", imageURL)
                else:
                    for i in animals:
                        if (i.startswith(command[command.find(" ")+1:])):
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
            randomHarold = random.randint(0, len(haroldImages)-1)
            haroldEmbed = discord.Embed(
                title = "Here's Harold",
                colour = discord.Colour(MITS_COLOR)
            )
            haroldEmbed.set_image(url="attachment://"+haroldImages[randomHarold])
            await message.channel.send(file=discord.File("Harold/"+haroldImages[randomHarold]), embed=haroldEmbed)
        elif (command.startswith("mm ") or command.startswith("lfg ")):
            await createLFGPost(message)
        else:
            await message.channel.send("That's not a valid command. Try using m!help to find the right command.", delete_after=10)

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

@client.event
async def on_reaction_add(reaction, user):
    await countAnnouncementReactions(reaction, user)

@client.event
async def on_reaction_remove(reaction, user):
    await countAnnouncementReactions(reaction, user)

# Check birthdays file each day, and post if any are on the current date
@tasks.loop(hours=24)
async def dailyBirthdays():
    todaysBirthdays = getTodaysBirthdays()
    if (todaysBirthdays != 0):
        await trashcanChannel.send(embed=todaysBirthdays)

# After Discord client is ready, define the channels and start the threads
@client.event
async def on_ready():
    print ('Discord Client ready!')
    
    global trashcanChannel
    global bargainChannel
    global announcementsChannel
    global motionChannel
    trashcanChannel = client.get_channel(trashcanChannelID)
    bargainChannel = client.get_channel(bargainChannelID)
    announcementsChannel = client.get_channel(announcementsChannelID)
    motionChannel = client.get_channel(motionChannelID)
    
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
