import requests
import discord

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