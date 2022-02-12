const { SlashCommandBuilder } = require("@discordjs/builders");
const Discord = require("discord.js");
//TODO FIX
module.exports = {
  data: new SlashCommandBuilder()
    .setName("purge")
    .setDescription("Purge messages")
    .addIntegerOption((opt) => {
      opt.setName("count").setRequired(true).setDescription("Number of messages to delete");
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
      await interaction.reply({
        embeds: [embed],
      });
    }
  },
};
