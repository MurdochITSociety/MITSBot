from mitsbot_globals import MITS_COLOR, discord, helpEmbed, addEventListener


# Create MITS Bot help embed
helpEmbed = discord.Embed(
    description='_ _\n_ _\n',
    colour=discord.Colour(MITS_COLOR)
)
helpEmbed.set_author(name="MITSBot Commands", icon_url="https://cdn.discordapp.com/emojis/756060351854018610.png")
helpEmbed.add_field(name='<:student:780271578608828437> __**Student Commands**__', value='\
    `m!resources` Get study and support resources. ', inline=False)

helpEmbed.add_field(name='_ _', value='_ _', inline=True)  # Gap between command sections
helpEmbed.add_field(name='<:birthday:779924273950490646> __**Birthday Commands**__', value=' \
    `m!addbday [Month] [Day]` Register a birthday. E.g. m!addbday January 1\n\
    `m!delbday` Remove a birthday.\n\
    `m!viewbday` View today\'s birthdays. ', inline=False)

helpEmbed.add_field(name='_ _', value='_ _', inline=True)  # Gap between command sections
helpEmbed.add_field(name=':book: __**Fact Commands**__', value=' \
    `m!catfact` Get a cool cat fact!\n\
    `m!javafact` Get a cool fact about Java! ', inline=False)

helpEmbed.add_field(name='_ _', value='_ _', inline=True)  # Gap between command sections
helpEmbed.add_field(name='<:dog:810097516409257984> __**Image Commands**__', value=' \
    `m!animal [animal]` Any animal you want (almost).\n\
    `m!animalgif [animal]` Same as the above. But a GIF!.\n\
    `m!dog` Pupper.\n\
    `m!cat` Cat.\n\
    `m!harold` Harold. ', inline=False)


async def sendHelpResponse(message):
    await message.channel.send(embed=helpEmbed)    


# Add event listener for discord command
addEventListener("help", sendHelpResponse)
addEventListener("h", sendHelpResponse)
addEventListener("commands", sendHelpResponse)
