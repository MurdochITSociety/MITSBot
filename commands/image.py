import random
import requests

from mitsbot_globals import bingAPIKey

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