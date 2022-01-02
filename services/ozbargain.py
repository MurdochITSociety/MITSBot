import discord
from discord.ext import tasks
import requests
from bs4 import BeautifulSoup

from mitsbot_globals import *
from fileio import getFileLines


# Filter deals that contain a blacklisted keyword
def filterDeal(deal):
    filterList = ["Alienware", "Vacuum", "Blender", "Coffee", "Washer", "Washing Machine", "Fryer", "Battery", "Batteries", "Lamp", "Mower", "Barista", "Shaver", "Purifier", "Camera"] 
    for filter in filterList:
        if filter.lower() in deal.lower():
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
