import discord

from mitsbot_globals import MITS_COLOR, client, mitsServerID, moderatorRoleID, motionChannel, announcementsChannel, motionChannelID, addEventListener

async def createAnnouncementPropEmbed(description, author, announcement):
    announcementPropEmbed = discord.Embed(
        title = "Announcement Proposal",
        description = description,
        colour = discord.Colour(MITS_COLOR)
    )
    announcementPropEmbed.add_field(name='Announcement Author', value=author)
    announcementPropEmbed.add_field(name='Announcement Message ID', value=announcement)
    return announcementPropEmbed


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


async def sendAnnouncementMessage(message):
    description = "@everyone The above announcement has been proposed. Please react to this message with a <:thumbsup:825609718181265490> to approve it, or a <:thumbsdown:825609718181265490> to deny it.\n\n_ _"
    announcementPropEmbed = await createAnnouncementPropEmbed(description,
                                                                "<@" + str(message.author.id) + ">",
                                                                str(message.id))
    proposal = await message.channel.send(embed=announcementPropEmbed)
    await proposal.add_reaction("👍")
    await proposal.add_reaction("👎")


# add discord client events for reactions
@client.event
async def on_reaction_add(reaction, user):
    await countAnnouncementReactions(reaction, user)


@client.event
async def on_reaction_remove(reaction, user):
    await countAnnouncementReactions(reaction, user)


addEventListener("announce ", sendAnnouncementMessage)
