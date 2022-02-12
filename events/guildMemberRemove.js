const {
  client
} = require('../app');
const DbConnect = require('../DB/DbConnect')


//when member leaves server
// client.on('guildMemberRemove', member => {
//   const guild = client.guilds.cache.get("445536297096839168");
//   const general = guild.channels.cache.get("709336331091705879");
//   general.send(`${member.user.username} left the server :sob:`);

// });