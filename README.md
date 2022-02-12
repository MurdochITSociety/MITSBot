# mits-bot-rewrite

Basic skeleton for a discord bot

Please note some of the events found in the events folder do not work and just server as examples

# Guide

To use this bot please follow the guide below.

1. Run `npm install` in your command-line
2. Create a `config.json` file and fill it in with the example Config
3. Run the `start.bat` or enter `npm run start-dev` (use `start-dev` to auto restart the bot if it crashes)

# Discord Bot Portal

## Invite the Bot with required permissions

1. Go to [Discord Permission Calculator](https://discordapi.com/permissions.html)
2. Get the Bots Application Id and insert it into the **Client ID** field
3. Select the appropriate Permissions
4. Press the link and invite it to your test server

## Give the Bot Slash Command permissions

1. In the Discord Developer Portal go toOauth2 -> URL Generator
2. Select the `applications.commands` checkbox
3. Copy the Generated URL into a new tab and go to the URL.

# Example Config

just create a config.json with the following

```json
{
  "token": "",
  "clientId": "",
  "guildId": "",
  "ImageUrl": "https://cdn.discordapp.com/attachments/275962822762954752/941955625758384189/mits_logo.png"
}
```
