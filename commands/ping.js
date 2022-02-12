const { SlashCommandBuilder } = require("@discordjs/builders");

module.exports = {
  data: new SlashCommandBuilder().setName("ping").setDescription("Ping, Pong!"),
  cooldown: 5,
  async execute(interaction) {
    await interaction.reply("Pinging!").then((sent) => {
      sent.edit(`Pong! this took: \`${sent.createdTimestamp - message.createdTimestamp}ms\` :heart:`);
    });
  },
};
