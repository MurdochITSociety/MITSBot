import random

from mitsbot_globals import javaFacts, addEventListener
from discordHelpers import sendTextEmbed


async def sendJavaFact(message):
    title = 'Here is a fact about Java!'
    desc = javaFacts[random.randint(0,len(javaFacts)-1)]
    print("Waiting to send java fact")
    await sendTextEmbed(message, title, desc)
    print("Sent java fact")


# add event listener for java fact command
addEventListener("javafact", sendJavaFact)
addEventListener("jfact", sendJavaFact)
