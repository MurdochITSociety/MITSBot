import os
import json
import discord

# Only the best color ;)
MITS_COLOR = 0xbe2a36

# globals, should be passed around eventually
#client = None
#bingAPIKey = None
#animals = None
#animalFilter = None
#haroldImages = None
#javaFacts = None
#motionChannelID = None
#trashcanChannelID = None
#bargainChannelID = None
#announcementsChannelID = None
#mitsServerID = None
#moderatorRoleID = None
#helpEmbed = None
#resourcesEmbed = None
#trashcanChannel = None
#bargainChannel = None
#announcementsChannel = None
#motionChannel = None
global client
global bingAPIKey
global animals
global animalFilter
global haroldImages
global javaFacts
global motionChannelID
global trashcanChannelID
global bargainChannelID
global announcementsChannelID
global mitsServerID
global moderatorRoleID
global helpEmbed
global resourcesEmbed
global trashcanChannel
global bargainChannel
global announcementsChannel
global motionChannel

client = discord.Client()

# Set working directory to directory of Python script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open('config.json', encoding='utf-8') as configFile:
    config = json.load(configFile)

token = config['token']

bingAPIKey = config['bingKey']
animals = config['animals']
animalFilter = config['animalsFilter']

haroldImages = os.listdir(config['Directories']['ImagesDir'])
javaFacts = config['javaFacts']

motionChannelID = config['Channels']['motionChannel']
trashcanChannelID = config['Channels']['trashcanChannel']
bargainChannelID = config['Channels']['bargainChannel']
announcementsChannelID = config['Channels']['announcementsChannel']
mitsServerID = config['serverID']
moderatorRoleID = config['Roles']['moderatorRole']

# Create MITS Bot help embed
helpEmbed = discord.Embed(
    description='_ _\n_ _\n',
    colour=discord.Colour(MITS_COLOR)
)
helpEmbed.set_author(name="MITSBot Commands", icon_url="https://cdn.discordapp.com/emojis/756060351854018610.png")
helpEmbed.add_field(name='<:student:780271578608828437> __**Student Commands**__', value='\
        `m!resources` Get study and support resources. ', inline=False)

helpEmbed.add_field(name='_ _', value='_ _', inline=True)  # Gap between command sections
helpEmbed.add_field(name='<:birthday:779924273950490646> __**Birthday Commands**__', value=' \
        `m!addbday [Month] [Day]` Register a birthday. E.g. m!addbday January 1\n\
        `m!delbday` Remove a birthday.\n\
        `m!viewbday` View today\'s birthdays. ', inline=False)

helpEmbed.add_field(name='_ _', value='_ _', inline=True)  # Gap between command sections
helpEmbed.add_field(name=':book: __**Fact Commands**__', value=' \
        `m!catfact` Get a cool cat fact!\n\
        `m!javafact` Get a cool fact about Java! ', inline=False)

helpEmbed.add_field(name='_ _', value='_ _', inline=True)  # Gap between command sections
helpEmbed.add_field(name='<:dog:810097516409257984> __**Image Commands**__', value=' \
        `m!animal [animal]` Any animal you want (almost).\n\
        `m!animalgif [animal]` Same as the above. But a GIF!.\n\
        `m!dog` Pupper.\n\
        `m!cat` Cat.\n\
        `m!harold` Harold. ', inline=False)

# Create Murdoch resources embed
resourcesEmbed = discord.Embed(
    title='<:student:780271578608828437><:student:780271578608828437> Murdoch Resources <:student:780271578608828437><:student:780271578608828437>',
    description='_ _\n_ _\n',
    colour=discord.Colour(MITS_COLOR)
)
resourcesEmbed.add_field(name='<:book:780285717124743168> Studying', value=' \
        [myMurdoch Learning](https://moodleprod.murdoch.edu.au/my/)\n\
        [Murdoch Library](https://www.murdoch.edu.au/library)\n\
        [Murdoch Referencing](https://www.murdoch.edu.au/library/help-support/support-for-students/referencing)\n\
        [Study Resources](https://moodleprod.murdoch.edu.au/course/view.php?id=9416#section-6)\n\
        [Murdoch Bookshop](https://our.murdoch.edu.au/Bookshop/)\n\
        [Student Hub Booking](https://studenthub.libcal.com/)')
resourcesEmbed.add_field(name='_ _', value='_ _', inline=True)  # Limits embed to two columns
resourcesEmbed.add_field(name='<:question:780285635021897729> Course Help', value=' \
        [Murdoch Handbook](https://handbook.murdoch.edu.au/)\n\
        [Dates and Timetables](https://timetables.murdoch.edu.au/)\n\
        [Course Plans](https://www.murdoch.edu.au/mymurdoch/support-advice/student-admin/enrolment/how-to-enrol/course-plans/)\n\
        [myMurdoch Advice](https://www.murdoch.edu.au/mymurdoch/support-advice/mymurdoch-advice)\n\
        [Academic Contacts](https://www.murdoch.edu.au/contacts/academic/)')
resourcesEmbed.add_field(name='_ _', value='_ _', inline=False)  # Gap between resources sections
resourcesEmbed.add_field(name='<:computer:780285373959634984> Student Software', value=' \
        [Azure Dev Tools](https://azureforeducation.microsoft.com/devtools)\n\
        [GitHub Developer Pack](https://education.github.com/pack)\n\
        [VMware Academy](https://e5.onthehub.com/WebStore/ProductsByMajorVersionList.aspx?ws=ef64204f-8ec4-de11-886d-0030487d8897&vsro=8)')
resourcesEmbed.add_field(name='_ _', value='_ _', inline=True)  # Limits embed to two columns
resourcesEmbed.add_field(name='<:briefcase:780285263585738815> Jobs and Internships', value=' \
        [GradConnection](https://au.gradconnection.com/graduate-jobs/information-technology/)\n\
        [GradAustralia](https://gradaustralia.com.au/)')
resourcesEmbed.add_field(name='_ _', value='_ _', inline=False)  # Gap between resources sections
resourcesEmbed.add_field(name='<:person_raising_hand:780285082228228116> Support', value=' \
        [Murdoch Support Services](https://www.murdoch.edu.au/life-at-murdoch/support-services)\n\
        [Murdoch Counselling](https://www.murdoch.edu.au/counselling)\n\
        [Murdoch Doctor](http://www.murdoch.edu.au/Medical/Making-an-appointment/)\n\
        [Mental Health Helplines](https://www.healthdirect.gov.au/mental-health-helplines)\n\
        [Headspace](https://headspace.org.au/)')
