from mitsbot_globals import addEventListener


async def createLFGPost(message):
    print("yo")


# add event listener for discord command
addEventListener("lfg", createLFGPost)
addEventListener("mm", createLFGPost)
