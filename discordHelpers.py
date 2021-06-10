from mitsbot_globals import discord, MITS_COLOR


async def sendTextEmbed(message, title, description):
    textEmbed = discord.Embed(
        title = title,
        colour = discord.Colour(MITS_COLOR),
        description = description
    )
    await message.channel.send(embed=textEmbed)


async def sendImageEmbed(message, title, imageURL):
    embed = discord.Embed(
        title = title,
        colour = discord.Colour(MITS_COLOR)
    )
    embed.set_image(url=imageURL)
    await message.channel.send(embed=embed)
