const { SlashCommandBuilder } = require("@discordjs/builders");

module.exports = {
  data: new SlashCommandBuilder().setName("ping").setDescription("Ping, Pong!"),
  cooldown: 5,
  async execute(interaction) {
    await interaction.reply("Pinging!");

    await interaction.editReply(`Pong! this took: \`${interaction.createdTimestamp - new Date().getTime()}ms\` :heart:`);
  },
};
