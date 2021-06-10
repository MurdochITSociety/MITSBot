import requests
import discord

from mitsbot_globals import MITS_COLOR, addEventListener


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


# add event listener for cat command
addEventListener("cat", sendCat)
addEventListener("feline", sendCat)
addEventListener("kitty", sendCat)
addEventListener("puss", sendCat)
