const { SlashCommandBuilder } = require("@discordjs/builders");
const Discord = require("discord.js");
module.exports = {
  data: new SlashCommandBuilder()
    .setName("Purge")
    .setDescription("Purge messages")
    .addIntegerOption((opt) => {
      opt.setName("Count").setRequired(true).setDescription("Number of messages to delete");
    }),
  cooldown: 5,
  async execute(interaction) {
    staff = interaction.member.roles.cache.some((role) => role.name == "Staff") || interaction.member.hasPermission("ADMINISTRATOR");
    if (staff) {
      toDelete = interaction.options.getNumber("Count", true) + 1;
      interaction.channel
        .bulkDelete(toDelete)
        .then((messages) => {
          interaction.reply(`Deleted ${messages.size - 1} messages!`);
        })
        .catch(console.error);
    } else {
      const embed = new Discord.MessageEmbed()
        .setTitle(":no_entry_sign: Permission Denied :no_entry_sign:")
        .setColor("#de1616")
        .setDescription("Error you must be Admin to use this command!");
      interaction.reply({
        embeds: [embed],
      });
    }
  },
};
