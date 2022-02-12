const { SlashCommandBuilder } = require("@discordjs/builders");

function rand() {
  let roll = Math.floor(Math.random() * 2) + 1;
  switch (roll) {
    case 1:
      return "Heads";
    case 2:
      return "Tails";
    default:
      break;
  }
}
module.exports = {
  data: new SlashCommandBuilder().setName("coinflip").setDescription("Heads? No Tails!"),
  cooldown: 5,
  async execute(interaction) {
    await interaction.reply("__");
    await interaction.editReply("\\");
    await interaction.editReply(`|`);
    await interaction.editReply(`/`);
    await interaction.editReply(`__`);
    await interaction.editReply(`**${rand()}**!`);
  },
};
