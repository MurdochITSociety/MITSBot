const Discord = require("discord.js");
const { SlashCommandBuilder } = require("@discordjs/builders");
const { ImageUrl } = require("../config.json");

module.exports = {
  data: new SlashCommandBuilder()
    .setName("help")
    .setDescription("In need of some help?")
    .addStringOption((opt) => opt.setName("name").setDescription("Command Set to view"))
    .addIntegerOption((opt) => opt.setName("number").setDescription("Command Set to view")),

  cooldown: 5,
  async execute(interaction) {
    const commandName = interaction.options.getString("name");
    const commandNum = interaction.options.getInteger("number") || -1;

    let embed;
    if (commandName == "" && commandNum == -1) {
      embed = new Discord.MessageEmbed()
        .setTitle("Help Categories")
        .setColor("#039efc")
        .setDescription("1. **Fun Commands**\n 2.**Admin Commands** \n **Usage:** /help fun")
        .setFooter({ text: "Note: some commands are buggy and may change" /* iconUrl: ImageUrl */ })
        .setThumbnail(ImageUrl);
    } else if (commandName == "fun" || commandNum == 1) {
      embed = new Discord.MessageEmbed()
        .setTitle("Fun Commands")
        .setColor("#ffaa00")
        .setDescription("1. **rtd**\n 2.**coinflip**\n 3.**ping** \n")
        .setFooter({ text: "Note: some commands are buggy and may change" /* iconUrl: ImageUrl */ });
    } else if (commandName == "admin" || commandNum == 2) {
      embed = new Discord.MessageEmbed()
        .setTitle("Admin Commands")
        .setColor("#ff1900")
        .setDescription(":construction: Coming Soon! :construction:")
        .setFooter({ text: "Note: some commands are buggy and may change" /* iconUrl: ImageUrl */ });
    }
    await interaction.reply({ embeds: [embed] });
  },
};
