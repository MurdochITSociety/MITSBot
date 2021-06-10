import requests

from discordHelpers import sendTextEmbed
from mitsbot_globals import addEventListener


async def sendCatFact(message):
    title = 'Here is a cat fact!'
    desc = ""
    try:
        data = requests.get('https://catfact.ninja/fact').json()
        desc = data['fact']
    except:
        desc = "Could not get a cat fact!"

    print("Waiting to send cat fact")
    await sendTextEmbed(message, title, desc)
    print("Sent cat fact")


# add event listener for cat command
addEventListener("catfact", sendCatFact)
addEventListener("felinefact", sendCatFact)
addEventListener("kittyfact", sendCatFact)
