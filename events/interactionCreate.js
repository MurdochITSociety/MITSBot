const { client } = require("../app");
const { Collection } = require("discord.js");
const cooldowns = new Discord.Collection();

//commands
client.on("interactionCreate", async (interaction) => {
  if (!interaction.isCommand()) return;

  const { commandName } = interaction;
  const command = client.commands.get(interaction.commandName);

  if (!command) return;

  if (!cooldowns.has(command)) {
    cooldowns.set(command, new Collection());
  }

  const now = Date.now();
  const timestamps = cooldowns.get(command);
  const cooldownAmount = (command.cooldown || 3) * 1000;

  if (timestamps.has(interaction.author.id)) {
    const expirationTime = timestamps.get(interaction.author.id) + cooldownAmount;

    if (now < expirationTime) {
      const timeLeft = (expirationTime - now) / 1000;
      return interaction.reply({
        content: `please wait ${timeLeft.toFixed(1)} more second(s) before reusing the \`${commandName}\` command.`,
        ephemeral: true,
      });
    }
  }
  timestamps.set(interaction.author.id, now);
  setTimeout(() => timestamps.delete(interaction.author.id), cooldownAmount);

  try {
    await command.execute(interaction);
  } catch (error) {
    console.error(error);
    await interaction.reply({ content: "there was an error trying to execute that command!", ephemeral: true });
  }
});
