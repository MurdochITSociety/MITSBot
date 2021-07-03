import discord
import random
import os

from mitsbot_globals import MITS_COLOR, haroldImages, addEventListener, config


haroldImages = os.listdir(config['Directories']['ImagesDir'])


async def sendHarold(message):
    randomHarold = random.randint(0, len(haroldImages) - 1)
    haroldEmbed = discord.Embed(
        title="Here's Harold",
        colour=discord.Colour(MITS_COLOR)
    )
    haroldEmbed.set_image(url="attachment://" + haroldImages[randomHarold])
    await message.channel.send(file=discord.File("Harold/" + haroldImages[randomHarold]), embed=haroldEmbed)


# add event listener for discord command
addEventListener("harold", sendHarold)
