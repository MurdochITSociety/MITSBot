import requests

from discordHelpers import sendTextEmbed

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