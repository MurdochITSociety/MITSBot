import random
import requests

from mitsbot_globals import bingAPIKey, animals, animalFilter, addEventListener
from discordHelpers import sendImageEmbed


async def getImage(searchTerm, imageType):
    randomPage = random.randint(0, 200)
    searchURL = "https://api.bing.microsoft.com/v7.0/images/search"
    headers = {"Ocp-Apim-Subscription-Key" : bingAPIKey}
    params  = {"q": searchTerm, "safeSearch": "Strict", "imageType": imageType, "count": "1", "offset": str(randomPage)}
    try:
        response = requests.get(searchURL, headers=headers, params=params)
        data = response.json()
        url = data["value"][0]["contentUrl"]
        return url
    except:
        return


async def sendAnimal(message):
    try:
        command = message.content.lower()[2:]
        if command == "an" or command == "animal":
            animal = animals[random.randint(0, len(animals) - 1)]
            imageURL = await getImage(animal + animalFilter, "Photo")
            await sendImageEmbed(message, "Here is a " + animal + ".", imageURL)
        else:
            for i in animals:
                # if the incoming animal matches one in the animals list
                if i.startswith(command[command.find(" ") + 1:]):
                    imageURL = await getImage(i + animalFilter, "Photo")
                    await sendImageEmbed(message, "Here is a " + i + ".", imageURL)
                    return
            await message.channel.send("Sorry, that animal cannot be found.", delete_after=10)
    except Exception as e:
        print(e)
        await message.channel.send("Sorry, the image retrieval failed.", delete_after=10)


async def sendAnimalGif(message):
    try:
        command = message.content.lower()[2:]
        if command == "ang" or command == "animalgif":
            animal = animals[random.randint(0, len(animals) - 1)]
            imageURL = await getImage(animal + animalFilter, "AnimatedGif")
            await sendImageEmbed(message, "Here is a " + animal + ".", imageURL)
        else:
            for i in animals:
                # if the incoming animal matches one in the animals list
                if i.startswith(command[command.find(" ") + 1:]):
                    imageURL = await getImage(i + animalFilter, "AnimatedGif")
                    await sendImageEmbed(message, "Here is a " + i + ".", imageURL)
                    return
            await message.channel.send("Sorry, that animal cannot be found.", delete_after=10)
    except Exception as e:
        print(e)
        await message.channel.send("Sorry, the image retrieval failed.", delete_after=10)

    
# add event listeners for discord commands
addEventListener("an", sendAnimal)
addEventListener("animal", sendAnimal)
addEventListener("ang", sendAnimalGif)
addEventListener("animalgif", sendAnimalGif)
