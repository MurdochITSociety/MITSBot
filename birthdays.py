import datetime
import discord
from discord.ext import tasks
from fileio import getFileLines

from mitsbot_globals import MITS_COLOR, trashcanChannel

# private func to read birthdays from file
def _getBdays():
    birthdays = getFileLines("birthdays.txt")
    return birthdays
  
# Private func to check if a user ID exists in the birthdays file
def _birthdayExists(userID):
    birthdays = _getBdays()
    for birthday in birthdays:
        if (userID in birthday):
            return True
    return False

def getTodaysBirthdays(MITS_COLOR):
    todaysBirthdays = []
    birthdaysEmbed = 0
    today = datetime.datetime.today()
    today = today.strftime("%B %d")
    
    birthdays = _getBdays()
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
            colour = discord.Colour(MITS_COLOR)
        )
        
    return birthdaysEmbed

async def addBday(message):
    userID = str(message.author.id)
    if (_birthdayExists(userID)):
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
    if (not _birthdayExists(userID)):
        await message.channel.send("Your birthday hasn't been registered yet. Try using m!help to register your birthday first.")
        return
    birthdays = _getBdays()
    f = open('birthdays.txt', "w")
    for birthday in birthdays:
        if (userID not in birthday):
            f.write(birthday)
    f.close()
    await message.channel.send("Your birthday has been deleted.")
    return
    
async def viewBday(message, MITS_COLOR):
    todaysBirthdays = getTodaysBirthdays(MITS_COLOR)
    if (todaysBirthdays != 0):
        await message.channel.send(embed=todaysBirthdays)
    else:
        await message.channel.send("It's nobody\'s birthday today :(")

# Check birthdays file each day, and post if any are on the current date
@tasks.loop(hours=24)
async def dailyBirthdays():
    todaysBirthdays = getTodaysBirthdays(MITS_COLOR)
    if (todaysBirthdays != 0):
        await trashcanChannel.send(embed=todaysBirthdays)
