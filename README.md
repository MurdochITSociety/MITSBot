# MITSBot

A bot for the Murdoch IT Society Discord.

**Current features:**

:moneybag: Scrape 'hot' electronics and computing deals from OzBargain, and post them to the Discord.

:birthday: Allow Discord members to register their birthdays with the bot, and announce any birthdays at 8AM each day.

:dog: Send dog, cat, and a variety of animal pictures on request.

:book: Offer a list of studying resources to Discord members by demand.

**Config File Base:**

```json
{
  "token": "",
  "bingKey": "",
  "serverID": "",
  "Directories": {
    "workingDir": "",
    "ImagesDir": ""
  },
  "Roles": {
    "moderatorRole": ""
  },
  "Channels": {
    "motionChannel": "",
    "trashcanChannel": "",
    "bargainChannel": "",
    "announcementsChannel": ""
  },
  "animals": [],
  "animalsFilter": ""
}
```
