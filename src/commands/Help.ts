import { SlashCommandBuilder } from '@discordjs/builders';
import { ColorResolvable, MessageEmbed } from 'discord.js';
import { Command } from "../types/Command";
import * as config from '../config.json';

export const command: Command = {
    actions: [ new SlashCommandBuilder()
        .setName("help")
        .setDescription("Get the list of available commands.") ],
    exec: async (bot, intr) => {
		const helpEmbed = new MessageEmbed()
			.setTitle('<:question:780285635021897729> Help')
			.setColor(config.embed_color as ColorResolvable)

		bot.commandHandler.actions.forEach((action: SlashCommandBuilder) => {
            helpEmbed.addField(action.name, action.description);
		});

        await intr.reply({ embeds: [helpEmbed] });
    }
};
