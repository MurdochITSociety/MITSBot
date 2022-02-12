const { SlashCommandBuilder } = require("@discordjs/builders");
function rand() {
  let roll = Math.floor(Math.random() * 6) + 1;
  return roll;
}
module.exports = {
  data: new SlashCommandBuilder().setName("rtd").setDescription("Roll the dice and see what you get!"),
  cooldown: 5,
  async execute(interaction) {
    await interaction.reply("Rolling Die!");
    await interaction.editReply(`**.**`);
    await interaction.editReply(`**..**`);
    await interaction.editReply(`**...**`);
    await interaction.editReply(`you rolled a **${rand()}** :game_die:`);
  },
};
