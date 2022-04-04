import { SlashCommandBuilder } from '@discordjs/builders';
import { ColorResolvable, MessageEmbed } from 'discord.js';
import { Command } from "../types/Command";
import * as config from '../config.json';

export const command: Command = {
    data: new SlashCommandBuilder()
        .setName("help")
        .setDescription("Get the list of available commands."),
    exec: async (bot, intr) => {
		const helpEmbed = new MessageEmbed()
			.setTitle('<:question:780285635021897729> Help')
			.setColor(config.embed_color as ColorResolvable)

		bot.commandHandler.commands.forEach(command => {
			helpEmbed.addField(command.data.name, command.data.description);
		});

        await intr.reply({ embeds: [helpEmbed] });
    }
};