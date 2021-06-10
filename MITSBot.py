# import local modules
from discordEvents import client, token # gets the discord client object and auth token

# --- Main ----
def main():
    # discordEvents adds events to the client, which respond to triggers
    # boot up the discord client, which will login and wait for these triggers
    client.run(token) 


# if only run if main script
if __name__ == "__main__":
    main()
