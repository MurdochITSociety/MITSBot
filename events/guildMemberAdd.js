const {
  client
} = require('../app');
const DbConnect = require('../DB/DbConnect')

//when member joins server
// client.on('guildMemberAdd', member => {
//   const guild = client.guilds.cache.get("445536297096839168");
//   const general = guild.channels.cache.get("709336331091705879");
//   general.send(`Welcome, ${member.user} to ${guild.name}!`);

//   let NewRole = guild.roles.cache.find(role => role.name === "member")
//   if (!member.roles.cache.some(role => role.name === "member")) {
//     member.roles.add(NewRole).catch(console.error);
//   }

// });