const { SlashCommandBuilder } = require("@discordjs/builders");
const Discord = require("discord.js");
//TODO FIX
module.exports = {
  data: new SlashCommandBuilder()
    .setName("purge")
    .setDescription("Purge messages")
    .addIntegerOption((opt) => opt.setName("count").setDescription("Number of messages to delete").setRequired(true)),
  cooldown: 5,
  async execute(interaction) {
    const staff = interaction.member.roles.cache.some((role) => role.name == "Staff") || interaction.memberPermissions.has("ADMINISTRATOR");
    if (staff) {
      toDelete = Math.min(interaction.options.getInteger("count", true), 100);
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
