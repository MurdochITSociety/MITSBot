import asyncio
import os
import datetime
import discord
import requests
import json
import random
from discord.ext import commands, tasks
from bs4 import BeautifulSoup

token = xxx
os.chdir(xxx)
client = discord.Client()

bingAPIKey = xxx
animals = ["aardvark","albatross","alligator","alpaca","ant","anteater","antelope","ape","armadillo","baboon","badger","bass","bat","bear","beaver","bee","bison","blue whale","boar","buffalo","bull","butterfly","camel","capybara","caracal","caribou","cassowary","cat","caterpillar","catfish","cattle","chamois","cheetah","chicken","chimpanzee","chinchilla","chough","clam","cobra","cockatiel","cockroach","cod","cormorant","cow","coyote","crab","crane","crocodile","crow","curlew","deer","dog","dogfish","dolphin","donkey","dotterel","dove","dragonfly","duck","dugong","dunlin","eagle","echidna","eel","eland","elephant","elk","emu","falcon","ferret","finch","fish","flamingo","fox","frog","gaur","gazelle","gerbil","giraffe","gnat","gnu","goat","goldfinch","goldfish","goose","gorilla","goshawk","grasshopper","grouse","guanaco","gull","hamster","hare","hawk","hedgehog","heron","herring","hippopotamus","horned lizard","hornet","horse","human","hummingbird","hyena","ibex","ibis","jackal","jaguar","jay","jellyfish","kangaroo","kingfisher","kiwi","koala","kookabura","kouprey","kudu","ladybug","lapwing","lark","lemur","leopard","lion","lizard","llama","lobster","locust","loris","louse","lyrebird","magpie","mallard","manatee","mandrill","mantis","marten","meerkat","mink","mongoose","monkey","moose","mouse","mule","naked mole rat","narwhal","newt","nightingale","octopus","okapi","opossum","oryx","ostrich","otter","owl","oyster","pangolin","panther","parrot","partridge","peafowl","pelican","penguin","pheasant","pig","pigeon","platypus","pony","porcupine","porpoise","quail","quelea","quetzal","quokka","rabbit","raccoon","ram","rat","raven","red panda","reindeer","rhinoceros","rook","salamander","salmon","sand dollar","sandpiper","sardine","scorpion","seahorse","seal","sea sponge","shag bird","shark","sheep","shrew","skunk","sloth","snail","snake","sparrow","sperm whale","sphynx","spider","spoonbill","squid","squirrel","starfish","starling","stingray","stinkbug","stork","sun conure","swallow","swan","tapir","tarsier","termite","tiger","tit bird","toad","trout","turkey","turtle","viper","vulture","wallaby","walrus","wasp","weasel","whale","wildcat","wolf","wombat","woodcock","woodpecker","worm","wren","yak","zebra"]
animalFilter = " animal NOT hunt NOT catch NOT kill NOT hunting NOT game NOT gore NOT death NOT bite NOT bites NOT eat NOT eats NOT sad NOT gun NOT fight NOT fights NOT faceoff NOT blood NOT bleed NOT injured NOT disease NOT hurt NOT diseased NOT sick NOT pain NOT bloody NOT abuse NOT abused NOT treatment NOT wound NOT wounds"
haroldImages = os.listdir(xxx)

# Create MITS Bot help embed
helpEmbed = discord.Embed(
                description = '_ _\n_ _\n',
                colour = discord.Colour(0xbe2a36)
            )
helpEmbed.set_author(name="MITSBot Commands", icon_url="https://cdn.discordapp.com/emojis/756060351854018610.png")
helpEmbed.add_field(name='<:student:780271578608828437> __**Student Commands**__', value='\
    `m!resources` Get study and support resources.', inline=False)
helpEmbed.add_field(name='_ _', value='_ _', inline=True) # Gap between command sections
helpEmbed.add_field(name='<:birthday:779924273950490646> __**Birthday Commands**__', value=' \
    `m!addbday [Month] [Day]` Register a birthday. E.g. m!addbday January 1\n\
    `m!delbday` Remove a birthday.\n\
    `m!viewbday` View today\'s birthdays.', inline=False)
helpEmbed.add_field(name='_ _', value='_ _', inline=True) # Gap between command sections
helpEmbed.add_field(name='<:dog:810097516409257984> __**Image Commands**__', value=' \
    `m!animal [animal]` Any animal you want (almost).\n\
    `m!dog` Pupper.\n\
    `m!cat` Cat.\n\
    `m!harold` Harold.', inline=False)
    
# Create Murdoch resources embed
resourcesEmbed = discord.Embed(
                title = '<:student:780271578608828437><:student:780271578608828437> Murdoch Resources <:student:780271578608828437><:student:780271578608828437>',
                description = '_ _\n_ _\n',
                colour = discord.Colour(0xbe2a36)
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

# Return lines from a file
def getFileLines(file):
    f = open(file, "r")
    lines = f.readlines()
    f.close
    return lines

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
        colour = discord.Colour(0xbe2a36)
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

def getBdays():
    birthdays = getFileLines("birthdays.txt")
    return birthdays
  
def getTodaysBirthdays():
    todaysBirthdays = []
    birthdaysEmbed = 0
    today = datetime.datetime.today()
    today = today.strftime("%B %d")
    
    birthdays = getBdays()
    for birthday in birthdays:
        birthdaydate = birthday[19:]
        if (today in birthdaydate):
            todaysBirthdays.append(birthday[:18])
            
    if (len(todaysBirthdays) != 0):
        embedDesc = '_ _\n'
        for birthday in todaysBirthdays:
            embedDesc += 'It\'s <@' + birthday + '>\'s birthday today!\n'
        embedDesc += '\nHappy Birthday!\n'
        birthdaysEmbed = discord.Embed(
            description = embedDesc,
            title = '<:birthday:779924273950490646><:birthday:779924273950490646> Today\'s Birthdays <:birthday:779924273950490646><:birthday:779924273950490646>',
            colour = discord.Colour(0xbe2a36)
        )
        
    return birthdaysEmbed
    
# Check if a user ID exists in the birthdays file
def birthdayExists(userID):
    birthdays = getBdays()
    for birthday in birthdays:
        if (userID in birthday):
            return True
    return False

async def addBday(message):
    userID = str(message.author.id)
    if (birthdayExists(userID)):
        await message.channel.send("Your birthday is already registered. To remove and re-submit your birthday, try using m!help.")
        return
    try:
        birthday = datetime.datetime.strptime(message.content[10:], '%b %d')
    except:
        try:
            birthday = datetime.datetime.strptime(message.content[10:], '%B %d')
        except:
            await message.channel.send("That wasn't quite right. Try using m!help to find the right command.")
            return
    f = open('birthdays.txt', "a")
    f.write(userID + ' ' + str(birthday.strftime("%B %d")) + '\n')
    f.close()
    await message.channel.send("Your birthday has been registered.")
    return
    
async def delBday(message):
    userID = str(message.author.id)
    if (not birthdayExists(userID)):
        await message.channel.send("Your birthday hasn't been registered yet. Try using m!help to register your birthday first.")
        return
    birthdays = getBdays()
    f = open('birthdays.txt', "w")
    for birthday in birthdays:
        if (userID not in birthday):
            f.write(birthday)
    f.close()
    await message.channel.send("Your birthday has been deleted.")
    return
    
async def viewBday(message):
    todaysBirthdays = getTodaysBirthdays()
    if (todaysBirthdays != 0):
        await message.channel.send(embed=todaysBirthdays)
    else:
        await message.channel.send("It's nobody\'s birthday today :(")

async def sendDog(message):
    data = requests.get('https://api.thedogapi.com/v1/images/search').json()
    try:
        title = 'Here is a ' + data[0]['breeds'][0]['name'] + '.'
    except:
        title = 'Here is a dog.'
    dogEmbed = discord.Embed(
        title = title,
        colour = discord.Colour(0xbe2a36)
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
        colour = discord.Colour(0xbe2a36)
    )
    catEmbed.set_image(url=data[0]['url'])
    await message.channel.send(embed=catEmbed)

async def getImage(searchTerm):
    randomPage = random.randint(0, 200)
    searchURL = "https://api.bing.microsoft.com/v7.0/images/search"
    headers = {"Ocp-Apim-Subscription-Key" : bingAPIKey}
    params  = {"q": searchTerm, "safeSearch": "Strict", "count": "1", "offset": str(randomPage)}
    try:
        response = requests.get(searchURL, headers=headers, params=params)
        data = response.json()
        url = data["value"][0]["thumbnailUrl"]
        return url
    except:
        return
            
async def sendImageEmbed(message, title, imageURL):
    embed = discord.Embed(
        title = title,
        colour = discord.Colour(0xbe2a36)
    )
    embed.set_image(url=imageURL)
    await message.channel.send(embed=embed)

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
        elif (command.startswith("dog") or command.startswith("doggo") or command.startswith("pupper") or command.startswith("pup") or command.startswith("woof")):
            await sendDog(message)
        elif (command.startswith("cat") or command.startswith("feline") or command.startswith("kitty") or command.startswith("puss")):
            await sendCat(message)
        elif (command.startswith("an")):
            try:
                if (command == "an"):
                    animal = animals[random.randint(0,len(animals)-1)]
                    imageURL = await getImage(animal + animalFilter)
                    await sendImageEmbed(message, "Here is a " + animal + ".", imageURL)
                else:
                    for i in animals:
                        if (i.startswith(command[command.find(" ")+1:])):
                            imageURL = await getImage(i + animalFilter)
                            await sendImageEmbed(message, "Here is a " + i + ".", imageURL)
                            return
                    await message.channel.send("Sorry, that animal cannot be found.")
            except Exception as e:
                print(e)
                await message.channel.send("Sorry, the image retrieval failed.")
        elif (command.startswith("harold")):
            randomHarold = random.randint(0, len(haroldImages)-1)
            haroldEmbed = discord.Embed(
                title = "Here's Harold",
                colour = discord.Colour(0xbe2a36)
            )
            haroldEmbed.set_image(url="attachment://"+haroldImages[randomHarold])
            await message.channel.send(file=discord.File("Harold/"+haroldImages[randomHarold]), embed=haroldEmbed)
        else:
            await message.channel.send("That's not a valid command. Try using m!help to find the right command.")

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
    trashcanChannel = client.get_channel(xxx)
    bargainChannel = client.get_channel(xxx)
    
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

client.run(token)
