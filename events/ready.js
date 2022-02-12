const package = require('../package.json')

const {
  client
} = require('../app')
const chalk = require('chalk');

const streamers = ['zuckles', 'anomaly', 'shroud', 'hjune', 'fitz', 'swaggersouls']

// The startup event
client.on('ready', () => {
  console.log('\n================================\n');
  console.log('   --', chalk.red(' Basic Bot Working  '), '      --');
  console.log('   --  Status:', chalk.green('Online   '), '      --\n');
  console.log('================================');
  setInterval(() => {
    let randStreamer = streamers[Math.floor(Math.random() * streamers.length)];
    client.user.setActivity(`==help (${package.version})`, {
      type: 'STREAMING',
      url: `https://www.twitch.tv/${randStreamer}`
    })
  }, 60000) // every 1 minute


});