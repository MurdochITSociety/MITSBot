//Discord Bot Entry Point!

//discord modules and variables
const { Collection, Client, Intents } = require("discord.js");

const clientIntents = new Intents();

clientIntents.add(
  Intents.FLAGS.GUILDS,
  Intents.FLAGS.GUILD_MEMBERS,
  Intents.FLAGS.GUILD_BANS,
  Intents.FLAGS.GUILD_INVITES,
  Intents.FLAGS.GUILD_VOICE_STATES,
  Intents.FLAGS.PRESENCES,
  Intents.FLAGS.MESSAGES,
  Intents.FLAGS.MESSAGE_REACTIONS,
  Intents.FLAGS.MESSAGE_TYPING,
  Intents.FLAGS.DIRECT_MESSAGES,
  Intents.FLAGS.DIRECT_MESSAGE_REACTIONS,
  Intents.FLAGS.DIRECT_MESSAGE_TYPING,
  Intents.FLAGS.GUILD_SCHEDULED_EVENTS
);

const client = new Client({ intents: clientIntents });

const { prefix, token } = require("./config.json");

client.commands = new Collection();

// Handlers
//export client for events
module.exports = {
  client: client,
};
// import events
require("./handlers")(client);

//catch any errors
process.on("unhandledRejection", (err) => console.error(`Uncaught Promise Error: \n${err.stack}`));

//login
client.login(token);
